from __future__ import print_function

import datetime
import time
import sys
import os
import faas

from faas import app
from faas.utils import NEAR_BYTE
from faas.auth_wrapper import verify_token
from flask import request


@app.route('/logs')
@verify_token()
def logs():
    seconds = request.args.get('seconds', default=1, type=int)
    generate_bytes_per_second = request.args.get(
        'bytes_per_second', default=1024, type=int
    )
    output_fd_param = request.args.get('output_fd', default="stdout")

    if output_fd_param in ["stdout", "stderr"]:
        output_fd = sys.stdout if output_fd_param == "stdout" else sys.stderr
    else:
        output_fd = open(
            os.path.join(
                str(faas.log_directory), os.path.basename(output_fd_param)
            ), "a+")

    output_per_second = NEAR_BYTE * generate_bytes_per_second + "\n"

    output_lines = list()

    for second in range(seconds):
        print(output_per_second, file=output_fd)
        output_fd.flush()
        output_lines.append(
            "{} - Wrote {} bytes in second".format(
                datetime.datetime.now(), generate_bytes_per_second, second
            )
        )
        time.sleep(1)
    output_lines.append(
        "Wrote {} bytes of logs to {}".format(
            generate_bytes_per_second * seconds, output_fd.name
        )
    )
    return "\n".join(output_lines)
