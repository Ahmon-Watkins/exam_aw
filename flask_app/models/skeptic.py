from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.user import User

class Skeptic:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.skeptic_id = data['skeptic_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_skeptic(cls, data):
        query = "INSERT INTO skeptics (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_skeptics_for_sighting(cls, sighting_id):
        query = "SELECT * FROM skeptics WHERE sighting_id = %(sighting_id)s;"
        data = {"sighting_id": sighting_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(result) for result in results]

    @classmethod
    def get_users_skeptical_of_sighting(cls, sighting_id):
        query = "SELECT users.* FROM users JOIN skeptics ON users.id = skeptics.user_id WHERE skeptics.sighting_id = %(sighting_id)s;"
        data = {"sighting_id": sighting_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [User(result) for result in results]
    
    @classmethod
    def is_user_skeptical(cls, user_id, sighting_id):
        query = "SELECT * FROM skeptics WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        data = {'user_id': user_id, 'sighting_id': sighting_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return len(result) > 0
    
    @classmethod
    def remove_skeptic(cls, user_id, sighting_id):
        query = "DELETE FROM skeptics WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        data = {'user_id': user_id, 'sighting_id': sighting_id}
        connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_skeptic_count(cls, sighting_id):
        query = "SELECT COUNT(*) AS count FROM skeptics WHERE sighting_id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result[0]['count'] if result else 0