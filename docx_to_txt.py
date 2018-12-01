import os
import docx
import win32com.client

FILE_DIR = '/Users/nasif/Desktop/Mine/Workspace/vs_workspace/IGF-Data-Mining/Transcripts_2012_docs/'

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getDocText(filename):
    DOC_FILEPATH = "c:/temp/something.docx"
    doc = win32com.client.GetObject(DOC_FILEPATH)
    return doc.Range().Text.encode("ascii", "ignore")

doc_list = os.listdir(FILE_DIR)
tag = ".docx"

for doc in doc_list:
    # if doc.endswith(tag):
    #     print("Extracting from " + doc)
    #     txtfile = open(FILE_DIR + doc + '.txt', 'w')
    #     txtfile.write(str(getText(FILE_DIR + "/" + doc).encode("ascii", "ignore")))
    #     txtfile.close
    #     os.remove(FILE_DIR + "/" + doc)
    if not doc.endswith(tag):
        print("Extracting from " + doc)
        try:
            obj = win32com.client.GetObject(FILE_DIR + "/" + doc)
            text = obj.Range().Text
            txtfile = open(FILE_DIR + doc + '.txt', 'w')
            txtfile.write(str(text.encode("ascii", "ignore")))
            txtfile.close
            os.remove(FILE_DIR + "/" + doc)
        except:
            pass


print ("Mission is a success")
# print("Original list " + str(len(doc_list)))