

class NetworkList():
    configInfo = []
    networkList = []
    configfile = ''
    
    def save(self):
        if self.configfile == '':
            return
        f = open(self.configfile, "w")
        for line in self.configInfo:
            f.write(line)
        for network in self.networkList:
            f.write(network.toString())
        f.close()
        
    def load(self,cfgfile):
        """Read the hostapd config file"""
        self.configfile = cfgfile
        f = open(cfgfile, "r")
        newNetwork = ''
        inNetwork = False
        for line in f:
            if line == "#network\n":
                if newNetwork != '':
                    self.networkList.append(newNetwork)
                newNetwork = MultinetNetwork()
                inNetwork = True
        
            if inNetwork:
                keyval = line.split('=')
                if keyval[0] == 'ignore_broadcast_ssid':
                    newNetwork.ignore_broadcast_ssid = keyval[1].rstrip()
                elif keyval[0] == 'ssid':
                    newNetwork.active = True
                    newNetwork.ssid = keyval[1].rstrip()
                elif keyval[0] == 'wpa_passphrase':
                    newNetwork.wpa_passphrase = keyval[1].rstrip()
            else:
                self.configInfo.append(line)       
        
        self.networkList.append(newNetwork)        
        f.close()
        
    def add(self,SSID,wpa_passphrase,ignore_broadcast_ssid = 0):
        newNetwork = MultinetNetwork()
        newNetwork.active = True
        newNetwork.ignore_broadcast_ssid = ignore_broadcast_ssid
        newNetwork.ssid = SSID
        newNetwork.wpa_passphrase = wpa_passphrase
        added = False
        for network in self.networkList:
            if network.active == False:
                loc = self.networkList.index(network)
                self.networkList[loc] = newNetwork;
                added = True
                break
            
        if added == True:
            self.save()  
        
        return added 
            
    def remove(self,SSID):
        networkFound = False
        for network in self.networkList:
            if network.ssid == SSID:
                networkFound = self.networkList.index(network)
                break
            
        if networkFound != False:    
            self.networkList[networkFound] = MultinetNetwork()
            self.networkList[networkFound].active = False
            self.save()
            return True
        
        return networkFound
            
            
        
class MultinetNetwork():
    active = False
    ignore_broadcast_ssid = ''
    ssid = ''
    wpa_passphrase = ''
    wpa = '2'
    wpa_pairwise = 'CCMP'

    def toString(self): 
        addStr = "#network\n"
        if self.active == True:
            addStr += "ssid=" + str(self.ssid) + "\n"
            addStr += "wpa=" + str(self.wpa) + "\n"
            addStr += "ignore_broadcast_ssid=" + str(self.ignore_broadcast_ssid) + "\n"
            addStr += "wpa_pairwise=" + str(self.wpa_pairwise) + "\n"
            addStr += "wpa_passphrase=" + str(self.wpa_passphrase) + "\n"
            addStr += "\n"   
        return addStr
    
    def toXML(self):
        xml = " <network>\n"
        xml += "    <active>TRUE</active>\n"
        xml += "    <ssid>" + self.ssid + "</ssid>\n"
        xml += "</network>\n"
        return xml
 
# self tests   
#n = NetworkList()
#n.load("./cfg/demo_hostapd.conf")
#n.add('Toshes test','q1w2e3r4t5y6',1)
#n.remove('SamsungLaptop')
#n.remove('HpDeskjet')
#n.add('HpDeskjettest','q1w2e3r4t5y6',1)
