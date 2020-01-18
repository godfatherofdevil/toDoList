import unittest
from mongoengine import connect, get_connection
import json
import copy

from todo import create_app


class TestTodoApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """ Define the test variables and initialize the app"""
        cls.app = create_app(config_name="test")
        cls.client = cls.app.test_client()
        cls.ROUTE_PREFIX = "http://localhost:5000/api/v1/todo"
        connect("mongoenginetest", host="mongomock://localhost", alias="testdb")
        cls.db = get_connection("testdb")

    @classmethod
    def tearDown(cls) -> None:
        get_connection("testdb").drop_database("mongoenginetest")

    def test__todo_lists_post(self):
        url = self.ROUTE_PREFIX + "/list"
        with self.client as c:
            # without payload
            rv = c.post(url)
            self.assertEqual(rv.status_code, 400)

            # invalid payload
            body = dict(invalid_name="test")
            rv = c.post(url, data=json.dumps(body), content_type="application/json")
            self.assertEqual(rv.status_code, 400)

            # valid payload
            body = dict(name="test")
            rv = c.post(url, data=json.dumps(body), content_type="application/json")
            self.assertEqual(rv.status_code, 201)

    def test__todo_lists_get(self):
        url = self.ROUTE_PREFIX + "/list"
        with self.client as c:
            # first create some lists in the db
            todo_lists = [
                {"name": "test_list1"},
                {"name": "test_list2"},
                {"name": "test_list3"},
            ]
            for l in todo_lists:
                c.post(url, data=json.dumps(l), content_type="application/json")

            rv = c.get(url)
            self.assertEqual(rv.status_code, 200)
            # assert that all lists are returned
            ret_list = json.loads(rv.data.decode("utf-8"))
            self.assertListEqual(ret_list, todo_lists)

    def test__todo_list_get_one(self):
        url = self.ROUTE_PREFIX + "/list"
        with self.client as c:
            # first create some lists in the db
            todo_lists = [
                {"name": "test_list1"},
                {"name": "test_list2"},
                {"name": "test_list3"},
            ]
            for l in todo_lists:
                c.post(url, data=json.dumps(l), content_type="application/json")

            rv = c.get(url + f"/{todo_lists[0].get('name')}")
            self.assertEqual(rv.status_code, 200)
            ret_list = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(ret_list[0], todo_lists[0])

            rv = c.get(url + f"/{todo_lists[1].get('name')}")
            self.assertEqual(rv.status_code, 200)
            ret_list = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(ret_list[0], todo_lists[1])

            rv = c.get(url + f"/{todo_lists[2].get('name')}")
            self.assertEqual(rv.status_code, 200)
            ret_list = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(ret_list[0], todo_lists[2])

    def test__todo_list_delete_one(self):
        url = self.ROUTE_PREFIX + "/list"
        with self.client as c:
            # first create some lists in the db
            todo_lists = [
                {"name": "test_list1"},
                {"name": "test_list2"},
                {"name": "test_list3"},
            ]
            for l in todo_lists:
                c.post(url, data=json.dumps(l), content_type="application/json")

            rv = c.delete(url + f"/{todo_lists[0].get('name')}")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                f"{todo_lists[0].get('name')} successfully deleted",
                rv.data.decode("utf-8"),
            )

    def test__todo_list_update_one(self):
        url = self.ROUTE_PREFIX + "/list"
        with self.client as c:
            # first create some lists in the db
            todo_lists = [
                {"name": "test_list1"},
                {"name": "test_list2"},
                {"name": "test_list3"},
            ]
            for l in todo_lists:
                c.post(url, data=json.dumps(l), content_type="application/json")

            # empty body
            rv = c.put(url + f"/{todo_lists[0].get('name')}")
            self.assertEqual(rv.status_code, 400)

            # not in database
            rv = c.put(url + "/random_list")
            self.assertEqual(rv.status_code, 400)

            rv = c.put(
                url + f"/{todo_lists[0].get('name')}",
                data=json.dumps({"name": "testlist01"}),
                content_type="application/json",
            )
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                f"{todo_lists[0].get('name')} is updated", rv.data.decode("utf-8")
            )

    def test__todo_item_post_get(self):
        url = self.ROUTE_PREFIX + "/item"
        with self.client as c:
            todo_list = {"name": "test_list"}
            c.post(
                self.ROUTE_PREFIX + "/list",
                data=json.dumps(todo_list),
                content_type="application/json",
            )

            todo_item_invalid = {
                "name": "invalid_item",
                "text": "some test text",
                "due_date": "30-03-2020",
                "status": False,
            }

            todo_item_valid = {
                "name": "test_todo_item",
                "text": "some test text that needs to be done",
                "due_date": "30/03/2020",
                "status": False,
            }

            # create invalid
            rv = c.post(
                url + f"/{todo_list.get('name')}",
                data=json.dumps(todo_item_invalid),
                content_type="application/json",
            )
            self.assertEqual(rv.status_code, 400)

            expected_items = list()
            expected_items.append(copy.deepcopy(todo_item_valid))
            # create valid
            rv = c.post(
                url + f"/{todo_list.get('name')}",
                data=json.dumps(todo_item_valid),
                content_type="application/json",
            )
            self.assertEqual(rv.status_code, 201)

            # create one more
            todo_item_valid["name"] = "test_todo_item_2"
            expected_items.append(copy.deepcopy(todo_item_valid))
            rv = c.post(
                url + f"/{todo_list.get('name')}",
                data=json.dumps(todo_item_valid),
                content_type="application/json",
            )
            self.assertEqual(rv.status_code, 201)

            # get all items in this todo_list
            rv = c.get(url + f"/{todo_list.get('name')}")
            all_items = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(len(expected_items), len(all_items))
            expected_1, expected_2 = (
                expected_items[0].get("name"),
                expected_items[1].get("name"),
            )
            all_returned = [item.get("name") for item in all_items]
            self.assertIn(expected_1, all_returned)
            self.assertIn(expected_2, all_returned)

    def test__todo_item_get_update_delete_one(self):
        url = self.ROUTE_PREFIX + "/item"
        with self.client as c:
            todo_list = {"name": "test_list"}
            c.post(
                self.ROUTE_PREFIX + "/list",
                data=json.dumps(todo_list),
                content_type="application/json",
            )
            todo_items = [
                {
                    "name": "test_todo_item",
                    "text": "some test text that needs to be done",
                    "due_date": "30/03/2020",
                    "status": False,
                },
                {
                    "name": "test_todo_item2",
                    "text": "some other item that needs to be done",
                    "due_date": "30/03/2020",
                    "status": False,
                },
            ]
            for item in todo_items:
                c.post(
                    url + f"/{todo_list.get('name')}",
                    data=json.dumps(item),
                    content_type="application/json",
                )

            # get one
            rv = c.get(url + f"/{todo_list.get('name')}/{todo_items[0].get('name')}")
            self.assertEqual(rv.status_code, 200)
            returned = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(list(returned.keys())[0], todo_items[0].get("name"))

            # update one
            updated_item = {
                "text": "some test text that needs to be done very fast",
                "due_date": "30/03/2020",
                "status": True,
            }
            rv = c.put(
                url + f"/{todo_list.get('name')}/{todo_items[0].get('name')}",
                data=json.dumps(updated_item),
                content_type="application/json",
            )
            self.assertEqual(rv.status_code, 200)
            returned = json.loads(rv.data.decode("utf-8"))
            self.assertEqual(
                {
                    "success": f"todo_item={todo_items[0].get('name')} successfully updated"
                },
                returned,
            )

            # delete one
            rv = c.delete(url + f"/{todo_list.get('name')}/{todo_items[0].get('name')}")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                f"{todo_items[0].get('name')} deleted from {todo_list.get('name')}",
                rv.data.decode("utf-8"),
            )
