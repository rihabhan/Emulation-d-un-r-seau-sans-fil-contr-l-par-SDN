  #!/usr/bin/env python

'Setting the position of Nodes and providing mobility using mobility models'
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController, OVSSwitch,Host
from mn_wifi.node import OVSAP

def topology(args):
    info(args)
    NODE2_IP='192.168.10.12'
    CONTROLLER_IP='192.168.10.10'
    "Create a network."

    "Create soldiers according to the predifined number given in args"
    Realnumber=int(args[-1])

    def create_soldiers():
	for i in range(Realnumber):
		add_soldier(i)

    net = Mininet_wifi(topo=None,controller=RemoteController, switch=OVSSwitch,accessPoint=OVSAP)
    c1=net.addController('c1',controller=RemoteController,ip=CONTROLLER_IP,port=6633)
    def add_drone():
       	ap2=net.addAccessPoint( 'ap2', ssid='ssid2', mode='g', channel='2',
                                 failMode="standalone", position='0,70,0',range='40')
	ap3=net.addAccessPoint( 'ap3',ssid='ssid3', mode='g', channel='3',
                                 failMode="standalone", position='70,0,0',range='40')
	ap4=net.addAccessPoint( 'ap4',ssid='ssid4', mode='g', channel='4',
                                 failMode="standalone", position='70,70,0',range='40')
        return (ap2,ap3,ap4) 
    def add_soldier(i):
	net.addStation('sta'+str(i+10), mac='00:00:00:00:00:0'+str(i), ip='10.0.0.'+str(i+10)+'/8',
                   min_x=10, max_x=30+10*i, min_y=50, max_y=70+10*i, min_v=5, max_v=10,range='10') 
    info("\n*** Creating nodes\n")
    create_soldiers()

    if '-m' in args:
        ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,ssid2', mode='g',
                                 channel='1', failMode="standalone",
                                 position='50,50,0')
    else:
        ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                                 failMode="standalone", position='50,50,0',range='40')
    info("add switch")
    s2=net.addSwitch('s2')
    info("*** Configuring nodes\n")
    net.configureNodes()
    info("configure GRE tunnel")
    s2.cmd('ovs-vsctl add-port s2 s2-grep1 -- set interface s2-gre1 type=gre options:remote_ip='+NODE2_IP)
    s2.cmdPrint('ovs-vsctl show')
    ap2,ap3,ap4=add_drone()
    net.addLink(s2,ap1)
    net.addLink(s2,ap2)
    net.addLink(s2,ap3)
    net.addLink(s2,ap4)
    net.plotGraph(min_x=-100,min_y=-100,max_x=400,max_y=400)

    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=100, max_y=100, seed=20)
                   
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([ c1 ])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])


    info("*** Running CLI\n")
    CLI(net)
   
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
