from flask import Flask, send_from_directory, render_template, request, Response, abort
import os
import time
from src.tools import format_file_size

app = Flask(__name__)

FILE_DIR = os.path.join(os.path.dirname(__file__), 'files')

if not os.path.exists(FILE_DIR):
	os.path.mkdir(FILE_DIR)
print(FILE_DIR)


@app.route('/download')
def download():
    return send_from_directory(os.path.join(FILE_DIR, request.args['dir'].replace("$.$", "\\")),
                               request.args["fileName"])


@app.route('/upload', methods=['POST'])
def upload():
    path = os.path.join(FILE_DIR, request.args['dir'], request.files.get("file").filename)
    if os.path.exists(path):
        return "文件已存在"
    request.files.get("file").save(path)
    return "200"


@app.route('/delete', methods=['POST'])
def delete():
    file_dir = os.path.join(FILE_DIR, request.json.get("dir"), request.json.get("fileName"))
    if os.path.isdir(file_dir):
        try:
            os.rmdir(file_dir)
        except OSError:
            abort(400)
    else:
        os.remove(file_dir)
    return "ok"


@app.route('/edit', methods=['POST'])
def edit():
    relate_dir = request.json.get("dir")
    old_file_nm = request.json.get('fileName')
    new_file_nm = request.json.get('newFileName')
    os.rename(os.path.join(FILE_DIR, relate_dir, old_file_nm), os.path.join(FILE_DIR, relate_dir, new_file_nm))
    return 'ok'


@app.route("/listdir", methods=['POST'])
def listdir():
    file_list = os.listdir(os.path.join(FILE_DIR, request.json.get('dir')))
    res = []
    file_res = []
    dir_res = []
    for file in file_list:
        file_dir = os.path.join(FILE_DIR, request.json.get('dir'), file)
        is_dir = os.path.isdir(file_dir)
        if is_dir:
            dir_res.append(
                {
                    'fileName': file,
                    'chgTime': time.ctime(os.path.getmtime(FILE_DIR)),
                    'isDir': is_dir
                }
            )
        else:
            file_res.append(
                {
                    'fileName': file,
                    'chgTime': time.ctime(os.path.getmtime(FILE_DIR)),
                    'isDir': is_dir,
                    'size': format_file_size(os.path.getsize(file_dir))
                }
            )
        res = dir_res + file_res
    return {'files': res}


@app.route("/createDir", methods=['POST'])
def create_dir():
    fold_dir = request.json.get('dir')
    fold_name = request.json.get('folderName')
    if os.path.isdir(os.path.join(FILE_DIR, fold_dir, fold_name)):
        abort(400)
    else:
        os.mkdir(os.path.join(FILE_DIR, fold_dir, fold_name))
        return 'ok'


@app.route("/")
def index():
    return render_template('index.html', curDir='')


if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=5200, debug=True)
