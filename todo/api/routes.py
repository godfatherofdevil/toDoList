from datetime import datetime

from flask import request, jsonify, abort
from werkzeug.exceptions import BadRequest

from mongoengine.errors import DoesNotExist

from todo.api import bp
from todo.model import ToDoList, ToDoItem

ROUTE_PREFIX = "/api/v1/todo"
DUE_DATE_TIME_FORMAT = "%d/%m/%Y"


@bp.route(f"{ROUTE_PREFIX}/list", methods=("POST", "GET"))
def create_list_todo_list():
    if request.method == "POST":
        try:
            body = request.get_json()
        except BadRequest as e:
            return jsonify({"error": "bad payload"}), 400
        name = body.get("name")
        todo_list = ToDoList(name=name)
        todo_list.save()

        return jsonify(({"success": f"{body.get('name')} created successfully"})), 201
    elif request.method == "GET":
        return_todo_list = ToDoList.objects().exclude("id")
        if return_todo_list:
            return jsonify(return_todo_list), 200
        else:
            return jsonify({"error": "todo list is empty, create some new"}), 404


@bp.route(f"{ROUTE_PREFIX}/list/<string:name>", methods=("GET", "PUT", "PATCH", "DELETE",))
def get_update_or_delete_todo_list(name):
    # name - todo_list to delete
    if request.method == "GET":
        return_todo_list = ToDoList.objects(name=name).exclude("id")
        if return_todo_list:
            return jsonify(return_todo_list), 200
        else:
            return jsonify({"error": f"{name} not found"}), 404
    elif request.method == "PUT" or request.method == "PATCH":
        try:
            body = request.get_json()
        except BadRequest as e:
            return jsonify({"error": "bad payload"}), 400

        todo_list_to_update = ToDoList.objects(name=name)
        if not todo_list_to_update:
            return jsonify({"error": f"{name} not found in the todo lists"}), 400

        new_name = body.get("name")
        if not new_name:
            return jsonify({"error": "to update a todo list, provide new name"}), 400

        todo_list_to_update.update(name=new_name)
        return jsonify({"success": f"{name} is updated to {new_name}"}), 200
    elif request.method == "DELETE":
        try:
            ToDoList.objects(name=name).delete()
        except DoesNotExist as de:
            return jsonify({"error": f"{name} does not exist in todo lists"}), 400
        else:
            return jsonify({"success": f"{name} successfully deleted from todo lists"}), 200


@bp.route(f"{ROUTE_PREFIX}/item/<string:todo_list_name>", methods=("POST", "GET", ))
def create_list_todo_item(todo_list_name):
    # todo_list_name - the todo_list name for which todo_item should be created
    todo_list = ToDoList.objects(name=todo_list_name).first()
    if not todo_list:
        abort(400)
    if request.method == "POST":
        try:
            body = request.get_json()
        except BadRequest as e:
            return jsonify({"error": f"bad payload: {str(e)}"}), 400

        name = body.get("name")
        text = body.get("text")
        due_date = datetime.strptime(body.get("due_date"), DUE_DATE_TIME_FORMAT)
        status = body.get("status")
        containing_todo_list = todo_list.id
        todo_item = ToDoItem(name=name, text=text, due_date=due_date, status=status, todo_list=containing_todo_list)
        todo_item.save()
        return jsonify({"success": f"item={text} in list={todo_list_name} created successfully"}), 201
    elif request.method == "GET":
        # list all the todo_items in todo_list_name
        todo_list_id = todo_list.id
        todo_items = ToDoItem.objects(todo_list=todo_list_id)
        return jsonify(todo_items), 200


@bp.route(f"{ROUTE_PREFIX}/item/<string:todo_list_name>/<string:item_name>", methods=("GET", "PUT", "PATCH", "DELETE"))
def get_update_or_delete_todo_item(todo_list_name, item_name):
    # todo_list_name - is the todo_list from which item item_name needs to be either
    # retrieved, updated or deleted
    todo_list = ToDoList.objects(name=todo_list_name).first()
    todo_item = ToDoItem.objects(name=item_name).first()
    if request.method == "GET":
        item_to_return = {k: getattr(todo_item, k) for k in todo_item if k != "todo_list"} if todo_item else {}
        return jsonify({f"{item_name}": item_to_return}), 200
    elif request.method == "PUT" or request.method == "PATCH":
        try:
            body = request.get_json()
        except BadRequest as e:
            return jsonify({"error": f"bad payload: {str(e)}"}), 400

        new_name = body.get("name") or item_name
        new_text = body.get("text")
        new_due_date = datetime.strptime(body.get("due_date"), DUE_DATE_TIME_FORMAT)
        new_status = body.get("status")
        todo_item.update(name=new_name, text=new_text, due_date=new_due_date, status=new_status)
        return jsonify({"success": f"todo_item={item_name} successfully updated"}), 200
    elif request.method == "DELETE":
        try:
            ToDoItem.objects(name=item_name).delete()
        except DoesNotExist as e:
            return jsonify({"error": f"{item_name} does not exists in {todo_list_name}"}), 400
        return jsonify({"success": f"{item_name} deleted from {todo_list_name}"}), 200
