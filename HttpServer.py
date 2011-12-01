'''
Created on 19 Oct 2011

@author: psxab
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl
import re
import subprocess

class MutinetREST(BaseHTTPRequestHandler):
    
    #configfile = "/root/multi-net/live_hostapd.conf"
    configfile = "./cfg/demo_hostapd.conf"
    restartScript = "/root/multi-net/restartMultinet.sh"
        
    def do_GET(self):
        args = self.path[1:]
        args = args.split('/');
        
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
        if len(args) != 2:
            return self.showGenorationInterface()
        else:
            sucsess = self.addNetworkToHostapdConfig(args[1],args[2])
            xml = "<?xml version=\"1.0\"?>"
            xml += "<result>\n"
            xml += "    <action>create</action>\n"
            xml += "    <success>%s</success>\n" % sucsess
            xml += "    <ssid>%s</ssid>\n" % args[1]
            xml += "</result>\n"
            return xml
    
    def remove(self,args):
        """Delete the requested network to the config file and restart multinet"""
        xml = "<?xml version=\"1.0\"?>\n"
        xml += "<result>\n"
        xml += "    <action>remove</action>\n"
        xml += "    <success>TRUE</success>\n"
        xml += "    <ssid>%s</ssid>\n" % args[1]
        xml += "</result>\n"
        return xml
    
    def listNetworks(self,args):
        """List configured networks multinet"""
        networks = self.readHostapdConfig()
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        xml += "<networkList>\n"
        for n in networks:
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
    
    def readHostapdConfig(self):
        """Read the hostapd config file"""
        f = open(self.configfile, "r")
        cfg = f.read()
        f.close()
        ssids = re.findall('(\nssid=.*\n.*\n.*\n.*\n)', cfg)
         
        networkList = []
        for i in range(len(ssids)):
            ssid = re.search('(?:ssid=)(.*)(?:\n)', ssids[i]).group(1)
            wpa = re.search('(?:wpa=)(.*)(?:\n)', ssids[i]).group(1)
            networkList.append(MultinetNetwork(ssid,wpa))
        
        return networkList

    def addNetworkToHostapdConfig(self,ssid,passphrase):
        """add a network to the hostapd config file"""
        
        networkList = self.readHostapdConfig()
        
        n = len(networkList)
        
        f = open(self.configfile, "r")
        cfg = f.read()
        f.close()
        ssids = re.findall('(\nssid=' + ssid + '\n)', cfg)
        if len(ssids) == 0 :
            addStr = "\n"
            addStr += "bss=wlan_" + str(n) + "\n"
            addStr += "ssid=" + ssid + "\n"
            addStr += "wpa=2\n"
            #addStr += "ignore_broadcast_ssid=1\n"
            addStr += "wpa_pairwise=CCMP\n"
            addStr += "wpa_passphrase=" + passphrase + "\n"
            addStr += "\n"
            fout = open(self.configfile, "a")
            fout.write(addStr)
            fout.close()
            self.restartMultinet()
            return "TRUE"
        else :
            return "FALSE"
        
    def restartMultinet(self):
        """restart hostapd"""
        subprocess.Popen(self.restartScript)
        return 1
        
        
class MultinetNetwork():
    ssid = ""
    wpa = ""
    def __init__(self,ssid,wpa):
        self.ssid = ssid
        self.wpa = wpa

    def toXML(self):
        xml = " <network>\n"
        xml += "    <active>TRUE</active>\n"
        xml += "    <ssid>" + self.ssid + "</ssid>\n"
        xml += "</network>\n"
        return xml

    
    
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
    