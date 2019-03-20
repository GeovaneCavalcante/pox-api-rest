from pox.core import core

from api.app import app

import os
import threading

log = core.getLogger()


def initialization(host, port):

    try:
        port = int(os.environ.get("PORT", port))
        app.run(host, port)
    except BaseException, error:
        log.error(error.message)


def launch(host, port):

    thread = threading.Thread(target=initialization,
                              kwargs={'host': host, 'port': port})
    thread.daemon = True
    thread.start()
