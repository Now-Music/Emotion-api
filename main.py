from xml.etree.ElementTree import tostring
from flask import Flask,request,jsonify
from matplotlib.pyplot import get
import emotions_byImage
import base64
import binascii

app = Flask(__name__)

@app.route('/',methods=['POST'])
def hello_world():
    img_data = b''
    #with open ("test.txt",'r') as fh:
    #    img_data = fh.read().encode('utf-8')
    img_data = request.json['message'].encode('utf-8')
    
    try: 
        weather_data = request.json['weather']
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))
        ret = emotions_byImage.get_emotion_by_image('imageToSave.png')
        return jsonify({
            "message" : f"{ret[0]} {weather_data}" 
        })
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


    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')