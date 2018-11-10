import requests
import os
from bs4 import BeautifulSoup

# The directory where all the transcripts are to saved after mining
FILE_DIR = '/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/Transcripts_2012/'

# send a GET request, pose as a Mozilla Firefox agent
url = "http://www.intgovforum.org/multilingual/content/igf-2012"
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
begin = "http://www.intgovforum.org/cms/component/content/article/1249"
end = "http://www.intgovforum.org/cms/component/content/article/114-preparatory-process/1260-igf-2012-closing-ceremony-"
begin_index = link_list.index(begin)
end_index = link_list.index(end)

# compose the cleaned out list with only the relevant links
print("Finding transcript only links...")
revised_list = link_list[begin_index:end_index+1]

# concatenate the extension of the relevant links and the base url to be able to
# access those links later on, print the result in a new list
final_links = []
for item in revised_list:
    # url = 'http://www.intgovforum.org'
    # concat = url + item
    final_links.append(item)

# access the links in final_links list
filenumber = 0 
for url in final_links:
    filenumber = filenumber + 1
    r = requests.get(url, headers=headers)
    print (url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')


# extract the JavaScript from the transcript and only leave the text
    for script in soup(["script", "style"]):
        script.extract()   

    text = soup.body.get_text()

# further clean the text by deleting blank spaces between lines and encode the 
# the final text in utf-8 format, in case there is any unknown letters
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = str(text.encode("ascii", "ignore"))

# write the final product to a text file: only works for the last link in the list
    #fob = open('/Users/oliviadziwak/Documents/Lab SC/2017/file_' + str(filenumber) + '.txt', 'w')
    fob = open(FILE_DIR + 'file_' + str(filenumber) + '.txt', 'w')
    fob.write(text)
    fob.close()
    print('Extracted and wrote transcript ' + str(filenumber) + ' to text file')

# iterate over the elements in the revised_list (with hyperlink extensions) and clean the links
# by removing the "/" 
final_list = []
number = 0
for element in revised_list:
    link = revised_list[number]
    split = link.split("/")
    final_list.append(split)
    number = number + 1

# after creating a list of lists, take only the 4th element and append it to a finalized list
finalized = []
file_num = 0
for element in final_list:
    try:
        result = element[8]
    except:
        result = "opening-ceremony"
    # finalized.append(result)

# rename the files appropriately by their names as appears on the link
    file_num = file_num + 1
    old_file = FILE_DIR + 'file_' + str(file_num) + '.txt'
    new_file = FILE_DIR + str(result) + '.txt'
    os.rename(old_file, new_file)
    