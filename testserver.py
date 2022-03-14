from flask import Flask, request

app=Flask(__name__)

@app.route('/test',methods=['POST'])
def test():
    print(request.json)
    return "test"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)