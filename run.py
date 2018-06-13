import argparse
import signal
import time

import faas
from faas.utils import is_crash_loop_set, get_crash_loop_file_identifier, get_application_tokens


def ignore_signal(signum, frame):
    print("Ignoring signal: {}".format(signum))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True, help="Port to listen on")
    parser.add_argument("--config-file", type=argparse.FileType(mode='r'),
                        help="Application config file")
    parser.add_argument("--host", default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--debug", action='store_true', help="Print debug info")
    parser.add_argument("--start-delay-seconds", default=0, type=int,
                        help="Start application after N seconds")
    parser.add_argument("--crash", action='store_true',
                        help="Crash application before starting socket")
    parser.add_argument("--ignore-signal", action='append', type=int,
                        help="Specify OS signal to be ignored in numeric format.")
    parser.add_argument("--require-authentication", action='store_true',
                        help="Enforce token base authentication")

    args = parser.parse_args()

    faas.require_authentication = args.require_authentication
    if faas.require_authentication:
        if not args.config_file:
            parser.error('The --require-authentication argument requires the --config-file')
        faas.application_tokens = get_application_tokens(args.config_file)

    options = {"threaded": True, "debug": True, "use_reloader": False}

    time.sleep(args.start_delay_seconds)
    if args.ignore_signal:
        # Using debug prevents from setting SIGTERM trap, therefore we need to disable it.
        options["debug"] = False
        for signal_to_ignore in args.ignore_signal:
            print("Setting trap for signal: {}".format(signal_to_ignore))
            signal.signal(signal_to_ignore, ignore_signal)

    crash_loop_set = is_crash_loop_set(get_crash_loop_file_identifier())

    if args.crash or crash_loop_set:
        raise Exception("Crash argument was set (crash loop: {}). Crashing!".format(crash_loop_set))
    faas.app.run(args.host, args.port, **options)
    while True:
        print "I'm still standing, which means FaaS app was terminated."
        time.sleep(1)

if __name__ == "__main__":
    main()
