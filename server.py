#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from app.gameApp import SoAGameServer

define("port", default=8000, help="run on the given port", type=int)
define("log", default=30, help="Set logging level. How detailed logging messages will be: 10 - DEBUG, 20 - INFO,"
                               "30 - WARNING, 40 - ERROR, 50 - CRITICAL ")

message = """------------SOA gameServer--------------

port: {0}
log level: {1}

----

"""

if __name__ == "__main__":
    tornado.options.parse_command_line()
    l = logging.getLogger()
    l.setLevel(options.log)
    #Tornado config
    soaApp = SoAGameServer()
    http_server = tornado.httpserver.HTTPServer(soaApp)
    http_server.listen(options.port)
    print message.format(options.port, logging.getLogger().getEffectiveLevel())
    tornado.ioloop.IOLoop.instance().start()

