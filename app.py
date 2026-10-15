"""Cloud Storage Explorer - a small web file manager for cloud buckets (S3) or a local folder."""
from flask import Flask, jsonify, redirect, render_template, request, send_file
from storage import get_backend

MAX_UPLOAD_MB = 50


def create_app(backend=None):
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
    store = backend or get_backend()

    @app.get("/")
    def index():
        return render_template("index.html", backend=store.name)

    @app.get("/api/list")
    def api_list():
        folders, files = store.list(request.args.get("prefix", ""))
        return jsonify(folders=folders, files=files)

    @app.post("/api/upload")
    def api_upload():
        prefix = request.form.get("prefix", "")
        for f in request.files.getlist("files"):
            if f.filename:
                store.upload(prefix, f.filename.replace("\\", "/").split("/")[-1], f.stream)
        return jsonify(ok=True)

    @app.get("/api/download")
    def api_download():
        key = request.args.get("key", "")
        if store.name == "s3":
            return redirect(store.download_url(key))
        path = store.download_path(key)
        if not path:
            return jsonify(error="Not found"), 404
        return send_file(path, as_attachment=True)

    @app.post("/api/delete")
    def api_delete():
        store.delete(request.get_json().get("key", ""))
        return jsonify(ok=True)

    @app.post("/api/folder")
    def api_folder():
        d = request.get_json()
        name = d.get("name", "").strip().strip("/")
        if not name:
            return jsonify(error="Name required"), 400
        store.create_folder(d.get("prefix", ""), name)
        return jsonify(ok=True)

    @app.errorhandler(ValueError)
    def bad_value(e):
        return jsonify(error=str(e)), 400

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
