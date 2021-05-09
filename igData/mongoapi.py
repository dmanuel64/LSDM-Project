'''
This file contains  some abstraction for interfacing with mongodb. 
Mostly this is used to insert a list of instagram posts into a mongodb instance,
and then take all the posts stored in a mongodb instance and dump them to a csv file.
'''

import csv
from pymongo import MongoClient
from bson.objectid import ObjectId

#Check to see if a post has already been inserted into the database. This helps make sure we're not continually redownloading and reinserting the same posts
def checkForPost(idStr: str, dbName: str, collectionName: str, connectionString: str = ''):
    if connectionString != '':
        client = MongoClient(connectionString)
    else:
        client = MongoClient()

    if client[dbName][collectionName].find_one({"_id": idStr}) == None:
        return False
    else:
        return True


#Insert a list of posts into a MongoDB database
#Returns the number of posts that were written to the database
def insertMongoPosts(postList: list, dbName: str, collectionName: str, connectionString: str = ''):
    #Initialize the count of inserted items to 0
    itemCount = 0
    #Either connect to the default db, or use the provided connection string to connect to a different one
    if connectionString != '':
        client = MongoClient(connectionString)
    else:
        client = MongoClient()

    #iterate through the list of posts that was passed
    for post in postList:
        try:
            if checkForPost(post['id'], dbName, collectionName, connectionString):
                continue
            #We want to use the instagram provided post ID as the mongodb id as well
            elif post['id'] != '':
                #Here we insert into the mongoDB database, setting the id field to the instagram provided one
                post['_id'] = post['id']
                client[dbName][collectionName].insert_one(post)
                itemCount += 1
        #If current post is not formatted correctly, then just skip it.
        except KeyError:
            continue
    return itemCount

#Get all the posts from a mongoDB collection and dump them into a CSV file
#Returns the number of posts that were written out
def mongo2CSV(file: str, dbName: str, collectionName: str, connectionString: str = ''):
    #Open the output file
    with open(file, 'w', newline='') as outputCSV:
        #create the CSV writer and open the connection to the database
        csv_writer = csv.writer(outputCSV)
        count = -1
        if connectionString != '':
            client = MongoClient(connectionString)
        else:
            client = MongoClient()

        #iterate through all posts and write each line to the CSV file
        for post in client[dbName][collectionName].find(): 
            #write the header if there have been no values written to the file yet
            if count < 0:
                header = post.keys()
                csv_writer.writerow(header)
                count += 1
            #write the data for the current post and then increment the count by 1
            csv_writer.writerow(post.values())
            count += 1
    return count
