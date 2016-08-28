from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pandas as pd

class DBHandler:
    def __init__(self):
        super(DBHandler).__init__()
        self.port = 27017
        self.host = "localhost"
        self.database = "news_ticker"
        self.table = "news"

    """
    get the analysis from each text and save insert it into the database
    """
    def insertData(self,headline,theme_list, prediction_list, analysis):
        try:
            client = MongoClient(self.host, self.port)
            db = client[self.database]
            db[self.table].insert_one(
                {
                    "headline": headline,
                    "theme list": theme_list,
                    "prediction list": prediction_list,
                    "analysis": analysis
                }
            )
            client.close()


        except ConnectionFailure as err:
            print(err)

    """
    get the data from the database and return it as a pandas dataframe
    """
    def getData(self):
        try:
            client = MongoClient(self.host, self.port)
            db = client[self.database]
            cursor = db[self.table].find()
            df = pd.DataFrame(list(cursor))
            client.close()
            return df


        except ConnectionFailure as err:
            print(err)




