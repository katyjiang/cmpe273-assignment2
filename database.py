import sqlite3
import os
import json

# json type is not a official type supported by sqlite3
# After test and trial, I found json type is in fact equal to TEXT
CREATE_SUBJECT_TABLE_SCHEMA = r"CREATE TABLE IF NOT EXISTS subject (test_id integer PRIMARY KEY AUTOINCREMENT, subject TEXT, answer_keys json)"
CREATE_SCANTRON_TABLE_SCHEMA = r"CREATE TABLE IF NOT EXISTS scantron (scantron_id integer PRIMARY KEY AUTOINCREMENT, test_id integer, scantron_url TEXT, subject TEXT, score integer, result json, FOREIGN KEY(test_id) REFERENCES subject(test_id))"

# The sql statement to insert data to table "subject"
# The question mark corresponding to column 'subject'/'answer_keys'
# Remember column 'test_id' is automatically generated
# the first value "null" is required in order to make auto-increment work
INSERT_SUBJECT_TABLE_SQL = r"insert into subject values(null, ?, ?)"
INSERT_SCANTRON_TABLE_SQL = r"insert into scantron values(null, ?, ?, ?, ?, ?)"

# We can write "select * from subject"
# but by writing following sql statement, later when we acess each row,
# we can guarantee row[0] represent test_id, row[1] represent subject, row[2]
# represent answer_keys
QUERY_SUBJECT_TABLE_SQL = r"select test_id, subject, answer_keys from subject"

QUERY_SCANTRON_TABLE_SQL= r"select scantron_id, scantron_url, subject, score, result from scantron"


# A function used to create folders/sqlite-database/sqlite-tables
# when correesponding folders/sqlite-database/sqlite-tables not exist
def createTable():

    # os.mkdir(string) will throw exception if the folder already exist
    try:
        os.mkdir("sqlite")
    except FileExistsError:
        pass # Do nothing

    # By using with statement, the connection will be closed automatically
    # when the statements inside "with" finished
    conn = sqlite3.connect("sqlite/score.db")
    cur = conn.cursor()
    cur.execute(CREATE_SUBJECT_TABLE_SCHEMA)
    cur.execute(CREATE_SCANTRON_TABLE_SCHEMA)
    conn.commit() # Save the change
    conn.close() # Close the connection


"""The argument is supposed to be a json data which conform
the format given in the teacher's instruction
We return the newly inserted row id
"""
def insertNewSubject(jsonData):
    conn = sqlite3.connect("sqlite/score.db")
    cur = conn.cursor()
    cur.execute(INSERT_SUBJECT_TABLE_SQL, [jsonData["subject"], json.dumps(jsonData["answer_keys"])])
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def querySubjectTable(test_id = None):
    query_string = QUERY_SUBJECT_TABLE_SQL
    if test_id is not None:
        query_string = query_string + r" where test_id == " + str(test_id)
    conn = sqlite3.connect("sqlite/score.db")
    cur = conn.cursor()
    cur.execute(query_string)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def insertNewScantron(jsonData, test_id):
    conn = sqlite3.connect("sqlite/score.db")
    cur = conn.cursor()
    cur.execute(INSERT_SCANTRON_TABLE_SQL, [test_id, jsonData["scantron_url"], jsonData["subject"], jsonData["score"], json.dumps(jsonData["result"])])
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def queryScantronTable(test_id):
    query_string = QUERY_SCANTRON_TABLE_SQL
    query_string = query_string + r" where test_id == " + str(test_id)
    conn = sqlite3.connect("sqlite/score.db")
    cur = conn.cursor()
    cur.execute(query_string)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# For test only
NEW_SUBJECT_JSON = """
{
    "subject": "Math",
    "answer_keys": {
        "1": "A",
        "2": "B",
        "3": "C",
        "49": "D",
        "50": "E"
    }
}"""
    
# For testing only
if __name__ == "__main__":
    createTable()
    data = json.loads(NEW_SUBJECT_JSON)
    insertNewSubject(data)
    rows = querySubjectTable()
    for row in rows:
        print(row["answer_keys"])
