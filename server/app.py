import sys
import tracemalloc
from flask import Flask
from threading import Thread
from os.path import join
from flask_cors import CORS

from server.routes import register_routes


class MainServer:

    def __init__(self, full_path):
        tracemalloc.start()
        self.full_path = full_path
        self._init_flask()

    def _init_flask(self):
        path_template = join(self.full_path, "server", "templates")
        path_static = join(self.full_path, "server", "static")

        self.app = Flask(
            import_name=__name__,
            static_folder=path_static,
            template_folder=path_template,
        )
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        register_routes(self.app, self.full_path)

    def init_server(self):
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        self.app.run("localhost", 5000)

    def stop_server(self):
        # Flask dev server doesn't support clean shutdown from another thread.
        # The daemon=True flag ensures the thread dies when the main app exits.
        pass
