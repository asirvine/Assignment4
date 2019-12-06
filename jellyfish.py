import math
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink


class JFTopo(Topo):
    "Jellyfish Topology"

    def __init__(self):
        Topo.__init__(self)
        Racks = 20
        M = 10
        R = 3
        D = 4

        print "Jellyfish Topology: Racks = ", Racks, ", M = ", M, ", R = ", R
        self.mr_switches = []
        self.mr_hosts = []
        graph = {}
        for r in range(Racks):
            graph[r] = []
            # a switch per rack.
            switch = self.addSwitch('s{}'.format(
                r+1), stp=True, failMode='standalone')

            print "Added switch", switch
            self.mr_switches.append(switch)

        numLinks = 0
        # racks * connections - # of servers
        totalRackLinks = int(math.floor(((Racks * D) - (M + R)) / 2))
        while numLinks < totalRackLinks:
            node1 = math.rand(Racks)
            node2 = math.rand(Racks)
            if node1 == node2:
                continue
            if len(graph[node1]) < D and len(graph[node2]) < D:
                graph[node1].append(node2)
                graph[node2].append(node1)
                numLinks += 1
                self.addLink(self.mr_switches[node1],
                             self.mr_switches[node2], delay='5ms')
                print "Added link between", self.mr_switches[node1], " and ", self.mr_switches[node2]

        # for r in range(Racks):
        #     # connect each switch to each other D - 1 times randomly
        #     # make sure there are no cycles

        # TODO: What is a host master or master node?

        servers = M+R
        for vertex in graph:
            if len(graph[vertex]) < D:
                # graph.append(-1*(servers+1))
                host = self.addHost('h{}s{}'.format(servers, vertex))
                self.addLink(host, self.mr_switches[vertex], delay='1ms')
                self.mr_hosts.append(host)
                servers -= 1

            # connect to a random Rack that hasn't already been connected to D times

        # for h in range(R):
        #     # connect to a random Rack that hasn't already been connected to D times

        # for r in range(M):
        #     for l in range(Racks):
        #         if (len(graph[l]) < D):
        #             # connect


topos = {'mytopo': (lambda: JFTopo())}
