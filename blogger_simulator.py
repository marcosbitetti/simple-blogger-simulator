#!/bin/python
import re, io, os, sys, math, string, cgi, time
#from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

path = os.path.realpath('./')
filename = 'index.html'
isMobile = False
httpPort = 8083

if len(sys.argv)>1:
    if sys.argv[1]=='true' or sys.argv[1]=='True' or sys.argv[1]=='mobile':
        isMobile = True
    if sys.argv[1]=='/?' or sys.argv[1]=='-?' or sys.argv[1]=='--help':
        print """Python Minimal Blogger Emulator
Modo de usar:
    python blogger_imiter.py [mobile|brownser] [porta]
  onde:
      [mobile|brownser] -> Se definido como mobile simula mobile
      [porta] -> porta de entrada
Exemplo:
python blogger_imiter.py
ou
python blogger_imiter.py mobile
ou
python blogger_imiter.py mobile 8083

Abrir o navegador e digitar:
http://localhost:8083/

Para para de Ctrl+C nesta janela.
"""
        exit()
if len(sys.argv)>2:
    httpPort = int(sys.argv[2])
    

def switch_content (command):
    global isMobile
    if command=='<b:if cond="data:blog.isMobile">':
        if isMobile:
            return True
        return False
    if command=='<b:else/>':
        if isMobile:
            return False
        return True
    if command.find('widget')>-1:
        return True
    return True


def parse_content (file_content):
    html = ""

    i = 0
    doRender = True
    match=re.search(r'\<b\:[^\<].*\>', file_content)
    while ( match ):
        if doRender:
            html += file_content[0:match.start()]
        doRender = switch_content(match.group())
        html += ''
        file_content = file_content[match.start()+len(match.group()):len(file_content)]
        match=re.search(r'\<b\:[^\<].*\>|\<\/b\:[^\<].*\>', file_content)
        i += 1
        if i>1000:
            break
    html += file_content

    headers  = "HTTP/1.1 200 OK\r\n"
    headers += "Server: Python Minimal Blogger Emulator\r\n"
    headers += "Content-Type: text/html;charset=UTF-8\r\n"
    headers += "Content-Length: %s\r\n" % len(html)
    headers += "\r\n"
    #headers += "Date: Thu, 31 Oct 2013 10:41:57 GMT"

    #print headers
    #print html
    return html

class HttpHandler (BaseHTTPRequestHandler):

    def do_GET(self):
        global path
        if self.path.endswith("/"):
            self.path += "index.html"
        fname = path + self.path.replace('/',os.sep)
        print "request %s" % self.path
        print os.path.isfile(fname)
        if not os.path.isfile(fname):
            self.send_error(404,'Arquivo nao encontrado: %s' % self.path)
            self.wfile.close()
        else:
            try:
                if self.path.endswith(".html"):
                    f = open( fname, "r" )
                    content = parse_content( f.read( os.path.getsize( fname ) ) )
                    f.close()
                    self.send_response(200)
                    self.send_header('Content-Type','text/html;charset=UTF-8')
                    self.send_header('Server','Python Minimal Blogger Emulator')
                    self.send_header('Content-Length',len(content))
                    self.send_header('Connection','close')
                    self.end_headers()
                    self.wfile.write(content)
                    self.wfile.close()
                    return
                else:
                    g_ext = re.search(r'\.\w+$',self.path)
                    if g_ext != None:
                        ext = g_ext.group()
                        #print ext
                        tp = "application/octet-stream"
                        if ext==".txt":
                            tp="text/plain"
                        if ext==".asc":
                            tp="text/plain"
                        if ext==".dat":
                            tp="text/plain"
                        if ext==".ini":
                            tp="text/plain"
                        if ext==".ascii":
                            tp="text/plain"
                        if ext==".json":
                            tp="application/json"
                        if ext==".js":
                            tp="text/javascript"
                        if ext==".coffee":
                            tp="text/coffeescript"
                        if ext==".css":
                            tp="text/css"
                        if ext==".jpg":
                            tp="image/jpeg"
                        if ext==".jpeg":
                            tp="image/jpeg"
                        if ext==".jpe":
                            tp="image/jpeg"
                        if ext==".png":
                            tp="image/png"
                        if ext==".gif":
                            tp="image/gif"
                        if ext==".ico":
                            tp="image/ico"
                        if ext==".svg":
                            tp="image/svg+xml"
                        if ext==".swf":
                            tp="application/x-shockwave-flash"
                        if ext==".htm":
                            tp="text/html"
                        if ext==".html":
                            tp="text/html"
                        if ext==".rhtm":
                            tp="text/html"
                        if ext==".xml":
                            tp="text/xml"
                        if ext==".flv":
                            tp="video/x-flv"
                        if ext==".mp4":
                            tp="video/mp4"
                        if ext==".ogg":
                            tp="video/ogg"
                        if ext==".webml":
                            tp="video/webml"
                        if ext==".apk":
                            tp="application/vnd.android.package-archive"

                        fname = path + self.path.replace('/',os.sep)
                        print "ler %s" % fname

                        sz = os.path.getsize( fname )
                        self.send_response(200)
                        self.send_header('Content-Type',tp)
                        self.send_header('Server','Python Minimal Blogger Emulator')
                        self.send_header('Content-Length',sz)
                        self.send_header('Connection','close')
                        self.end_headers()

                        f = open( fname, "rb" )
                        self.wfile.write( f.read( os.path.getsize( fname ) ) )
                        f.close()
                        self.wfile.close()

            except IOError:
                print "error"
                self.send_error(404,'Arquivo nao encontrado: %s' % self.path)
                self.wfile.close()

        # windows only
        #except WindowsError:
        #    self.send_error(404,'Arquivo nao encontrado: %s' % self.path)

    def do_POST(self):
        self.do_GET(self)


                            
try:
    server = HTTPServer( ('',httpPort), HttpHandler )
    print "roando servidor"
    server.serve_forever()
except KeyboardInterrupt:
    print 'encerrando'
    server.socket.close()
