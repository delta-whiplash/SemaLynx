from flask import Flask, render_template, jsonify, request
import datetime

from .db_action import SemaBox, SemaBoxDB

db: SemaBoxDB = SemaBoxDB("semabox.db") # LA DB
liste_semabox = ["semabox1", "semabox2", "semabox3"]
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
    connected = bool(request.form['connected'])
    lastCheck = datetime.datetime.strptime(request.form['lastCheck'], "%Y-%m-%d %H:%M:%S")
    semabox = SemaBox(
        name=name, 
        ip=ip, 
        connected=connected, 
        lastCheck=lastCheck
    )
    db.addSemaBox(semabox)
    return jsonify({'result': 'success'})

@app.route('/api/manage-semabox/get/<semaboxID>', methods=['GET'])
def getSemabox(semaboxID: str):
    semabox = db.getSemaBox(int(semaboxID))
    return semabox.dict()


@app.route('/api/manage-semabox/getAll', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)