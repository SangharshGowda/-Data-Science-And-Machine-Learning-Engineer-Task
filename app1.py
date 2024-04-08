from fastapi import FastAPI
from pydantic import BaseModel
import subprocess


app = FastAPI()

from keras.models import load_model

model = load_model('model.h5')



class internalstatus(BaseModel):
    externalStatus: str  
@app.get('/')
def index():
    return {'message': 'Hello, Settyl'}

@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To my deployed environment': f'{name}'}


@app.post("/predict")
async def predict_internalstatus(data:internalstatus ):
    
    externalStatus = data.externalStatus

    
    predicted_class_index = model.predict([externalStatus])[0]

    
    class_labels = {
        0: 'Arrival',
        1: 'Departure',
        2: 'Empty Container Released',
        3: 'Empty Return',
        4: 'Gate In',
        5: 'Gate Out',
        6: 'In-transit',
        7: 'Inbound Terminal',
        8: 'Loaded on Vessel',
        9: 'Off Rail',
        10: 'On Rail',
        11: 'Outbound Terminal',
        12: 'Port In',
        13: 'Port Out',
        14: 'Unloaded on Vessel'
    }
   
    prediction = class_labels.get(predicted_class_index, "Unknown Class")

    
    return {"prediction": prediction}


command = ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]


process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the prediction API!"}
