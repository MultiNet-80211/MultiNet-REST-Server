import pyudev
import os
import time
import urllib
import urllib2
import base64

mount_path = "/media/"
configfilename = "multinet.conf"
MultiNetAPIAddress = "http://10.0.0.1"
MultiNetAPIUsername = "admin"
MultiNetAPIPassword = "admin"
base64string = base64.encodestring('%s:%s' % (MultiNetAPIUsername, MultiNetAPIPassword))[:-1]

cfgList = {}

def checkForConfigChanges():
    time.sleep(5)
    mounts = os.listdir(mount_path)
    """look for removed files"""
    removecfg = ""
    for c in  cfgList:
        found = False
        for m in  mounts:
            if m == c:
                found = True
                break
                
        if found == False:
            removeNetwork(cfgList[c])
            removecfg = c
            break
        
    if removecfg != "":
        cfgList.pop(c)
        
    """look for new files"""
    for d in  mounts:
        fileName = mount_path + "/" + d + "/" + configfilename
        if os.path.isfile(fileName):
            f = open(fileName)
            line = f.readline()
            f.close()
            if cfgList.has_key(d):
                """we have his configured already!"""
                if cfgList[d] != line:
                    """the info has changed update the network information"""
                    cfgList[d] = line
            else:
                cfgList[d] = line
                addNetwork(cfgList[d])

def addNetwork(cfg):
    url = MultiNetAPIAddress + "/create/" + urllib.quote(cfg)
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    authheader =  "Basic %s" % base64string
    req.add_header("Authorization", authheader)
    f = urllib2.urlopen(req)
    print f.read()

def removeNetwork(cfg):
    parts = cfg.split('/')
    url = MultiNetAPIAddress + "/remove/" + urllib.quote(parts[0])
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    authheader =  "Basic %s" % base64string
    req.add_header("Authorization", authheader)
    f = urllib2.urlopen(req)
    print f.read()
     
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')
for action, device in monitor:
    if 'ID_FS_TYPE' in device:
        print('{0} partition {1}'.format(action, device.get('ID_FS_LABEL')))
        checkForConfigChanges()
            
        
        #print(device.get('DEVPATH'))
        #print(device.get('ID_PATH'))
        #print(device.get('ID_FS_UUID'))
        #print device.keys()