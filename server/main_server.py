import sys
import tracemalloc
from flask import (
    Flask
)

from threading import (
    Thread
)

from os.path import (
    join
)
from flask_cors import CORS

from .router.router import Router


class MainServer:
    
    def __init__(self, full_path) -> None:
        
        tracemalloc.start()
        self.full_path = full_path
        
        self.initComponents()
        
    def initComponents(self):
        
        path_template = join(self.full_path, "client", "views")
        path_static = join(self.full_path, "client", "static")
        
        self.app = Flask(
            import_name=__name__,
            static_folder=path_static,
            template_folder=path_template,
        )
        CORS(
            self.app, 
            resources={r"/*": {"origins": "*"}}
        )
        
        self.routes()
        
    def initServer(self):
        self.hilo = Thread(target=self.initServer2)
        self.hilo.setName("threadServer")
        self.hilo.start()
       
    def initServer2(self):
        HOST = "localhost"
        PORT = "5000"
        
        self.app.run(HOST, PORT)
        sys.stdout = open("./output.txt", "w")
        
    
    def stopServer(self):
        self.stopServer2()
        
    def stopServer2(self):

        self.hilo.__stop()
    
    def routes(self):
        Router(self.app, self.full_path)
    