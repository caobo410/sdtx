#!/bin/sh

set -e

SHMJ_CONFIGURATION_DIR=/etc/shmj
SHMJ_CONFIGURATION_FILE=$SHMJ_CONFIGURATION_DIR/shmj-server.conf
SHMJ_DATA_DIR=/var/lib/shmj
SHMJ_GROUP="shmj"
SHMJ_LOG_DIR=/var/log/shmj
SHMJ_USER="shmj"

if ! getent passwd | grep -q "^shmj:"; then
    groupadd $SHMJ_GROUP
    adduser --system --no-create-home $SHMJ_USER -g $SHMJ_GROUP
fi
# Register "$SHMJ_USER" as a postgres user with "Create DB" role attribute
su - postgres -c "createuser -d -R -S $SHMJ_USER" 2> /dev/null || true
# Configuration file
mkdir -p $SHMJ_CONFIGURATION_DIR
# can't copy debian config-file as addons_path is not the same
echo "[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = $SHMJ_USER
db_password = False
addons_path = /opt/shmj/dist/addons
" > $SHMJ_CONFIGURATION_FILE
chown $SHMJ_USER:$SHMJ_GROUP $SHMJ_CONFIGURATION_FILE
chmod 0640 $SHMJ_CONFIGURATION_FILE
# Log
mkdir -p $SHMJ_LOG_DIR
chown $SHMJ_USER:$SHMJ_GROUP $SHMJ_LOG_DIR
chmod 0750 $SHMJ_LOG_DIR
# Data dir
mkdir -p $SHMJ_DATA_DIR
chown $SHMJ_USER:$SHMJ_GROUP $SHMJ_DATA_DIR

INIT_FILE=/lib/systemd/system/shmj_mes.service
touch $INIT_FILE
chmod 0700 $INIT_FILE
cat << 'EOF' > $INIT_FILE
[Unit]
Description=shanghai mingjiang mes system
After=network.target

[Service]
Type=simple
User=shmj
Group=shmj
ExecStart=/usr/bin/shmj_mes.py --config=/etc/shmj/shmj-server.conf --without-demo=all

[Install]
WantedBy=multi-user.target
EOF
easy_install pyPdf vatnumber pydot psycogreen
