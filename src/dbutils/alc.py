
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

def idc():
   return Column(Integer, primary_key=True) #_idc
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
def foreignidc(key):
   return Column(Integer, ForeignKey(key))
def enumc(*kwopts):
	return Column(Enum(*kwopts))


