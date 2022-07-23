from asyncio.windows_events import NULL
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
 


class Item:
    def __init__(self, data):
        self.id = data['id']
        self.creator_first_name = data["creator_first_name"]
        self.creator_last_name = data["creator_last_name"]
        self.name = data["name"]
        self.cost = data['cost']
        self.description = data['description']
        self.user_id = data["user_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL('projects-group').query_db(query)
        items = []
        # Iterate over the db results and create instances
        for item in results:
            items.append( cls(item) )
        return items
    
    
    
    
    @classmethod
    def get_all_items_with_users(cls):
        query = "SELECT users.first_name as creator_first_name, users.last_name as creator_last_name, items.* from items left join users on users.id = items.user_id;"
        results = connectToMySQL('projects-group').query_db(query)
        items = []
        for item in results:
            items.append( cls(item) )
        return items
     
    
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO items ( name, cost, description, user_id, created_at, updated_at ) VALUES ( %(name)s, %(cost)s, %(description)s, %(user_id)s, NOW() , NOW() );" 
        return connectToMySQL('projects-group').query_db( query, data ) 
    
    
    
    @classmethod
    def get_item(cls, data):
        query = "SELECT users.first_name as creator_first_name, users.last_name as creator_last_name, items.* from items left join users on users.id = items.user_id where items.id = %(id)s;"
        results = connectToMySQL('projects-group').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    
    @classmethod
    def get_user_items(cls, data):
        query = "SELECT * from items where user_id = %(user_id);"
        results = connectToMySQL('projects-group').query_db(query, data)
        items = []
        for item in results:
            items.append( cls(item) )
        return items
    
    
    
    
    @classmethod
    def update_item(cls, data):
        query = "UPDATE items SET name = %(name)s, cost = %(cost)s, description = %(description)s, created_at = NOW(), updated_at = NOW() WHERE items.id = %(id)s;"
        return connectToMySQL('projects-group').query_db(query, data)
    
    
    @classmethod
    def delete_item(cls, data):
        query = "DELETE from items where items.id = %(id)s;"
        return connectToMySQL('projects-group').query_db(query, data)
    
    
    
    @staticmethod
    def is_valid(item):
        is_valid = True # we assume this is true
        if len(item['name']) <= 0:
            flash("Item name is required.")
            is_valid = False
        if int(item['cost']) < 1 or int(item['cost']) == None:
            flash("Cost is required.")
            is_valid = False
        if len(item['description']) <= 0:
            flash("Description is required.")
            is_valid = False
        return is_valid