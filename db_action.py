from dataclasses import dataclass
from sqlite3worker import Sqlite3Worker
from typing import Union 
import datetime


@dataclass
class SemaBox:
    id: Union[int, None] = None
    name: Union[str, None] = None
    ip: Union[str, None] = None
    connected: Union[bool, None] = None
    lastCheck: Union[datetime.datetime, None] = None
    version: Union[str, None] = None

    def dict(self) -> dict:
        """
        Transforme l'objet actuel en un dictionnaire JSON
        """
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'connected': self.connected,
            'lastCheck': self.lastCheck.strftime("%Y-%m-%d %H:%M:%S"),
            'version': self.version
        }

class SemaBoxDB:
    db: Sqlite3Worker


    def __init__(self, dbPath: str) -> None:
        self.db = Sqlite3Worker(dbPath)
        self.db.execute("CREATE TABLE IF NOT EXISTS semabox (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, connected INTEGER, lastCheck TEXT, version TEXT)")
        return 

    def addSemaBox(self, semabox: SemaBox) -> None: 
        """
        Add a semabox to the database
        """
        self.db.execute("INSERT INTO semabox (name, ip, connected, version) VALUES (?, ?, ?, ?)", (semabox.name, semabox.ip, semabox.connected, semabox.version))
        return
    
    def getAllSemaBox(self) -> list[SemaBox]:
        """
        get status of all semabox
        """
        result = self.db.execute("SELECT * FROM semabox")
        return [SemaBox(x[0], x[1], x[2], x[3], datetime.datetime.strptime(x[4], "%Y-%m-%d %H:%M:%S"), x[5]) for x in result]

    def getSemaBox(self, id: int) -> SemaBox:
        """
        get info about a particular semabox
        """
        result = self.db.execute("SELECT * FROM semabox WHERE id = ?", (id,))
        return SemaBox(result[0][0], result[0][1], result[0][2], result[0][3], datetime.datetime.strptime(result[0][4], "%Y-%m-%d %H:%M:%S"), result[0][5])

    def updateSemaBox(self, semabox: SemaBox) -> None:
        """
        update data of particular semabox
        """
        self.db.execute("UPDATE semabox SET name = ?, ip = ?, connected = ?, lastCheck = ?, version = ? WHERE id = ?", (semabox.name, semabox.ip, semabox.connected, semabox.lastCheck.strftime("%Y-%m-%d %H:%M:%S"), semabox.version, semabox.id))
        return

    def getAfter15mnSemabox(self) -> list[SemaBox]:
        """
        get semabox that have not been checked for more than 15 minutes
        """
        result = self.db.execute("SELECT * FROM semabox WHERE lastCheck < datetime('now', '-15 minutes')")
        return [SemaBox(x[0], x[1], x[2], x[3], datetime.datetime.strptime(x[4], "%Y-%m-%d %H:%M:%S"), x[5]) for x in result]