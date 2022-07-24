from flask_app.config.mysqlconnection import connectToMySQL
class Purchase:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data["user_id"]
        self.item_id = data["item_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from purchases;"
        results = connectToMySQL('projects-group').query_db(query)
        purchases = []
        for purchase in results:
            purchases.append(cls(purchase))
        return purchases
    
    @classmethod
    def get_item_purchase(cls, data):
        query = "SELECT * from purchases left join items on items.id = purchases.item_id where item_id = %(item_id)s;"
        results = connectToMySQL('projects-group').query_db(query, data)
        purchases = []
        for purchase in results:
            purchases.append( cls(purchase) )
        return purchases
    
    
    @classmethod
    def add_purchase(cls, data):
        query = "INSERT INTO purchases (user_id, item_id, created_at, updated_at) VALUES (%(user_id)s, %(item_id)s , NOW(), NOW());" # this returns an id
        return connectToMySQL('projects-group').query_db(query, data)
    
    
    
    @classmethod
    def delete_purchase(cls, data):
        query = "DELETE from purchases where user_id = %(user_id)s and item_id = %(item_id)s;"
        return connectToMySQL('projects-group').query_db(query, data)
    
    @classmethod
    def delete_item_purchases(cls, data):
        query = "DELETE from purchases where item_id = %(item_id)s;"
        return connectToMySQL('projects-group').query_db(query, data)