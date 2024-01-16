  #!/usr/bin/env python

'Setting the position of Nodes and providing mobility using mobility models'
import sys
import time
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController, OVSSwitch,Host
from mn_wifi.node import OVSAP

def topology(args):
    info(args)
    node2_IP='192.168.10.11'
    CONTROLLER_IP='192.168.10.10'
    "Create a network."
	
    "Create soldiers according to the predifined number given in args"
    Realnumber=int(args[-1])
 
    def create_soldiers():
	for i in range(Realnumber):
		add_soldier(i+1)

    net = Mininet_wifi(topo=None,controller=RemoteController, switch=OVSSwitch,accessPoint=OVSAP)
    c1=net.addController('c1',controller=RemoteController,ip=CONTROLLER_IP,port=6633)
    def add_drone():
    	ap2=net.addAccessPoint( 'ap2', ssid='ssid2', mode='g',channel='2',failMode="standalone", position='70,0,0',range='40')
	ap3=net.addAccessPoint( 'ap3',ssid='ssid3', mode='g', channel='3',
                                 failMode="standalone", position='0,70,0',range='40')
	ap4=net.addAccessPoint( 'ap4',ssid='ssid4', mode='g', channel='4',
                                 failMode="standalone", position='70,70,0',range='40')
        ap5=net.addAccessPoint('ap5',ssid='ssid5',mode='g',channel='5', failMode="standalone", position='0,0,0',range='40')

	return(ap2,ap3,ap4,ap5)
    def add_soldier(i):
	net.addStation('sta'+str(i), mac='00:00:00:00:00:0'+str(i), ip='10.0.0.'+str(i)+'/8',
                   min_x=10, max_x=30+10*i, min_y=50, max_y=70+10*i, min_v=5, max_v=10,range='10')
    def add_ap1():
    	ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                                 failMode="standalone", position='50,50,0',range='40')
    	return ap1                
    info("\n*** Creating nodes\n")
    create_soldiers()
        
    #net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
     #             min_x=10, max_x=30, min_y=50, max_y=70, min_v=5, max_v=10,range='20')
   # net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
    #               min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5,range='20')
   # if '-m' in args:
   #     ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,ssid2', mode='g',
   #                              channel='1', failMode="standalone",
   #                              position='50,50,0')
   # else:
   #     ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
   #                              failMode="standalone", position='50,50,0',range='40')



    info("add switch")
    s1=net.addSwitch('s1')
    #Configure the GRE tunnel
    s1.cmd('ovs-vsctl add-port s1 s1-grep1 -- set interface s1-gre1 type=gre options:remote_ip='+node2_IP)
    s1.cmdPrint('ovs-vsctl show')
    
    ap1=add_ap1()
    
    ap2,ap3,ap4,ap5=add_drone()
    info("*** Configuring nodes\n")
    net.configureNodes()

    net.plotGraph(min_x=-100,min_y=-100,max_x=400,max_y=400)
		
    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=100, max_y=100, seed=20)
                         
    net.addLink(s1,ap1)               
    net.addLink(s1,ap2)               
    net.addLink(s1,ap3)               
    net.addLink(s1,ap4)               
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([ c1 ])
    #net.start()
   # time.sleep(3)
     
  #  net.stopMobilitsy(time=5)
   # net.setMobilityModel(time=0, model='RandomDirection',
   #                      max_x=100, max_y=100, seed=20) 
    CLI(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
