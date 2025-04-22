# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Test(db.Model):

    __tablename__ = 'Test'

    id = db.Column(db.Integer, primary_key=True)

    #__Test_FIELDS__
    test = db.Column(db.Text, nullable=True)
    test2 = db.Column(db.Integer, nullable=True)

    #__Test_FIELDS__END

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)


class Test2(db.Model):

    __tablename__ = 'Test2'

    id = db.Column(db.Integer, primary_key=True)

    #__Test2_FIELDS__
    test1 = db.Column(db.String(255),  nullable=True)
    test2 = db.Column(db.Boolean, nullable=True)
    test3 = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Test2_FIELDS__END

    def __init__(self, **kwargs):
        super(Test2, self).__init__(**kwargs)



#__MODELS__END
