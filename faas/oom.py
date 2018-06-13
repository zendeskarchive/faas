from __future__ import print_function

import time
import datetime

from faas import app
from faas.utils import NEAR_BYTE, get_current_process_rss
from faas.auth_wrapper import verify_token
from flask import request


@app.route('/oom')
@verify_token()
def oom():
    memory_mb_to_allocate = request.args.get('memory_mb_to_allocate', default=0, type=int)
    steps = request.args.get('steps', default=1, type=int)
    sleep_between_steps = request.args.get(
        'sleep_between_steps', default=0, type=int
    )

    output_lines = list()
    mem_acc = ""
    for i in range(steps):
        step_bytes = (1024**2 * memory_mb_to_allocate) / steps
        output_lines.append(
            "{} - Added {} MB in step {}".format(
                datetime.datetime.now(), step_bytes/1024**2, i
            )
        )
        mem_acc += NEAR_BYTE * step_bytes
        if sleep_between_steps:
            time.sleep(sleep_between_steps)

    output_lines.append(
        "Allocated {} mb of memory. Process RSS: {} bytes\n".format(
            memory_mb_to_allocate, get_current_process_rss()
        )
    )

    return "\n".join(output_lines)
