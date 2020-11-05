#!/bin/sh

# sudo apt install python3-pip
# sudo ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.8/site-packages/lsb_release.py

# cd $(cd "$(dirname "$0")" && pwd)

read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1]}
}

# export $(xargs < .env)
# echo ${G_APP_NAME}

export G_APP_NAME=$(read_var G_APP_NAME .env)
export G_WORK_PATH=$(read_var G_WORK_PATH .env)

if [[ -z $G_WORK_PATH ]]; then
    export G_APP_NAME="edge_server"
fi
if [[ -z $G_WORK_PATH ]]; then
    export G_WORK_PATH="/var/www/"
fi

mkdir -p $G_WORK_PATH

rm -rf $G_WORK_PATH/.venv && \
python3 -m venv $G_WORK_PATH/.venv && \
. $G_WORK_PATH/.venv/bin/activate && \
python3 -m pip install --upgrade pip && \
python3 -m pip install --trusted-host pypi.python.org -r $(pwd)/requirements.txt

rm -rf $G_WORK_PATH/$G_APP_NAME
cp -r $(pwd) $G_WORK_PATH
