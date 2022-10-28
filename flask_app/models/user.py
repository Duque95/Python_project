# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
from flask_app import flash
from flask_app.models.dance import Dance
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE = 'dances'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users

    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user

    @classmethod
    def get_one_with_email(cls,data) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        else:
            user = User(result[0])
        return user

    # ! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 chars", 'first_name')
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        # for the edit user, no password is provided.
        if 'password' in user:
            if user['password'] != user['password_confirmation']:
                flash("passwords must match!", 'password')
                is_valid = False
            if len(user['password']) < 8:
                flash("password must be at least 8 chars", 'password')
                is_valid = False
        return is_valid


# TODO create a class method to retrive all the dances that belong to a certain user
    @classmethod
    def get_one_with_dances(cls, data):
# TODO write a join sql query to get a user and all its dances
        query = "SELECT * FROM users LEFT JOIN dances ON users.id = dances.user_id WHERE users.id = %(id)s;"
# TODO the query will be a list of dictionaries. Each dictionary will contain all the attributes of the user and one of the user's dances.
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
# TODO create an instance of the user class that will have the dances attribute. The attribute is a list of all that user's dances
        user = User(results[0])
# TODO loop over the list of dictionaries returned from the database.
        for result in results:
# TODO create a dictionary to hold and format the dance's data from each dictionary.
# TODO append `dances.`to the attributes where needed:
            temp_dance = {
            'id' : result['dances.id'],
            'name' : result['name'],
            'description' : result['description'],
            'user_id' : result['user_id'],
            'created_at' : result['dances.created_at'],
            'updated_at' : result['dances.updated_at']
            }
# TODO once the dictionary is created for each dances, append it to the dances attribute list. Inside the append method, convert the dictionary created in the previous step to an instance of the dance class.
            user.dances.append(Dance(temp_dance))
# TODO finally, return the user created above. It will contain the dances attribute created in the for loop above.
        return user