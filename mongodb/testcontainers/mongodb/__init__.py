#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
from pymongo import MongoClient
from testcontainers.core.generic import DbContainer
from testcontainers.core.waiting_utils import wait_container_is_ready


class MongoDbContainer(DbContainer):
    """
    Mongo document-based database container.

    Example:

        .. doctest::

            >>> from testcontainers.mongodb import MongoDbContainer

            >>> with MongoDbContainer("mongo:latest") as mongo:
            ...    db = mongo.get_connection_client().test
            ...    # Insert a database entry
            ...    result = db.restaurants.insert_one(
            ...        {
            ...            "address": {
            ...                "street": "2 Avenue",
            ...                "zipcode": "10075",
            ...                "building": "1480",
            ...                "coord": [-73.9557413, 40.7720266]
            ...            },
            ...            "borough": "Manhattan",
            ...            "cuisine": "Italian",
            ...            "name": "Vella",
            ...            "restaurant_id": "41704620"
            ...        }
            ...    )
            ...    # Find the restaurant document
            ...    cursor = db.restaurants.find({"borough": "Manhattan"})
    """
    MONGO_INITDB_ROOT_USERNAME = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "test")
    MONGO_INITDB_ROOT_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "test")
    MONGO_DB = os.environ.get("MONGO_DB", "test")

    def __init__(self, image: str = "mongo:latest", port_to_expose: int = 27017, **kwargs) -> None:
        super(MongoDbContainer, self).__init__(image=image, **kwargs)
        self.command = "mongo"
        self.port_to_expose = port_to_expose
        self.with_exposed_ports(self.port_to_expose)

    def _configure(self) -> None:
        self.with_env("MONGO_INITDB_ROOT_USERNAME", self.MONGO_INITDB_ROOT_USERNAME)
        self.with_env("MONGO_INITDB_ROOT_PASSWORD", self.MONGO_INITDB_ROOT_PASSWORD)
        self.with_env("MONGO_DB", self.MONGO_DB)

    def get_connection_url(self) -> str:
        return self._create_connection_url(
            dialect='mongodb',
            username=self.MONGO_INITDB_ROOT_USERNAME,
            password=self.MONGO_INITDB_ROOT_PASSWORD,
            port=self.port_to_expose,
        )

    @wait_container_is_ready()
    def _connect(self) -> MongoClient:
        return MongoClient(self.get_connection_url())

    def get_connection_client(self) -> MongoClient:
        return self._connect()
