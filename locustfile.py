import base64

from locust import HttpUser, TaskSet, task
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)
class WebTasks(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.verify = False

    @task
    def load(self):
        base64string = base64.encodebytes(('%s:%s' % ('vahirwad', 'varad')).encode('utf8')).decode('utf8').replace('\n', '')

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class Web(HttpUser):
    tasks    = [WebTasks]
    min_wait = 0
    max_wait = 0
