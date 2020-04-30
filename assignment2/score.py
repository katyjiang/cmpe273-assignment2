import sys
import json
from database import createTable, insertNewSubject, querySubjectTable
from ocr import process
from collections import OrderedDict

""" We will use pytesseract to do OCR on the scantron, the output from OCR
is multiple lines (in fact is 50 lines in our code) of text. We will anaylze
each line to get the answer marked by tester. 
So how? since tester will use their pencil to completely 
mark the box, so each line should have 4 columns of text, we analyze
each column, thus we can get which letter is marked by tester
Example, say user marked B black, then OCR output of this line
will have 4 columns which should have text "A", "C", "D", "E",
if we found those 4 text, we know user select B

In some case, the line didn't have 4 cloumns, then we will think user
select C :)))

test_id is the subject of the subject the scantron correspond to
filePath is the path of the scantron
return value will be a dict, has three key-value pairs,
<subject, ?>
<score, ?>
<result, {}>"""
def calculate_score(test_id, file_path):

    # Get the correct answer from datbase for text_id
    oneRow = querySubjectTable(test_id)[0] # We know the result will have only 1 row
    answer_keys = oneRow[2] # Our query guarantee column 2 is the answer keys
    answer_keys = json.loads(answer_keys) # Convert string to json object

    # Get 50 lines of text from student's submission
    text = process(file_path)
    lines = text.splitlines() # will split text into multiple lines

    # The value we return from this function
    ret = {"subject": oneRow[1]}

    
    # Now do the score calculation
    line_number = 1
    total_score = 0
    result = OrderedDict()
    for line in lines:
        user_selection = get_user_selection(line)
        correct_answer = answer_keys[str(line_number)]
        
        if user_selection == correct_answer:
            total_score = total_score + 1
            
        tmp = {"actual": user_selection, "expected": correct_answer}
        result.update({str(line_number): tmp})

        line_number = line_number + 1

        if line_number > 50:
            break

    ret.update({"score": total_score})
    ret.update({"result": result})

    return ret

# Get user selection, returned value either be "A" or "B"
# or "C" or "D" or "E".
def get_user_selection(line):
    columns = line.split() # By default split by whitespace
    
    # define an array to indicate whether we have found "A", "B"
    # "C", "D", "E"
    found = [False, False, False, False, False]

    # It should have 5 columns, but sometimes ocr doesn't work
    # perfectly.
    for col in columns:
        if "A" in col:
            found[0] = True
        if "B" in col:
            found[1] = True
        if "C" in col:
            found[2] = True
        if "D" in col:
            found[3] = True
        if "E" in col:
            found[4] = True

    not_found = -1
    for i in range(5):
        if not found[i]:
            not_found = i
            break

    if not_found == -1:
        return "C" # A mysterious theory every student should know :)
    elif not_found == 0:
        return "A"
    elif not_found == 1:
        return "B"
    elif not_found == 2:
        return "C"
    elif not_found == 3:
        return "D"
    elif not_found == 4:
        return "E"

# For testing purpose only, how to run the test?
# 1) Download the scantron-100.jpg to the same folder as this file
# 2) Open terminal, run
#    ====================================
#    python3.8 databse.py
#    ====================================
#    which will insert a test answer to the database
# 3) then run
#    ====================================
#    python3.8 score.py scantron-100.jpg
#    ====================================
if __name__ == "__main__":
    print(calculate_score(1, sys.argv[1]))
    
    
    

