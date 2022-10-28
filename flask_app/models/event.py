# import the function that will return an instance of a connection
from operator import is_
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the event table from our database
from flask_app import flash
from pprint import pprint

DATABASE = 'dances'

class Event:
    def __init__( self , data ):
        self.todo = data['todo']
        self.date = data['date']
        self.user_id = data['dance_id']
    # Now we use class methods to query our database
    
    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        return results

    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print (result)
        event = Event(result[0])
        return event

    # ! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (todo, date, dance_id) VALUES (%(todo)s, %(date)s, %(dance_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)