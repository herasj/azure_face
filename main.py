import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import random
import string
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from string import Template
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

from dotenv import load_dotenv, find_dotenv
load_dotenv(override=True)

#Env variables
KEY = os.environ['FACE_KEY']
print("KEY: ",KEY)
ENDPOINT = os.environ['FACE_ENDPOINT']
print("ENDPOINT: ",ENDPOINT)

#Auth
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

#https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg
#https://www.euroresidentes.com/empresa/motivacion/wp-content/uploads/sites/7/2014/04/como-motivar-a-las-personas-euroresidentes.jpg

# Cargar imagen
single_face_image_url = 'https://i.ytimg.com/vi/dF_UadKIUzE/maxresdefault.jpg'
single_image_name = os.path.basename(single_face_image_url)

#Detectar caras
detected_faces = face_client.face.detect_with_url(url=single_face_image_url)

if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

# Rectangulo a dibujar
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Descargar img
response = requests.get(single_face_image_url)
img = Image.open(BytesIO(response.content))

# Por cada cara que se detecte se dibujará un cuadrado
print('Se dibuja un rectangulo sobre la cara detectada')
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')
randname = randomString(15)
print("Random: ",randname)

#Guardar imagen en la carpeta detected....
t = Template('./detected_faces/$name.jpg') #Path de guardado
path = t.substitute(name=randname) #Template string
img.save(path)