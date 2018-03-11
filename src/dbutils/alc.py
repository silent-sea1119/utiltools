
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey


_boolc = Column(Boolean)
_intc = Column(Integer)
_floatc = Column(Float)
_idc = Column(Integer, primary_key=True)
_textc = Column(Text)
_datetimetc = Column(DateTime)

IS_SQLITE = False

def idc(autoincrement=True):
   if not IS_SQLITE:
      return Column(Integer, primary_key=True) #_idc
   return Column(Integer, primary_key=True, autoincrement=autoincrement)
   #return Column(Integer, sqlite_autoincrement=True, autoincrement=False, unique=True, index=True) #buggy bastard

def boolc():
   return Column(Boolean) #_boolc
def intc():
   return Column(Integer) #_intc
def floatc():
   return Column(Float) #_floatc
def textc():
   return Column(Text) #_textc
def stringc(length=None):
   return Column(String(length=length))
def datetimec():
   return Column(DateTime) #_datetimec
def foreignidc(key, primary_key=False):
   return Column(Integer, ForeignKey(key), primary_key=primary_key)
def enumc(*kwopts):
   return Column(Enum(*kwopts))

def pyenumc(pyenum): #https://stackoverflow.com/questions/2676133/best-way-to-do-enum-in-sqlalchemy
   return Column(Enum(pyenum))

def foreign_id_c(string, primary_key=True):
   return Column(Integer, ForeignKey(string), primary_key=primary_key)


