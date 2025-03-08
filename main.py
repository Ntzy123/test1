from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)
DIRECTORY = "download/"

@app.route('/')
def index():
    return render_template('index.html')


###/download下载页面
#遍历目录
def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

#设置download路由
@app.route('/download')
def list_directory():
    files = list_files(DIRECTORY)
    return render_template('file_list.html', files=files)

#限制文件路径防止被路径遍历攻击
@app.route('/download/<path:filename>')
def download_file(filename):
    safe_path = os.path.join(DIRECTORY, filename)
    if not safe_path.startswith(DIRECTORY):
        abort(403)
    return send_from_directory(DIRECTORY, filename, as_attachment=True)


#启动
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
