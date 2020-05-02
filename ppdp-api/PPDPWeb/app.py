from flask import Flask, render_template, request
from flask_jsonpify import jsonify
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
import ppdp_middleware
import twitter_credentials 
import twitter_client
import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import re
import csv
import nltk
from nltk.stem.porter import *
import joblib
import mongo_client
import kanonymizer
from textblob import TextBlob
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from tabulate import tabulate
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from sklearn.naive_bayes import MultinomialNB
from flask_swagger_ui import get_swaggerui_blueprint
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

class FileExportService():
    def save_as_csv(self, tweets, savename):
        with open(savename, 'w', newline='', encoding='utf-8') as csvFile:
         writer = csv.writer(csvFile, delimiter=';')
         writer.writerows(tweets)

        csvFile.close()


class TweetExporter():
    def get_tweets_by_keyword(self, api, keyword, num_items):
        return tweepy.Cursor(api.search, q=keyword,  tweet_mode='extended', lang='en').items(num_items)

    def get_tweets_by_account(self, api, handler, num_items):
        return tweepy.Cursor(api.user_timeline, id=handler, tweet_mode='extended', lang='en').items(num_items)

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PPDP Workflow"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

CORS(app)
api = Api(app)
ppdp = ppdp_middleware.PPDP()
twitter_client = twitter_client.TwitterClient()    
apiTwitter = twitter_client.get_twitter_client_api()
file_exporter = FileExportService()
tweet_exporter = TweetExporter()
mongoClient = mongo_client.MongoSevice()
kanonymizer = kanonymizer.KAnonymizer()


# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

class PPDPIntegrator(Resource):
    def get(self):
        return "API works"

    @app.route('/train/')
    def buildmodel():
        train = pd.read_csv('D:/Projects/Other/ppdp-framework/tweets.csv', encoding = "unicode_escape")
        print("file read")
        tweets_train = train["Tweet"].fillna("")

        x = []
        for tweet in tweets_train:
            x.append([nltk.tag.str2tuple(t) for t in tweet.split()])

        # Split the dataset for training and testing
        #cutoff = int(.75 * len(x))
        #training_sentences = x[:cutoff]
        #test_sentences = x[cutoff:]

        kfold = KFold(5, True, 1)

        clf = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', DecisionTreeClassifier(criterion='entropy'))
        ])
        clf2 = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', MultinomialNB())
        ])
        clf3 = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', SVC(kernel='linear'))
        ])
        clf4 = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', KNeighborsClassifier(n_neighbors=5))
        ])

        for train_index, test_index in kfold.split(x):
            print("***************** starting fold**********************")
            training_sentences = np.array(x)[train_index]
            test_sentences = np.array(x)[test_index]
            X, y = ppdp.transform_to_dataset(training_sentences)

            y = [x if x != None else "None" for x in y]

            X_test, y_test = ppdp.transform_to_dataset(test_sentences)
            y_test = [x if x != None else "None" for x in y_test] 

            #### Decision Tree Classifier Section
            #print("Decision Tree Classifier")
            #clf.fit(X[:10000], y[:10000]) 
            #filename = 'finalized_model.sav'
            #joblib.dump(clf, filename)
            #loaded_model = joblib.load(filename)
            #print(str(loaded_model.score(X_test, y_test)))
            #y_pred = loaded_model.predict(X_test)
            #print(confusion_matrix(y_test, y_pred))
            #print(classification_report(y_test, y_pred))
            #### End of Decision Tree Classifier Section


            #### Naive Bayes Classifier Section
            #print("Naive Bayes Classifier")
            #clf2.fit(X[:10000], y[:10000])
            #filenamenb = 'finalized_model_nb.sav'
            #joblib.dump(clf2, filenamenb)
            #loaded_model2 = joblib.load(filenamenb)
            #print(str(loaded_model2.score(X_test, y_test)))
            #y_pred2 = loaded_model2.predict(X_test)
            #print(confusion_matrix(y_test, y_pred2))
            #print(classification_report(y_test, y_pred2))
            #### End of Naive Bayes Classifier Section

            #### KNN Classifier Section
            #print("KNN Classifier")
            #clf4.fit(X[:10000], y[:10000])
            #filenameknn = 'finalized_model_knn.sav'
            #joblib.dump(clf4, filenameknn)
            #loaded_model4 = joblib.load(filenameknn)
            #print(str(loaded_model4.score(X_test, y_test)))
            #y_pred4 = loaded_model4.predict(X_test)
            #print(confusion_matrix(y_test, y_pred4))
            #print(classification_report(y_test, y_pred4))
            #### End of KNN Classifier Section

            #### SVM Classifier Section
            print("SVM Classifier")
            clf3.fit(X[:10000], y[:10000])
            filenamesvm = 'finalized_model_svm.sav'
            joblib.dump(clf3, filenamesvm)
            loaded_model3 = joblib.load(filenamesvm)
            print(str(loaded_model3.score(X_test, y_test)))
            y_pred3 = loaded_model3.predict(X_test)
            print(confusion_matrix(y_test, y_pred3))
            print(classification_report(y_test, y_pred3))
            #### End of SVM Classifier Section
     

        return jsonify(accuracy = str(loaded_model.score(X_test, y_test)))

    @app.route('/tag', methods=["POST"])
    def tag():
        sentence = request.get_json().get('sentence')
        print(sentence)
        filename = 'finalized_model_svm.sav'
        loaded_model = joblib.load(filename)
        tagset = ""
        sanitized_tweet = ""
        postags = ppdp.pos_tag(sentence.split(), loaded_model)
        for i in postags:
            if i[1] == "None":
                tagset = tagset + " " + str(i[0])
            else:
                tagset = tagset + " " + str(i[0])+ "/" + str(i[1])
            sanitized = ppdp.sanitize(i)
            sanitized_tweet = sanitized_tweet + ' ' + sanitized
        return jsonify(tags = tagset, sanitizations = sanitized_tweet)

    @app.route('/psuedonimizedataset')
    def psuedonimizedataset():
        train = pd.read_csv('D:/Projects/Other/ppdp-framework/experiment.csv', encoding = "unicode_escape")
        tweets= train["Tweet"].fillna("")
        print(tweets)

        filename = 'finalized_model_svm.sav'
        loaded_model = joblib.load(filename)

        collection = mongoClient.connecttodb()
        collectionOriginal = mongoClient.connecttooriginaldb()
        mongoClient.deleterecords(collection)
        mongoClient.deleterecords(collectionOriginal)

        sanitized_list = []
        rowno = 0
        count = 0
        totalwordcount = 0

        taggedList = []

        for tweet in tweets:
            age = ""
            region = ""
            gender = ""
            job = ""
            religion = ""
            language = ""
            marital = ""
            ageus = ""
            regionus = ""
            genderus = ""
            jobus = ""
            religionus = ""
            languageus = ""
            maritalus = ""
            sa = ""
            rowno = rowno + 1
            print(rowno)
            sanitized_tweet = ''
            tagset = ''
            for i in ppdp.pos_tag(tweet.split(), loaded_model):
                if i[1] == "None":
                    tagset = tagset + " " + str(i[0])
                else:
                    tagset = tagset + " " + str(i[0])+ "/" + str(i[1])
                sanitized = ppdp.sanitize(i)
                sanitized_tweet = sanitized_tweet + ' ' + sanitized
                totalwordcount = totalwordcount + 1
                if(sanitized != i[0]):
                    count = count + 1
                    if i[1] == "QIGENDER":
                        gender = sanitized
                        genderus = i[0]
                    elif i[1] == "QIAGE":
                        age = sanitized
                        ageus = i[0]
                    elif i[1] == "QIJOB":
                        job = sanitized
                        jobus = i[0]
                    elif i[1] == "QIREGION":
                        region = sanitized
                        regionus = i[0]
                    elif i[1] == "QIRELIGION":
                        religion = sanitized
                        religionus = i[0]
                    elif i[1] == "QILANG":
                        language = sanitized
                        languageus = i[0]
                    elif i[1] == "QIMARITAL":
                        marital = sanitized
                        maritalus = i[0]
                if i[1] == "SA":
                    sa = i[0]
            sanitized_list.append(sanitized_tweet)
            taggedList.append(tagset)
            mongoClient.savetodb(collection, age, region, gender, job, religion, language,marital, sa, rowno)
            mongoClient.savetodb(collectionOriginal, ageus, regionus, genderus, jobus, religionus, languageus, maritalus, sa, rowno)
        sanitizedouttweets = [[tweet] for tweet in sanitized_list]
        file_exporter.save_as_csv(sanitizedouttweets, "sanitized_tweets_experiment.csv")
        sanitizedpercentage = (count/totalwordcount) * 100
        print("************************sanitization statistics*******************************************")
        print("Total number of terms sanitized: " + str(count))
        print("Percentage of terms sanitized: " + str(round(sanitizedpercentage, 2)) + "%")
        return jsonify(tagged = taggedList, exportedtweet = tweets.to_json(orient = "records"), sanitized = sanitized_list, count = str(count), percentage = str(round(sanitizedpercentage, 2)) + "%")

    @app.route('/kanonimizedataset')
    def kanonimizedataset():
        train = pd.read_csv('D:/Projects/Other/ppdp-framework/experiment.csv', encoding = "unicode_escape")
        tweets= train["Tweet"].fillna("")
        print(tweets)

        collection = mongoClient.connecttodb()
        collectionOriginal = mongoClient.connecttooriginaldb()
        mongoClient.deleterecords(collection)
        mongoClient.deleterecords(collectionOriginal)

        sanitized_list = []
        rowno = 0
        count = 0
        totalwordcount = 0
        filename = 'finalized_model_svm.sav'
        loaded_model = joblib.load(filename)
        for tweet in tweets:
                ageus = ""
                regionus = ""
                genderus = ""
                jobus = ""
                religionus = ""
                languageus = ""
                maritalus = ""
                sa = ""
                rowno = rowno + 1
                print(rowno)
                for i in ppdp.pos_tag(tweet.split(), loaded_model):
                    sanitized = ppdp.sanitize(i)
                    if(sanitized != i[0]):
                        if i[1] == "QIGENDER":
                            genderus = i[0]
                        elif i[1] == "QIAGE":
                            ageus = i[0]
                        elif i[1] == "QIJOB":
                            jobus = i[0]
                        elif i[1] == "QIREGION":
                            regionus = i[0]
                        elif i[1] == "QIRELIGION":
                            religionus = i[0]
                        elif i[1] == "QILANG":
                            languageus = i[0]
                        elif i[1] == "QIMARITAL":
                            maritalus = i[0]
                    if i[1] == "SA":
                        sa = i[0]
                mongoClient.savetodb(collectionOriginal, ageus, regionus, genderus, jobus, religionus, languageus, maritalus, sa, rowno)
        kanonymized = kanonymizer.execute_anonymization()
        rowno = 0
        for tweet in tweets:
            age = ""
            region = ""
            gender = ""
            job = ""
            religion = ""
            language = ""
            marital = ""
            sanitized_tweet = ''
            tags = list(ppdp.pos_tag(tweet.split(), loaded_model))
            rowno = rowno + 1
            for val in kanonymized.iterrows():
                rownos = val[1]['rows'].split(',')
                if str(rowno) in rownos:
                    for i in tags:
                        tag = i[1]
                        word = i[0]
                        if tag == "DI":
                            word = "*****"
                            count = count + 1
                        elif tag == "QIGENDER":
                            word = val[1]['gender']
                            gender = word
                            count = count + 1
                        elif tag == "QIAGE":
                            word = str(val[1]['age'])
                            age = word
                            count = count + 1
                        elif tag == "QIJOB":
                            word = val[1]['job']
                            job = word
                            count = count + 1
                        elif tag == "QIREGION":
                            word = val[1]['region']
                            region = word
                            count = count + 1
                        elif tag == "QIRELIGION":
                            word = val[1]['religion']
                            religion = word
                            count = count + 1
                        elif tag == "QILANG":
                            word = val[1]['language']
                            language = word
                            count = count + 1
                        elif tag == "QIMARITAL":
                            word = val[1]['marital']
                            marital = word
                            count = count + 1
                        elif tag == "SA":
                            sa = val[1]['sa']
                        sanitized_tweet = sanitized_tweet + ' ' + word
                        totalwordcount = totalwordcount + 1
                    sanitized_list.append(sanitized_tweet)
                    mongoClient.savetodb(collection, age, region, gender, job, religion, language, marital, sa, rowno)
                    break
        sanitizedpercentage = (count/totalwordcount) * 100
        print("************************sanitization statistics*******************************************")
        print("Total number of terms sanitized: " + str(count))
        print("Percentage of terms sanitized: " + str(round(sanitizedpercentage, 2)) + "%")
        print("******************************************************************************************")

        sanitizedouttweets = [[tweet] for tweet in sanitized_list]
        file_exporter.save_as_csv(sanitizedouttweets, "sanitized_tweets_experiment.csv")
        return jsonify(exportedtweet = kanonymized.to_json(orient = "records"), sanitized = sanitized_list, count = str(count), percentage = str(round(sanitizedpercentage, 2)) + "%")

    @app.route('/export', methods=["POST"])
    def export():
        print("starting export..............................")
        keyword = request.get_json().get('keyword')
        #keyword = request.form["keyword"]
        print(keyword)
        tweets = tweet_exporter.get_tweets_by_keyword(apiTwitter, keyword,20)
        outtweets = [[tweet.full_text] for tweet in tweets]
        file_exporter.save_as_csv(outtweets, "exported_tweets.csv")

        collection = mongoClient.connecttodb()
        collectionOriginal = mongoClient.connecttooriginaldb()
        mongoClient.deleterecords(collection)
        mongoClient.deleterecords(collectionOriginal)

        sanitized_list = []
        rowno = 0
        count = 0
        totalwordcount = 0
        filename = 'finalized_model_svm.sav'
        loaded_model = joblib.load(filename)
        taggedList = []

        for tweet in outtweets:
            age = ""
            region = ""
            gender = ""
            job = ""
            religion = ""
            language = ""
            marital = ""
            ageus = ""
            regionus = ""
            genderus = ""
            jobus = ""
            religionus = ""
            languageus = ""
            maritalus = ""
            sa = ""
            rowno = rowno + 1
            sanitized_tweet = ''
            print(tweet)
            sanitized_tweet = ''
            tagset = ''
            for i in ppdp.pos_tag(tweet[0].split(), loaded_model):
                if i[1] == "None":
                    tagset = tagset + " " + str(i[0])
                else:
                    tagset = tagset + " " + str(i[0])+ "/" + str(i[1])
                sanitized = ppdp.sanitize(i)
                sanitized_tweet = sanitized_tweet + ' ' + sanitized
                totalwordcount = totalwordcount + 1
                if(sanitized != i[0]):
                    count = count + 1
                    if i[1] == "QIGENDER":
                        gender = sanitized
                        genderus = i[0]
                    elif i[1] == "QIAGE":
                        age = sanitized
                        ageus = i[0]
                    elif i[1] == "QIJOB":
                        job = sanitized
                        jobus = i[0]
                    elif i[1] == "QIREGION":
                        region = sanitized
                        regionus = i[0]
                    elif i[1] == "QIRELIGION":
                        religion = sanitized
                        religionus = i[0]
                    elif i[1] == "QILANG":
                        language = sanitized
                        languageus = i[0]
                    elif i[1] == "QIMARITAL":
                        marital = sanitized
                        maritalus = i[0]
                if i[1] == "SA":
                    sa = i[0]
            taggedList.append(tagset)
            sanitized_list.append(sanitized_tweet)
            mongoClient.savetodb(collection, age, region, gender, job, religion, language, marital, sa, rowno)
            mongoClient.savetodb(collectionOriginal, ageus, regionus, genderus, jobus, religionus, languageus, maritalus, sa, rowno)
        sanitizedouttweets = [[tweet] for tweet in sanitized_list]
        file_exporter.save_as_csv(sanitizedouttweets, "sanitized_tweets.csv")
        sanitizedpercentage = (count/totalwordcount) * 100
        print("************************sanitization statistics*******************************************")
        print("Total number of terms sanitized: " + str(count))
        print("Percentage of terms sanitized: " + str(round(sanitizedpercentage, 2)) + "%")
        return jsonify(exportedtweet = outtweets, tagged = taggedList, sanitized = sanitized_list, count = str(count), percentage = str(round(sanitizedpercentage, 2)) + "%")

    @app.route('/evaluate')
    def evaluate():
        collection = mongoClient.connecttodb()
        collectionOriginal = mongoClient.connecttooriginaldb()
        counts = mongoClient.countrows(collection, "gender")
        genderarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                genderarray.append(grouparray)

        counts = mongoClient.countrows(collection, "age")
        agerarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                agerarray.append(grouparray)

        counts = mongoClient.countrows(collection, "job")
        jobarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                jobarray.append(grouparray)

        counts = mongoClient.countrows(collection, "region")
        regionarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                regionarray.append(grouparray)

        counts = mongoClient.countrows(collection, "religion")
        religionarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                religionarray.append(grouparray)

        counts = mongoClient.countrows(collection, "language")
        languagearray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                languagearray.append(grouparray)

        counts = mongoClient.countrows(collection, "marital")
        maritalarray = []
        for group in counts:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"] * group["count"]]
                maritalarray.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "gender")
        genderarrayLoss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                genderarrayLoss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "age")
        agearrayLoss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                agearrayLoss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "job")
        jobarrayloss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                jobarrayloss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "region")
        regionarrayloss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                regionarrayloss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "religion")
        religionarrayloss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                religionarrayloss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "language")
        languagearrayloss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                languagearrayloss.append(grouparray)

        countsOriginal = mongoClient.countrows(collectionOriginal, "marital")
        maritalarrayloss = []
        for group in countsOriginal:
            if group["_id"] != "":
                grouparray = [group["_id"], group["count"]/len(countsOriginal)]
                maritalarrayloss.append(grouparray)

        return jsonify(gender = genderarray, age = agerarray, job = jobarray, region = regionarray, religion = religionarray, language = languagearray, marital = maritalarray, genderLoss = genderarrayLoss, ageLoss = agearrayLoss, jobloss = jobarrayloss, regionloss = regionarrayloss, religionLoss = religionarrayloss, languageloss = languagearrayloss, maritalloss = maritalarrayloss)

    @app.route('/exportkanonymize', methods=["POST"])
    def exportandkanonymize():
        keyword = request.get_json().get('keyword')
        tweets = tweet_exporter.get_tweets_by_keyword(apiTwitter, keyword,20)
        outtweets = [[tweet.full_text] for tweet in tweets]
        file_exporter.save_as_csv(outtweets, "exported_tweets_kanonymize.csv")

        collection = mongoClient.connecttodb()
        collectionOriginal = mongoClient.connecttooriginaldb()
        mongoClient.deleterecords(collection)
        mongoClient.deleterecords(collectionOriginal)

        sanitized_list = []
        rowno = 0
        count = 0
        totalwordcount = 0
        filename = 'finalized_model_svm.sav'
        loaded_model = joblib.load(filename)
        for tweet in outtweets:
                ageus = ""
                regionus = ""
                genderus = ""
                jobus = ""
                religionus = ""
                languageus = ""
                maritalus = ""
                sa = ""
                rowno = rowno + 1
                for i in ppdp.pos_tag(tweet[0].split(), loaded_model):
                    sanitized = ppdp.sanitize(i)
                    if(sanitized != i[0]):
                        if i[1] == "QIGENDER":
                            genderus = i[0]
                        elif i[1] == "QIAGE":
                            ageus = i[0]
                        elif i[1] == "QIJOB":
                            jobus = i[0]
                        elif i[1] == "QIREGION":
                            regionus = i[0]
                        elif i[1] == "QIRELIGION":
                            religionus = i[0]
                        elif i[1] == "QILANG":
                            languageus = i[0]
                        elif i[1] == "QIMARITAL":
                            maritalus = i[0]
                    if i[1] == "SA":
                        sa = i[0]
                mongoClient.savetodb(collectionOriginal, ageus, regionus, genderus, jobus, religionus, languageus, maritalus, sa, rowno)
        kanonymized = kanonymizer.execute_anonymization()
        rowno = 0
        for tweet in outtweets:
            age = ""
            region = ""
            gender = ""
            job = ""
            religion = ""
            language = ""
            marital = ""
            sanitized_tweet = ''
            tags = list(ppdp.pos_tag(tweet[0].split(), loaded_model))
            print(tags)
            rowno = rowno + 1
            for val in kanonymized.iterrows():
                rownos = val[1]['rows'].split(',')
                if str(rowno) in rownos:
                    for i in tags:
                        tag = i[1]
                        word = i[0]
                        if tag == "DI":
                            word = "*****"
                            count = count + 1
                        elif tag == "QIGENDER":
                            word = val[1]['gender']
                            gender = word
                            count = count + 1
                        elif tag == "QIAGE":
                            word = str(val[1]['age'])
                            age = word
                            count = count + 1
                        elif tag == "QIJOB":
                            word = val[1]['job']
                            job = word
                            count = count + 1
                        elif tag == "QIREGION":
                            word = val[1]['region']
                            region = word
                            count = count + 1
                        elif tag == "QIRELIGION":
                            word = val[1]['religion']
                            religion = word
                            count = count + 1
                        elif tag == "QILANG":
                            word = val[1]['language']
                            language = word
                            count = count + 1
                        elif tag == "QIMARITAL":
                            word = val[1]['marital']
                            marital = word
                            count = count + 1
                        elif tag == "SA":
                            sa = val[1]['sa']
                        sanitized_tweet = sanitized_tweet + ' ' + word
                        totalwordcount = totalwordcount + 1
                    sanitized_list.append(sanitized_tweet)
                    mongoClient.savetodb(collection, age, region, gender, job, religion, language, marital, sa, rowno)
                    break
        sanitizedpercentage = (count/totalwordcount) * 100
        print("************************sanitization statistics*******************************************")
        print("Total number of terms sanitized: " + str(count))
        print("Percentage of terms sanitized: " + str(round(sanitizedpercentage, 2)) + "%")
        print("******************************************************************************************")

        sanitizedouttweets = [[tweet] for tweet in sanitized_list]
        file_exporter.save_as_csv(sanitizedouttweets, "sanitized_tweets_kanonymize.csv")
        return jsonify(exportedtweet = kanonymized.to_json(orient = "records"), sanitized = sanitized_list, count = str(count), percentage = str(round(sanitizedpercentage, 2)) + "%")

    @app.route('/utilityExperiment/')
    def utilityExperiment():
        train = pd.read_csv('D:/Projects/Other/ppdp-framework/classification_train.csv')
        print(train)
        test = pd.read_csv('D:/Projects/Other/ppdp-framework/classification_test.csv')
        print(test)
        combi = train.append(test, ignore_index=True)

        #combi['tidy_tweet'] = np.vectorize(ppdp.remove_pattern(combi['tweet'], "@[\w]*"))
        combi['tidy_tweet'] = combi['tweet']
        combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
        combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
        print(combi)
        tokenized_tweet = combi['tidy_tweet'].apply(lambda x: x.split())

        stemmer = PorterStemmer()

        tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])
        for i in range(len(tokenized_tweet)):
            tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

        combi['tidy_tweet'] = tokenized_tweet

        all_words = ' '.join([text for text in combi['tidy_tweet']])
        normal_words =' '.join([text for text in combi['tidy_tweet'][combi['label'] == 0]])
        negative_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 1]])

        HT_regular = ppdp.hashtag_extract(combi['tidy_tweet'][combi['label'] == 0])
        HT_negative = ppdp.hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])
        HT_regular = sum(HT_regular,[])
        HT_negative = sum(HT_negative,[])
        
        bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        bow = bow_vectorizer.fit_transform(combi['tidy_tweet'])
        tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(combi['tidy_tweet'])

        train_bow = bow[:31962,:]
        test_bow = bow[31962:,:]

        # splitting data into training and validation set
        xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, train['label'], random_state=42, test_size=0.3)

        print("********************** model training")
        lreg = LogisticRegression()
        lreg.fit(xtrain_bow, ytrain) # training the model

        prediction = lreg.predict_proba(xvalid_bow) # predicting on the validation set
        prediction_int = prediction[:,1] >= 0.3 # if prediction is greater than or equal to 0.3 than 1 else 0
        prediction_int = prediction_int.astype(np.int)

        f1 = f1_score(yvalid, prediction_int)# calculating f1 score
        print(str(f1))
        return jsonify(accuracy = str(f1))

    @app.route('/utilityExperimentAnonymize/')
    def utilityExperimentAnonymize():
        train = pd.read_csv('D:/Projects/Other/ppdp-framework/classification_train_anonymized.csv', encoding='latin1')
        print(train)
        test = pd.read_csv('D:/Projects/Other/ppdp-framework/classification_test_anonymized.csv', encoding='latin1')
        print(test)
        combi = train.append(test, ignore_index=True)

        #combi['tidy_tweet'] = np.vectorize(ppdp.remove_pattern(combi['tweet'], "@[\w]*"))
        combi['tidy_tweet'] = combi['tweet']
        combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
        combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in str(x).split() if len(w)>3]))
        print(combi)
        tokenized_tweet = combi['tidy_tweet'].apply(lambda x: str(x).split())

        stemmer = PorterStemmer()

        tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])
        for i in range(len(tokenized_tweet)):
            tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

        combi['tidy_tweet'] = tokenized_tweet

        all_words = ' '.join([text for text in combi['tidy_tweet']])
        normal_words =' '.join([text for text in combi['tidy_tweet'][combi['label'] == 0]])
        negative_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 1]])

        HT_regular = ppdp.hashtag_extract(combi['tidy_tweet'][combi['label'] == 0])
        HT_negative = ppdp.hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])
        HT_regular = sum(HT_regular,[])
        HT_negative = sum(HT_negative,[])
        
        bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        bow = bow_vectorizer.fit_transform(combi['tidy_tweet'])
        tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(combi['tidy_tweet'])

        train_bow = bow[:31962,:]
        test_bow = bow[31962:,:]

        # splitting data into training and validation set
        xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, train['label'], random_state=42, test_size=0.3)

        print("********************** model training")
        lreg = LogisticRegression()
        lreg.fit(xtrain_bow, ytrain) # training the model

        prediction = lreg.predict_proba(xvalid_bow) # predicting on the validation set
        prediction_int = prediction[:,1] >= 0.3 # if prediction is greater than or equal to 0.3 than 1 else 0
        prediction_int = prediction_int.astype(np.int)

        f1 = f1_score(yvalid, prediction_int)# calculating f1 score
        print(str(f1))
        return jsonify(accuracy = str(f1))

api.add_resource(PPDPIntegrator, '/')
if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449, debug=True)