#!/bin/sh

# sudo apt install python3-pip
# sudo ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.8/site-packages/lsb_release.py

# cd $(cd "$(dirname "$0")" && pwd)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 0980a45... test connections
=======
>>>>>>> b0510df... applied uwsgi
read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1]}
}

# export $(xargs < .env)
# echo ${G_APP_NAME}

export G_APP_NAME=$(read_var G_APP_NAME .env)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi
export G_WORK_PATH=$(read_var G_WORK_PATH .env)

if [[ -z $G_WORK_PATH ]]; then
    export G_APP_NAME="edge_server"
fi
if [[ -z $G_WORK_PATH ]]; then
    export G_WORK_PATH="/var/www/"
fi

=======
export G_APP_NAME = $(read_var G_APP_NAME .env)
export G_WORK_PATH = $(read_var G_WORK_PATH .env)
<<<<<<< HEAD
=======
# export G_WORK_PATH=$(read_var G_WORK_PATH .env)
>>>>>>> 0980a45... test connections
=======
export G_WORK_PATH=$(read_var G_WORK_PATH .env)
>>>>>>> c1e6c90... fixed minor errors

if [[ -z $G_WORK_PATH ]]; then
    export G_APP_NAME="edge_server"
fi
if [[ -z $G_WORK_PATH ]]; then
<<<<<<< HEAD
    export G_WORK_PATH = "/var/www/edge_server"
    
>>>>>>> f1dd3e0... applied uwsgi
=======
    export G_WORK_PATH="/var/www/"
fi

>>>>>>> 0980a45... test connections
=======

if [[ -z $G_WORK_PATH ]]; then
    export G_APP_NAME = "edge_server"
if [[ -z $G_WORK_PATH ]]; then
    export G_WORK_PATH = "/var/www/edge_server"
    
>>>>>>> f1dd3e0... applied uwsgi
>>>>>>> b0510df... applied uwsgi
mkdir -p $G_WORK_PATH

rm -rf $G_WORK_PATH/.venv && \
python3 -m venv $G_WORK_PATH/.venv && \
. $G_WORK_PATH/.venv/bin/activate && \
python3 -m pip install --upgrade pip && \
python3 -m pip install --trusted-host pypi.python.org -r $(pwd)/requirements.txt

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
rm -rf $G_WORK_PATH/$G_APP_NAME
=======
>>>>>>> f1dd3e0... applied uwsgi
=======
cp -r $G_WORK_PATH/$G_APP_NAME
>>>>>>> 0980a45... test connections
=======
rm -rf $G_WORK_PATH/$G_APP_NAME
>>>>>>> 7ed39aa... fixed minor errors
=======
rm -rf $G_WORK_PATH/$G_APP_NAME
=======
>>>>>>> f1dd3e0... applied uwsgi
>>>>>>> b0510df... applied uwsgi
cp -r $(pwd) $G_WORK_PATH
