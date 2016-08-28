from PyQt4.QtCore import QThread,SIGNAL
from urllib.request import urlopen
import file_handler

import html_parser
class Worker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.url = "http://edition.cnn.com/politics"
        self.start()


    def run(self):
        print("working")
        while True:
            try:
                response = urlopen(self.url)
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

                link = "http://edition.cnn.com/"+ html_parser.getUrl(html_string)
                response = urlopen(link)
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                headline, text = html_parser.getText(html_string)

                file_handler.append_to_file(link)
                self.emit(SIGNAL("output(QString, QString)"),headline,text)
                self.sleep(30)
            except:
                print("cannot crawl page")

    def __del__(self):
        self.wait()







