from ..modules.dataExcel import Horario
from ..modules.appConfig import AppConfig

from os.path import (
    join
)

from flask import (
    jsonify,
    render_template,
    send_file,
    request
)

from ..modules.recycleBin import RecycleBin

def Router(_app, full_path_project):
    
    rb = RecycleBin()
    
    full_path = full_path_project
    
    app_config = AppConfig(full_path)
    
    horario_a = Horario(full_path, "Horario.xlsx")
    horario_b = Horario(full_path, "HorarioB.xlsx")
    
    path_images = join(full_path, "client", "static", "img")
    
    @_app.route("/img/wallpaper.jpg")
    def wall():
        return send_file(join(path_images, "wallpaper.jpg"))
    
    @_app.route("/img/trashBin.png")
    def imgTrash():
        return send_file(join(path_images, "trashBin.png"))
    
    @_app.route("/api/data")
    def api_Data():
        week = app_config.get_all().get("activeWeek", "A")
        horario = horario_a if week == "A" else horario_b
        return jsonify(horario.getHorario())
    
    @_app.route("/api/config")
    def getConfig():
        return jsonify(app_config.get_all())
    
    @_app.route("/api/config", methods=["POST"])
    def setConfig():
        data = request.get_json()
        updated = app_config.update(data)
        return jsonify(updated)
    
    @_app.route("/")
    def index():
        
        return render_template("index.html")
    
    @_app.route("/api/binInfo")
    def dataBin():
        try:
            result = rb.getNumFiles()
            if result == "Error":
                return jsonify({'numFiles': 0, 'size': '0', 'status': 'Empty'})
            numFiles, size, status = result
            return jsonify({
                'numFiles': numFiles,
                'size': size,
                'status': status
            })
        except Exception as e:
            return jsonify({'numFiles': 0, 'size': '0', 'status': 'Empty'})
    
    @_app.route("/api/empty")
    def emptyTrash():
        try:
            returned = rb.emptyTrash()
            return jsonify({'message': returned})
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
    
    @_app.route("/api/getInfoFiles")
    def infoFiles():
        try:
            names, paths = rb.getPropertiesFile()
            return jsonify({
                'names': names,
                'paths': paths
            })
        except Exception as e:
            return jsonify({'names': [], 'paths': [], 'error': str(e)})
    
    @_app.route("/api/restore", methods=["POST"])
    def restoreFile():
        data = request.get_json()
        path = data.get('path', '')
        
        try:
            result = rb.restoreFile(path)
            return jsonify({'message': result})
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
