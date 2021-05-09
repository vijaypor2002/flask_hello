import requests
import cv2
import mysql.connector
import time
import base64
from PIL import Image
import io
import numpy
"""
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="vijay1234",
    database="testdb"
    )
"""
mydb = mysql.connector.connect(
    host="brloanahxtcslcmfwhto-mysql.services.clever-cloud.com",
    user="uxw10c85ggpbahsb",
    passwd="jjoMTYaOhcOJjG2WOEzD",
    database="brloanahxtcslcmfwhto"
    )


def create_table(x):
    cursor = mydb.cursor()
    sql = """CREATE TABLE {} (secure INT, image LONGBLOB)""".format(x)
    cursor.execute(sql)

def delete_table(x):
    cursor = mydb.cursor()
    sql = "DROP TABLE {}".format(x)
    cursor.execute(sql)
    
def insert_table(path,x):
    cursor = mydb.cursor()
    file = open(path,'rb').read()
    file = base64.b64encode(file)
    args = (1, file)
    query = 'INSERT INTO {} VALUES(%s, %s)'.format(x)
    cursor.execute(query,args)
    mydb.commit()

def search(value,x):
    cursor = mydb.cursor()
    query = 'SELECT image FROM {} WHERE secure={}'.format(x,value)
    cursor.execute(query)
    data = cursor.fetchall()
    stat=1
    if(len(data)==0):
        stat=0
        return value,stat
    else:
        image = data[0][0]
        binary_data = base64.b64decode(image)
        image = Image.open(io.BytesIO(binary_data))
        opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        return opencvImage,stat


