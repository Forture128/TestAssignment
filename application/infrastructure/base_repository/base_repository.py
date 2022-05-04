from datetime import datetime
from typing import Optional, Type

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session, aliased, Query

from application.dependencies.database import Base, get_db
from application.infrastructure.model.base_model import BaseModelMixin


class BaseRepo:
    model: BaseModelMixin

    def __int__(self, db: Session = Depends(get_db)):
        self.db = db

    def query(self, *filters):
        _filter = [self.model.is_deleted == False, *filters]
        return self.db.query(self.model).filter(*_filter)

    def count(self, query: Query, model: Optional[Type[BaseModelMixin]] = None):
        if model is None:
            model = self.model
        q = aliased(model, query.subquery())
        return self.db.query(func.count(distinct(q.id))).scalar()

    def paginate(self, query: Query,
                 page: int = 0,
                 size: Optional[int] = None,
                 model: Optional[Type[BaseModelMixin]] = None,
                 count_only: Optional[bool] = False
                 ):
        if count_only:
            return self.count(query, model)
        items = query.all()[page * size:(page + 1) * size] if size is not None else query.all()
        items = jsonable_encoder(items)
        return self.count(query, model), items

    def get_by_id(self, id: str):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def add(self, instance: Base):
        self.db.add(instance)
        self.db.commit()
        return instance

    def update(self, id: str, instance: BaseModelMixin):
        updated: BaseModelMixin = self.query(self.model.id == id).one_or_none()
        keys = [i.name for i in instance.__table__.columns]
        need_commit = False
        if updated is not None:
            for key in keys:
                if getattr(instance, key) is not None:
                    need_commit = True
                    setattr(updated, key, getattr(instance, key))
            if need_commit:
                if instance.updated_at is None and 'updated_at' in keys:
                    updated.updated_at = datetime.now()
                self.db.commit()
        return updated

    def delete(self, id: str):
        exist = self.query(self.model.id == id).one_or_none()

        if exist is not None:
            exist.is_deleted = True
            self.db.commit()

        return exist

    def apply_sort(self):
        pass
