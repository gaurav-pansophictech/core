import uuid
from typing import Any, Dict, Type, List, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

DataObject = Dict[str, Any]


def to_dict(obj) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DBInterface:
    """
    DBInterface is an abstract class that defines the methods for interacting with a database.
    This class provides a blueprint for defining the methods for adding, updating and retrieving data from a database.
    The concrete implementations of this class should define the actual database operations.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def read_by_id(self, id: str) -> DataObject:
        item = await self.collection.find_one({"_id": ObjectId(id)})
        return item

    async def create(self, data: DataObject) -> DataObject:
        result = await self.collection.insert_one(data)
        return result

    async def get_single_item_by_filters(self, fields: dict) -> Any:
        item = await self.collection.find_one(fields)
        return item

    async def get_multiple_items_by_filters(self, fields: dict) -> Any:
        items = []
        async for field in self.collection.find(fields):
            field.pop("_id")
            items.append(field)
        return items

    async def create_with_uuid(self, data: DataObject) -> DataObject:
        data.update({"id": str(uuid.uuid4())})
        result = await self.collection.insert_one(data)
        data = await self.collection.find_one({"_id": result.inserted_id})
        return data
