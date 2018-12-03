import sqlite3
import os
import time
import requests
from bs4 import BeautifulSoup

# The file directory to put the database in
FILE_DIR = '/Users/nasif/Desktop/Mine/Workspace/vs_workspace/IGF-Data-Mining/'
# The global variable that says the script which year of transcripts to add to the database
TRANSCRIPT_YEAR = 2012
# The global indexes that needs to be changed to reflect the current transcript year
# Lets the script know where the transcript only links start and end.
BEGIN_URL = 'http://www.intgovforum.org/cms/IGF-OpeningSession-301006.txt'
END_URL = 'http://www.intgovforum.org/cms/IGF-Closing%20Ceremony.txt'

# Connect to the database and initialize the cursor
connection = sqlite3.connect(FILE_DIR + "TranscriptsIGF.db")
cursor = connection.cursor()

# Create the TABLE for the database and commit the changes
sql_command = """CREATE TABLE IF NOT EXISTS Transcripts (
    Year INTEGER,
    Panel_Name TEXT,
    Content TEXT,
    URL TEXT,
    Date_Accessed TEXT
);"""
cursor.execute (sql_command)
connection.commit()

# send a GET request, pose as a Mozilla Firefox agent
url = 'http://www.intgovforum.org/multilingual/content/first-igf-meeting-athens-greece'
headers={'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
print (url)
print (headers)
print ("Getting the urls for transcripts of the year " + str(TRANSCRIPT_YEAR) + "...")
html = r.text

# convert html into BS object
soup = BeautifulSoup(html, 'html.parser')
hrefs = soup.find_all('a')

# get all the links from the main page into a list
url_list = []
url_first_half = '' # http://www.intgovforum.org
for link in hrefs: 
	url_second_half = link.get('href')
	url_list.append(url_first_half + str(url_second_half))

# Select links that are transcript related and discard all the others
begin = url_first_half + BEGIN_URL
end = url_first_half + END_URL
begin_index = url_list.index(begin)
end_index = url_list.index(end)
url_list = url_list[begin_index : end_index + 1] # List now only has transcript urls

print ("Fetched all the URLs successfully.")
print ("Starting to add everything to the database.")

# Gather all the appropriate column information from the transcript file directory to add to the database
list_of_files = os.listdir(FILE_DIR + "/Transcripts_" + str(TRANSCRIPT_YEAR))


# TEST
# index = 0
# for f in list_of_files:
#     list_of_files[index] = list_of_files[index][:-4]
#     index = index + 1

# url_list.remove("http://www.intgovforum.org/cms/../index.php/component/chronocontact/?chronoformname=WSProposals2010View&wspid=61")
# url_list.remove("http://www.intgovforum.org/cms/dynamic-coalitions/694-dc10")

print ("Number of transcripts in folder " + str(len(list_of_files)))
# print ("Number of transcript urls " + str(len(url_list)))


# url_list.sort(key = lambda x : int(x.split("/")[-1][0:3]))
# url_list.sort
# list_of_files.sort()


# index = 0
# for url in url_list:
#     url_list[index] = url.split("/")[-1]
#     index = index + 1

# print (url_list)
# print (list_of_files)

# print (set(url_list).difference(set(list_of_files)))

# for u,f in zip(url_list, list_of_files):
#     print (u + "| XXXXXXXXX |" + f)

# Index for the url_list
index = 0
for file in list_of_files:
    # Add the name of the file to be used as the name_of_panel later when it gets added to the database
    panel_name = file
    # Find the file in the directory so that it can be read
    input = FILE_DIR + "/Transcripts_" + str(TRANSCRIPT_YEAR) + "/" + file
    file_content = open(input, "r").read().replace("\\", "") # Replace all the backslashes in the file
    # Get the url of the current transcript file
    file_url = url_list[index]
    index = index + 1
    # Find the last accessed (data modified) of the transcript file
    epoch = os.path.getmtime(input)
    # Convert epoch time (which is in seconds) into date and time
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    # Add the values into appropriate columns in the database
    cursor.execute("INSERT INTO Transcripts VALUES (?, ?, ?, ?, ?)", (TRANSCRIPT_YEAR, panel_name, file_content, file_url, date))
    connection.commit() # Commit the changes
    print("Added " + file + " to the database")
print("Successfully added everything to the database!")

# panel_name_list = ["Opening Ceremony", 
# "Opening Session",
# "Realizing a multilingual internet",
# "Access",
# "Open Dialogue",
# "Dimensions of cyber security and cyber crime",
# "Fostering security, privacy, and openness",
# "Open dialogue",
# "Transition from ipv4 to ipv6", 
# "Global, regional and national arrangements",
# "Open dialogue", 
# "Emerging Issues", 
# "Taking stock and the way forward", 
# "Closing session"]

# url_list_new = ["http://www.intgovforum.org/cms/hydera/Opening%20Ceremony.pdf",
# "http://www.intgovforum.org/cms/hydera/Opening%20Session.pdf",
# "http://www.intgovforum.org/cms/hydera/RaMInternet.pdf",
# "http://www.intgovforum.org/cms/hydera/Access.pdf",
# "http://www.intgovforum.org/cms/hydera/Open%20Dialogue.pdf",
# "http://www.intgovforum.org/cms/hydera/HBD%20Cybercrime%204Dec08.txt",
# "http://www.intgovforum.org/cms/hydera/HBD%20Security%20Privacy%20Openness%204Dec08.txt",
# "http://www.intgovforum.org/cms/hyderabad_prog/Open%20Dialogue.html",
# "http://www.intgovforum.org/cms/hyderabad_prog/Transition%20from%20IPv4%20to%20IPv6.html",
# "http://www.intgovforum.org/cms/hyderabad_prog/AfIGGN.html",
# "http://www.intgovforum.org/cms/hyderabad_prog/OD_CIR.html",
# "http://www.intgovforum.org/cms/hyderabad_prog/Emerging%20issues.txt",
# "http://www.intgovforum.org/cms/hyderabad_prog/TSAWF.html",
# "http://www.intgovforum.org/cms/hyderabad_prog/Closing%20ceremony.html"]

# # Index for the url_list
# index = 0
# for file in list_of_files:
#     # Add the name of the file to be used as the name_of_panel later when it gets added to the database
#     panel_name = panel_name_list[index]
#     # Find the file in the directory so that it can be read
#     input = FILE_DIR + "/Transcripts_" + str(TRANSCRIPT_YEAR) + "/" + file
#     file_content = open(input, "r").read().replace("\\", "") # Replace all the backslashes in the file
#     # Get the url of the current transcript file
#     file_url = url_list_new[index]
#     index = index + 1
#     # Find the last accessed (data modified) of the transcript file
#     epoch = os.path.getmtime(input)
#     # Convert epoch time (which is in seconds) into date and time
#     date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
#     # Add the values into appropriate columns in the database
#     cursor.execute("INSERT INTO Transcripts VALUES (?, ?, ?, ?, ?)", (TRANSCRIPT_YEAR, panel_name, file_content, file_url, date))
#     connection.commit() # Commit the changes
#     print("Added " + file + " to the database")
# print("Successfully added everything to the database!")

connection.close()