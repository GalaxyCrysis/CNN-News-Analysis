from PyQt4 import QtCore,QtGui,uic
from PyQt4.QtCore import SIGNAL
from worker import Worker
import file_handler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.datasets import fetch_20newsgroups
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from DBHandler import DBHandler


class NewsTicker(QtGui.QMainWindow):
    def __init__(self):
        super(NewsTicker,self).__init__()
        uic.loadUi("gui.ui")
        #init dataset and vecotirzer and train with naive bayes
        self.twenty_news = fetch_20newsgroups(subset="train",remove=('headers', 'footers', 'quotes'))
        self.vectorizer =  TfidfVectorizer(max_df=0.95,min_df=2, stop_words="english")
        self.twenty_train_data = self.vectorizer.fit_transform(self.twenty_news.data)
        self.naive_bayes = MultinomialNB(alpha=0.2)
        self.naive_bayes.fit(self.twenty_train_data,self.twenty_news.target)


        #see if there are links in the file
        list = file_handler.getFileData()
        for link in list:
            if link!= "":
                self.updateUi()

        thread = Worker()
        self.connect(thread, SIGNAL("output(Qstring, QString)"), self.analyzeText)
        thread.start()
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()
        self.show()

    """
    analyze the text: create tfidf vectorizer and transform the text
    then init the NFM and get the themes from the text
    predict the data with the already trained naive bayes classifier
    finally insert the data into the database
    """
    def analyzeText(self, headline, text):

        tfidf = self.vectorizer.transform(text)
        feature_names = self.vectorizer.get_feature_names()

        nfm = NMF(n_components=5,random_state=101).fit(tfidf)
        theme_list = list()
        prediction_list = list()
        top_words = 15
        for topic_idx, topic in enumerate(nfm.components_):
            string = ""
            string += "Theme " + str(topic_idx + 1) + ": "
            for i in topic.argsort()[:-top_words:-1]:
                string += feature_names[i] + " "

            theme_list.append(string)

        #create array for prediction for each theme
        new_list = ""
        for theme in theme_list:
            new_list += theme + ","

        theme_tfidf = self.vectorizer.transform(new_list.split(","))

        #predict the new tfidf with naivebayes
        prediction = self.naive_bayes.predict(theme_tfidf)
        for i in range(0,len(prediction)):
            string = "Theme "+i + ": " + self.twenty_news.target_names[prediction[i]]
            prediction_list.append(string)

        predicted_score = np.mean(prediction == self.twenty_news.target)
        f1score = metrics.f1_score(self.twenty_news.target,prediction,average="weighted")

        #save data into the database
        db_handler = DBHandler()
        db_handler.insertData(headline,theme_list,prediction_list,predicted_score,f1score)
        #update ui
        self.updateUi()

    """
    get the data from the database and update the ui
    """
    def updateUi(self):
        # delete all widgets from layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget)
            widget.setParent(None)

        handler = DBHandler()
        dataframe = handler.getData()

        for row in reversed(dataframe):
            label = QtGui.QLabel(row["headline"])
            themes = QtGui.QLabel("Themes:")
            theme_browser = QtGui.QTextBrowser()
            for theme in row["theme list"]:
                theme_browser.append(theme_browser.toPlainText() + theme + "\n")
            predictions = QtGui.QLabel("Predictions:")
            prediction_browser = QtGui.QTextBrowser()
            for prediction in row["prediction list"]:
                prediction_browser.append(prediction_browser.toPlainText() + prediction + "\n")

            score = QtGui.QLabel("Score: " + row["analysis"])
            
            f1 = QtGui.QLabel("F1-Score: "+ row["f1"])
            #set new layout
            self.layout.addWidget(label)
            self.layout.addWidget(themes)
            self.layout.addWidget(theme_browser)
            self.layout.addWidget(predictions)
            self.layout.addWidget(prediction_browser)
            self.layout.addWidget(score)
            self.layout.addWidget(f1)
            self.widget.setLayout(self.layout)
            self.scrollArea.setWidget(self.widget)











