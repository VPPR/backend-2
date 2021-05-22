from typing import Generic, List, Optional, TypeVar

from mongoengine import Document
from pydantic.main import BaseModel

Model = TypeVar("Model", bound=Document)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
GetAllSchema = TypeVar("GetAllSchema", bound=BaseModel)


class CRUDBase(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Model):
        self.model = model

    def get(self, id: str) -> Optional[Model]:
        return self.model.objects(id=id).first()

    def get_all(self, skip: int, limit: int) -> List[GetAllSchema]:
        return [f for f in self.model.objects().skip(skip).limit(limit)]

    def create(self, obj_in: CreateSchema) -> Model:
        object = self.model(**obj_in.dict())
        object.save()
        return object

    def update(self, model: Model, obj: UpdateSchema) -> Model:
        model.update(**obj.dict(exclude_none=True))
        return model.reload()

    def delete(self, model: Model) -> Model:
        model.delete()
        return model
