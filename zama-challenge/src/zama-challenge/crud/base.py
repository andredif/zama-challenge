from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.database import Base
from ..exceptions import NotFoundException


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_or_404(self, db: Session, id: Any) -> Optional[ModelType]:
        db_istance = db.query(self.model).filter(self.model.id == id).first()
        if not db_istance:
            raise NotFoundException(self.model.__tablename__)
        return db_istance

    def get_multi(
        self, db: Session, *, ids: List[Any]
    ) -> List[ModelType]:
        return [self.get(db, id) for id in ids]

    def get_all(self, db: Session) -> Optional[List[ModelType]]:
        return db.query(self.model).all()

    def get_by_data(self, db:Session, *, data: Dict[str,str]) -> Optional[List[ModelType]]:
        return db.query(self.model).filter_by(**data).all()

    def get_by_data_kwargs(self, db: Session, **kwargs) -> Optional[List[ModelType]]:
        return self.get_by_data(db=db, data=kwargs)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush([db_obj])
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.flush()
        return obj

    def remove_obj(self, db:Session, *, obj: ModelType) -> ModelType:
        db.delete(obj)
        db.flush()
        return obj

    def remove_multi(self, db: Session, *, ids: List[Any]
    ) -> List[ModelType]:
        return [self.remove(db, id=id) for id in ids]
