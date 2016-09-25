#!/usr/bin/python


import MySQLdb 
import json
import redis

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


def fetch_from_redis(redis_hostname, port, db,counter_name):
	try:
		POOL = redis.ConnectionPool(host = redis_hostname, port = 6379, db = 0)
    		my_server = redis.Redis(connection_pool=POOL)
    		response = my_server.get(counter_name)
    		return response
	except:
		print "Unable to connect redis server"
		



def create_analytics_html(file_name = "analytics.html", analytics_dict = {}):
	no_of_students = analytics_dict["NUMBER OF STUDENTS ENROLLED"]
	div_str = """    
         <!--This section is for analytics to be shown on home page"
         <section id="recent-works">
        <div class="container">
            <div class="center wow fadeInDown">
                <h2>Current Usage Analytics</h2>
            </div>

            <div class="row">
                <div class="col-xs-12 col-sm-4 col-md-3">
                    <div class="recent-work-wrap">
                        <img class="img-responsive" src="${static.url("images/portfolio/recent/item1.png")}" alt="">
                        <div class="overlay">
                            <div class="recent-work-inner">
                                <h1>""" + no_of_students + """analytics_dict </h1>
                            </div> 
                        </div>
                    </div>
                </div>   

                <div class="col-xs-12 col-sm-4 col-md-3">
                    <div class="recent-work-wrap">
                        <img class="img-responsive" src="${static.url("images/portfolio/recent/item2.png")}" alt="">
                        <div class="overlay">
                            <div class="recent-work-inner">
                                <h3><a href="#">Business theme</a></h3>
                                <p>There are many variations of passages of Lorem Ipsum available, but the majority</p>
                                <a class="preview" href="${static.url("images/portfolio/full/item2.png")}" rel="prettyPhoto"><i class="fa fa-eye"></i> View</a>
                            </div> 
                        </div>
                    </div>
                </div> 

                <div class="col-xs-12 col-sm-4 col-md-3">
                    <div class="recent-work-wrap">
                        <img class="img-responsive" src="${static.url("images/portfolio/recent/item3.png")}" alt="">
                        <div class="overlay">
                            <div class="recent-work-inner">
                                <h3><a href="#">Business theme </a></h3>
                                <p>There are many variations of passages of Lorem Ipsum available, but the majority</p>
                                <a class="preview" href="${static.url("images/portfolio/full/item3.png")}" rel="prettyPhoto"><i class="fa fa-eye"></i> View</a>
                            </div> 
                        </div>
                    </div>
                </div>



            </div><!--/.row-->
        </div><!--/.container-->
    </section><!--/#recent-works-->"""



with open("credentials.json") as cred_file:
	cred_data = json.load(cred_file)

# Connect to database 
conn_obj = connect_db(cred_data)


#Read parameters and queries from analytics-paramater.json file 
with open("analytics-parameter.json") as query_file:
	user_data = json.load(query_file)

#Declare a dictionary to keep all the counters in
analytics_dict = {}
for key, value in user_data.items():
	result_set = fetch_data(conn_obj, value['QUERY'], value['GET_LIST'])
	analytics_dict[key] = result_set

print analytics_dict


