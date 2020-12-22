#!/bin/bash
set -euxo pipefail

main() {
  ARGS_MAIN="run:app --proxy-headers --timeout-keep-alive ${APP_TIMEOUT_KEEP_ALIVE:-75} --log-level ${APP_LOG_LEVEL:-info}"
  ARGS_NETWORK="--host ${APP_LISTEN_INTERFACE:-0.0.0.0} --port ${APP_PORT:-5000}"
  ARGS_ADDITIONAL="$@"
  [[ ${APP_UNIX_SOCKET_FILE:-""} != "" ]] && ARGS_NETWORK="--uds ${APP_UNIX_SOCKET_FILE}"
  run_service "$ARGS_MAIN $ARGS_NETWORK $ARGS_ADDITIONAL"
}

run_service(){
    exec uvicorn $@
}

main "$@"
