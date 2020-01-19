# toDoList #
* simple todo REST web service built with flask and mongodb.
* tested with python 3.7 (you can try with any other version but 3.7 is desirable)
## steps to run locally-
1. `git clone https://github.com/godfatherofdevil/toDoList.git`
2. `cd toDoList`
3. `python -m venv .env`
4. `source .env/bin/activate`
5. `python -m pip install -r requirements.txt`
6. ensure mongodb is running on localhost @ port 27017
 * either native installation of mongo
 * or `docker run -d -p 27017:27017 --name mongo_local mongo:latest`
 7. `export TODO_ENV=dev` (by default it is 'dev' this step is required for other environments)
 8. `python app.py`
 
 Now the toDoList web service will be running on `http://0.0.0.0:5000`
 
 ## steps to query the API
 There are two kinds of endpoints - one for todo list and one for todo items in those list
 1. `curl -X GET http://0.0.0.0:5000/api/v1/todo/list` 
 This will list all the todo lists
 2. `curl -X POST -H "Content-Type: application/json" -d '{"name": "<todo list name>"}' `
 This will create a new todo list 
 3. `curl -X DELETE http://0.0.0.0:5000/api/v1/todo/list/<string:list_name>`
 This will delete the specified list, same for PUT and PATCH to update
 4. `curl -X POST -H "Content-Type: application/json" http://0.0.0.0:5000/api/v1/todo/item/<string:list_name> 
 -d '{"name": "phase1", "text": "some item that need to be finished in <list_name> category", "due_date": "30/01/2020", "status": false}'`
 Note that all the fields for item are required and due_date has format of DD/MM/YYYY
 5. `curl -X GET http://0.0.0.0:5000/api/v1/todo/item/<string:list_name>`
 This will return the list of all the items for this todo_list
 6. `curl -X DELETE http://0.0.0.0:5000/api/v1/todo/item/<string:list_name>/<string:item>`
 This will delete the item from the specified todo_list
 Same for PUT and PATCH to update the todo_items

