import re

from flask import Flask, Response, request, redirect, url_for, request
from datetime import datetime
import json
from UserResource import UserResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.get("/status/health")
def get_status():
    t = str(datetime.now())
    msg = {
        "name": "UserResource-Microservice",
        "health": "Good",
        "at time": t
    }

    result = Response(json.dumps(msg), status=200, content_type="application/json")
    return result


@app.route("/users/<AccountID>", methods=["GET", 'PUT', 'DELETE'])
def get_user_by_account_id(AccountID):

    if request.method == 'GET':
        result = UserResource.get_by_AccountID(AccountID)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp

    if request.method == "PUT":
        FirstName = request.form.get('FirstName', default = None)
        LastName = request.form.get('LastName', default = None)
        Password = request.form.get('Password', default = None)
        MiddleName = request.form.get('MiddleName', default = None)

        if not FirstName and not LastName and not Password and not MiddleName:
            rsp = Response("You need to update something", status=400, content_type="text/plain")
        else:
            UserResource.update_user_infor(AccountID,FirstName,LastName,MiddleName, Password)
            rsp = redirect(url_for('get_user_by_account_id', AccountID=AccountID))

        return rsp


    if request.method == 'DELETE':
        result = UserResource.delete_account(AccountID)

        if result:
            rsp = Response("Delete successful", status=200, content_type="text/plain")
        else:
            rsp = Response("Delete Fail, please check entry again", status=400, content_type="text/plain")
    return rsp



@app.route("/users/<AccountID>/UserOrders", methods=["GET", "POST", 'DELETE'])
def get_user_order_by_accountID(AccountID):
    # check whether user exist before checking all other things
    head_infor = UserResource.get_by_AccountID(AccountID)
    if not head_infor:
        rsp = Response("USER NOT FOUND", status=404, content_type="text/plain")
        return rsp
    if request.method == 'GET':

        per_page = request.args.get('per_page', default = 10, type = int) # define how many results you want per page
        page = request.args.get('page', default = 1, type=int)
        offset = (page - 1) * per_page  # offset for SQL query
        count = len(UserResource.get_order_by_userID(AccountID, 10000, 0))
        number_pages = (count // per_page) + 1

        result = UserResource.get_order_by_userID(AccountID, per_page,offset)

        if result:
            result.insert(0, head_infor)
            result[0]['page'] = page
            result[0]['numberPages'] = number_pages
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp

    if request.method == "POST":
        OrderID = request.form.get('OrderID', default = None, type = int)
        if not OrderID:
            rsp = Response("You need to enter a OrderID", status=400, content_type="text/plain")

        elif UserResource.check_duplicate_orderID(OrderID):
            rsp = Response("Duplicate OrderID", status=400, content_type="text/plain")

        else:
            res = UserResource.add_user_order(AccountID,OrderID)
            if res:
                rsp = redirect(url_for('get_user_order_by_accountID', AccountID=AccountID))
            else:
                rsp = Response("Update fail", status=400, content_type="text/plain")
        return rsp


    if request.method == 'DELETE':
        OrderID = request.form.get('OrderID', default=None, type=int)
        if not OrderID:
            rsp = Response("You need to enter a OrderID", status=400, content_type="text/plain")

        elif not UserResource.check_duplicate_orderID(OrderID):
            rsp = Response("OrderID not exist", status=400, content_type="text/plain")
        else:
            res = UserResource.delete_user_order(OrderID)
            if res:
                rsp = rsp = redirect(url_for('get_user_order_by_accountID', AccountID=AccountID))
            else:
                rsp = Response("delete fail", status=400, content_type="text/plain")

        return rsp


@app.route("/users/<AccountID>/FavoriteRestaurants", methods=["GET", "POST", "DELETE"])
def get_user_restaurants(AccountID):
    head_infor = UserResource.get_by_AccountID(AccountID)
    if not head_infor:
        rsp = Response("USER NOT FOUND", status=404, content_type="text/plain")
        return rsp
    if request.method == 'GET':

        per_page = request.args.get('per_page', default = 10, type = int) # define how many results you want per page
        page = request.args.get('page', default = 1, type=int)
        offset = (page - 1) * per_page  # offset for SQL query
        count = len(UserResource.get_order_by_userID(AccountID, 10000, 0))
        number_pages = (count // per_page) + 1

        result = UserResource.get_restaurants_by_userID(AccountID, per_page,offset)

        if result:
            result.insert(0, head_infor)
            result[0]['page'] = page
            result[0]['numberPages'] = number_pages
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp

    if request.method == "POST":
        RestaurantID = request.form.get('RestaurantID', default = None, type = int)
        RestaurantName = request.form.get('RestaurantName', default='Unknown_restaurant', type=str)

        if not RestaurantID:
            rsp = Response("You need to enter a RestaurantID", status=400, content_type="text/plain")

        elif UserResource.check_duplicate_RestaurantID(RestaurantID):
            rsp = Response("Duplicate RestaurantID, you already favor this restaurant", status=400, content_type="text/plain")

        else:
            res = UserResource.add_user_restaurant(AccountID,RestaurantID,RestaurantName)
            if res:
                rsp = redirect(url_for('get_user_restaurants', AccountID=AccountID))
            else:
                rsp = Response("Update fail", status=400, content_type="text/plain")
        return rsp

    if request.method == 'DELETE':
        RestaurantID = request.form.get('RestaurantID', default = None, type = int)
        if not RestaurantID:
            rsp = Response("You need to enter a RestaurantID", status=400, content_type="text/plain")
        elif not UserResource.check_duplicate_RestaurantID(RestaurantID):
            rsp = Response("Favorite restaurant not exist", status=400, content_type="text/plain")
        else:
            res = UserResource.delete_user_restaurant(RestaurantID)
            if res:
                rsp = rsp = redirect(url_for('get_user_restaurants', AccountID=AccountID))
            else:
                rsp = Response("delete fail", status=400, content_type="text/plain")
        return rsp




@app.route("/users", methods=["GET",'POST'])
def get_user_infor():
    if request.method == 'GET':
        FirstName = request.args.get('FirstName', default = None)
        LastName = request.args.get('LastName', default = None)
        Email = request.args.get('Email', default = None)
        per_page = request.args.get('per_page', default = 10, type = int) # define how many results you want per page
        page = request.args.get('page', default = 1, type=int)
        offset = (page - 1) * per_page  # offset for SQL query
        #limit = request.args.get('limit', default = 50, type=int)

        if FirstName or LastName or Email:
            result = UserResource.get_user_by_query(FirstName, LastName, Email, per_page, offset)
            count = len(UserResource.get_user_by_query(FirstName, LastName, Email, 1000, 0))
        else:
            count = UserResource.count_rows('user')['count(*)']
            result = UserResource.get_users(per_page, offset)
        if result:
            number_pages = (count // per_page) + 1
            result.insert(0, {'page': page, 'numberPages': number_pages})
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp


    if request.method == 'POST':
        FirstName = request.form.get('FirstName', default = None)
        LastName = request.form.get('LastName', default = None)
        Email = request.form.get('Email', default = None)
        Password = request.form.get('Password', default = None)
        MiddleName = request.form.get('MiddleName', default = '')
        if not FirstName or not LastName or not Password or not Email:
            rsp = Response("Please Enter Correct Information", status=400, content_type="text/plain")

        elif not UserResource.check_email_avalibility(Email):
            rsp = Response("Email have been used", status=400, content_type="text/plain")
        else:

            result = UserResource.create_accountID(FirstName, LastName, MiddleName, Email, Password)
            # if insertion happen, server will return accountID, else return 0
            if result:
                rsp = redirect(url_for('get_user_by_account_id', AccountID= result))
            else:
                rsp = Response("Fail to create Account", status=400, content_type="text/plain")
        return rsp


@app.route("/test_post", methods=["POST"])
def test_post_method():
    if request.method == 'POST':

        user = request.form.get("id")
        return user



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

