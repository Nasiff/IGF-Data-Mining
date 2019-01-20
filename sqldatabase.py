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

print ("Number of transcripts in folder " + str(len(list_of_files)))

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
connection.close()