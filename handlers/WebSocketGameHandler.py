# -*- coding: utf-8 -*-
import logging
import json

import tornado.websocket

from app.GlobalManager import GlobalManager
from app.GameObjects import Room
from app.constants import Message
from app.exceptions import *

class WebSocketGameHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        GlobalManager.newPlayerConnected(self)

    def on_message(self, message):
        logging.warning("Message Received: "+message)
        messageCode = None
        try:
            parsedMessage = json.loads(message)
            messageCode = parsedMessage.get('type', None)
        except AttributeError:
            logging.error("wsHandler on_message AttributeError. Message: "+message)
            self.write_message(json.dumps({"type":Message.CriticalError,
                                           "description":"JSON AttributeError.", "message":message}))
        except ValueError:
            logging.error("wsHandler on_message Val error: "+message)

        #Choose action:

        if messageCode == Message.GetCard:
            self.write_message(json.dumps({"type":"cardReceived","card":
                                                                    {"name":"Stormtrooper","health":52, "attack":72}}))

        #------ROOM ACTION------
        elif messageCode == Message.GetListOfRoom:
            self.write_message(json.dumps({"type":Message.ListOfRooms,"rooms": Room.getListOfRooms()}))

        elif messageCode == Message.CreateRoom:
            #Возвращает id комнаты, или сообщает что игрок уже в другой комнате.
            roomName = parsedMessage.get("name", None)
            try:
                roomId = GlobalManager.createRoom(self, roomName)
            except PlayerException as e:
                self.write_message(json.dumps({"type":Message.Error,"description": e.value}))
                logging.warning("WShandler createRoom" + str(e.value))
            else:
                self.write_message(json.dumps({"type":Message.RoomCreated,"id": roomId}))

        elif messageCode == Message.ConnectToRoom:
            roomInfo = GlobalManager.connectToRoom(self, parsedMessage)
            self.write_message(json.dumps({"type":Message.ConnectedToRoom,"roomInfo": json.dumps(roomInfo) }))

        elif messageCode == Message.LeaveRoom:
            GlobalManager.playerLeavesTheRoom(self)

        elif messageCode == Message.DestroyRoom:
            GlobalManager.destroyRoom(self)

        elif messageCode == Message.ChatMessage:
            GlobalManager.notifyAllPlayersInRoom(self, parsedMessage)

        #-------PLAYER ACTION-----------
        elif messageCode == Message.SetName:
            GlobalManager.setPlayerName(self, parsedMessage)




    def on_close(self):
        GlobalManager.playerDisconnected(self)