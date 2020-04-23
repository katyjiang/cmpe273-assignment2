# Assignment 2 for [sithu/cmpe273-spring20] (https://github.com/sithu/cmpe273-spring20/tree/master/assignment2)

In my code, there are four python files and a test-data json file

* ocr.py
* app.py
* database.py
* score.py
* test-data.json

What each python file do is described below (Each file has plenty of comments if it doesn't bother you)

## ocr.py
ocr.py is using pytesseract to provide Optical Character Recognition capability. This file is also self-testable (need a scantron jpg file), suppose you already downloaded the scantron-100.jpg from [sithu/cmpe273-spring20] (https://github.com/sithu/cmpe273-spring20/tree/master/assignment2), you can run

```
python3.8 ocr.py scantron-100.jpg
```

The output is text (multiple lines) of the answer section of the scantron jpg

What does my code do? I first crop the part of the "answer section" of scantron-100.jpg, then do OCR only on this cropped part, this will avoid unnecessary noise, make the score calculation more accurate.

Caveat:

* Need to install [pytesseract](https://pypi.org/project/pytesseract/), [pillow](https://pypi.org/project/Pillow/) into your machine
* Need to install [Google tesseract](https://github.com/tesseract-ocr/tesseract), check instruction for how to
* python3.5 might also work afaik


## app.py
This file is used to start a restful web server (flask), you can start up the server either by run

```
python3.8 app.py
```

Or

```
pip3 install pipenv
pipenv install flask==1.1.1
pipenv shell
env FLASK_APP=app.py flask run

```
app.py is used to handle http request


## database.py
sqlite3 is required to store data, this file is holding all database CRUD functions.
I create two table, one for test-correct-answer, one for tester-submission.

The created db file will be stored in _./sqlite/_ folder, this file is also self-runnable, just run

```
python3.8 database.py
```

## score.py
This file is used by app.py, score.py use ocr.py to calculate score, and save the score into sqlite3 using database.py
This file is also self-runnable, but multiple steps required, check the code comment for howto

## test-data.json
A json file represent a Math subject correct answer


# Run the code as a whole
For simplicity, I will use Postman to verify functionality (You can also use CURL)

```
python3.8 app.py # Will start up the server
_Open Postman, copy the content of test-data.json, POST it to the server_
_Again use Postman to POST the scantron-100.jpg to the server (check a YouTube video for howto)_
_Do whatever assignment2 instructed to do_

```

# Note
When the web server start up, it will create two folders in current working directory, one is named "sqlite" for database file, another named "files" for user uploaded scantron jpg
