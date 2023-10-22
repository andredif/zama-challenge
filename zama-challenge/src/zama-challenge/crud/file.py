from typing import Any, Dict, Optional,List, Union

from sqlalchemy.orm import Session

from ..models.models import  File
from ..schemas import FileCreate, FileUpdate

from .. import crud
from .base import CRUDBase, ModelType


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    def create(self, db: Session, *, obj_in: FileCreate) -> File:
        file= super().create(db, obj_in=obj_in)
        return file


file = CRUDFile(File)
