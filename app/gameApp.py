import os

import tornado.web

from handlers.IndexHandler import IndexHandler
from handlers.WebSocketGameHandler import WebSocketGameHandler


class SoAGameServer(tornado.web.Application):
    def __init__(self):
         handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketGameHandler),
        ]
         settings={
            "template_path" : os.path.join(os.path.dirname(__file__), "..", "webApp", "templates"),
            "static_path" : os.path.join(os.path.dirname(__file__), "..", "webApp", "static"),
         }
         tornado.web.Application.__init__(self, handlers, debug=True, **settings)
