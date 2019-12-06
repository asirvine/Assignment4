#
# Vanderbilt University, Computer Science
# CS4287-5287: Principles of Cloud Computing
# Author: Aniruddha Gokhale
# Created: Nov 2016
# Modified: Nov 2017
# Modified: Oct 2018
# Modified: Oct 2019
#
# 

Purpose:
-------------
The code here is used to demonstrate the homegrown wordcount MapReduce
framework on a cluster of Docker containers maintained by Docker Swarm as well as in a
network topology created using Mininet SDN emulator.

Since the code has been developed using the Python language binding of the ZeroMQ middleware,
you must install the pyzmq Python package:

sudo -H pip install --upgrade pyzmq  (if using Python 2.7)
sudo -H pip3 install --upgrade pyzmq  (if using Python 3.6)

This code base will be used for Programming Assignment #3 and Homework #3.

************** Instructions Below are needed for Assignment **************

===================================================================
                      Docker instructions for the federated cloud execution
===================================================================

In the following we discuss how to use the Docker implementation of
the code base both in a standalone VM mode or in Swarm mode.

+++++++++++++++++++++++++++++++++
Testing standalone in Laptop VM
+++++++++++++++++++++++++++++++++

Start your 18.04 VM on the laptop and open three shells

Step (1): Build images
-------------------------------
docker build -f ./dockerfile_master -t <some tag for master> .
docker build -f ./dockerfile_map -t <some tag for map> .
docker build -f ./dockerfile_reduce -t <some tag for reduce> .

I am using tags: vu_mr_master, vu_mr_map, vu_mr_reduce, respectively (where mr stands for
map-reduce)

Step (2): Run each image in its own shell
-------------------------------------------------------
In Shell 1, we run the master as follows:

         docker run -it --name <some name> vu_mr_master 

I used the name MyMR_Master

In Shell 2, we run the map worker as follows:

         docker run -it --name <some name> vu_mr_map /bin/bash

I used the name MyMR_Map

In Shell 3, we run the reduce worker as follows:

         docker run -it --name <some name> vu_mr_reduce /bin/bash

I used the name MyMR_Reduce

Step (3): Running the map-reduce wordcount
-------------------------------------------------------------

On shell 1 which is now running master, type the following at the prompt
which is # (# is not part of the command):

# ifconfig

and note down the IP address of the container. On my machine it was
172.17.0.2. 

# cd /root
# python mr_wordcount.py -p 5556 -M 1 -R 1 small.txt

On shell 2 which is now running map worker, type the following at the prompt
which is # (# is not part of the command):

# cd /root
# python mr_mapworker.py <master IP addr> <master port>

For me, it was python mr_mapworker.py 172.17.0.2 5556

On shell 3 which is now running reduce worker, type the following at
the prompt which is # (# is not part of the command):

# cd /root
# python mr_reduceworker.py <master IP addr> <master port>

For me, it was python mr_reduceworker.py 172.17.0.2 5556

Shell 1: Watch the completion of the program and time it took to run.

You can try the same with M = 1 and R = 1 as above but for the big.txt
file.

The master file runs 20 iterations of the same experiment and saves
the results in a file called "metrics.csv". The contents look like
this (using the -i 10 i.e., 10 iterations):

Map phase       Shuffle Phase   Reduce Phase    Finalize        Total
9.90979909897, 10.3850190639, 2.70907187462, 0.00508713722229, 23.0089771748
10.027493, 10.3473410606, 2.68525505066, 0.00602102279663, 23.0661101341
9.85127687454, 10.6124820709, 2.69362902641, 0.00514888763428, 23.1625368595
....

===========================================================================
                +++++++++++++++++++++++++++++++++
                                    Using Docker Swarm
                +++++++++++++++++++++++++++++++++

In the Swarm mode, we are going to exploit various features. For
instance, the --replicas will be used to create as many Map and Reduce
workers as we desire for the experiment. However, when they complete,
we do not want the manager to restart them. So we are going to use
--restart-condition none so the Swarm manager does not restart 
them.  See the start_* scripts that are provided.  Moreover, we are
not going to allow any map and reduce workers to execute on the master
node. So we are going to use the --constraints option for the
workers. On the other hand, we are going to force the mapreduce master
to start on the swarm master, also using the --constraints option.

Step (1)
------------
Say we use 3 VMs on Chameleon. One of them has floating IP so we can
log into it from outside.  That VM will be the master of the Swarm.

Step (2)
-----------
Copy the entire directory contents to the designated master node using
scp or pscp

Step (3)
-----------
Create the private registry on the master node (see slides). Start the Swarm using the
instructions and screenshots from my slides on containers. 

Step (4)
-----------
Build the images exactly as described above in the standalone
case. Now consult the "self-study" slides on private registry and how
to push these images into the private registry (See Week 7 slides on Docker starting
at slide 37)

Initialize the swarm on the master node, and join worker nodes from
other hosts.  A sample snapshot showing the "docker node ls" output is
shown below.  The leader (manager) node in this example is asg-ubuntu-vm.


Check the status of the swarm
------------------------------------------
ubuntu@asg-ubuntu-vm:~$ docker node ls
ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
ltozdclbs5fev9atq9tuxl705     asg-chameleon-ubuntu   Ready               Active 
cvhb6vnr5oi8amiksbc2313qq     asg-db-vm              Ready               Active 
5rlle5srporcfhifjykx9a8vv *   asg-ubuntu-vm          Ready               Active              Leader


Create an overlay network
-------------------------------------
ubuntu@asg-ubuntu-vm:~$ docker network create --driver overlay MyMR_Network

You could provide the --subnet to create your own subnet instead of
the default

Starting the map-reduce master
--------------------------------------------
Start the master using the start_master.sh script that is
provided. The main command is shown below:

docker service create --replicas 1 --name MyMR_Master --constraint 'node.hostname == asg-ubuntu-vm' -t --network MyMR_Network -p 5556:5556 -p 5557:5557 -p 5558:5558 -p 5559:5559 -p 5560:5560 129.59.107.155:5000/vu_mr_master /bin/bash

Explanation for the parameters:
* --replica 1: Only 1 replica
* --name MyMR_Master: name of service is MyMR_Master
* --constraint 'node.hostname == asg-ubuntu-vm': Constrained to run on
    the master node 
* -t: Attached a pseudo terminal
* --network MyMR_Network: Attach our service to the network we created
* -p is used to map the host-level port to container-level port. This
is needed because for some reason we are not able to have containers
from one cloud talk to containers on another cloud despite being in the same
swarm network.

* We do not run any command because we will do docker exec

Verify if the service is running
----------------------------------------

The "service ls" tells us if the replicas are up 

ubuntu@asg-ubuntu-vm:~$ docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE                                     PORTS
c1hyn7vn5too        MyMR_Master         replicated          1/1                 129.59.107.155:5000/vu_mr_master:latest


The "service ps" tells us its status and what node it is running
on. See a sample 

ubuntu@asg-ubuntu-vm:~$ docker service ps MyMR_Master
ID                  NAME                IMAGE                                     NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
j0p4073i73hk        MyMR_Master.1       129.59.107.155:5000/vu_mr_master:latest   asg-ubuntu-vm       Running             Running 5 minutes ago               

To ensure our service container is connected to the network, inspect
the network and identify the IP address assigned to the master in the
overlay network

ubuntu@asg-ubuntu-vm:~$ docker network inspect MyMR_Network
[
    {
        "Name": "MyMR_Network",
        "Id": "85695glk074xbhilnotmmcxrq",
        "Created": "2017-11-21T04:17:05.386263849Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.0.0.0/24",
                    "Gateway": "10.0.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "43136b664eb4ef4a7dd5949f5d2c343f4a42f8ccf1e8108b9cf6a1d2fcd80672": {
                "Name": "MyMR_Master.1.j0p4073i73hklejqf7i2gpwc2",
                "EndpointID": "856424bad6a2e3693742e235369a7bf69b1a6e9b24758dbbd66ed62e3675d7bc",
                "MacAddress": "02:42:0a:00:00:03",
                "IPv4Address": "10.0.0.3/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "asg-ubuntu-vm-66014e981c98",
                "IP": "129.59.107.155"
            }
        ]
    }
]

Running the MapReduce master code
----------------------------------------------------
Now start the MapReduce master code. Open a new ssh terminal to your
Horizon master VM and do "cd MapReduce_Docker" assuming you have
copied the entire directory to the VM.

Execute the line as below. Note that the complex id after
MyMR_Master.1.<> is specific to what Docker has created on your
system. After typing MyMR_Master and pressing a tab will autocomplete
it in the shell. Otherwise you have to note down the service and
copy-paste that complex id.

ubuntu@asg-ubuntu-vm:~$ docker exec -it MyMR_Master.1.j0p4073i73hklejqf7i2gpwc2   /bin/bash
root@43136b664eb4:/#
root@43136b664eb4:/# ifconfig
eth0      Link encap:Ethernet  HWaddr 02:42:0a:00:00:03
          inet addr:10.0.0.3  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1
          RX packets:9238 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9238 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:682908 (682.9 KB)  TX bytes:498588 (498.5 KB)

root@43136b664eb4:/# cd root
root@43136b664eb4:/# python mr_wordcount -i 10 -M <num of maps> -R
<num of reduce> -p 5556 <big data file>


Running the Map and Reduce workers
-----------------------------------------------------
In your first ssh window to the Horizon master, run the

start_workers.sh script

Note that the number of --replicas mentioned in this script should
match exactly what you provided the master for the -M and -R
parameters.

See the contents of the script below:

docker service create --restart-condition "none" --replicas 10 --name MyMR_Map --constraint 'node.hostname != asg-ubuntu-vm' -t --network MyMR_Network 129.59.107.155:5000/vu_mr_map python /root/mr_mapworker.py 129.59.107.155 5556

docker service create --restart-condition "none" --replicas 3 --name MyMR_Reduce --constraint 'node.hostname != asg-ubuntu-vm' -t --network MyMR_Network 129.59.107.155:5000/vu_mr_reduce python /root/mr_reduceworker.py 129.59.107.155 5556

Observing progress
---------------------------
Switch to the second ssh window to the master and you will see the
execution progressing with some debug messages getting printed. At the
end the experiment will end. Now is the time to copy the saved results
file from the container to the host

Go to ssh window 1 and type the following:

docker cp MyMR_Master.1.<the id for your docker>:/root/metrics.csv metrics_<M>_<R>.csv

where the M and R are what you used as parameters for M and R in the
experiment.

Stopping services:
-------------------------
Go to ssh window 1 on master VM and invoke

stop_services.sh

Repeat the experiment for different values of M and R and observe how
the execution time varies.

===================================================================
Mininet architecture and instructions to run the code
-------------------------------------------------------------------------

The mininet part is based on code written to work with Mininet. This
code base started as Mininet-only but then was combined with Docker
based architecture. The MapReduce  part uses a process-based
implementation of map and reduce tasks that run on the emulated hosts
of Mininet.   

Our mininet topology can comprise up to 3 racks. Each rack has a
switch.  The first rack comprises the master controller node. The 
second rack comprises all the map worker nodes.  The third rack
comprises all the reduce worker nodes.  If we have less than three 
racks specified, then the controller is collocated with the
workers. For instance, when two racks are specified, the controller
and reduce workers are on rack #1 and map workers are on rack #2. If
only one rack is specified, then the controller and both worker types
are all on the same rack.

The difference between the rack placement impacts to some extent the
response time because the switch to switch delay is set at 5
milliseconds while the host to its nearest switch is set at 1
millisecond. 

Running the code for Mininet
----------------------------------------
Step (1)
-----------
bash prompt>  sudo python mr_mininet -p 5557 -M 10 -R 3 -r 3 big.txt

(see handout on what values of M, R and r are to be tested. The
example above shows 10 Maps, 3 Reduce, and 3 racks)

-p is for the base port of master (default 5557)
-M is for number of maps
-R is for number of reducers (keep it smaller than maps)
-r is for number of racks (allowed values 1, 2 or 3)

This will create the appropriate topology. There will also be a file
created called commands.txt which has all the commands that you can
run in one stroke. See below on how to run it.  The only command it
does not contain is how to run the Master, which you have to do on
your own. I have purposely commented out the generation of the command
for the master in mr_mininet.py.  The master controller will need to
be run manually so that you can observe the output and also figure out
if  the process ran to completion or not.

Step (2)
-----------
On the mininet prompt, do the following:

mininet> xterm h1s1

This will pop up an xterm window on host h1s1, which is the host on
which the master is always going to be executed because the host
"h1s1" is on rack #1.  So that we get more accurate timing
measurements, we do the following first. 

Step (3)
-----------
Now go back to the window with your mininet prompt and type the
following: 

mininet> source commands.txt

This will execute the map and reduce workers on the different hosts
mentioned in the commands.txt file (which is a generated file).

Step (4)
-----------
Now go to the Xterm window and type the following at the root prompt:

prompt # python mr_wordcount.py -p 5557 -M 10 -R 3 big.txt

Note that you *MUST* use the same port and number of map/reduce as what
you provided to the mininet topology generation. I know this is a
potential erroneous step which is why I had automated it but then we
cannot see the output. Hence, this small additional step. But be
careful.

You will notice some output on the xterm window showing the progress
of the entire map-reduce process.  The process should end after it is
completed running the default number of iterations.  The results are
collected in a file called metrics.csv and will have results that look
like this:

Map phase	Shuffle Phase	Reduce Phase	Finalize	Total
6.94446802139, 6.81741690636, 2.31004285812, 0.00345706939697, 16.0753848553
5.57244801521, 6.34157085419, 2.15737915039, 0.00122714042664, 14.0726251602
6.02635216713, 6.69039011002, 2.27755093575, 0.00219702720642, 14.9964902401

In your directory, there should also be a results.csv file which is
the final word count result. There will also be a number of *.out
files, which are the output of all the processes that started on each
of the hosts.   But these files are not of interest to us

****************** The above is needed for HW3 ************************

=============================================================================
                                Features of this sample code:
                                -----------------------------------------
(1)
We implement more realistic process-based map-reduce workers where the
map and reduce tasks are handled in separate processes running on
different emulated machines (hosts) of mininet or in docker containers
managed by Swarm.

(2)
For mininet, we create data center-like topologies where we can have a
single rack where all machines are connected to a single switch, or
two racks where the master and reduce nodes are on rack, while map
nodes are on a second rack, or where all categories of nodes are on
their own racks. Each rack has its switch.  Inside Docker, we can
create a swarm spanning federated clouds to get a sense of the
realistic end-to-end delays

(3)
We use ZeroMQ's PUSH-PULL pattern to send tasks from master to
workers, and have the workers send their results to the "sink" which
is the master.  This is a gentle introduction to using ZeroMQ, which
is a messaging capability that makes writing socket-based code simpler
and elegant while eliminating a large number of accidental
complexities. It also supports many communication patterns. We use one
that is needed for us because we need a "barrier synchronization step"
after the map and reduce steps. This is achieved using the push-pull
and source-worker-sink pattern.

Since this is a load-balancing pattern, we had to use 4 different
ports on which various activities take place. Minimally, we are
required to specify the base port for the Master and then all the four
ports are derived from this.

Master to Map comm: via base port (default value 5556)
Master to Reduce comm: base_port + 1
Barrier to ensure all workers are up: base_port + 2
Map to MapSink results barrier comm: base_port + 3
Reduce to ReduceSink results barrier comm: base_port + 4

You do not need to know ZeroMQ. However, you will need to install
zeromq in your laptop VM and also in the Docker containers

sudo apt-get install python-zmq

(4)
We also demonstrate a newer and more elegant way of command line
parsing in Python using the "argparse" package. This makes both
optional and positional command line parsing extremely simple and very
elegant as shown in the sample code.

The parameters to the main program are:
-p <base port of master>
-M <num of map workers>
-R <num of reduce workers>
-r <num of racks>

(5)
We show how a mininet emulator that emulates a given topology can be
used to kickstart the map-reduce job on the emulated hosts. The
topology generator synthesizes the script used to run all the map and
reduce workers on the appropriate nodes. So you are required to issue
just one command.

For Docker, the swarm will start as many maps and reduces as we ask it
to start on the Docker worker nodes.

(6)
We use the Pickle Python package to demonstrate save/load of in-memory
data structures like lists of lists into a file. This makes it very
simple to do the reduce activity.

Directory contents
----------------------------
Files in this directory are as follows

mr_mininet.py:          main master file that starts the mininet
                        topology and invokes the wordcount on the
                        master node of the topology. This file is not
                        used for Docker.
                        
mr_topology.py:        Topology class used to create the network
                       topology in mininet. Used by
                       mr_mininet.py. This file is not used for Docker
                       demonstration. 
                                            
mr_wordcount.py:       main file to invoke the map reduce wordcount
                       framework.  

mr_framework.py:       Implements the entire logic for the wordcount map reduce

mr_thread.py:          A thread class used by the MR framework to
                       start the barrier threads we need that to
                       behave as the map and reduce barrier sinks.

mr_mapworker.py:       Logic for map task. Runs as a separate program.

mr_reduceworker.py:    Logic for reduce task. Runs as a separate program.

big.txt:                 Our big data sample file

small.txt:               Our small data file (for testing smaller
                         sized data)

commands.txt:            Sample generated file my mininet that we run
                         manually so it kickstarts jobs on individual
                         emulated hosts.

mr_barriersink.py:        Unused file. It implements the barrier as a
                          process instead of thread. But this
                          complicates things.
                          
dockerfile_master:       Build files for docker containers
dockerfile_map
dockerfile_reduce

start_master.sh:        To start a master in the swarm
start_workers.sh        To start workers in the swarm (after master is started)
stop_services.sh        To stop all the services after the experiment
==========================================================================

                                                ---------------------------
                                                For the Assignment
                                                ---------------------------

For the assignment on the energy data, you will use this framework but
will need to make modifications to various files so that the
wordcount-centric logic is replaced by energy data. The files that
will need modifications are mentioned below. Inside each file, there
are markers shown with:
    #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
 and explanation that goes with it to describe what changes may be
 needed in that function.

mr_framework.py:
        Since this is the master file, most of the logic is fine but
        changes may be needed in how to divide the energy data file,
        what you do when intermediate files are created, etc.

mr_mapworker.py:
        This file currently encode the wordcount map logic and must be
        changed to energy logic.  Please see the do_work function.

mr_reduceworker.py:
        This file currently encode the wordcount reduce logic and must be
        changed to energy logic.  Please see the do_work function.

mr_wordcount.py:
        This is the driver program that invokes the mr_framework. Most
        likely the only change you may need to make is rename the file
        to mr_energy.py or something like that.


