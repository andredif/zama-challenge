import asyncio
import logging
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Response, Depends, UploadFile
from fastapi.params import Body, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .exceptions import *
from . import DEFAULT_RESPONSE
from .schemas import FileUploaded, MerkleRoot
from .. import crud

from .dependencies import get_api_key, get_db


logger = logging.getLogger("uvicorn_app")

router = APIRouter(
    prefix="/api/v1",
    tags=["zama-challenge"],
    responses=DEFAULT_RESPONSE,
    dependencies=[Depends(get_api_key)]
)


@router.post(
    "/upload", response_model=FileUploaded,
    response_model_exclude_unset=True
    )
async def upload_file(
    uploaded_file: UploadFile,
    db: Session = Depends(get_db)
):
    """
    Send a new file to the system.

    - **File**: the file to be uploaded.

    """
    uploaded_file = crud.file.create(
        db=db, obj_in={}
    )
    return FileUploaded(uploaded_file)


@router.get(
    "/files/{identifier}", response_model=MerkleRoot,
    response_model_exclude_unset=True
    )
async def get_file_merkle_root(
    identifier: str = Path(..., title="Unique identifier for the requested file"),
):
    """
    Verify if the merkle root of the file on the server matches with the ones kept by the user.

    - **Identifier**: the unique file identifier in the systems.

    """
    ...