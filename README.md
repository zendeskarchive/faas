# FaaS - Failure as a service
Provides many misbehavior cases as a Service.

## General configuration

### Available command line flags

* `--port` - Port to listen on
* `--host` - Host to listen on. Default 0.0.0.0
* `--config-file` - Application config file
* `--debug` - Print debug info
* `--start-delay-seconds` - Start application after N seconds. Default 0
* `--crash` - Crash application before starting socket
* `--ignore-signal` - Specify OS signal to be ignored in numeric format
* `--require-authentication` - Enforce token base authentication. If set, `--config-file` is required as well.

## Global GET parameters

* `delay` - Default 1. How long app should sleep before processing request. This can simulate time-consuming operations.
* `return_status_code` - What status code should be returnet after processing request.


## Possible calls

### `GET /info`

Displays various informations about current server process.

### `GET /restart`

Kill application and let it be restarted. If `crash_loop` is set, during next startup, app will restart again.
Parameters
+ `exit_code` - Default: 0. Exit code number to exit with.
+ `crash_loop` - Default: False. Sets crash loop for this process by creating file `$PWD/crash_loop_${CRASH_LOOP_ENV_VAR}`. During startup, application will crash before opening listen socket if this file is found. `$CRASH_LOOP_ENV_VAR` is set by default to `NOMAD_ALLOC_ID` which leads to crash loop files: `$PWD/crash_loop_$ENV['NOMAD_ALLOC_ID']'`.

Exits the application with specified `exit_code`.

### `GET /oom`

Allocate `memory_mb_to_allocate` until reaching memory limit and possibly being killed by OOM killer.

Parameters
+ `memory_mb_to_allocate` - Default: 0. How much memory applicationw will allocate in total.
+ `steps` - Default: 1. Split allocating memory to N steps.
+ `sleep_between_steps` - Default: 0. Sleep between steps (in seconds).

### `GET /logs`

Generate `generate_bytes_per_second` logs to given `output_fd_param`

Parameters
+ `bytes_per_second` - Default: 1024. How much logs we should generate per second.
+ `seconds` - Default: 1. For how long generate logs.
+ `output_fd_param` - Default: stdout. File to which generate logs. This parameter has two special words:
    + `stdout` - generate logs to stdout
    + `stderr` - generate logs to stderr

### `GET /stop_listener`

Stop TCP listener but keep the main process runnning.
