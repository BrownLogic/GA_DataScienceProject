# Follows the pattern from grid_search_text_feature_extraction

from __future__ import print_function

from pprint import pprint
from time import time
import logging

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from database import login_info
import MySQLdb
import pandas as pd

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


###############################################################################
# stage the data
def get_the_data(num_of_records):
    # Returns review dataframe
    con = MySQLdb.connect(**login_info)
    con.set_character_set(
        'utf8')  # thanks to https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    sql = " SELECT stars, review_text  " \
          " FROM review " \
          " WHERE  business_id IN " \
          "      ( SELECT DISTINCT bc.business_id " \
          "        FROM bus_categories bc INNER JOIN vw_restaurant_categories rc " \
          "           ON bc.category = rc.category) " \
          " ORDER BY rand() LIMIT {0} "

    ret = pd.read_sql_query(sql.format(num_of_records), con=con)
    con.close()
    ret['review_type'] = ret['stars'].map(lambda x: 'unfavorable' if x < 3 else 'favorable')

    return ret


###############################################################################
# define a pipeline combining a text feature extractor with a simple
# classifier
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'vect__max_df': (0.5, 0.75, 1.0),
    # 'vect__max_features': (None, 5000, 10000, 50000), #I think that 50000 features is what is blowing out the memory
    'vect__max_features': (None, 5000, 10000),  # I think that 50000 features is what is blowing out the memory
    'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),  # unigrams or bigrams or trigrams
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
    'clf__n_iter': (10, 50, 80),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier

    # redirect to file

    num_of_records = 1000

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=1, verbose=3)

    print("Performing grid search on {:,} records...".format(num_of_records))
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()

    review = get_the_data(num_of_records)

    grid_search.fit(review['review_text'], review['review_type'])
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
