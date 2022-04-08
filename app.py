from flask import Flask,request,jsonify
import emotions_byImage
import base64
import binascii
import requests
import json
import config

app = Flask(__name__)


@app.route('/',methods=['POST'])
def root():
    #img_data = b''
    #with open ("test.txt",'r') as fh:
    #    img_data = fh.read().encode('utf-8')
    params = request.json['data'][0]
    img_data = params['picture_base64'].encode('utf-8')
    try: 
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))
        ret = emotions_byImage.get_emotion_by_image('imageToSave.png')
        datas = {
            "weather" : params['weather'],
            "month":params['month'],
            "emotion" : ret[0],
            "state": params['state'],
            "genres": params['genres'],
            "user_age":params['user_age'] 
        }
        print(datas)
        response = requests.post(config.URL1,data = json.dumps(datas))
        print(response.json())
        if response.status_code==200:
            print("back success")
            return response.json()
        else:
            return "error"

    except KeyError:
        print(KeyError)
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