# import the function that will return an instance of a connection
from operator import is_
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the dance table from our database
from flask_app import flash
from pprint import pprint

DATABASE = 'dances'

class Dance:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']

        self.images = data['images']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dances;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of dances
        dances = []
        # Iterate over the db results and create instances of dances with cls.
        for dance in results:
            dances.append( cls(dance) )
        return dances

    @classmethod
    def get_all_with_user(cls):
        query = "SELECT * FROM dances JOIN users ON dances.user_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        # Create an empty list to append our instances of dances
        dances = []
        # Iterate over the db results and create instances of dances with cls.
        for dance in results:
            dances.append( cls(dance) )
        return dances

    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM dances WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print (result)
        dance = Dance(result[0])
        return dance

    # ! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO dances (name, description, user_id) VALUES (%(name)s, %(description)s, %(user_id)s); %(images)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE dances SET name = %(name)s, description = %(description)s, images = %(images)s WHERE id = %(id)s ;"
        return connectToMySQL(DATABASE).query_db(query, data)


    # ! DELETE
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM dances WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_dance(dance:dict) -> bool:
        is_valid = True
        if len(dance['name']) < 3:
            flash('name is too short!!')
            is_valid = False
        return is_valid