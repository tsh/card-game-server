# -*- coding: utf-8 -*-
import uuid
import json

from app.constants import Message
from app.exceptions import *


class Player(object):
    """
    Класс описывает модель игрока, и его взаимодействие с клиентом
    """
    def __init__(self, connection, name= "Nameless One"):
        """
        connection <WebSocketHandler> физическое соедениние с клиентом
        name <string> имя игрока
        """
        self.connection = connection
        self.name = name
        self.room = None    #комната в которой сейчас находится игрок

    def sendToPlayer(self, message):
        """
        Отправляет сообщение клиенту
        """
        self.connection.write_message(message)

    def notifyPlayer(self, messageType = None, description = None, message = None, data = None):
        """
        формирует стандартные сообщения на основании переданого типа. Если есть пояснения добавляит их как description
        """
        messageToSend = {}
        if description:
            messageToSend["description"] = description
        if message:
            messageToSend["message"] = message

        if messageType == Message.PlayerConnected:
            messageToSend["type"] = Message.PlayerConnected
            #data contains connected <Player> object.
            messageToSend["playerInfo"] = {"name": data.name}

        #no specific rule. Just send type.
        else:
            messageToSend["type"] =  messageType

        self.sendToPlayer(json.dumps(messageToSend))


    def sendWelcomeMessage(self):
        self.sendToPlayer(json.dumps({"type":"cardReceived","card":
                                                                    {"name":"elf","health":2, "attack":2}}))


class Room(object):
    """
    Игровая комната "внутри" которой происходит игра.
    """
    rooms = {}  #Список созданных комнат

    def __init__(self, player1, roomName=None):
        """
        Создает комнату с одним игроком.
        player1 <Player> игрок создавший комнату
        """
        self.id = str(uuid.uuid4())
        self.roomName = roomName
        self.player1 = player1
        self.player2 = None
        Room.rooms[self.id]=self #Добавить комнату в список созданных

    def destroyRoom(self):
        """Удаляет комнату, и информирует второго игрока"""
        if self.player2:
            self.player2.room = None
            self.player2.notifyPlayer(Message.RoomDestroyed)
        self.player1.room = None
        Room.rooms.pop(self.id, None)

    def playerDisconnected(self, player):
        #Отключившийся игрок создатель комнаты
        if self.player1 == player:
            self.destroyRoom()
        else:
            self.player1.sendToPlayer(Message.PlayerDisconnected)

    @classmethod
    def getListOfRooms(cls):
        mes = []
        for k in cls.rooms:
            roomData = {
                "id"    : cls.rooms[k].id,
                "name"  : cls.rooms[k].roomName,
                #Eсли игрок в комнате, вернуть имя.
                "player1": cls.rooms[k].player1.name if cls.rooms[k].player1 is not None else None,
                "player2": cls.rooms[k].player2.name if cls.rooms[k].player2 is not None else None
            }
            mes.append(roomData)
        return  mes

    def getRoomInfo(self):
        return {
                "id"    : self.id,
                "name"  : self.roomName,
                "player1": self.player1.name,
                "player2": self.player2.name
        }

    @classmethod
    def getRoomById(cls, id):
        return cls.rooms.get(id, None)

    def addPlayerToRoom(self, player):
        """
        Добавляет второго игрока в комнату.
        возращает True в случае успеха, False в случае если место игрока занято.
        """
        if self.player2 == None:
            self.player2 = player
            self.player1.notifyPlayer(Message.PlayerConnected, data=self.player2)
            return True
        else:
            return False

    def notifyAllPlayers(self, message):
        if self.player1:
            self.player1.sendToPlayer(message)
        if self.player2:
            self.player2.sendToPlayer(message)