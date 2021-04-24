import csv
from pymongo import MongoClient

#Insert a list of posts into a MongoDB database
#Returns the number of posts that were written to the database
def insertMongoPosts(postList: list, dbName: str, collectionName: str, connectionString: str = ''):
    itemCount = 0
    if connectionString != '':
        client = MongoClient(connectionString)
    else:
        client = MongoClient()
    for post in postList:
        try:
            if post['id'] != '':
                #Here we insert into the mongoDB database
                post['_id'] = post['id']
                client[dbName][collectionName].insert_one(post)
                itemCount += 1
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
