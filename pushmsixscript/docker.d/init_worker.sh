#!/bin/bash
set -o errexit -o pipefail

test_var_set() {
  local varname=$1

  if [[ -z "${!varname}" ]]; then
    echo "error: ${varname} is not set"
    exit 1
  fi
}

export REQUEST_TIMEOUT_SECONDS=90
export LOGIN_URL=https://login.microsoftonline.com
export TOKEN_RESOURCE=https://manage.devcenter.microsoft.com
export STORE_URL=https://manage.devcenter.microsoft.com/v1.0/my/applications/
export MOCK_APPLICATION_ID=MOCK-APP-ID
export RELEASE_ROLLOUT_PERCENTAGE=25.0

case $ENV in
  dev|fake-prod)
    ;;
  prod)
    test_var_set 'TENANT_ID'
    test_var_set 'CLIENT_ID'
    test_var_set 'CLIENT_SECRET'
    export TENANT_ID=`echo $TENANT_ID | base64 -d`
    export CLIENT_ID=`echo $CLIENT_ID | base64 -d`
    export CLIENT_SECRET=`echo $CLIENT_SECRET | base64 -d`
    ;;
  *)
    exit 1
    ;;
esac

case $COT_PRODUCT in
  firefox)
    export BETA_APPLICATION_ID=9NZW26FRNDLN
    export RELEASE_APPLICATION_ID=9NZVDKPMR9RD
    export TASKCLUSTER_SCOPE_PREFIX="project:releng:microsoftstore:"
    ;;
  thunderbird)
    export BETA_APPLICATION_ID=ZZZZZTBDZZZZZ
    export RELEASE_APPLICATION_ID=ZZZZZTBDZZZZZ
    export TASKCLUSTER_SCOPE_PREFIX="project:comm:thunderbird:releng:microsoftstore:"
    ;;
  *)
    exit 1
    ;;
esac
