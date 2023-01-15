Project scope:
--------------
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis. So, we need to complete the below tasks:

1- A database named "sparkify"
2- We will create 5 different data tables (4 dimentions and 1 fact table) which are the components of star schema.
3- We will create a pipeline to iterate over the data files and insert their data in the tables we created.
4- After completing the above steps, we will be able to run queries to analyze the data available after inserting them in our tables.

How to run the Python scripts:
-------------------------------
Scripts in this project will be run in the Jupyter notebooks using the % magic commands. I used a notebook named "Project-1" to explore data and run commands.

An explanation of the files in the repository:
----------------------------------------------
We have 2 types of files that we will use to extract our data,
1- Song files (Includes the main data related to songs properites like song title, duration...etc)
2- Log files (Includes the main data related to users who use the app like their names, session data...etc)
Both are in the JSON format, and we will use pandas library to read them and inset them into our created tables.

State and justify your database schema design and ETL pipeline:
---------------------------------------------------------------
The database design in our case is 'star schema' since we have 1 main table (Fact) that we will join with the remaining 4 tables to obtain all the data required for analysis.
Our ETL is designed based on defined functions that extracts the data from files in the form of lists, and then inserts these lists in the created tables using the table insert sql queries we prepared.
