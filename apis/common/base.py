from mongoengine import Document, DateTimeField
from bson import ObjectId
from datetime import date, datetime


class BaseDAO:
    id: ObjectId
    created_at: datetime
    updated_at: datetime


class BaseDocument(Document):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    meta = {'abstract': True}
