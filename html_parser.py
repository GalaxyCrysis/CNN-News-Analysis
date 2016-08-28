from bs4 import BeautifulSoup
import file_handler
"""
getUrl function: search for all links in the html and compare them with the saved html links in the file
if a link is not in the list, add the link onto the file and return the link
"""
def getUrl(html):
    soup = BeautifulSoup(html,"html.parser")
    list = file_handler.getFileData()

    for tag in soup.find_all("a"):
        for item in list:
            if item != tag.get("href"):
                file_handler.append_to_file(tag.get("href"))
                return tag.get("href")

"""
get Text function: We search for headline and  the main article div and then for all divs with the the plain text and add it to the text string.
Finally return the text strings for text analyzing
"""
def getText(html):
    soup = BeautifulSoup(html,"html.parser")
    text = ""
    headline = ""
    for tag in soup.find_all("h1"):
        headline = tag.get_text()
        break

    for tag in soup.find_all("div"):
        if tag.get("itemprop") == "articleBody":
            for div in tag.find_all("div"):
                if div.has_attr("class"):
                    for attr in div.get("class"):
                        if attr == "zn-body__paragraph":
                            text += div.get_text()


    return (headline,text)





















