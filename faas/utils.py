import time
import psutil
import os
import yaml
import faas

# It's not exact byte, but as we generate more data
# the difference is insignificant
NEAR_BYTE = "z"
CRASH_LOOP_FILE_FORMAT = "crash_loop_{identifier}"


def get_current_process_rss():
    pid = os.getpid()
    return get_process_rss(pid)


def get_process_rss(pid):
    process = psutil.Process(pid)
    return process.memory_info().rss


def parse_global_args(request):
    delay = request.args.get('delay', default=1, type=int)
    return time.sleep(delay)


def get_crash_loop_file_identifier():
    return os.environ.get(
        os.environ.get("CRASH_LOOP_ENV_VAR", "NOMAD_ALLOC_ID"),
        None
    )


def set_crash_loop(identifier):
    with open(CRASH_LOOP_FILE_FORMAT.format(identifier=identifier), 'w+') as f:
        f.write("life is a crash.")
    return True


def is_crash_loop_set(identifier):
    return os.path.exists(
        CRASH_LOOP_FILE_FORMAT.format(identifier=identifier)
    )


def get_application_tokens(config_file_path, service_name='faas'):
    tokens = []
    try:
        with open(config_file_path) as f:
            config_world = yaml.load(f)
        application_token = config_world[service_name]['application_token']
        if isinstance(application_token, list):
            tokens = application_token
        else:
            tokens = [application_token]
    except KeyError:
        print("Missing key {}.application_tokens in config file. Exiting.".format(service_name))
        os._exit(1)
    except IOError or ValueError as e:
        print("Unable to parse {} file: {}. Exiting".format(
            config_file_path, str(e)
        ))
        os._exit(1)
    return tokens
