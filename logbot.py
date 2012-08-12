#!/usr/bin/env python2
# coding: utf-8

import sys
import socket
import string
import time
import logging.handlers
import os

HOST="irc.freenode.net"
PORT=6667
NICK="logbot"
IDENT="logbot"
REALNAME="logbot"
CHANS=["#Orz"]

os.environ["TZ"]="Asia/Shanghai"
time.tzset()

readbuffer=""
s=socket.socket()
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
for CHAN in CHANS:
    s.send("JOIN :%s\r\n" % CHAN)
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)
hlog=logging.handlers.RotatingFileHandler("irclog.log", maxBytes=10485760, backupCount=3)
hlog.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger().addHandler(hlog)
logging.info(":: Start logging.")

quiting=False
while not quiting:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()
    for line in temp:
        try:
            line=string.rstrip(line)
            sline=string.split(line)
            if sline[0]=="PING":
                s.send("PONG %s\r\n" % sline[1])
            else:
                logging.info(line)
                if sline[1]=="PRIVMSG":
                    rnick=sline[0][1:].split("!")[0]
                    if line.find(" PRIVMSG %s :" % NICK)!=-1:
                        if line.split(" PRIVMSG %s :" % NICK)[1]=="Get out of this channel!": # A small hack
                            s.send("QUIT :Client Quit\r\n")
                            quiting=True
                        else:
                            s.send("PRIVMSG %s :%s: 我不接受私信哦。\r\n" % (rnick, rnick))
        except Exception as e:
            logging.info(":: Error: %s" % e)
logging.info(":: Stop logging.")

# vim: et ft=python sts=4 sw=4 ts=4
