#!/usr/bin/python3
#MYSQL_USER=root MYSQL_PWD=root MYSQL_HOST=localhost MYSQL_DB=tomodachi_db
from models import *
from models.interest import Interest
name = {"name":"Bleach"}
inte = Interest(**name)
print(inte.to_dict())
storage.new(inte)
storage.save()