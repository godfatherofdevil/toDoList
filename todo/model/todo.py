from mongoengine import (
    Document,
    StringField,
    DateField,
    BooleanField,
    ReferenceField,
    CASCADE,
)


class ToDoList(Document):
    name = StringField(required=True, min_length=3, max_length=200)

    def __repr__(self):
        return f"{self.__name__}={self.name}"


class ToDoItem(Document):
    # name field is required to query in the routes
    name = StringField(required=True, min_length=3, max_length=200, primary_key=True)
    text = StringField(required=True, min_length=20, max_length=500)
    due_date = DateField(required=True)
    status = BooleanField(required=True, default=False)
    todo_list = ReferenceField("ToDoList", reverse_delete_rule=CASCADE)

    def __repr__(self):
        return f"{self.__name__}={self.name}"
