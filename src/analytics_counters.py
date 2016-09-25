#!/usr/bin/python


import MySQLdb 
import json

# Function to connect to database using credentials from database file 
def connect_db(credentials_dict = {}):

	username = credentials_dict['DB_USERNAME']
	password = credentials_dict['DB_PASSWD']
	db       = credentials_dict['DB_NAME']
	host     = credentials_dict['DB_SERVER']	

        try:
                db_con = MySQLdb.connect(host,username,password,db)
                print db_con
                return db_con
        except:
                print("Unable to connect to database")
		exit(1)

# Function to No of students enrolled 
def fetch_data(db_obj, sql_query, get_list):
	cursor = db_obj.cursor()
	result_set = cursor.execute(sql_query)
	if get_list == "no":
		return result_set
	else :
		result_set = cursor.fetchall()
		return result_set



with open("credentials.json") as cred_file:
	cred_data = json.load(cred_file)

# Connect to database 
conn_obj = connect_db(cred_data)


with open("analytics-parameter.json") as query_file:
	user_data = json.load(query_file)

analytics_dict = {}

for key, value in user_data.items():
	result_set = fetch_data(conn_obj, value['QUERY'], value['GET_LIST'])
	analytics_dict[key] = result_set

print analytics_dict
