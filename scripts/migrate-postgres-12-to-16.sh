#!/bin/sh
set -eu

# Offline migration for the Docker Compose postgres_data volume.
# The script keeps both a logical SQL dump and a byte-for-byte copy of the
# PostgreSQL 12 volume so a failed migration can be rolled back.

die() {
    echo "Error: $*" >&2
    exit 1
}

command -v docker >/dev/null 2>&1 || die "Docker is required."
[ -f docker-compose.yml ] || die "Run this script from the repository root."
[ -f .env ] || die "Missing .env file."

if docker compose version >/dev/null 2>&1; then
    compose="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    compose="docker-compose"
else
    die "Docker Compose is required."
fi

timestamp=$(date +%Y%m%d-%H%M%S)
backup_dir=${BACKUP_DIR:-"$PWD/backups"}
dump_file="$backup_dir/postgres-12-$timestamp.sql"
source_container="registration-ui-pg12-migration-$timestamp"
target_container="registration-ui-pg16-migration-$timestamp"

mkdir -p "$backup_dir"
chmod 700 "$backup_dir"

cleanup() {
    docker rm -f "$source_container" "$target_container" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

echo "Stopping the application..."
$compose down

# Create (but do not start) the db service if necessary, solely to ask Docker
# which physical volume backs the Compose postgres_data mount.
db_container=$($compose ps -aq db)
if [ -z "$db_container" ]; then
    $compose create db >/dev/null
    db_container=$($compose ps -aq db)
fi
[ -n "$db_container" ] || die "Could not identify the Compose db container."

data_volume=$(docker inspect \
    --format '{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}' \
    "$db_container")
[ -n "$data_volume" ] || die "Could not identify the postgres_data volume."

backup_volume="${data_volume}_pg12_backup_${timestamp}"

echo "Source volume: $data_volume"
echo "SQL backup:    $dump_file"
echo "Volume backup: $backup_volume"
printf "This will replace the source volume with PostgreSQL 16 after backing it up. Continue? [y/N] "
read -r answer
case "$answer" in
    y|Y|yes|YES) ;;
    *) echo "Migration cancelled."; exit 0 ;;
esac

# Remove the stopped service container so Docker permits removal of its volume.
$compose rm -f db >/dev/null

echo "Starting temporary PostgreSQL 12..."
docker run -d --name "$source_container" \
    --env-file .env \
    -v "$data_volume:/var/lib/postgresql/data" \
    postgres:12-alpine >/dev/null

attempt=0
until docker exec "$source_container" sh -c 'pg_isready --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"' >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    [ "$attempt" -lt 60 ] || die "PostgreSQL 12 did not become ready. The original volume is unchanged."
    sleep 1
done

echo "Creating logical backup..."
umask 077
docker exec "$source_container" sh -c 'pg_dumpall --username "$POSTGRES_USER"' > "$dump_file"
[ -s "$dump_file" ] || die "The SQL backup is empty. The original volume is unchanged."
grep -q "PostgreSQL database cluster dump complete" "$dump_file" || \
    die "The SQL backup appears incomplete. The original volume is unchanged."

docker stop "$source_container" >/dev/null
docker rm "$source_container" >/dev/null

echo "Copying the original data volume for rollback..."
docker volume create "$backup_volume" >/dev/null
docker run --rm --entrypoint sh \
    -v "$data_volume:/from:ro" \
    -v "$backup_volume:/to" \
    postgres:12-alpine -c 'cp -a /from/. /to/'

echo "Creating a fresh PostgreSQL 16 volume..."
docker volume rm "$data_volume" >/dev/null
docker volume create "$data_volume" >/dev/null

docker run -d --name "$target_container" \
    --env-file .env \
    -v "$data_volume:/var/lib/postgresql/data" \
    postgres:16-alpine >/dev/null

attempt=0
until docker exec "$target_container" sh -c 'pg_isready --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"' >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    [ "$attempt" -lt 60 ] || die "PostgreSQL 16 did not become ready. Restore the volume backup shown above."
    sleep 1
done

echo "Restoring into PostgreSQL 16..."
# pg_dumpall includes the bootstrap role that PostgreSQL 16 already created.
# Its harmless 'role already exists' error must not hide other restore errors,
# so capture the log and reject every error except that one.
restore_log="$backup_dir/postgres-16-restore-$timestamp.log"
if ! docker exec -i "$target_container" sh -c \
    'psql --username "$POSTGRES_USER" --dbname postgres --set ON_ERROR_STOP=off' \
    < "$dump_file" > "$restore_log" 2>&1; then
    die "Restore command failed. See $restore_log; the PostgreSQL 12 volume backup is intact."
fi
if grep '^ERROR:' "$restore_log" | grep -v 'already exists' >/dev/null 2>&1; then
    die "Restore reported errors. See $restore_log; the PostgreSQL 12 volume backup is intact."
fi

# pg_dumpall restores the source role's password state. Older installations
# may have a NULL or MD5 password, neither of which can authenticate against
# PostgreSQL 16's default SCRAM host rules. Reset the application role from the
# current .env value after restoring. The password is expanded only inside the
# temporary database container and is never written to the migration logs.
printf '%s\n' 'ALTER ROLE :"db_user" PASSWORD :'\''db_password'\'';' | \
    docker exec -i "$target_container" sh -c \
      'psql --username "$POSTGRES_USER" --dbname postgres --quiet \
        --set=db_user="$POSTGRES_USER" --set=db_password="$POSTGRES_PASSWORD"'

docker stop "$target_container" >/dev/null
docker rm "$target_container" >/dev/null

echo "Running the application migrations on PostgreSQL 16..."
$compose up -d db
# Existing static volumes may be owned by root from older application images.
$compose run --rm --user root --entrypoint chown web -R app:app /code/static
$compose run --rm web python manage.py migrate
$compose up -d

echo "Migration complete."
echo "Keep these backups until the application has been verified:"
echo "  $dump_file"
echo "  Docker volume: $backup_volume"
