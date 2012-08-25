#!/usr/bin/env python2
# coding: utf-8

import sys
import socket
import string
import time
import logging.handlers
import os

import libirc

HOST="irc.freenode.net"
PORT=6667
NICK="logbot"
IDENT="logbot"
REALNAME="logbot"
CHANS=["#Orz"]

os.environ["TZ"]="Asia/Shanghai"
time.tzset()

c=libirc.IRCConnection()
c.connect(HOST, PORT)
c.setnick(NICK)
c.setuser(IDENT, REALNAME)
for CHAN in CHANS:
    c.join(CHAN)
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)
hlog=logging.handlers.RotatingFileHandler("irclog.log", maxBytes=1048576, backupCount=3)
hlog.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger().addHandler(hlog)
logging.info(":: Start logging.")

quiting=False
while not quiting:
    try:
        if not c.sock:
            quiting=True
            time.sleep(10)
            logging.info(":: Restart logging.")
            os.execlp("python2", "python2", __file__)
            break
        raw=c.recvline(block=True)
        if raw:
            line=c.parse(line=raw)
            if line:
                if line["cmd"]=="PRIVMSG" and line["dest"]==NICK and line["msg"]==u"Get out of this channel!": # A small hack
                    logging.info(":: %s asked to leave." % line["nick"])
                    c.quit(u"%s asked to leave." % line["nick"])
                    quiting=True
                else:
                    logging.info(raw)
    except Exception as e:
        logging.info(":: Error: %s" % e)
    except socket.error as e:
        logging.info(":: Network error: %s" % e)
        c.quit("Network error.")
logging.info(":: Stop logging.")

# vim: et ft=python sts=4 sw=4 ts=4
