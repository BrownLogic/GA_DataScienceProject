"""
PersistModel.py:  Saves models and results to a database.
Assumes tables already setup in database.
"""

import MySQLdb
import time
from database import login_info
from sklearn import metrics


class PersistModel:
    """
    This class accepts the results of a classification and saves scores
    and context to a database.
    """
    def __init__(self, connection):
        """
        Initializes class
        :param connection: Open MySQLdb connection
        :return:
        """
        connection.set_character_set('utf8')
        self.db = connection
        self.cursor = self.db.cursor()

    def save_model(self, run_time_stamp, train_time, test_time, classifier_info, transform_info, data_info, run_notes,
                   labels, y_test, y_pred):
        """
        Accepts context information, actual and predicted values, executes scoring
        and saves info (including confusion matrix) to database.
        :param run_time_stamp: String timestamp associated with execution
        :param train_time: Time representation of duration for training
        :param test_time: Time representation of duration for test
        :param classifier_info: String representation of Classifer
        :param transform_info: String representation of Transformer
        :param data_info: Dictionary for context
                "sql": SQL used to generate the data
                "shape": shape of the pandas dataset.
        :param run_notes: String description of execution
        :param labels: sorted list of all possible y values for confusion matrix
        :param y_test: Actual y values - to use in scoring
        :param y_pred: Predicted y values - to use in scoring
        """
        accuracy_score = round(metrics.accuracy_score(y_test, y_pred), 3)
        f1_score = round(metrics.f1_score(y_test, y_pred, average='macro'), 3)  # Multiclass
        #        f1_score = round(metrics.f1_score(y_test, y_pred, average='binary', pos_label='favorable'),3) #binary
        confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
        category_scores = metrics.precision_recall_fscore_support(y_test, y_pred, average=None)

        run_id = self.save_model_run(run_time_stamp, round(train_time, 3), round(test_time, 3), accuracy_score,
                                     f1_score, classifier_info, transform_info, data_info, run_notes)
        self.save_scores(run_id, labels, category_scores)
        self.save_confusion_matrix(run_id, confusion_matrix, labels)

    def save_model_run(self, run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info,
                       data_info, run_notes):
        """
        Saves context information to header table.
        :param run_time_stamp: String timestamp associated with execution
        :param train_time: Time representation of duration for training
        :param test_time: Time representation of duration for test
        :param accuracy: accuracy score
        :param f1_score: f1 score
        :param classifier_info: String representation of Classifer
        :param transform_info: String representation of Transformer
        :param data_info: Dictionary for context
                "sql": SQL used to generate the data
                "shape": shape of the pandas dataset.
        :param run_notes: String description of execution
        :return Rowid (primary key) from model_runs
        """
        sql = " INSERT INTO model_runs " \
              " (run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info, data_info, run_notes) " \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql,
                            [run_time_stamp, train_time, test_time, accuracy, f1_score, classifier_info, transform_info,
                             data_info, run_notes])
        self.db.commit()
        return self.cursor.lastrowid

    def save_scores(self, run_id, labels, scores):
        """
        Saves the individual scores for each label to database
        :param run_id: the model run ID (parent key) for this run
        :param labels: sorted list of all possible y values for confusion matrix
        :param scores: List of scores for each of the labels
        """
        for i in range(len(labels)):
            self.save_score(run_id, labels[i], scores[0][i], scores[1][i], scores[2][i])

    def save_score(self, run_id, class_label, precision, recall, f1_score):
        """
        Saves each individual score to database
        :param run_id: the model run ID (parent key) for this run
        :param class_label: each label
        :param precision: precision score
        :param recall: recall score
        :param f1_score: f1 score
        """
        sql = " INSERT INTO model_scores " \
              " (run_id, class_label, precision_score, recall_score, f1_score) " \
              " VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, [run_id, class_label, round(precision, 3), round(recall, 3), round(f1_score, 3)])
        self.db.commit()

    def save_confusion_matrix(self, run_id, confusion_matrix, labels):
        """
        This function accepts a confusion matrix and saves it to database
        as a set of row, column, values to the database
        :param run_id: the model run ID (parent key) for this run
        :param confusion_matrix: Confusion Matrix
        :param labels: sorted list of all possible y values for confusion matrix
        """
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix[i])):
                sql = " INSERT INTO model_confusion_matrix " \
                      " (run_id, row_class, col_class, the_value) " \
                      " VALUES (%s, %s, %s, %s) "
                self.cursor.execute(sql, [run_id, labels[i], labels[j], confusion_matrix[i][j]])
        self.db.commit()


def unit_test():
    """
    Stub function for exercising class
    """
    db = MySQLdb.connect(**login_info)
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

    # Test Save
    """
    Stub function for exercising class
    """
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
        "scores": ([.11, .12, .13], [.21, .22, .23], [.31, .32, .33], [41, 42, 43])
    }

    model_persistor.save_scores(**scores_parms)

    confusion_matrix_parms = {
        "run_id": run_id,
        "confusion_matrix": [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
        "labels": ['one', 'two', 'three']
    }

    model_persistor.save_confusion_matrix(**confusion_matrix_parms)
    db.close()


if __name__ == '__main__':
    unit_test()
