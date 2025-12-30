#!/usr/bin/env bash

echo "PostgreSQL configuration (press Enter to use defaults)"

read -p "Host [localhost]: " host
host=${host:-localhost}

read -p "Port [5432]: " port
port=${port:-5432}

read -p "User [postgres]: " user
user=${user:-postgres}

read -s -p "Password [docker]: " password
echo
password=${password:-docker}

cat <<EOF > database.ini
[postgresql]
host=$host
port=$port
user=$user
password=$password
EOF

echo "database.ini created successfully."
