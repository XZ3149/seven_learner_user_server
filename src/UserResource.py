import pymysql
import os
import random

class UserResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user= usr,
            password= pw,
            host= h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn



    @staticmethod
    def get_by_AccountID(key):

        sql = "SELECT AccountID, FirstName,MiddleName, LastName, Email FROM Userinfor.user where AccountID=%s";
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()
        return result

    def get_users(limit = 10, offset = 0):
        sql = f'SELECT AccountID, FirstName, LastName, Email FROM Userinfor.user limit {limit} offset {offset}';
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    def get_user_by_query(FirstName, LastName, Email, limit = 20, offset = 0):

        query_str = 'where'
        if FirstName:
            query_str += f' FirstName="{FirstName}" and'
        if LastName:
            query_str += f' LastName="{LastName}" and'
        if Email:
            query_str += f' Email="{Email}" and'
        query_str = query_str[:-4]

        conn = UserResource._get_connection()
        cur = conn.cursor()
        sql = f'SELECT AccountID, FirstName, MiddleName, LastName, Email FROM Userinfor.user {query_str} ORDER BY LastName limit ' \
              f'{limit} offset {offset}';
        print(sql)
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    def check_email_avalibility(Email):
        sql = f'SELECT count(*) FROM Userinfor.user where Email="{Email}"';
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchone()
        if result['count(*)'] == 0:
            return True
        else:
            return False



    def count_rows(table_name, conditions = ''):
        sql = f'SELECT count(*) FROM Userinfor.{table_name} {conditions}';
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchone()

        return result


    def create_accountID(FirstName, LastName, MiddleName, Email, Password):
        """this is the function use to create account"""
        AccountID = random.randrange(10000000,99999999)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        sql = 'SELECT * FROM Userinfor.user where AccountID=%s'

        while (cur.execute(sql, AccountID)):
            AccountID = random.randrange(10000000, 99999999)

        sql = 'insert into Userinfor.user (AccountID, FirstName, LastName,MiddleName,Email,Password) values (%s, %s, %s,%s, %s,%s)'
        res = cur.execute(sql, [AccountID,FirstName, LastName, MiddleName, Email, Password])
        if res:
            return AccountID
        return res

    def update_user_infor(AccountID, FirstName, LastName, MiddleName, Password):
        sql = 'update Userinfor.user set '

        if FirstName:
            sql += f'FirstName = %s, '
        if LastName:
            sql += f'LastName = %s, '
        if MiddleName:
            sql += f'MiddleName = %s, '
        if Password:
            sql += f'Password = %s, '

        sql = sql[:-2] + f' where AccountID = {AccountID}'
        values = []
        for i in [FirstName,LastName,MiddleName,Password]:
            if i:
                values += [[i]]
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, values)
        return res


    def delete_account(AccountID):
        """this is the function use to delete an account"""

        sql_order = f'delete from Userinfor.UserOrder where UserAccountID=%s'
        sql_restaurants = f'delete from Userinfor.FavoriteRestaurants where UserAccountID=%s'
        sql_user= f'delete from Userinfor.user where AccountID=%s'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql_order, AccountID)
        cur.execute(sql_restaurants,AccountID)
        result = cur.execute(sql_user, AccountID)

        return result

    def get_order_by_userID(AccountID, limit = 20, offset = 0):
        """this is the function use to get order information for a user"""
        sql = f'select OrderID from Userinfor.UserOrder where UserAccountID=%s limit {limit} offset {offset}'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, AccountID)
        result = cur.fetchall()

        return result



    def check_duplicate_orderID(orderID):
        sql = f'select * from Userinfor.UserOrder where OrderID=%s'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, orderID)
        result = cur.fetchall()
        if result:
            return True
        else:
            return False


    def add_user_order(AccountID, OrderID):
        sql = f'insert into Userinfor.UserOrder values ({AccountID}, {OrderID})'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)

        return res

    def count_userorder(AccountID):
        sql = f'select OrderID from Userinfor.UserOrder where UserAccountID=%s'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, AccountID)
        return res

    def delete_user_order(OrderID):
        sql = f'delete from Userinfor.UserOrder where OrderID= {OrderID}'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        return res


    def get_restaurants_by_userID(AccountID, limit = 20, offset = 0):
        """this is the function use to get order information for a user"""
        sql = f'select RestaurantID, RestaurantName from Userinfor.FavoriteRestaurants where UserAccountID=%s limit {limit} offset {offset}'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, AccountID)
        result = cur.fetchall()

        return result

    def count_user_restaurants(AccountID):
        sql = f'select RestaurantID from Userinfor.FavoriteRestaurants where UserAccountID=%s'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, AccountID)
        return res

    def check_duplicate_RestaurantID(RestaurantID):
        sql = f'select * from Userinfor.FavoriteRestaurants where RestaurantID=%s'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, RestaurantID)
        result = cur.fetchall()
        if result:
            return True
        else:
            return False


    def add_user_restaurant(AccountID, RestaurantID, RestaurantName):
        sql = f'insert into Userinfor.FavoriteRestaurants values ({AccountID}, {RestaurantID}, "{RestaurantName}")'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        return res

    def delete_user_restaurant(RestaurantID):
        sql = f'delete from Userinfor.FavoriteRestaurants where RestaurantID= {RestaurantID}'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        return res
















