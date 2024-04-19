from ..modules.dataExcel import Horario

from os.path import (
    join
)

from flask import (
    jsonify,
    render_template,
    send_file
)

def Router(_app, full_path_project):
    
    full_path = full_path_project
    
    horario = Horario(full_path)
    
    @_app.route("/api/data")
    def api_Data():
        
        horas = horario.getHorario()
        
        return jsonify(horas)
    
    @_app.route("/")
    def index():
        
        return render_template("index.html")
    
    @_app.route("/img/wallpaper.jpg")
    def wall():
        return send_file(join(full_path, "client", "static", "img", "wallpaper.jpg"))