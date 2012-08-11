#!/usr/bin/python2
# coding: utf-8

import sys
import cgi

sys.stdout.write("<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\r\n</head>\r\n<body>\r\n<table style=\"white-space: nowrap; width: 100%\" cellpadding=\"0\" cellspacing=\"4\">\r\n")
line=sys.stdin.readline()
while line:
    try:
        time=line[:24]
        sraw=line[25:]
        raw=sraw.split(None, 3)
        if raw[0]!='PING':
            if raw[1]=="PRIVMSG":
                dest=raw[2]
                if dest.startswith("#"):
                    nick=raw[0].split("!", 1)[0][1:]
                    msg=raw[3][1:]
                    if msg.startswith("\001ACTION "):
                        msg=msg.strip("\001").lstrip("ACTION ")
                        nick="* "+nick
                    else:
                        nick=nick+":"
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\">%s</td><td style=\"white-space: normal\">%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(msg)))
            elif raw[1]=="JOIN":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                dest=raw[2]
                sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\">%s</td><td>(%s) 加入 %s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(ident), cgi.escape(dest)))
            elif raw[1]=="PART":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                dest=raw[2]
                if len(raw)>=4:
                    desc=": %s" % raw[3]
                else:
                    desc=""
                sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\">%s</td><td>(%s) 离开 %s%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(ident), cgi.escape(dest), cgi.escape(desc)))
            elif raw[1]=="QUIT":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                if len(raw)>=2:
                    desc=": %s" % sraw.split(None, 2)[2][1:]
                else:
                    desc=""
                sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\">%s</td><td>(%s) 退出%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), cgi.escape(desc)))
            elif raw[1]=="NICK":
                nick, ident=raw[0].split("!", 1)
                nick=nick[1:]
                newnick=sraw.split(None, 2)[2][1:]
                sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\">%s</td><td>(%s) 更改昵称为 %s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), cgi.escape(newnick)))
    except Exception as e:
        sys.stdout.write("<tr><td colspan=\"4\">解析出错: %s</td></tr>\r\n" % cgi.escape(str(e)))
    line=sys.stdin.readline()
sys.stdout.write("</table>\r\n</body>\r\n</html>\r\n")

# vim: et ft=python sts=4 sw=4 ts=4