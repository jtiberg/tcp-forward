# tcp-forward
Tcp forward application written in Python3

It's meant as a tool for developers or others that wants to forward a tcp port.

Although you could use iptables+tcpdump to achieve the same function, that would require root access and would be a little more cumbersome IMHO.


## Requirements
Python 3.5 - no libraries

## Usage:
    $ ./fwd.py
    SYNTAX: fwd.py <local port> <remove host> <remote port> |-v for verbose mode|

### Example (used with 'curl localhost:1234')
    $ ./fwd.py 1234 google.com 80 -v
    2020-10-14 09:16:32 INFO	Forwarding 1234 -> google.com:80
    2020-10-14 09:16:32 INFO	Note: X> means data flowing to remote in connection with id X. X< means data from remote
    2020-10-14 09:16:36 INFO	1	Connection from ('127.0.0.1', 59796)
    2020-10-14 09:16:36 INFO	1>	78 bytes
    2020-10-14 09:16:36 DEBUG	1>	b'GET / HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\n\r\n'
    2020-10-14 09:16:36 INFO	1<	1024 bytes
    2020-10-14 09:16:36 DEBUG	1<	b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nReferrer-Policy: no-referrer\r\nContent-Length: 1561\r\nDate: Wed, 14 Oct 2020 07:16:36 GMT\r\n\r\n<!DOCTYPE html>\n<html lang=en>\n  <meta charset=utf-8>\n  <meta name=viewport content="initial-scale=1, minimum-scale=1, width=device-width">\n  <title>Error 404 (Not Found)!!1</title>\n  <style>\n    *{margin:0;padding:0}html,code{font:15px/22px arial,sans-serif}html{background:#fff;color:#222;padding:15px}body{margin:7% auto 0;max-width:390px;min-height:180px;padding:30px 0 15px}* > body{background:url(//www.google.com/images/errors/robot.png) 100% 5px no-repeat;padding-right:205px}p{margin:11px 0 22px;overflow:hidden}ins{color:#777;text-decoration:none}a img{border:0}@media screen and (max-width:772px){body{background:none;margin-top:0;max-width:none;padding-right:0}}#logo{background:url(//www.google.com/images/branding/googlelogo/1x/googlelogo_color_150x54dp.png) no-repeat;margin-left:-5px}@media only screen and (min-resolution:192dpi){#logo{background:url(/'
    2020-10-14 09:16:36 INFO	1<	692 bytes
    2020-10-14 09:16:36 DEBUG	1<	b'/www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) no-repeat 0% 0%/100% 100%;-moz-border-image:url(//www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) 0}}@media only screen and (-webkit-min-device-pixel-ratio:2){#logo{background:url(//www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) no-repeat;-webkit-background-size:100% 100%}}#logo{display:inline-block;height:54px;width:150px}\n  </style>\n  <a href=//www.google.com/><span id=logo aria-label=Google></span></a>\n  <p><b>404.</b> <ins>That\xe2\x80\x99s an error.</ins>\n  <p>The requested URL <code>/</code> was not found on this server.  <ins>That\xe2\x80\x99s all we know.</ins>\n'
    2020-10-14 09:16:36 INFO	1>	disconnected
