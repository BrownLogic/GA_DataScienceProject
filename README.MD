# GA Project
This project represents the majority of the work that I did to complete the GA 
Data Science class project.  

The final project turned out to be a classification problem:  
    Predict the number of stars that a review has based on the text content 
    of the reviews.  

As I approached the problem, I didn't make any assumptions about which data that I would need to use.  As a result, I spent a lot of time writing parsers and storage for *all* of the files. 

Additionally, I discovered that processing the data takes a long time. Much of my initial analysis was spent in brute-force iterating with multiple classifiers.  At first, I kept track of the results in text files but soon discovered that it was tedious fiddling with various parameters and trying to remember the specific ones that resulted in the results I was reviewing.  Additionally, I lost several days worth of work and processing time when results exceeded the buffer.  

To solve this problem, I built some tables and code to exercise the models and save runs and context about those runs.
  
After the best 'score' was identified, the final charts and graphs were put together into Jupyter notebook and PowerPoint deck.  

# Database
There are two sets of tables in the database ProjectDB
1.  The tables to store the Yelp data
2.  The tables to store the classifier runs and scores.
 
## Yelp Data
The Yelp data is comprised of 18 tables (6 parent tables, 12 child and relationship tables).  
![Yelp Data](./SupportFiles/YelpTables.png)



## Run Tables
The Run data is comprised of 3 tables (1 parent, 2 child tables).  See comments on PersistModel.py for more details.

![Run Data](./SupportFiles/RunTables.png)



## Database creation
The DDL for creating the tables and views can be found in the ProjectDB.ddl.sql file.  The assumption is that the ProjectDB schema has already been created in a MySQL instance.

If you only want to load the Run tables, you can use ModelExerciserTables.ddl.sql.

--
# Steps for loading the data
1.  Download the challenge data from Yelp.  Note:  this set of data was was pulled down from yelp 11/2015.  Since then, Yelp has updated the data set, so your results may vary.
2.  There is a Category heirarchy file that is useful for getting to parent categories.  It can be found here: https://www.yelp.com/developers/documentation/v2/all_category_list
3.  Create MySQL instance projectdb
4.  Execute SQL in ProjectDB.ddl.sql
5.  Update user and password in file database.py
6.  Update path (and confirm file names) in LoadAll.py

The load could take a while depending on system and pipe speed.

--
At this point the data is loaded and you can interrogate as you like.

# Steps for creating runs
The primary engine for creating runs is ModelExerciser.py.  
1.  Review and/or update the SQL in get_data().
2.  Review and/or update the transformer in transform_data().
3.  Update exercise_models() to specify whether you want get_a_model() or get_lots_o_models().  Initially, I'd start with get_a_model().
4.  Update get_a_model() (or get_lots_o_models())  so that the return lists contain the classfiers you are interested in.  
5.  Run ModelExerciser.py

--
At this point, your models have been run and the results saved to database.  You can review the contents of the model_runs table to see particulars, including scores, notes, transform and classifier_info.
