from xml.etree.ElementTree import tostring
from flask import Flask,request,jsonify
from matplotlib.pyplot import get
import emotions_byImage
import base64
import binascii
import requests
import json

url = "http://192.168.0.14:8000"
url2 ="http://192.168.0.11:8080"

app = Flask(__name__)


@app.route('/',methods=['POST'])
def root():
    #img_data = b''
    #with open ("test.txt",'r') as fh:
    #    img_data = fh.read().encode('utf-8')
    img_data = request.json['picture_base64'].encode('utf-8')
    try: 
        weather_data = request.json['weather']
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))
        ret = emotions_byImage.get_emotion_by_image('imageToSave.png')
        datas = {
            "weather" : request.json['weather'],
            "month":request.json['month'],
            "emotion" : ret[0],
            "state": request.json['state'],
            "genres": request.json['genres'],
            "user_age":request.json['user_age'] 
        }
        print(datas)
        response = requests.post(url,data = json.dumps(datas))
        if response.status_code==200:
            requests.post(url2,data = response.json)
            return "success"
        else:
            return "error"

    except KeyError:
        return jsonify({
            "status":202,
            "error" : "Accept",
            "message" : "No Weather Data",
        })
    
    except IndexError:
         return jsonify({
            "status":202,
            "error" : "Accept",
            "message" : "No face in Image",
        })

    except binascii.Error:
        return jsonify({
            "status":202,
            "error" : "Accept",
            "message" : "Wrong Base64",
        })


@app.route('/back',methods=['POST'])
def back():
    response = requests.post('http://192.168.0.2:5001/test',data=request.json['weather'])
    if response.status_code==200: 
        return "success"
    else:
        return "error"
    



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')