from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app.models.user import User
from flask import flash

class Sighting:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of_sighting = data['date_of_sighting']
        self.sasquatch_count = data['sasquatch_count']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.skeptics = None
        #self.comments=None
#Create
    @classmethod
    def create_sighting(cls, data):
        query = """
                    INSERT INTO sightings (location, what_happened, date_of_sighting, sasquatch_count, user_id) 
                    VALUES (%(location)s, %(what_happened)s, %(date_of_sighting)s, %(sasquatch_count)s, %(user_id)s);
        
        """
        # data is a dictionary that will be passed into the save method from server.py
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_sighting(data):
        is_valid = True  # We assume this is true
        
        if len(data['location']) < 2:
            flash("Location is required.")
            is_valid = False
        if len(data['what_happened']) < 2:
            flash("Description is required.")
            is_valid = False
        if not data['date_of_sighting']:
            flash("Date of sighting is required.")
            is_valid = False
        if not data['sasquatch_count'] or int(data['sasquatch_count']) < 1:
            flash("Sasquatch count must be at least 1.")
            is_valid = False
        
        return is_valid
# #READ
#             #This is not a normal one to many route this will select all and is good for posting to a wall.
    @classmethod
    def get_all_sightings_with_creator(cls):
            # Get all tweets, and their one associated User that created it
            query = "SELECT * FROM sightings JOIN users ON sightings.user_id = users.id;"
            results = connectToMySQL(cls.DB).query_db(query)
            all_sightings = []
            for row in results:
                # Create a Tweet class instance from the information from each db row
                one_sighting = cls(row)
                # Prepare to make a User class instance, looking at the class in models/user.py
                one_sightings_author_info = {
                    # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                    "id": row['users.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                }
                # Create the User class instance that's in the user.py model file
                author = User(one_sightings_author_info)
                # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
                one_sighting.creator = author
                # Append the Tweet containing the associated User to your list of tweets
                all_sightings.append(one_sighting)
            return all_sightings
    @classmethod
    def get_sighting_by_id_with_creator(cls, sighting_id):
        query = """
            SELECT * FROM sightings 
            JOIN users ON sightings.user_id = users.id 
            WHERE sightings.id = %(sighting_id)s;
        """
        data = {"sighting_id": sighting_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if result:
            sighting_data = result[0]
            creator_data = {
                "id": sighting_data['users.id'],
                "first_name": sighting_data['first_name'],
                "last_name": sighting_data['last_name'],
                "email": sighting_data['email'],
                "password": sighting_data['password'],
                "created_at": sighting_data['created_at'],
                "updated_at": sighting_data['updated_at']
            }
            creator = User(creator_data)
            
            sighting = cls(sighting_data)  # Create a Sighting instance
            sighting.creator = creator  # Associate the creator User instance with the Sighting
            return sighting
        else:
            return None


#update
    @classmethod
    def edit_sighting(cls, data):
        query = """
            UPDATE sightings
            SET location = %(location)s,
                what_happened = %(what_happened)s,
                date_of_sighting = %(date_of_sighting)s,
                sasquatch_count = %(sasquatch_count)s
            WHERE id = %(id)s;
        """
        
        return connectToMySQL(cls.DB).query_db(query, data)
#delete
    @classmethod
    def delete_sighting(cls, sighting_id):
        query = "DELETE FROM sightings WHERE id = %(sighting_id)s;"
        data = {"sighting_id": sighting_id}
        return connectToMySQL(cls.DB).query_db(query, data)
