from PersistModel import PersistModel
import MySQLdb
import time
from database import login_info
import pandas as pd
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2, SelectFromModel

def get_data():
    con = MySQLdb.connect(**login_info)
    sql = "SELECT * FROM review_for_practice"


    reviews = pd.read_sql_query (sql, con)
    con.close()
    reviews['review_type'] = reviews['stars'].map(lambda x: "{:g} stars".format(x) if x>1 else "1 star ")
    data_info = {
        "sql":sql,
        "shape":reviews.shape
    }
    return {"data":reviews, "data_info":str(data_info)}

def transform_data(data, data_info):
    X = data['review_text']
    y = data['review_type']
    data_train, data_test, y_train, y_test = cross_validation.train_test_split(X, y, train_size = .8)
    categories = sorted(y.unique().tolist())
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english', decode_error='ignore',
                                 ngram_range=(1,3))

    transform_info = str(vectorizer)
    X_train = vectorizer.fit_transform(data_train)
    X_test = vectorizer.transform(data_test)

    return {
        "transform_info":transform_info,
        "data_info":data_info,
        "data_train":data_train,
        "data_test":data_test,
        "y_train": y_train,
        "y_test": y_test,
        "categories": categories,
        "X_train": X_train,
        "X_test": X_test
    }

def exercise_model(clf, run_notes, the_data):
    run_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    t0 = time.time()
    clf.fit(the_data["X_train"], the_data["y_train"])
    train_time = time.time() - t0

    t0 = time.time()
    pred = clf.predict(the_data["X_test"])
    test_time = time.time() - t0

    con = MySQLdb.connect(**login_info)
    model_peristor = PersistModel(con)
    model_peristor.save_model(run_time_stamp,train_time,test_time, str(clf),
                              the_data["transform_info"],the_data["data_info"],
                              run_notes,the_data["categories"],the_data["y_test"], pred)
    con.close()


def exercise_models():
    the_data = transform_data(**get_data())
    the_models = []
    the_models.append((RidgeClassifier(tol=1e-2, solver="lsqr"), 'Ridge Classifier'))
    the_models.append((Perceptron(n_iter=50), "Perceptron"))
    the_models.append((PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"))
    the_models.append((KNeighborsClassifier(n_neighbors=10), "kNN"))
    the_models.append((RandomForestClassifier(n_estimators=100), "Random forest"))

    for penalty in ["l2", "l1"]:
        the_models.append((LinearSVC(loss='l2',
                                    penalty=penalty,dual=False, tol=1e-3),"%s penalty" % penalty.upper()))

        the_models.append((SGDClassifier(alpha=.0001, n_iter=50,
                                           penalty=penalty),"%s penalty" % penalty.upper()))

    the_models.append((SGDClassifier(alpha=.0001, n_iter=50,
                                       penalty="elasticnet"),"Elastic-Net penalty"))

    the_models.append((NearestCentroid(), "NearestCentroid (aka Rocchio classifier)"))
    the_models.append((MultinomialNB(alpha=.01), 'Naive Bayes Multi'))
    the_models.append((BernoulliNB(alpha=.01), 'Naive Bayes Bernoulli'))
    the_models.append((Pipeline([
            ('feature_selection', SelectFromModel(LinearSVC(penalty="l1", dual=False, tol=1e-3))),
            ('classification', LinearSVC())
            ]), 'LinearSVC with L1'))

    for clf, description in the_models:
        exercise_model(clf, description, the_data)

if __name__ == '__main__':
    exercise_models()