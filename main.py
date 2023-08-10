from flask import Flask, render_template, request, send_from_directory
import sqlite3, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

db = sqlite3.connect('album.db')
db.execute("CREATE TABLE IF NOT EXISTS photos(pid INTEGER PRIMARY KEY, photo TEXT);")
db.commit()
db.close()

@app.route('/', methods=["GET","POST"])
def home():
  if request.method == "POST" and \
  request.files and 'photo' in request.files: # check existance of photos and file
    # get file
    photo = request.files['photo']
    # protect file
    filename = secure_filename(photo.filename)
    # form and save file
    path = os.path.join('uploads', filename)
    photo.save(path)
    db = sqlite3.connect('album.db')
    db.execute("INSERT INTO photos(photo) VALUES(?)", (filename,))
    db.commit()
    db.close()
    
  return render_template('index.html')
@app.route('/view')
def view():
  db = sqlite3.connect('album.db')
  recs = db.execute("SELECT * FROM photos;")
  pics = []
  for rec in recs:
    pics.append(rec[1])
  db.close()
  return render_template('view.html', pics=pics)

@app.route('/photos/<filename>')
def get_file(filename):
  return send_from_directory('uploads', filename)
app.run(host='0.0.0.0', port=81)

