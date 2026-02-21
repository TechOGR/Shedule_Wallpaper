from os.path import join
from flask import jsonify, render_template, send_file, request

from server.modules.excel import Horario
from server.modules.config import AppConfig
from server.modules.recycle_bin import RecycleBin


def register_routes(app, full_path):
    rb = RecycleBin()
    app_config = AppConfig(full_path)

    horario_a = Horario(full_path, "Horario.xlsx")
    horario_b = Horario(full_path, "HorarioB.xlsx")

    path_images = join(full_path, "server", "static", "img")

    @app.route("/img/wallpaper.jpg")
    def wall():
        return send_file(join(path_images, "wallpaper.jpg"))

    @app.route("/img/trashBin.png")
    def img_trash():
        return send_file(join(path_images, "trashBin.png"))

    @app.route("/api/data")
    def api_data():
        week = app_config.get_all().get("activeWeek", "A")
        horario = horario_a if week == "A" else horario_b
        return jsonify(horario.getHorario())

    @app.route("/api/config")
    def get_config():
        return jsonify(app_config.get_all())

    @app.route("/api/config", methods=["POST"])
    def set_config():
        data = request.get_json()
        updated = app_config.update(data)
        return jsonify(updated)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/binInfo")
    def data_bin():
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
        except Exception:
            return jsonify({'numFiles': 0, 'size': '0', 'status': 'Empty'})

    @app.route("/api/empty")
    def empty_trash():
        try:
            returned = rb.emptyTrash()
            return jsonify({'message': returned})
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500

    @app.route("/api/getInfoFiles")
    def info_files():
        try:
            names, paths = rb.getPropertiesFile()
            return jsonify({
                'names': names,
                'paths': paths
            })
        except Exception as e:
            return jsonify({'names': [], 'paths': [], 'error': str(e)})

    @app.route("/api/restore", methods=["POST"])
    def restore_file():
        data = request.get_json()
        path = data.get('path', '')

        try:
            result = rb.restoreFile(path)
            return jsonify({'message': result})
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
