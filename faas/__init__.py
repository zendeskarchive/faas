from flask import Flask

app = Flask(__name__)

import faas.index
import faas.restart
import faas.oom
import faas.logs
import faas.info
import faas.stop_listener

require_authentication = False
application_tokens = []
log_directory = ""
