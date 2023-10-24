#-------------------------------------------------------------------------
# AUTHOR: Nathan Pham
# FILENAME: db_connection_mongo.py
# SPECIFICATION: implementing a mongodb database and using pymongo
# FOR: CS 4250- Assignment #2
# TIME SPENT: 2.5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
import datetime

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    DB_NAME = "corpus"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    index = {}
    docTextList = docText.lower().replace(".","").replace("?","").replace("!","").replace(",","")
    docTextList = docTextList.split(" ")

    for text in docTextList:
        if text in index:
            index[text] = index.get(text) + 1
        else:
            index[text] = 1


    # create a list of dictionaries to include term objects.
    # --> add your Python code here
    term = []
    docTextListUnqiue = list(set(docTextList))
    for text in docTextListUnqiue:
        tempDict = {}
        tempDict[text] = len(text)
        term.append(tempDict)

    #Producing a final document as a dictionary including all the required document fields
    # --> add your Python code here
    docId = int(docId)
    document = {
        "id": docId,
        "title": docTitle,
        "text": docText,
        "num_chars": len(docText),
        "date": docDate,
        "categories": {
            "category": docCat
        },
        "index": index,
        "terms": term
    }

    # Insert the document
    # --> add your Python code here
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    docId = int(docId)
    col.delete_one({"id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    deleteDocument(col, docId)

    # Create the document with the same id
    # --> add your Python code here
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    pipeline = [
    {
        '$project': {
            'title': 1, 
            'index': 1
        }
    }
]
    index = col.aggregate(pipeline)
    invertedIndex = "{"
    for terms in index:
        keys = list(terms["index"].keys())
        values = list(terms["index"].values())
        for key, value in zip(keys, values):
            invertedIndex += "\'"+ key + "\':\'"+ terms["title"] + ":" + str(value) + "\',"
    invertedIndex = invertedIndex[:-1]
    invertedIndex += "}"

    return invertedIndex