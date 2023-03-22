from flask import Flask, render_template, jsonify, request
import datetime
import time
import requests
import threading
from db_action import SemaBox, SemaBoxDB

db: SemaBoxDB = SemaBoxDB("semalynx.db") # LA DB

app = Flask(__name__)
# default page
@app.route('/')
def home():
    return render_template('index.html')




############## API ##############
@app.route('/api/manage-semabox/add', methods=['POST'])
def addSemabox():
    name = request.form['name']
    ip = request.form['ip']
    version = request.form['version']
    semabox = SemaBox(
        name=name, 
        ip=ip,
        connected=1,
        version=version
    )
    db.addSemaBox(semabox)
    return jsonify({'result': 'success'})

@app.route('/api/manage-semabox/get/<semaboxID>', methods=['GET'])
def getSemabox(semaboxID: str):
    semabox = db.getSemaBox(int(semaboxID))
    return semabox.dict()


@app.route('/api/manage-semabox/getAll', methods=['GET'])
def getAllSemabox():
    semaboxes = db.getAllSemaBox()
    return [x.dict() for x in semaboxes] # Transforme la liste d'objet en liste de dictionnaire

@app.route('/api/manage-semabox/update', methods=['POST'])
def updateSemabox():
    id = request.form['id']
    name = request.form['name']
    ip = request.form['ip']
    connected = bool(request.form['connected'])
    lastCheck = datetime.datetime.strptime(request.form['lastCheck'], "%Y-%m-%d %H:%M:%S")
    semabox = SemaBox(
        id=int(id),
        name=name, 
        ip=ip, 
        connected=connected, 
        lastCheck=lastCheck
    )
    db.updateSemaBox(semabox)
    return jsonify({'result': 'success'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify('OK')

def check_if_still_connected():
    while True :
        for semabox in db.getAfter15mnSemabox():
            print("Check semabox: "+semabox.name)
            
            response = requests.get("http://"+semabox.ip+":5000/version")
            try:
                response.status_code == 200
                semabox.connected = 1
                if semabox.version != response.text:
                    semabox.version = response.text
            except:
                semabox.connected = 0
            
            db.updateSemaBox(semabox)

        time.sleep(15*60)

if __name__ == '__main__':
    # Check if semabox is still connected
    threading.Thread(target=check_if_still_connected).start()
    app.run(debug=True,host='0.0.0.0', port=5000)
    
   



