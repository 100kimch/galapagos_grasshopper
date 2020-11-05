#!/bin/sh

# cd $(cd "$(dirname "$0")" && pwd)

# . .venv/bin/activate

# export FLASK_APP=app
# export FLASK_ENV=development
# flask run --host 0.0.0.0

read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1]}
}

export G_APP_NAME=$(read_var G_APP_NAME .env)
export G_WORK_PATH=$(read_var G_WORK_PATH .env)

if [[ -z $G_WORK_PATH ]]; then
    export G_APP_NAME="edge_server"
fi
if [[ -z $G_WORK_PATH ]]; then
    export G_WORK_PATH="/var/www/"
fi

source ${G_WORK_PATH}.venv/bin/activate
uwsgi --ini uwsgi.ini
