"""
LoadAll.py: processes all of the Yelp JSON files and loads them into the database
Modify if you only want to include *some* of the data
"""

import LoadBusiness as LB
import LoadCheckIn as LC
import LoadReview as LR
import LoadTips as LT
import LoadUser as LU



def LoadAll():
    #path = '/home/ubuntu/projects/ga_yelp/yelp_data_raw/{}'
    path = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\{}'

    #LB.parse_file(path.format('yelp_academic_dataset_business.json'),101,5000)
    #LU.parse_file(path.format('yelp_academic_dataset_user.json'),101,5000)
    #LR.parse_file(path.format('yelp_academic_dataset_review.json'),101,5000)
    #LC.parse_file(path.format('yelp_academic_dataset_checkin.json'),101,5000)
    #LT.parse_file(path.format('yelp_academic_dataset_tip.json'),101,5000)

    LB.parse_file(path.format('yelp_academic_dataset_business.json'))
    LU.parse_file(path.format('yelp_academic_dataset_user.json'))
    LR.parse_file(path.format('yelp_academic_dataset_review.json'))
    LC.parse_file(path.format('yelp_academic_dataset_checkin.json'))
    LT.parse_file(path.format('yelp_academic_dataset_tip.json'))


if __name__ == '__main__':
    LoadAll()
