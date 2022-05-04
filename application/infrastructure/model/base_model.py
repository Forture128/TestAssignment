import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID


class BaseModelMixin(object):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    inserted_by = Column(String(length=500), default="Zymo")
    updated_by = Column(String(length=500), default="Zymo")
    is_deleted = Column(Boolean, default=False, nullable=False)
