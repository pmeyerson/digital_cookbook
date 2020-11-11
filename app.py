from flask import Flask, render_template, redirect
from pymongo import MongoClient
from bson import Decimal128
from classes import *

# from flask mongoengine tutorial

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.TaskManager

if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({'name':'task_id', 'value':0})

def updateRecipeID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def createRecipe(form):
    title = form.title.data
    shortdesc = form.shortdesc.data
    amount = float(form.amount.data)
    unit = form.unit.data
    ingredient_list = form.ingredient_list.data
    task_id = db.settings.find_one()['value']

    
    task = {
        'id':task_id, 
        'title':title, 
        'shortdesc':shortdesc,
        'ingredient_list': [{"amount": amount, "unit": unit, "ingredient": ingredient_list}]
    }

    db.tasks.insert_one(task)
    updateRecipeID(1)
    return redirect('/')

def deleteRecipe(form):
    key = form.key.data
    title = form.title.data

    if(key):
        print(key, type(key))
        db.tasks.delete_many({'id':int(key)})
    else:
        db.tasks.delete_many({'title':title})

    return redirect('/')

def updateRecipe(form):
    key = form.key.data
    amount = float(form.amount.data)
    unit = form.unit.data
    ingredient = form.ingredient.data

    ## need to get existing value and append, not overwrite
    ingredient_list = db.tasks.find_one({"id": int(key)})["ingredient_list"] or []
    ingredient_list.append({"amount": amount, "unit": unit, "ingredient": ingredient})
    
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"ingredient_list": ingredient_list}
        }
    )

    return redirect('/')

def resetRecipe(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name':'task_id', 'value':0})
    return redirect('/')

@app.route('/', methods=['GET','POST'])
def main():
    # create form
    cform = CreateRecipe(prefix='cform')
    dform = DeleteRecipe(prefix='dform')
    uform = MeasuredIngredient(prefix='uform')
    reset = ResetRecipe(prefix='reset')

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

    return render_template('home.html', cform = cform, dform = dform, uform = uform, \
            data = data, reset = reset)

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=4005)
