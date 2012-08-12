#!/usr/bin/python2
# coding: utf-8

import sys
import cgi

sys.stdout.write("<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\r\n</head>\r\n<body>\r\n<table style=\"white-space: nowrap; width: 100%\" cellpadding=\"0\" cellspacing=\"4\">\r\n")
line=sys.stdin.readline().rstrip("\n")
while line:
    try:
        time=line[:23]
        sraw=line[25:]
        if sraw.startswith(":: "):
            sys.stdout.write("<tr style=\"color: gray\"><td style=\"text-align: right\">%s</td><td colspan=\"2\"></td><td style=\"white-space: normal\">%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(sraw[3:])))
        else:
            raw=sraw.split(None, 3)
            if raw[0]!='PING':
                if raw[1]=="PRIVMSG":
                    dest=raw[2]
                    if dest.startswith("#"):
                        nick=raw[0].split("!", 1)[0][1:]
                        msg=raw[3][1:]
                        if msg.startswith("\001ACTION "):
                            msg=msg.strip("\001").lstrip("ACTION ")
                            nick="<b>* "+cgi.escape(nick)+"</b>"
                            style="; color: darkblue"
                        else:
                            nick=cgi.escape(nick)+":"
                            style=""
                        sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right%s\">%s</td><td style=\"white-space: normal\">%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), style, nick, cgi.escape(msg)))
                elif raw[1]=="JOIN":
                    nick, ident=raw[0].split("!", 1)
                    nick=nick[1:]
                    dest=raw[2]
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td><b>[<i>%s</i>]</b> 加入 %s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(ident), cgi.escape(dest)))
                elif raw[1]=="PART":
                    nick, ident=raw[0].split("!", 1)
                    nick=nick[1:]
                    dest=raw[2]
                    if len(raw)>=4:
                        desc=" <b>(%s)</b>" % cgi.escape(raw[3].lstrip(":").strip())
                    else:
                        desc=""
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td><b>[<i>%s</i>]</b> 离开 %s%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(ident), cgi.escape(dest), desc))
                elif raw[1]=="QUIT":
                    nick, ident=raw[0].split("!", 1)
                    nick=nick[1:]
                    if len(raw)>=2:
                        desc=" <b>(%s)</b>" % cgi.escape(sraw.split(None, 2)[2].lstrip(":").strip())
                    else:
                        desc=""
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\"><b>%s</b></td><td><b>[<i>%s</i>]</b> 退出%s</td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), desc))
                elif raw[1]=="NICK":
                    nick, ident=raw[0].split("!", 1)
                    nick=nick[1:]
                    newnick=sraw.split(None, 2)[2][1:]
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\"></td><td style=\"text-align: right\"><b>%s</b></td><td><b>[<i>%s</i>]</b> 更改昵称为 <b>%s</b></td></tr>\r\n" % (cgi.escape(time), cgi.escape(nick), cgi.escape(ident), cgi.escape(newnick)))
                elif raw[1]=="MODE":
                    nick=raw[0].split("!", 1)[0][1:]
                    dest=raw[2]
                    newmode=raw[3].lstrip(":").strip()
                    sys.stdout.write("<tr><td style=\"text-align: right\">%s</td><td style=\"text-align: left\">%s</td><td style=\"text-align: right\"><b>%s</b></td><td>设定模式 <b>(%s)</b></td></tr>\r\n" % (cgi.escape(time), cgi.escape(dest), cgi.escape(nick), cgi.escape(newmode)))
    except Exception as e:
        sys.stdout.write("<tr><td colspan=\"4\" style=\"color: red\">解析出错: %s</td></tr>\r\n" % cgi.escape(str(e)))
    line=sys.stdin.readline()
sys.stdout.write("</table>\r\n</body>\r\n</html>\r\n")

# vim: et ft=python sts=4 sw=4 ts=4
