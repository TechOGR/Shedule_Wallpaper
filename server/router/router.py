from ..modules.dataExcel import Horario

from os.path import (
    join
)

from flask import (
    jsonify,
    render_template,
    send_file
)

from ..modules.recycleBin import RecycleBin

def Router(_app, full_path_project):
    
    rb = RecycleBin()
    
    full_path = full_path_project
    
    horario = Horario(full_path)
    
    path_images = join(full_path, "client", "static", "img")
    
    @_app.route("/img/wallpaper.jpg")
    def wall():
        return send_file(join(path_images, "wallpaper.jpg"))
    
    @_app.route("/img/trashBin.png")
    def imgTrash():
        return send_file(join(path_images, "trashBin.png"))
    
    @_app.route("/api/data")
    def api_Data():
        
        horas = horario.getHorario()
        
        return jsonify(horas)
    
    @_app.route("/")
    def index():
        
        return render_template("index.html")
    
    @_app.route("/api/binInfo")
    def dataBin():
        numFiles, size, status = rb.getNumFiles()
        
        objeto = {
            'numFiles': numFiles,
            'size': size,
            'status': status
        }
        
        return _app.json.dumps(objeto)
    
    @_app.route("/api/empty")
    def emptyTrash():
        
        returned = rb.emptyTrash()
        
        objeto = {
            'message': returned
        }
        
        return _app.json.dumps(objeto)
    
    @_app.route("/api/getInfoFiles")
    def infoFiles():
        
        names, paths = rb.getPropertiesFile()
        with open("./esto.txt", "w") as f:
            f.write(str({"names": names, "paths": paths}))
            f.close()
            
        objeto = {
            'names': names,
            'paths': paths
        }
        print(objeto)
        
        return _app.json.dumps(objeto)