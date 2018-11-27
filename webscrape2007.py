import requests
import os
from bs4 import BeautifulSoup

# The directory where all the transcripts are to saved after mining
FILE_DIR = '/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/Transcripts_2007/'

# send a GET request, pose as a Mozilla Firefox agent
url = "http://www.intgovforum.org/multilingual/content/second-igf-meeting-rio-de-janeiro-brazil"
headers = {'User-Agent' : 'Mozilla/5.0'}
print("Establishing connection to: " + url)
print(headers)
r = requests.get(url, headers=headers)
html = r.text

# Convert html into BS object
soup = BeautifulSoup(html, 'html.parser')
hrefs = soup.find_all('a')

# get all the links from the main page into a list
print("Getting all the links on the page...")
link_list = []
for link in hrefs: 
    links = link.get('href')
    link_list.append(links)
print (links)

# identify the links of interest by examining the link_list
begin = "http://www.intgovforum.org/cms/Rio_Meeting/IGF2-opening-12NOV07.txt"
end = "http://www.intgovforum.org/cms/Rio_Meeting/IGF2-Closing-15NOV07.txt"
begin_index = link_list.index(begin)
end_index = link_list.index(end)

# compose the cleaned out list with only the relevant links
print("Finding transcript only links...")
revised_list = link_list[begin_index:end_index+1]

# after creating a list of lists, take only the 4th element and append it to a finalized list
print(revised_list)
file_num = 0

for element in revised_list:
    headers = {'User-Agent' : 'Mozilla/5.0'}
    print("Establishing connection to: " + element)
    print(headers)
    r = requests.get(element, headers=headers)
    transcript_text = r.text
    # print("*******************************************************")
    # print(transcript_text)
    try:
        name = revised_list[file_num]
        file_num = file_num + 1
        fob = open(FILE_DIR + str(file_num).zfill(2) + " " + name.split("/")[-1] + '.txt', 'w')
        fob.write(transcript_text)
        fob.close()
        print('Extracted and wrote transcript ' + str(file_num) + ' to text file')
    except UnicodeEncodeError:
        pass