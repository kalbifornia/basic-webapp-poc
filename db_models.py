#db_models.py
from sqlalchemy import Column,Integer,String,Boolean,create_engine,ForeignKey,UniqueConstraint
from sqlalchemy.orm import (relationship, backref)
from app import db  #Note: This imports from the main "app" module, and the app module imports from this.

#MiddlewareApp and MiddlewareServer have a M:M relationship. One app can run on 0-to-many servers, and one server can run 0-to-many apps.
class MiddlewareApp(db.Model):
    __tablename__ = "middlewareapp"
    id = Column("id",Integer,primary_key=True)
    name = Column("name",String(30),unique=True)
    description = Column("description",String(200))
    app_servers = relationship("MiddlewareAppServer", order_by = "MiddlewareAppServer.id", back_populates = "app")

class MiddlewareServer(db.Model):
    __tablename__ = "middlewareserver"
    id = Column("id",Integer,primary_key=True)
    name = Column("name",String(30),unique=True)
    is_windows = Column("is_windows",Boolean)
    server_apps = relationship("MiddlewareAppServer", order_by="MiddlewareAppServer.id", back_populates = "server")

class MiddlewareAppServer(db.Model):
    __tablename__ = "middlewareappserver"
    id = Column("id",Integer,primary_key=True)
    app_id = Column("app_id",Integer,ForeignKey("middlewareapp.id"))
    server_id = Column("server_id",Integer,ForeignKey("middlewareserver.id"))
    app = relationship("MiddlewareApp", back_populates="app_servers")
    server = relationship("MiddlewareServer", back_populates="server_apps")
    __table_args__ = (UniqueConstraint("app_id","server_id",name="UniqueAppServer"),)

db.create_all() #This will actually create the database tables (if they don't already exist) for the model classes above which are tied to db (db defined and configured in "app" module)
