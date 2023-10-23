#-------------------------------------------------------------------------
# AUTHOR: Nathan Pham
# FILENAME: db_connection.py
# SPECIFICATION: use psycopg2 to access the database and use sql commands
# FOR: CS 4250- Assignment #1
# TIME SPENT: 4 hr
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "password"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, cursor_factory=RealDictCursor)
        return conn
    except:
        print("Database not connected successfully")
    

def createCategory(cur, catId, catName):

    # Insert a category in the database
    # --> add your Python code here
    sql = "INSERT INTO categories (id, name) VALUES (%s, %s)"
    
    recset = [catId, catName]
    cur.execute(sql, recset)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    cur.execute("SELECT id FROM categories WHERE name = %(docCat)s", {'docCat': docCat})
    recset = cur.fetchall()
    catId = recset[0]['id']


    # 2 Insert the document in the database
    # --> add your Python code here
    sql = "INSERT INTO documents (doc, text, title, num_chars, date, id_category) VALUES (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, len(docText), docDate, catId]
    cur.execute(sql,recset)

    # 3 Update the potential new terms. Remember to format the terms to lowercase and to remove punctuation marks.
    # 3.1 Find all terms that belong to the document
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    docText = docText.lower().replace(".","").replace("?","").replace("!","")
    docTextList = docText.split(" ")
    docTextListUnqiue = list(set(docTextList))

    cur.execute("SELECT term FROM terms")
    recset = cur.fetchall()
    
    dbTermList = []
    for item in recset:
        dbTermList.append(item['term'])

    for text in docTextListUnqiue:
        if text not in dbTermList:
            sql = "INSERT INTO terms (term, num_chars) VALUES (%s, %s)"
            recset = [text, len(text)]
            cur.execute(sql, recset)


    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    docDict = {}
    for text in docTextList:
        if text in docDict:
            docDict[text] = docDict.get(text) + 1
        else:
            docDict[text] = 1

    for key in list(docDict.keys()):
        sql = "INSERT INTO index (term, id_doc, count) VALUES (%s, %s, %s)"
        recset = [key, docId, docDict[key]]
        cur.execute(sql, recset)


def deleteDocument(cur, docId):

    # 1 Query the index based on the document
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    cur.execute("SELECT term FROM index WHERE id_doc = %(docId)s", {'docId': docId})
    recset = cur.fetchall()
    termToBeChecked = []
    for item in recset:
        termToBeChecked.append(item['term'])
    cur.execute("DELETE FROM index WHERE id_doc = %(docId)s", {'docId': docId})

    cur.execute("SELECT term FROM index")
    recset = cur.fetchall()
    currentTermsInIndex = []
    for item in recset:
        currentTermsInIndex.append(item['term'])

    for term in termToBeChecked:
        if term not in currentTermsInIndex:
            cur.execute("DELETE FROM terms WHERE term = %(term)s", {'term': term})


    # 2 Delete the document from the database
    # --> add your Python code here
    cur.execute("DELETE FROM documents WHERE doc = %(docId)s", {'docId': docId})

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    invertedIndex = "{"
    cur.execute("SELECT index.term, documents.title, index.count FROM index INNER JOIN documents ON index.id_doc = documents.doc ORDER BY index.term ASC")
    recset = cur.fetchall()
    for item in recset:
        invertedIndex += "'" + item['term'] + "':'" + item['title'] + "':'" + str(item['count']) + ","
    invertedIndex = invertedIndex[:-1]
    invertedIndex += "}"
    return invertedIndex

    