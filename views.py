import flask

import models as Todo


def index():
    # As a list to test debug toolbar
    Todo.Todo.objects().delete()  # Removes
    Todo.Todo(title="Simple todo A", text="12345678910").save()  # Insert
    Todo.Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = list(Todo.Todo.objects[:10])
    todos = Todo.Todo.objects.all()
    return flask.render_template("index.html", todos=todos)


def pagination():
    Todo.Todo.objects().delete()
    for i in range(10):
        Todo.Todo(title="Simple todo {}".format(i), text="12345678910").save()  # Insert

    page_num = int(flask.request.args.get("page") or 1)
    todos_page = Todo.Todo.objects.paginate(page=page_num, per_page=3)

    return flask.render_template("pagination.html", todos_page=todos_page)
