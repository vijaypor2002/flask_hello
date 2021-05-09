from flask import Flask,request,jsonify
from tensorflow.keras.models import load_model
import cv2
from database import search
import numpy as np

model = load_model('my_model')

def preprocessing_image(data):
    data = cv2.cvtColor(data,cv2.COLOR_BGR2GRAY)
    data = data.reshape(1,28,28)
    return data

def prediction(data):
    value = model.predict(data)
    pred = np.argmax(value.tolist()[0])    
    return pred

app = Flask(__name__)
@app.route('/',methods=['GET'])
def index():
    return jsonify({'message' : 'Hello, World!'})

@app.route('/predict',methods=['GET','POST'])
def predict():
    data = request.get_json()
    ind = data['secure_num']
    image,stat = search(ind,'trail')
    if(stat==0):
        return jsonify({'data': 'secure num did not match any image'})
    else:
        image = preprocessing_image(image)
        pred = prediction(image)
        return jsonify({'data': int(pred)})

if __name__ == "__main__":
    app.run(debug=True)
