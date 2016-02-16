"""
ModelExerciser.py: This file is specific to Yelp review data, but can
be more genaralized.  At various points along the way, objects in memory
are saved to file (pickled) with a datetime stamp.  This can take up
a lot of space but for long running processes, it's handy to
be able to load them up without going through all of the steps.
"""

import MySQLdb
from PersistModel import PersistModel
import time
import cPickle as pickle
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
from sklearn.feature_selection import SelectFromModel

execution_time_stamp = time.strftime('%Y%m%d_%H%M%S')


def get_data():
    """
    Gets data from database and does *some* feature enrichment.
    :return: Dictionary with two elements:
            "data": pandas dataframe
            "data_info": Dictionary for context
                "sql": SQL used to generate the data
                "shape": shape of the pandas dataset.
    """
    print ('{} -- getting data'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
    con = MySQLdb.connect(**login_info)
    # sql = "SELECT * FROM review_for_practice"

    # sql = " SELECT stars, review_text  " \
    #       " FROM review " \
    #       " WHERE  business_id IN " \
    #       "      ( SELECT DISTINCT bc.business_id " \
    #       "        FROM bus_categories bc INNER JOIN vw_restaurant_categories rc " \
    #       "           ON bc.category = rc.category) " \
    #       " ORDER BY rand() LIMIT 50000 "

    # sql = " SELECT stars, review_text  " \
    #       " FROM vw_restaurants_in_usa "

    sql = " SELECT stars, review_text  " \
          " FROM vw_restaurants_in_usa " \
          " ORDER BY rand() LIMIT 50000 "

    reviews = pd.read_sql_query(sql, con)
    con.close()
    reviews['review_type'] = reviews['stars'].map(lambda x: "{:g} stars".format(x) if x > 1 else "1 star ")
    #    reviews['review_type'] = reviews['stars'].map(lambda x: 'unfavorable' if x <3 else 'favorable')
    data_info = {
        "sql": sql,
        "shape": reviews.shape
    }
    print ('{} -- data loaded'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
    return {"data": reviews, "data_info": str(data_info)}


def transform_data(data, data_info):
    """
    This function accepts 'raw' data, splits it into test and training sets
    extracts features using TfidfVectorizer and then pickles the results for
    later use
    :param data: Pandas dataframe
    :param data_info: Dictionary for context information returned from GetData
    :return: Dictionary containing results:
       "transform_info": string version of the vectorizer,
        "data_info": data_info passed to function
        "data_train": training dataframe
        "data_test": test dataframe
        "y_train": y_train
        "y_test": y_test
        "categories": sorted list of all possible y values for confusion matrix
        "X_train": X_train
        "X_test": X_test

    """
    print ('{} -- transforming data'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
    X = data['review_text']
    y = data['review_type']
    data_train, data_test, y_train, y_test = cross_validation.train_test_split(X, y, train_size=.8)
    categories = sorted(y.unique().tolist())
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=0,
                                 stop_words='english', decode_error='ignore',
                                 ngram_range=(1, 3))

    transform_info = str(vectorizer)
    X_train = vectorizer.fit_transform(data_train)
    X_test = vectorizer.transform(data_test)

    print ('{} -- data transformed'.format(time.strftime('%Y-%m-%d %H:%M:%S')))

    data_file_name = "X_train_{}.pickle".format(execution_time_stamp)
    with open(data_file_name, 'wb') as handle:
        pickle.dump(X_train, handle)

    data_file_name = "X_test_{}.pickle".format(execution_time_stamp)
    with open(data_file_name, 'wb') as handle:
        pickle.dump(X_test, handle)

    data_file_name = "y_train_{}.pickle".format(execution_time_stamp)
    with open(data_file_name, 'wb') as handle:
        pickle.dump(y_train, handle)

    data_file_name = "y_test_{}.pickle".format(execution_time_stamp)
    with open(data_file_name, 'wb') as handle:
        pickle.dump(y_test, handle)

    return {
        "transform_info": transform_info,
        "data_info": data_info,
        "data_train": data_train,
        "data_test": data_test,
        "y_train": y_train,
        "y_test": y_test,
        "categories": categories,
        "X_train": X_train,
        "X_test": X_test
    }


def exercise_model(clf, run_notes, the_data):
    """
    Runs a processes the data using the classifer, saves the classifier to disk (pickle)
    and saves the results to database.
    :param clf: SKLearn classifier
    :param run_notes: String description of execution
    :param the_data: Dictionary returned from transform_data
    """

    print ('{} -- exercising model {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), run_notes))

    run_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    t0 = time.time()
    clf.fit(the_data["X_train"], the_data["y_train"])
    train_time = time.time() - t0

    print ('{} -- train time {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), train_time))

    data_file_name = "{}_{}.pickle".format(run_notes, execution_time_stamp)
    with open(data_file_name, 'wb') as handle:
        pickle.dump(clf, handle)

    t0 = time.time()
    pred = clf.predict(the_data["X_test"])
    test_time = time.time() - t0

    print ('{} -- test time {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), test_time))

    con = MySQLdb.connect(**login_info)
    model_peristor = PersistModel(con)
    model_peristor.save_model(run_time_stamp, train_time, test_time, str(clf),
                              the_data["transform_info"], the_data["data_info"],
                              run_notes, the_data["categories"], the_data["y_test"], pred)
    con.close()

    print ('{} -- completed model {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), run_notes))


def get_lots_o_models():
    """
    Returns a list of SKLearn classifiers to exercise
    :return: List of instantiated classifiers.
    """
    the_models = []
    the_models.append((RidgeClassifier(tol=1e-2, solver="lsqr"), 'Ridge_Classifier'))
    the_models.append((Perceptron(n_iter=50), "Perceptron"))
    the_models.append((PassiveAggressiveClassifier(n_iter=50), "Passive_Aggressive"))
    the_models.append((KNeighborsClassifier(n_neighbors=10), "kNN"))
    the_models.append((RandomForestClassifier(n_estimators=100), "Random_Forest_100"))
    #    the_models.append((RandomForestClassifier(n_estimators=10), "Random_Forest_10"))
    #    the_models.append((RandomForestClassifier(n_estimators=1000), "Random_Forest_1000"))

    for penalty in ["l2", "l1"]:
        the_models.append((LinearSVC(loss='squared_hinge',
                                     penalty=penalty, dual=False, tol=1e-3), "%s_penalty" % penalty.upper()))

        the_models.append((SGDClassifier(alpha=.0001, n_iter=50,
                                         penalty=penalty), "%s penalty" % penalty.upper()))

    the_models.append((SGDClassifier(alpha=.0001, n_iter=50,
                                     penalty="elasticnet"), "Elastic-Net penalty"))

    the_models.append((NearestCentroid(), "NearestCentroid_aka_Rocchio_classifier)"))
    the_models.append((MultinomialNB(alpha=.01), 'Naive_Bayes_Multi'))
    the_models.append((BernoulliNB(alpha=.01), 'Naive_Bayes_Bernoulli'))
    the_models.append((Pipeline([
        ('feature_selection', SelectFromModel(LinearSVC(penalty="l1", dual=False, tol=1e-3))),
        ('classification', LinearSVC())
    ]), 'LinearSVC_with_L1'))

    return the_models


def get_a_model():
    """
    Returns a list of one SKLearn classifiers to exercise
    Used while testing and for one-off investigations
    :return: List of instantiated classifiers.
    """
    the_models = []
    the_models.append((LinearSVC(loss='squared_hinge',
                                 penalty='l2', dual=False, tol=1e-3, class_weight='balanced'), "L2_penalty"))

    return the_models


def exercise_models():
    """
    Primary function for getting data and exercising the models
    """
    the_data = transform_data(**get_data())
    the_models = get_a_model()
    #    the_models = get_lots_o_models()
    counter = 1
    total_models = len(the_models)
    print ('{} -- Excercising {} models'.format(time.strftime('%Y-%m-%d %H:%M:%S'), total_models))

    for clf, description in the_models:
        exercise_model(clf, description, the_data)
        print ('{} -- Finished {} of {} models'.format(time.strftime('%Y-%m-%d %H:%M:%S'), counter, total_models))
        counter += 1


if __name__ == '__main__':
    exercise_models()
