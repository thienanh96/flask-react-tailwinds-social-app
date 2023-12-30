from mongoengine import Document, DateTimeField
from bson import ObjectId
from datetime import date


class BaseDAO:
    id: ObjectId
    created_at: date
    updated_at: date


class BaseDocument(Document):
    created_at: DateTimeField
    updated_at: DateTimeField

    meta = {'abstract': True}
