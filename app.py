import os
from hailai import *
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #print('upload_image filename: ' + os.path.join(app.config['UPLOAD_FOLDER'], filename))

            path = getListImg(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            list = os.listdir(path)
            listImg = []
            for x in list:
                listImg.append(os.path.join(path, x))
            print((listImg))
            return render_template('upload.html', filename=os.path.join(app.config['UPLOAD_FOLDER'], filename), listImg=listImg)
        else:

            return redirect(request.url)
    else:
        return render_template('upload.html')



# chạy server
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port='5555')