from flask import Flask, escape, request
import json
from database import createTable, insertNewSubject, querySubjectTable, insertNewScantron, queryScantronTable 
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from score import calculate_score

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

HOST="127.0.0.1"
PORT="5000"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False # Prevent sort

# Create folder named "files" to save the files upload by user
def createUploadFolder():
    try:
        os.mkdir(UPLOAD_FOLDER)
    except FileExistsError:
        pass # Do nothing


# We call createTable/createUploadFolder first
createTable()
createUploadFolder()

@app.route('/api/tests', methods=["POST"])
def create_subject():
    data = request.get_json()
    test_id = insertNewSubject(data)
    data.update([("test_id", test_id), ("submissions", [])])
    return data, 201 # 201 is http predefined status code

@app.route('/api/tests/<test_id>/scantrons', methods=['GET', 'POST'])
def upload_file(test_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Now calculate score
            result = calculate_score(test_id, UPLOAD_FOLDER + "/" + filename)
            result.update({"scantron_url": "http://" + HOST + ":" + PORT + "/files/" + filename})
            
            # Insert into database
            row_id = insertNewScantron(result, test_id)

            result.update({"scantron_id": row_id})
            return result, 201

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/tests/<test_id>', methods=["GET"])
def get_all_submission(test_id):
    oneRow = querySubjectTable(test_id)[0]
    result = {"test_id": oneRow[0], "subject": oneRow[1], "answer_keys": json.loads(oneRow[2])}
    scantron_submissions = queryScantronTable(test_id)
    submissions = []
    for row in scantron_submissions:
        tmp = {}
        tmp.update({"scantron_id": row[0]})
        tmp.update({"scantron_url": row[1]})
        tmp.update({"subject": row[2]})
        tmp.update({"score": row[3]})
        tmp.update({"result": json.loads(row[4])})
        submissions.append(tmp)
    result.update({"submissions": submissions})
    return result

# Say after user upload a file pp.png (either use Postman or Curl or our upload.html),
# then user type "http://localhost:5000/files/pp.png" in the browser,
# following function will be called
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    # Turn debug mode to True if you want to test it
    app.run(debug=False)
    
