"""
Runs all of the files
"""
import ClearData as Cld
import LoadBusiness as LB
import LoadCheckIn as LC
import LoadReview as LR
import LoadTips as LT
import LoadUser as LU

def LoadAll():
    #Cld.clear_database()
    #LB.parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_business.json')
    #LC.parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_checkin.json')
    LR.parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_review.json')
    LT.parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_tip.json')
    #LU.parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_user.json')

if __name__ == '__main__':
    LoadAll()

