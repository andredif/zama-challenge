from doctest import Example
from typing import List, Optional, Text
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator


class MerkleRoot(BaseModel):
    merkle_root: str

class FileUploaded(MerkleRoot):
    p_key: str

