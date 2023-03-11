from flask import Flask, render_template, jsonify, request
import datetime
import schedule
import time
import requests

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



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
    
@app.before_first_request
def activate_job():
    def run_job():
        for semabox in db.getAfter15mnSemabox():
            response = requests.get("http://"+semabox.ip+":5000/health")
            if response.status_code == 200:
                semabox.connected = 1
            else:
                semabox.connected = 0
            db.updateSemaBox(semabox)

    schedule.every(15).minutes.do(run_job)
    
    # Start the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)

