
#add data onto an the file
def append_to_file(link):
    with open("news.txt","a")as file:
        file.write(link + "\n")

#get all links from the file and add them to the list. Finally return the list
def getFileData():
     data = list()
     with open("news.txt", "rt")as file:
         for line in file:
             data.append(line.replace("\n",""))

     return data







