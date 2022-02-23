from xml.etree.ElementTree import tostring
from flask import Flask,request
from matplotlib.pyplot import get
import emotions_byImage
import base64

app = Flask(__name__)

@app.route('/',methods=['POST'])
def hello_world():
    img_data = b''
    #with open ("test.txt",'r') as fh:
    #    img_data = fh.read().encode('utf-8')
    img_data = request.json['message'].encode('utf-8')
        
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    ret = emotions_byImage.get_emotion_by_image('imageToSave.png')
    #print(request.json['message'])
    print(ret[0])
    return ret[0]

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')