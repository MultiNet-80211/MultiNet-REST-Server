'''
Created on 19 Oct 2011

@author: psxab
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl
import cgi
import subprocess
import os
from base64 import b64decode
from HostapdConfig import NetworkList

class MutinetREST(BaseHTTPRequestHandler):
    
    configfile = "/root/multi-net/live_hostapd.conf"
    #configfile = "./cfg/demo_hostapd.conf"
    restartScript = "/root/multi-net/restartMultinet.sh"
    adminUser = "admin"
    adminPass = "admin"
    networkCfg = NetworkList()
    networkCfg.load(configfile)
    
    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"MultiNet\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_POST(self):
        args = self.path[1:]
        args = args.split('/')
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        if args[0] == "saveAll":
            xml = self.saveAll(args,postvars)
        else: 
            xml = "Unsuported Method"
            
        return self.sendPage(xml);
        
    def do_GET(self):
        args = self.path[1:]
        args = args.split('/')
        
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            return
        
        auth = self.headers.getheader('Authorization')
        (authType, data) = auth.split(' ')
        
        if authType != "Basic":
            xml = "Unsuported Auth Method"
            return xml
        
        (username, _, password) = b64decode(data).partition(':')
        print "username = " + username + " password = " + password
        if username != self.adminUser or password != self.adminPass:
            self.do_AUTHHEAD()
            return

        if len(args) == 0:
            xml = "Unsuported Method"
                            
        if args[0] == "create" :
            xml = self.create(args)
        elif args[0] == "remove":
            xml = self.remove(args)
        elif args[0] == "list":
            xml = self.listNetworks(args)
        else: 
            xml = self.getFile(args)
        
        return self.sendPage(xml);
    
    def create(self,args):
        """Add the requested network to the config file and restart multinet"""
        if len(args) < 3:
            return "Wrong parameter  count"
        else:
            sucsess = self.networkCfg.add(args[1],args[2],0)
            xml = "<?xml version=\"1.0\"?>"
            xml += "<result>\n"
            xml += "    <action>create</action>\n"
            xml += "    <success>%s</success>\n" % sucsess
            xml += "    <ssid>%s</ssid>\n" % args[1]
            xml += "</result>\n"
            self.restartMultinet()
            return xml
    
    def remove(self,args):
        if len(args) < 1:
            return "Wrong parameter  count"
        else:
            sucsess = self.networkCfg.remove(args[1])
            """Delete the requested network to the config file and restart multinet"""
            xml = "<?xml version=\"1.0\"?>\n"
            xml += "<result>\n"
            xml += "    <action>remove</action>\n"
            xml += "    <success>%s</success>\n" % sucsess
            xml += "    <ssid>%s</ssid>\n" % args[1]
            xml += "</result>\n"
            self.restartMultinet()
            return xml
    
    def listNetworks(self,args):
        """List configured networks multinet"""
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        xml += "<networkList>\n"
        for n in self.networkCfg.networkList:
            if n.active == True:
                xml += n.toXML();
            
        xml += "</networkList>\n"
        return xml
    
    def showGenorationInterface(self):
        """Interface to generate valid QRcodes"""
        f = open("./generate.html", "r")
        html = f.read()
        f.close()
        return html
    
    def getFile(self,args):
        try:
            path = "./" 
            path += "/".join(args)
            
            if path.endswith(".py") or path.endswith(".pyc") or path.endswith(".conf"):
                return "Unsupported Operation"
            
            f = open(path, 'rb')
            html = f.read()
            f.close()
            return html
        except IOError:
            return "Unsupported Operation"
      
            
    def sendPage(self, body = "", t = "text/html"):
        body = body.encode('UTF-8')
        self.send_response(200)
        self.send_header("Content-type", " " + t + "; charset=UTF-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()
        return
        
    def restartMultinet(self):
        """restart hostapd"""
        subprocess.Popen(self.restartScript)
        return 1
    
    def saveAll(self,args,postvars):
        #save data to disk!!
        p= os.path.join(os.getcwd(),'trial','data') 
        for item in postvars:
            f = open(p + '/' + item + '.csv', 'a+')
            tmp = "".join(postvars[item])
            print(tmp)
            f.write(tmp + "\n")
            f.close()
        return "<h1>ALL done thanks for taking part !</h1><div>Answers saved successfully!</div>"
        
def main():
    try:
        server_address = ('', 80)
        httpd = HTTPServer(server_address, MutinetREST)
        #httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem', server_side=True)
        print('started httpserver...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        httpd.socket.close()

if __name__ == '__main__':
    main()
    