# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:

"""
import email

eml = [b'Received: from dashing08$163.com ( [61.141.136.15] ) by',
       b' ajax-webmail-wmsvr116 (Coremail) ; Mon, 9 Jan 2017 21:30:51 +0800 (CST)',
       b'X-Originating-IP: [61.141.136.15]', b'Date: Mon, 9 Jan 2017 21:30:51 +0800 (CST)',
       b'From: dashing08 <dashing08@163.com>', b'To: letsp2p@163.com', b'Subject: for python to download',
       b'X-Priority: 3', b'X-Mailer: Coremail Webmail Server Version SP_ntes V3.5 build',
       b' 20160729(86883.8884) Copyright (c) 2002-2017 www.mailtech.cn 163com',
       b'X-CM-CTRLDATA: T3FIwWZvb3Rlcl9odG09NDAwOjM4OA==', b'Content-Type: multipart/alternative; ',
       b'\tboundary="----=_Part_224835_593764436.1483968651532"', b'MIME-Version: 1.0',
       b'Message-ID: <48457a95.ea63.159836ca10c.Coremail.dashing08@163.com>', b'X-Coremail-Locale: zh_CN',
       b'X-CM-TRANSID:dMGowEBJ90GMkHNYNxS9AA--.11052W',
       b'X-CM-SenderInfo: xgdvxxdqjqmqqrwthudrp/xtbBURxaulaDsre+zAABsO',
       b'X-Coremail-Antispam: 1U5529EdanIXcx71UUUUU7vcSsGvfC2KfnxnUU==', b'',
       b'------=_Part_224835_593764436.1483968651532', b'Content-Type: text/plain; charset=GBK',
       b'Content-Transfer-Encoding: base64', b'',
       b'dGhpcyBpcyB3aGVyZSBjb250ZXh0IHN0YXJ0cy4gbm93IHNvbWUgY2hpbmVzZSBjaGFyYWN0ZXJz',
       b'IHdpbGwgYXBwZWFyLgrE47rDysC956OhCm5leHQgd2lsbCBjb21lIHNvbWUgaHRtbCBjb250ZXh0',
       b'LgpKVU1QIFRPIEJBSURVCmZvbnQgdmFyaWVzLi4uCgo=', b'------=_Part_224835_593764436.1483968651532',
       b'Content-Type: text/html; charset=GBK', b'Content-Transfer-Encoding: base64', b'',
       b'PGRpdiBzdHlsZT0ibGluZS1oZWlnaHQ6MS43O2NvbG9yOiMwMDAwMDA7Zm9udC1zaXplOjE0cHg7',
       b'Zm9udC1mYW1pbHk6QXJpYWwiPjxkaXY+dGhpcyBpcyB3aGVyZSBjb250ZXh0IHN0YXJ0cy4gbm93',
       b'IHNvbWUgY2hpbmVzZSBjaGFyYWN0ZXJzIHdpbGwgYXBwZWFyLjxicj7E47rDysC956OhPGJyPm5l',
       b'eHQgd2lsbCBjb21lIHNvbWUgaHRtbCBjb250ZXh0Ljxicj48YSBocmVmPSJodHRwOi8vd3d3LmJh',
       b'aWR1LmNvbSI+SlVNUCBUTyBCQUlEVTwvYT48YnI+PGk+PHU+Zm9udCB2YXJpZXM8L3U+PC9pPi4u',
       b'Ljxicj48YnI+PC9kaXY+PGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJtb3otZXh0ZW5zaW9u',
       b'Oi8vOWRlMTk3YjAtYmQ0ZC1lMzQ2LTk4MTQtMjUxMzM5OGRhMzFhL2J1aWxkL2luZGV4LmNzcyI+',
       b'PC9kaXY+PGJyPjxicj48c3BhbiB0aXRsZT0ibmV0ZWFzZWZvb3RlciI+PGRpdiBpZD0ibmV0ZWFz',
       b'ZV9tYWlsX2Zvb3RlciI+PGRpdiBzdHlsZT0iYm9yZGVyLXRvcDojQ0NDIDFweCBzb2xpZDtwYWRk',
       b'aW5nOjEwcHggNXB4O2ZvbnQtc2l6ZToxNXB4O2NvbG9yOiM3Nzc7bGluZS1oZWlnaHQ6MjJweCI+',
       b'PGEgaHJlZj0iaHR0cDovL3lvdS4xNjMuY29tL2l0ZW0vZGV0YWlsP2lkPTEwNDMwMTkmZnJvbT13',
       b'ZWJfZ2dfbWFpbF9qaWFvYmlhb183IiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9ImNvbG9yOiMzMzY2',
       b'RkY7dGV4dC1kZWNvcmF0aW9uOm5vbmUiPqG+zfjS19fU06p8MzDM7M7e08fNy7v1ob9NVUpJzay/',
       b'7sjVyr288tS8w/vGrLrQ0c/RobzbvfYyOdSqo6zC7cnPyOsmZ3Q7Jmd0OzwvYT4KICZuYnNwOyAm',
       b'bmJzcDs8L2Rpdj48L2Rpdj48L3NwYW4+', b'------=_Part_224835_593764436.1483968651532--']

eml = [b'Received: from letsp2p$163.com ( [183.14.29.105] ) by ajax-webmail-wmsvr138', b' (Coremail) ; Mon, 9 Jan 2017 23:06:33 +0800 (CST)', b'X-Originating-IP: [183.14.29.105]', b'Date: Mon, 9 Jan 2017 23:06:33 +0800 (CST)', b'From: letsp2p <letsp2p@163.com>', b'To: letsp2p@163.com', b'Subject: =?GBK?Q?for_python_using_=D6=D0=CE=C4writing?=', b'X-Priority: 3', b'X-Mailer: Coremail Webmail Server Version SP_ntes V3.5 build', b' 20160729(86883.8884) Copyright (c) 2002-2017 www.mailtech.cn 163com', b'X-CM-CTRLDATA: 00IZ5GZvb3Rlcl9odG09MjczOjQwMA==', b'Content-Type: multipart/alternative; ', b'\tboundary="----=_Part_145634_1881443682.1483974393390"', b'MIME-Version: 1.0', b'Message-ID: <4a1af506.986f.15983c43e2e.Coremail.letsp2p@163.com>', b'X-Coremail-Locale: zh_CN', b'X-CM-TRANSID:isGowEDpYUL6pnNYwgN8AA--.7081W', b'X-CM-SenderInfo: pohw21kss6il2tof0z/xtbBDgxa2VQG9VWkZQACsw', b'X-Coremail-Antispam: 1U5529EdanIXcx71UUUUU7vcSsGvfC2KfnxnUU==', b'', b'------=_Part_145634_1881443682.1483974393390', b'Content-Type: text/plain; charset=GBK', b'Content-Transfer-Encoding: base64', b'', b'Q2hpbmVzZSBiZWdpbnMgYXMgZm9sbG93czoKztLRp8+wUHl0aG9uwb249tTCwcujrLfHs6PT0NCn', b'wsqhowq087zStry63M+yu7bV4sPFseCzzNPv0dQKdGhhbmtzLgo=', b'------=_Part_145634_1881443682.1483974393390', b'Content-Type: text/html; charset=GBK', b'Content-Transfer-Encoding: base64', b'', b'PGRpdiBzdHlsZT0ibGluZS1oZWlnaHQ6MS43O2NvbG9yOiMwMDAwMDA7Zm9udC1zaXplOjE0cHg7', b'Zm9udC1mYW1pbHk6QXJpYWwiPjxkaXY+Q2hpbmVzZSBiZWdpbnMgYXMgZm9sbG93czo8YnI+ztLR', b'p8+wUHl0aG9uwb249tTCwcujrLfHs6PT0NCnwsqhozxicj6087zStry63M+yu7bV4sPFseCzzNPv', b'0dQ8YnI+dGhhbmtzLjxicj48L2Rpdj48bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Im1vei1l', b'eHRlbnNpb246Ly85ZGUxOTdiMC1iZDRkLWUzNDYtOTgxNC0yNTEzMzk4ZGEzMWEvYnVpbGQvaW5k', b'ZXguY3NzIj48L2Rpdj48YnI+PGJyPjxzcGFuIHRpdGxlPSJuZXRlYXNlZm9vdGVyIj48ZGl2IGlk', b'PSJuZXRlYXNlX21haWxfZm9vdGVyIj48ZGl2IHN0eWxlPSJib3JkZXItdG9wOiNDQ0MgMXB4IHNv', b'bGlkO3BhZGRpbmc6MTBweCA1cHg7Zm9udC1zaXplOjE1cHg7Y29sb3I6Izc3NztsaW5lLWhlaWdo', b'dDoyMnB4Ij48YSBocmVmPSJodHRwOi8veW91LjE2My5jb20vaXRlbS9kZXRhaWw/aWQ9MTExMzAy', b'MSZmcm9tPXdlYl9nZ19tYWlsX2ppYW9iaWFvXzYiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0iY29s', b'b3I6IzMzNjZGRjt0ZXh0LWRlY29yYXRpb246bm9uZSI+ob65/cTqy83A8crX0aGhvyZsdDvRz9Gh', b'zNi5qSZndDvN+NLXzrbR69btyOLA8ca3v6jP3sG/t6LK26Oswu3Jz8fA0ru33SZndDsmZ3Q7PCEt', b'LdHP0aHM2LmpLS0+PC9hPgogJm5ic3A7ICZuYnNwOzwvZGl2PjwvZGl2Pjwvc3Bhbj4=', b'------=_Part_145634_1881443682.1483974393390--']
eml = b'\n'.join(eml)  # 拼接bytes
# 解析
msgb = email.message_from_bytes(eml)  # email.message.Message对象
print(msgb)  # 会把内容print出来，而不是对象名称
print(type(msgb))
# help(email.message_from_bytes)
subject = msgb.get('subject')
print('raw-subject:', subject)  # 已经是字符串了
h = email.header.Header(subject)
print('header:',type(h))
dh = email.header.decode_header(h)
print('decoded-header:',dh)  # [(string, charset)]
print(dh[0][0].decode())
