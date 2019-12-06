import math
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink


class FatTree_Topo (Topo):
    "FatTree Topology."

    def __init__(self):
        Topo.__init__(self)
        Racks = 20
        M = 10
        R = 3
        D = 4
        # look at one Rack
        # connect that Rack with D - 1 Racks
        # connect each of those with D - 1 racks ... until you're out of racks

        # racksLeft = int(math.ceil((M + R) / 2))
        # while Racks > racksLeft:

        self.mr_switches = []
        self.mr_hosts = []

        # rackIndex = 0
        # graph = {}

        # while Racks > 0:
        #     if self.mr_switches[rackIndex]:

        for r in range(Racks):
            # if r == 0:
            #     # first, put in the top node
            #     switch = self.addSwitch('s{}'.format(r))
            #     self.mr_switches.append(switch)
                # graph[r] = []
                # continue
            # elif (len(graph[rackIndex]) == D):
            #     rackIndex += 1

            switch = self.addSwitch('s{}'.format(r))
            self.mr_switches.append(switch)
            # graph[r] =
            # self.addLink(self.mr_switches[rackIndex],
            #              self.mr_switches[r], delay='5ms')
            # graph[r].append(rackIndex)
            # graph[rackIndex].append(r)

        self.addLink(self.mr_switches[0], self.mr_switches[5])
        self.addLink(self.mr_switches[0], self.mr_switches[7])
        self.addLink(self.mr_switches[0], self.mr_switches[9])
        self.addLink(self.mr_switches[0], self.mr_switches[11])
        self.addLink(self.mr_switches[1], self.mr_switches[5])
        self.addLink(self.mr_switches[1], self.mr_switches[7])
        self.addLink(self.mr_switches[1], self.mr_switches[9])
        self.addLink(self.mr_switches[1], self.mr_switches[11])
        self.addLink(self.mr_switches[2], self.mr_switches[6])
        self.addLink(self.mr_switches[2], self.mr_switches[8])
        self.addLink(self.mr_switches[2], self.mr_switches[10])
        self.addLink(self.mr_switches[2], self.mr_switches[12])
        self.addLink(self.mr_switches[3], self.mr_switches[6])
        self.addLink(self.mr_switches[3], self.mr_switches[8])
        self.addLink(self.mr_switches[3], self.mr_switches[10])
        self.addLink(self.mr_switches[3], self.mr_switches[12])
        self.addLink(self.mr_switches[4], self.mr_switches[12])
        self.addLink(self.mr_switches[4], self.mr_switches[13])
        self.addLink(self.mr_switches[5], self.mr_switches[12])
        self.addLink(self.mr_switches[6], self.mr_switches[14])
        self.addLink(self.mr_switches[6], self.mr_switches[15])
        self.addLink(self.mr_switches[7], self.mr_switches[14])
        self.addLink(self.mr_switches[7], self.mr_switches[15])
        self.addLink(self.mr_switches[8], self.mr_switches[16])
        self.addLink(self.mr_switches[8], self.mr_switches[17])
        self.addLink(self.mr_switches[9], self.mr_switches[16])
        self.addLink(self.mr_switches[9], self.mr_switches[17])
        self.addLink(self.mr_switches[10], self.mr_switches[18])
        self.addLink(self.mr_switches[10], self.mr_switches[19])
        self.addLink(self.mr_switches[11], self.mr_switches[18])
        self.addLink(self.mr_switches[11], self.mr_switches[19])

        # leafSwitches = rackIndex + 1
        # leafNodes = range(leafSwitches, Racks)

        


        # 12 to 21
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(1, 13))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[12], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[12]
        self.mr_hosts.append(host)

        # 12 to 22
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(2, 13))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[12], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[12]
        self.mr_hosts.append(host)


        # 13 to 23
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(3, 14))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[13], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[13]
        self.mr_hosts.append(host)

        # 13 to 24
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(4, 14))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[13], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[13]
        self.mr_hosts.append(host)


        # 14 to 25
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(5, 15))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[14], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[14]
        self.mr_hosts.append(host)

        # 14 to 26
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(6, 15))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[14], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[14]
        self.mr_hosts.append(host)


        # 15 to 27
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(7, 16))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[15], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[15]
        self.mr_hosts.append(host)

        # 15 to 28
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(8, 16))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[15], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[15]
        self.mr_hosts.append(host)


        # 16 to 29
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(9, 17))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[16], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[16]
        self.mr_hosts.append(host)

        # 16 to 30
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(10, 17))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[16], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[16]
        self.mr_hosts.append(host)


        # 17 to 31
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(11, 18))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[17], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[17]
        self.mr_hosts.append(host)

        # 17 to 32
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(12, 18))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[17], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[17]
        self.mr_hosts.append(host)


        # 18 to 33
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(13, 19))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[18], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[18]
        self.mr_hosts.append(host)

        # 18 to 34
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(14, 19))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[18], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[18]
        self.mr_hosts.append(host)


        # 19 to 35
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(15, 20))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[19], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[19]
        self.mr_hosts.append(host)

        # 19 to 36
        # Now add the master node (host master) on rack 1, i.e., switch 1
        host = self.addHost('h{}s{}'.format(16, 20))
        print "Added master host", host
        # zero based indexing
        self.addLink(host, self.mr_switches[19], delay='1ms')
        print "Added link between ", host, " and switch ", self.mr_switches[19]
        self.mr_hosts.append(host)
















        # host_index = 0
        # switch_index = 0
        # # Now add the master node (host master) on rack 1, i.e., switch 1
        # host = self.addHost('h{}s{}'.format(host_index+1, switch_index+1))
        # print "Added master host", host
        # # zero based indexing
        # self.addLink(host, self.mr_switches[switch_index], delay='1ms')
        # print "Added link between ", host, " and switch ", self.mr_switches[switch_index]
        # self.mr_hosts.append(host)


        # TODO: Error is right here.
        # numServers = 0

        # leafNode = 12
        # while numServers < 16:
        #     # for leafNode in leafNodes:
        #     # if numServers == 0:
        #     #     # TODO: only breaks out of lower level loop
        #     #     break

        #     host = self.addHost('h{}s{}'.format(numServers + 1, leafNode + 1))
        #     self.addLink(host, self.mr_switches[leafNode], delay='1ms')
        #     self.mr_hosts.append(host)

        #     # leafNode += 1
        #     numServers += 1

        #     host = self.addHost('h{}s{}'.format(numServers, leafNode))
        #     self.addLink(host, self.mr_switches[leafNode], delay='1ms')
        #     self.mr_hosts.append(host)

        #     leafNode += 1
        #     numServers += 1


topos = {'mytopo': (lambda: FatTree_Topo())}
