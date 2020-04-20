# FaaS - Failure as a Service
Provides many misbehavior cases as a Service.

## General configuration

### Available command line flags

* `--port` - port to listen on
* `--host` - host to listen on (defaults to 0.0.0.0)
* `--config-file` - application config file
* `--log-directory` - application log directory (defaults to `cwd`)
* `--debug` - print debug info
* `--start-delay-seconds` start application after N seconds (defaults to 0)
* `--crash` - crash application before starting socket
* `--ignore-signal` - specify OS signal to be ignored in numeric format
* `--require-authentication` - enforce token base authentication - if set, `--config-file` is required as well

## Global GET parameters

* `delay` - wait N seconds before processing a request - this can simulate time-consuming operations (defaults to 1)
* `return_status_code` - what status code should be returned after processing a request


## Possible calls

### `GET /info`

Displays various informations about current server process.

### `GET /restart`

Kill application and let it be restarted. If `crash_loop` is set, during next startup, app will restart again.
Parameters
+ `exit_code` - exit code number to exit with (defaults to 0)
+ `crash_loop` - sets crash loop for this process by creating file `$PWD/crash_loop_${CRASH_LOOP_ENV_VAR}` - during startup, application will crash before opening listen socket if this file is found and `$CRASH_LOOP_ENV_VAR` is set by default to `NOMAD_ALLOC_ID` which leads to crash loop files: `$PWD/crash_loop_$ENV['NOMAD_ALLOC_ID']'` (defaults to False)

Exits the application with specified `exit_code`.

### `GET /oom`

Allocate `memory_mb_to_allocate` until reaching memory limit and possibly being killed by OOM killer.

Parameters
+ `memory_mb_to_allocate` - how much memory application will allocate in total (defaults to 0)
+ `steps` - split allocating memory to N steps (defaults to 1)
+ `sleep_between_steps` - sleep for N seconds between steps (defaults to 0)

### `GET /logs`

Generate `generate_bytes_per_second` logs to a given `output_fd_param`.

Parameters
+ `bytes_per_second` - how much logs we should generate per second (defaults to 1024)
+ `seconds` - generate logs for N seconds (defaults to 1)
+ `output_fd_param` - file to which generate logs (filename or stdout/stderr, defaults to stdout)

### `GET /stop_listener`

Stop TCP listener but keep the main process runnning.

## Copyright and license

Copyright 2020 Zendesk

Licensed under the [Apache License, Version 2.0](LICENSE)
