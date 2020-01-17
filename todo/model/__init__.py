from .todo import ToDoList, ToDoItem


def ensure_indexes():
    ToDoList.ensure_index()
    ToDoItem.ensure_index()
