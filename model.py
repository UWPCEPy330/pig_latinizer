import os

from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect

db = connect('sqlite:///my_database.db')

class ConvertedStrings(Model):
    code = CharField(max_length=255, unique=True)
    value = CharField(max_length=255)

    class Meta:
        database = db