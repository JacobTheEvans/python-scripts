import nmap
import optparse

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print("[*] " + tgtHost + " tcp/" + tgtPort + " " + state)

def main():
    parser = optparse.OptionParser("Usage scanner.py -H <target host> -p <target port>")
    parser.add_option("-H",dest="tgtHost",type="String",help="specify target host")
    parser.add_option("-p",dest="tgtPort",type="String",help="specify target port[s] serparate by a comma")
    (options,args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPort  = str(options.tgt).split(',')

    #Dev Note: May have to change None in either of the statments below to "None"

    if (tgtHost == None) | (tgtPorts[0] == None):
        print parser.usage
        exit(0)
    for tgtPort in tgtPorts:
        nmapscan(tgtHost, tgtPort)

if __name__ = "__main__":
    main()
        
    
    
 
