"""
LoadAll.py: processes all of the Yelp JSON files and loads them into the database
Modify if you only want to include *some* of the data
"""

import LoadBusiness as LB
import LoadCheckIn as LC
import LoadReview as LR
import LoadTips as LT
import LoadUser as LU
import LoadCategory as LY


def load_all():
    """
    Loads all of the files from the Yelp data set
    """
    path = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\{}'

    # Used for sandboxing with smaller data sets
    # LB.parse_file(path.format('yelp_academic_dataset_business.json'),101,5000)
    # LU.parse_file(path.format('yelp_academic_dataset_user.json'),101,5000)
    # LR.parse_file(path.format('yelp_academic_dataset_review.json'),101,5000)
    # LC.parse_file(path.format('yelp_academic_dataset_checkin.json'),101,5000)
    # LT.parse_file(path.format('yelp_academic_dataset_tip.json'),101,5000)

    LB.parse_file(path.format('yelp_academic_dataset_business.json'))
    LU.parse_file(path.format('yelp_academic_dataset_user.json'))
    LR.parse_file(path.format('yelp_academic_dataset_review.json'))
    LC.parse_file(path.format('yelp_academic_dataset_checkin.json'))
    LT.parse_file(path.format('yelp_academic_dataset_tip.json'))

    # Categories wasn't a part of the original data set.
    # It contained the hierarchy that allowed me to filter only restaurants.
    LY.parse_file(path.format('categories.json'))


if __name__ == '__main__':
    load_all()
