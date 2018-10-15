from datetime import datetime
from werkzeug.security import generate_password_hash
from .database import FastFoodDB


class User(FastFoodDB):
    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 is_admin=False):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def add(self):
        ''' Add uset to user table'''
        self.cursor.execute(
            ''' INSERT INTO users(username, email, password, is_admin) VALUES(%s, %s,%s, %s)''',
            (self.username, self.email, self.password, self.is_admin))

        self.connection.commit()
        self.cursor.close()

    def get_user_by_username(self, username):
        ''' get user by username '''
        self.cursor.execute(''' SELECT * FROM users WHERE username=%s''',
                            (username, ))

        user = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if user:
            return self.objectify_user(user)
        return None

    def get_user_by_email(self, email):
        ''' get user by email '''
        self.cursor.execute(''' SELECT * FROM users WHERE email=%s''',
                            (email, ))

        user = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if user:
            return self.objectify_user(user)
        return None

    def objectify_user(self, data):
        ''' coerse a tuple user to an object '''
        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password = data[3]
        self.is_admin = data[4]

        return self


class Order(FastFoodDB):
    def __init__(self,
                 username=None,
                 destination=None,
                 name=None,
                 price=None,
                 status="Pending"):
        super().__init__()
        self.username = username
        self.destination = destination
        self.name = name
        self.price = price
        self.status = status
        self.date = datetime.now()

    def add(self):
        ''' Add food order to database'''
        self.cursor.execute(
            ''' INSERT INTO orders(username, destination, name, price, status, date) VALUES(%s, %s, %s,%s, %s, %s)''',
            (self.username, self.destination, self.name, self.price,
             self.status, self.date))

        self.connection.commit()
        self.cursor.close()

    def get_by_id(self, order_id):
        '''fetch an order by id'''
        self.cursor.execute(''' SELECT * FROM orders WHERE id=%s''',
                            (order_id, ))

        order = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if order:
            return self.objectify(order)
        return None

    def delete(self, order_id):
        ''' Delete order '''
        self.cursor.execute(''' DELETE FROM orders WHERE id=%s''',
                            (order_id, ))
        self.connection.commit()
        self.cursor.close()

    def accept_status(self, order_id):
        """ Accept an order """
        self.cursor.execute(
            """
        UPDATE orders SET status=%s WHERE id=%s
        """, ('accepted', order_id))

        self.connection.commit()
        self.cursor.close()

    def decline_order(self, order_id):
        """ decline a specific order """
        self.cursor.execute(
            """
        UPDATE orders SET status=%s WHERE id=%s
        """, ('declined', order_id))

        self.connection.commit()
        self.cursor.close()

    def complete_accepted_order(self, order_id):
        """ mark an order as completed  """
        self.cursor.execute(
            """
        UPDATE foodorders SET status=%s WHERE id=%s
        """, ('completed', order_id))

        self.connection.commit()
        self.cursor.close()

    def get_all_foodorders(self):
        '''  Get all food orders '''
        self.cursor.execute(''' SELECT * FROM orders''')

        orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if orders:
            return [self.objectify(order) for order in orders]
        return None

    def accepted_orders(self):
        ''' Get the Orders accepted by admin '''
        self.cursor.execute("SELECT * FROM orders WHERE status=%s",
                            ('accepted', ))

        accepted_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if accepted_orders:
            return [
                self.objectify(accepted_order)
                for accepted_order in accepted_orders
            ]
        return None

    def declined_orders(self):
        ''' return declined orders '''
        self.cursor.execute("SELECT * FROM orders WHERE status=%s",
                            ('declined', ))

        declined_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if declined_orders:
            return [
                self.objectify(declined_order)
                for declined_order in declined_orders
            ]
        return None

    def completed_orders(self):
        ''' Get all completed orders '''
        self.cursor.execute("SELECT * FROM foodorders WHERE status=%s",
                            ('completed', ))

        completed_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if completed_orders:
            return [
                self.objectify(completed_order)
                for completed_order in completed_orders
            ]
        return None

    def serialize(self):
        '''return an object as dictionary'''
        return dict(
            id=self.id,
            username=self.username,
            name=self.name,
            price=self.price,
            destination=self.destination,
            status=self.status,
            date=self.date)

    def objectify(self, data):
        ''' map tuple to an object '''
        order = Order(
            username=data[1],
            destination=data[2],
            name=data[3],
            price=data[4],
            status=data[5])
        order.id = data[0]
        order.date = str(data[6])
        self = order
        return self


class FoodItem(FastFoodDB):
    def __init__(self, name=None, description=None, price=None):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now()

    def add(self):
        ''' Add food item to fooditems table'''
        self.cursor.execute(
            ''' INSERT INTO fooditems(name, description, price, date) VALUES(%s, %s, %s, %s)''',
            (self.name, self.description, self.price, self.date))

        self.connection.commit()
        self.cursor.close()

    def get_food_by_id(self, food_id):
        '''fetch an item by id'''
        self.cursor.execute(''' SELECT * FROM fooditems WHERE id=%s''',
                            (food_id, ))

        item = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if item:
            return self.objectify(item)
        return None

    def get_food_by_name(self, name):
        '''fetch an item by name'''
        self.cursor.execute(''' SELECT * FROM fooditems WHERE name=%s''',
                            (name, ))

        item = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if item:
            return self.objectify(item)
        return None

    def get_all_fooditems(self):
        '''  Get all food items '''
        self.cursor.execute(''' SELECT * FROM fooditems''')

        items = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if items:
            return [self.objectify(item) for item in items]
        return None

    def delete(self, food_id):
        ''' Delete food '''
        self.cursor.execute(''' DELETE FROM orders WHERE id=%s''',
                            (food_id, ))
        self.connection.commit()
        self.cursor.close()


    def serialize(self):
        '''return a object as dictionary'''
        return dict(
            name=self.name,
            description=self.description,
            price=self.price,
            id=self.id,
            date=str(self.date)
            )

    def objectify(self, data):
        ''' map tuple to an object '''
        item = FoodItem(name=data[1], description=data[2], price=data[3])
        item.id = data[0]
        item.date = data[4]
        self = item
        return self
