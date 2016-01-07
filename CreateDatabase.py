#

import sqlite3

#Create the file
dbfilename = "C:\\Users\\matt\\Documents\\Projects\\GA_DataScienceProject\\DsProject.db"
db = sqlite3.connect(dbfilename)

"""
{
  'type': 'business',
  'business_id': (encrypted business id),
  'name': (business name),
  'neighborhoods': [(hood names)],
  'full_address': (localized address),
  'city': (city),
  'state': (state),
  'latitude': latitude,
  'longitude': longitude,
  'stars': (star rating, rounded to half-stars),
  'review_count': review count,
  'categories': [(localized category names)]
  'open': True / False (corresponds to permanently closed, not business hours),

{
I need these tables

Business
Bus_Neighborhoods
Bus_Categories
Bus_Attributes
Bus_Hours

"""
