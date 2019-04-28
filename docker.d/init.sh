#!/bin/bash
set -e
# APP_CHANNEL should be set to "dev" or "production" depending on the environment
test $APP_CHANNEL

CONFIGDIR=/app/configs
CONFIGLOADER=/app/bin/configloader
SCRIPTWORKER=/app/bin/scriptworker

# TaskCluster doesn't accept WORKER_ID longer than 22 chars, take the meaningful last 22 characters
export WORKER_ID=${HOSTNAME:-22}
export TASK_SCRIPT_CONFIG="$CONFIGDIR/worker.json"

mkdir -p -m 700 $CONFIGDIR

# Eval JSON-e expressions in the config templates
$CONFIGLOADER /app/docker.d/configs/scriptworker.yaml $CONFIGDIR/scriptworker.json
$CONFIGLOADER /app/docker.d/configs/$APP_CHANNEL/worker.json $CONFIGDIR/worker_config.json

echo $ED25519_PRIVKEY > $CONFIGDIR/ed25519_privkey
chmod 600 $CONFIGDIR/ed25519_privkey

exec $SCRIPTWORKER $CONFIGDIR/scriptworker.json
