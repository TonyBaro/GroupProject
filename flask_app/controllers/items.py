from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.item import Item
from flask_app.models.user import User
from flask_app.models.image import Image
from flask_app.models.purchase import Purchase


@app.route("/items")
def all_items():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id": session["user_id"]
    }
    image_data = {
        "user_id": session['user_id']
    }
    return render_template("allItems.html", 
                            allItems = Item.get_all_items_with_users(), 
                            user = User.get_user_by_id(data),
                            img = Image.get_user_image(image_data) )




@app.route('/create/item', methods = ["POST"])
def create_item():
    if "user_id" not in session:
        return redirect("/logout")
    if Item.is_valid(request.form):
        data = {
            "name": request.form['name'],
            "cost" : request.form['cost'],
            "description": request.form['description'],
            "user_id": session['user_id'],
            
        }
        Item.save(data)
        return redirect("/items")
    else:
        return redirect("/dashboard")


@app.route('/update/item', methods = ["POST"])
def update_item():
    if "user_id" not in session:
        return redirect("/logout")
    if Item.is_valid(request.form):
        data = {
            "id": request.form["id"],
            "name": request.form['name'],
            "cost" : request.form['cost'],
            "description": request.form['description']
            }
        Item.update_item(data)
        return redirect("/items")
    else:
        return redirect(f"/edit/item/{request.form['id']}")




@app.route("/view/item/<int:id>")
def view_item(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id" : session["user_id"]
    }
    
    
    data = {
        "id" : id
    }
    
    image_data = {
        "user_id": session['user_id']
    }

    item_data = {
        "item_id": id
    }

    in_database = Purchase.get_item_purchase(item_data)

    return render_template("viewItem.html", 
                            item = Item.get_item(data),
                            user = User.get_user_by_id(user_data),
                            img = Image.get_user_image(image_data),
                            in_database=in_database)


@app.route("/edit/item/<int:id>")
def edit_item(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    user_data = {
        "id" : session["user_id"]
    }
    
    data = {
        "id": id
    }

    image_data = {
        "user_id": session['user_id']
    }
    return render_template("updateItem.html",
                            user = User.get_user_by_id(user_data),
                            item = Item.get_item(data),
                            img = Image.get_user_image(image_data))

@app.route("/delete/item/<int:id>")
def delete_item(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "id": id,
    }
    
    Item.delete_item(data)
    return redirect("/items")


@app.route("/buy/item", methods=["POST"])
def buy_item():
    in_database = Purchase.get_item_purchase(request.form)
    data = {
        "user_id": request.form["user_id"],
        "item_id": request.form['item_id']
    }
    if not in_database:
        Purchase.add_purchase(data)
        return redirect(f"/view/item/{request.form['item_id']}")
    else:
        return redirect(f"/view/item/{request.form['item_id']}")
        