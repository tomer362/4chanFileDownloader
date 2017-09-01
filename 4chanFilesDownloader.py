import requests
from bs4 import BeautifulSoup
import urllib2
import os
import threading

def get_data_from_thread(input_url, optional_board_folder = None):
    try:
        source_code = requests.get(input_url)
        content = source_code.content
        soup = BeautifulSoup(content, "html.parser")
        directory_name = input_url.split('/')[-1]
        if not os.path.exists(directory_name):
            allFiles = soup.findAll("a", {"class": "fileThumb"})
            allFilesTexts = soup.findAll("div", {"class": "fileText"})

            if len(allFiles) != 0:
                print "\nCreating A directory for the data from", directory_name, "thread...", "\n"
                if optional_board_folder != None:
                    os.makedirs((optional_board_folder + '/' + directory_name))
                    links_file = open((optional_board_folder + "/" + directory_name + "/links.txt"), "w")
                else:
                    os.makedirs(directory_name)
                    links_file = open(directory_name + "links.txt")
                i = 0
                for file in allFiles:
                    file_original_name = allFilesTexts[i].find('a').contents[0]
                    print file_original_name, "Downloading"
                    resource = urllib2.urlopen(("http:" + file['href']))

                    if optional_board_folder != None:
                        file_name = (optional_board_folder + "/" + directory_name + "/" + file_original_name)
                        output_file = open(file_name, "wb")
                        output_file.write(resource.read())
                        output_file.close()
                    else:
                        file_name = (directory_name + "/" + file_original_name)
                        output_file = open(file_name, "wb")
                        output_file.write(resource.read())
                        output_file.close()
                    links_file.write(file['href'] + " : " + file_original_name + "\n")
                    i += 1
                links_file.close()

            else:
                print "\nNo Files in", input_url.split('/')[-1], "thread\n"
        else:
            print "Already A Directory Named As The Thread"
    except:
        print "\n\n\nWIERD!!!\n\n\n"


def get_data_from_board(board_url):
    source_code = requests.get(board_url)
    content = source_code.content
    soup = BeautifulSoup(content, "html.parser")

    directory_name = soup.find("div", {"class": "boardTitle"}).contents[0]
    directory_name = (directory_name.split("/")[1] + directory_name.split("/")[2])
    print directory_name
    if not os.path.exists(directory_name):
        print "\nCreating A directory for the data from", directory_name, "board...", "\n"
        os.makedirs(directory_name)

        threads_links_objects = soup.findAll("a", {"class": "replylink"})
        threads = []
        for thread_link_object in threads_links_objects:

            thread_link = board_url + "/" + thread_link_object['href']
            threads.append(threading.Thread(target = get_data_from_thread, args = (thread_link, directory_name)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    else:
        print "Already Taken board folder name"

def check_if_real_shortcut(board_shortcut):
    source_code = requests.get("http://boards.4chan.org/wsg/")
    content = source_code.content
    soup = BeautifulSoup(content, "html.parser")

    board_list = soup.find("span", {"class" : "boardList"})
    for i in board_list.contents:
        if i.find("a") == None:
            if ''.join(i.find(text=True)) == board_shortcut:
                return True
    return False


#input_url = raw_input("Enter Url of a board:")

board_shortcut = raw_input("Enter Board Shortcut: ")
if check_if_real_shortcut(board_shortcut) == True:
    get_data_from_board(("http://boards.4chan.org/" + board_shortcut + "/"))
else:
    print "Not A Real Board from 4chan"



