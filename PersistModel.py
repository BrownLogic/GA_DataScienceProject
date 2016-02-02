"""
PersistModel.py:  Saves a model to the database
"""

import MySQLdb
import time
from database import login_info
from sklearn import metrics

class PersistModel:
    def __init__(self, connection):
        connection.set_character_set('utf8')
        self.db = connection
        self.cursor = self.db.cursor()

    def save_model(self, run_time_stamp, train_time, test_time, classifier_info, transform_info, data_info, run_notes, labels, y_test, y_pred ):
        accuracy_score = round(metrics.accuracy_score(y_test, y_pred),3)
        f1_score = round(metrics.f1_score(y_test, y_pred, average='macro'),3)
        confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
        category_scores = metrics.precision_recall_fscore_support(y_test, y_pred,average=None )

        run_id = self.save_model_run(run_time_stamp, round(train_time,3), round(test_time,3), accuracy_score, f1_score, classifier_info, transform_info, data_info, run_notes)
        self.save_scores(run_id, labels,category_scores)
        self.save_confusion_matrix(run_id,confusion_matrix, labels)

    def save_model_run(self, run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info, data_info, run_notes):

        sql = " INSERT INTO model_runs " \
              " (run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info, data_info, run_notes) " \
              " values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, [run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info, data_info, run_notes])
        self.db.commit()
        return self.cursor.lastrowid

    def save_scores(self, run_id, labels, scores):
        """
            precision: float (if average is not None) or array of float, shape = [n_unique_labels] :
            recall: float (if average is not None) or array of float, , shape = [n_unique_labels] :
            fbeta_score: float (if average is not None) or array of float, shape = [n_unique_labels] :
            support: int (if average is not None) or array of int, shape = [n_unique_labels] :
        """
        for i in range(len(labels)):
            self.save_score(run_id, labels[i], scores[0][i], scores[1][i],scores[2][i])

    def save_score(self, run_id, class_label, precision, recall, f1_score):
        sql = " INSERT INTO model_scores " \
              " (run_id, class_label, precision_score, recall_score, f1_score) " \
              " values (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, [run_id, class_label, round(precision,3), round(recall,3), round(f1_score,3)])
        self.db.commit()

    def save_confusion_matrix(self, run_id, confusion_matrix, labels ):
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix[i])):
                sql = " INSERT INTO model_confusion_matrix " \
                      " (run_id, row_class, col_class, the_value) " \
                      " values (%s, %s, %s, %s) "
                self.cursor.execute(sql, [run_id, labels[i], labels[j], confusion_matrix[i][j]])
        self.db.commit()

def unit_test():

    db = MySQLdb.connect(**login_info)
    #db.set_character_set('utf8') #From http://stackoverflow.com/questions/3942888/unicodeencodeerror-latin-1-codec-cant-encode-character
    model_persistor = PersistModel(db)

    save_model_run_parms = {
        "run_time_stamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "train_time": 15.1,
        "test_time": 4.2,
        "accuracy": 0.568,
        "f1_score": 0.56,
        "classifier_info": "lots of gobbldygook",
        "transform_info": "transform gobbldygook",
        "data_info": "data gobbldygood",
        "run_notes": "even more gobblgygook"
    }

    #Test Save
    run_id = model_persistor.save_model_run(**save_model_run_parms)
    score_parms = {
        "run_id": run_id,
        "class_label": "my_class",
        "precision": 0.65,
        "recall": 0.30,
        "f1_score": 0.43
    }

    model_persistor.save_score(**score_parms)

    scores_parms = {
        "run_id": run_id,
        "labels": ['one', 'two', 'three'],
        "scores": ([.11,.12,.13],[.21,.22,.23],[.31,.32,.33],[41,42,43])
    }

    model_persistor.save_scores(**scores_parms)

    confusion_matrix_parms = {
        "run_id": run_id,
        "confusion_matrix": [[11,12,13],[21,22,23],[31,32,33]],
        "labels": ['one', 'two', 'three']
    }

    model_persistor.save_confusion_matrix(**confusion_matrix_parms)
    db.close()

if __name__ == '__main__':
    unit_test()

