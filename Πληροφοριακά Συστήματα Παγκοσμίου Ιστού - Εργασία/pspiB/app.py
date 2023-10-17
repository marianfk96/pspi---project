# BEGIN CODE HERE

from flask import Flask, json, request , jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import numpy as np
from numpy.linalg import norm
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import TEXT, DESCENDING 



# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])



@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE

    #Get request
    name=request.args.get("name") #retrieving the value of the "name" 

    #The $regex operator is used to match documents that contain the provided "name" value  
    query = {"name": {"$regex":name}}
    
    #find() method with the provided query and sorts the results in descending order based on the "price" field.
    cursors = list(mongo.db.products.find(query).sort("price", DESCENDING))
    
    #the "_id" field of each document is converted to a string
    for cursor in cursors:
        cursor["_id"] = str(cursor["_id"])

    #the cursors list is converted to JSON format using jsonfy()
    return jsonify(cursors), 200
    

       
    # END CODE HERE

@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    
    #Post request
    new_product = request.json
    
    #Check if the name of the new product exists in our database
    exists = mongo.db.products.find_one({"name": new_product["name"]})
    
    #If the name exists ,update the it
    if exists is not None:
        mongo.db.products.update_one({"name": new_product["name"]}, {"$set": {"production_year": new_product["production_year"]}})
        mongo.db.peoducts.update_one({"name": new_product["name"]}, {"$set": {"price": new_product["price"]}})
        mongo.db.products.update_one({"name": new_product["name"]}, {"$set": {"color": new_product["color"]}})
        mongo.db.products.update_one({"name": new_product["name"]}, {"$set": {"size": new_product["size"]}})
        
        return new_product
    #If it doesn't exist ,add it in the database
    else:
        mongo.db.products.insert_one(new_product)
        return new_product
         
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE

    #Post request
    new_product = request.json
    products = mongo.db.products.find()
    
    #A list that will have our final result
    similar_products = []
    
    #Create a vector from the new product that the post request returned
    new_product_list = [ new_product["production_year"],new_product["price"],new_product["color"], new_product["size"]]
    new_product_vector = np.array(new_product_list,dtype=np.float64)

    for product in products:
        #Create a vector for every single product in our database
        product_list = [ product["production_year"], product["price"], product["color"], product["size"]]
        product_vector = np.array(product_list,dtype=np.float64)
        #Implement the cosine similarity function 
        cos_sim = np.dot(product_vector, new_product_vector) / ((norm(product_vector) * norm(new_product_vector)))
        print(cos_sim)
        if cos_sim >0.7:
            similar_products.append(product["name"])
    

    return jsonify(similar_products)
    # END CODE HERE




@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE

    #Insert your parth where the chromedriver is in your computer
    path="C:\Program Files (x86)\chromedriver.exe"
    #Our webdriver is Google Chrome
    driver = webdriver.Chrome(path)
    #Insert the url from where you want to extract data
    url ="https://qa.auth.gr/el/x/studyguide/600000438/current"
    driver.get(url)


   #Get request
    semester=int(request.args.get('semester'))

    #Find the table which has the elements you want to extract
    table= driver.find_element(By.ID, "exam"+ str(semester))
    #Save the data in each row in a list named rows
    rows = table.find_elements(By.CSS_SELECTOR,"tr")
    
    #
    titles = []
    first_row = rows[0]  
    for row in rows:
      #Save the titles of each lesson in this semester 
      title_element = row.find_element(By.CLASS_NAME, 'title')
      #Except the first row in the table which it isn't a title 
      if title_element != first_row.find_element(By.CLASS_NAME, 'title'):
        titles.append(title_element.text)
     
     
    driver.quit()
    return titles
    
    # END CODE HERE
    
    
    