from flask import Flask, render_template, redirect
from pymongo import MongoClient
from bson import Decimal128
from classes import *
from six import iteritems
from pprint import pprint as pp

# from flask mongoengine tutorial

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY="yoursecretkey"))
client = MongoClient("localhost:27017")
db = client.TaskManager

if db.settings.find({"name": "task_id"}).count() <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({"name": "task_id", "value": 0})


def updateRecipeID(value):
    task_id = db.settings.find_one()["value"]
    task_id += value
    db.settings.update_one({"name": "task_id"}, {"$set": {"value": task_id}})


def createRecipe(form):
    title = form.title.data
    shortdesc = form.shortdesc.data
    amount = float(form.amount.data)
    unit = form.unit.data
    ingredient_list = form.ingredient_list.data
    task_id = db.settings.find_one()["value"]

    task = {
        "id": task_id,
        "title": title,
        "shortdesc": shortdesc,
        "ingredient_list": [
            {"amount": amount, "unit": unit, "ingredient": ingredient_list}
        ],
    }

    db.tasks.insert_one(task)
    updateRecipeID(1)
    return redirect("/")


def deleteRecipe(form):
    key = form.key.data
    title = form.title.data

    if key:
        print(key, type(key))
        db.tasks.delete_many({"id": int(key)})
    else:
        db.tasks.delete_many({"title": title})

    return redirect("/")


def updateRecipe(form):
    key = form.key.data
    amount = float(form.amount.data)
    unit = form.unit.data
    ingredient = form.ingredient.data

    ## need to get existing value and append, not overwrite
    ingredient_list = db.tasks.find_one({"id": int(key)})["ingredient_list"] or []
    ingredient_list.append({"amount": amount, "unit": unit, "ingredient": ingredient})

    db.tasks.update_one(
        {"id": int(key)}, {"$set": {"ingredient_list": ingredient_list}}
    )

    return redirect("/")


def CreateShoppingList(form):
    keys = form.keys.data
    for key in keys.split(","):
        query = {"id": int(key)}
        new_values = {"$set": {"selected": True}}
        db.tasks.update_one(query, new_values)

    docs = db.tasks.find({"selected": True})
    data = []
    for item in docs:
        data.append(item)
    shopping_list = {}

    for item in data:
        for element in item["ingredient_list"]:
            if element["ingredient"] not in shopping_list:
                key = element["ingredient"]
                value = element
                shopping_list[key] = value
            else:
                key = element["ingredient"]

                if element["unit"] == shopping_list[key]["unit"]:
                    value = shopping_list[key]["amount"] + element["amount"]
                    shopping_list[key]["amount"] = value

    return redirect("/shopping")


def resetRecipe(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({"name": "task_id", "value": 0})
    return redirect("/")


@app.route("/shopping/", methods=["GET", "POST"])
def main_shopping_list():

    gform = GetShoppingList(prefix="gform")

    if gform.validate_on_submit() and gform.create.data:
        return CreateShoppingList(gform)

    docs = db.tasks.find({"selected": True})
    shopping_list = {}
    recipe_names = []

    for item in docs:
        recipe_names.append(item["title"])
        for element in item["ingredient_list"]:
            if element["ingredient"] not in shopping_list:
                key = element["ingredient"]
                value = element
                shopping_list[key] = value
            else:
                key = element["ingredient"]

                if element["unit"] == shopping_list[key]["unit"]:
                    value = shopping_list[key]["amount"] + element["amount"]
                    shopping_list[key]["amount"] = value

    shopping_list = [value for key, value in iteritems(shopping_list)]
    return render_template(
        "shopping.html",
        gform=gform,
        shopping_list=shopping_list,
        recipe_names=recipe_names,
    )


@app.route("/", methods=["GET", "POST"])
def main():
    # create form
    cform = CreateRecipe(prefix="cform")
    dform = DeleteRecipe(prefix="dform")
    uform = MeasuredIngredient(prefix="uform")
    reset = ResetRecipe(prefix="reset")

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createRecipe(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteRecipe(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateRecipe(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetRecipe(reset)

    # read all data
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template(
        "home.html", cform=cform, dform=dform, uform=uform, data=data, reset=reset
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4005)
