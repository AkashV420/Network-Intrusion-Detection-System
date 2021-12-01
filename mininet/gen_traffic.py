#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, DefaultController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from startopo import StarTopo

from os import path
from os import mkdir
import random
import time
import sys
import re
import numpy as np

small_flow_min = 100  # KBytes = 100KB
small_flow_max = 10240  # KBytes = 10MB
big_flow_min = 10240  # KBytes = 10MB
big_flow_max = 1024*1024*10  # KBytes = 10 GB

protocol_list = ['--udp', '']  # udp / tcp
port_min = 1025
port_max = 65536

sampling_interval = '1'  # seconds

big_bandwidth_list = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M',
                           '200M', '300M', '400M', '500M', '600M', '700M', '800M', '900M', '1000M']

small_bandwidth_list = ['100K', '200K', '300K', '400K', '500K', '600K', '700K', '800K', '900K', '1000K',
                       '2000K', '3000K', '4000K', '5000K', '6000K', '7000K', '8000K', '9000K', '10000K', '1000K']


def random_normal_number(low, high):
    range = high - low
    mean = int(float(range) * float(75) / float(100)) + low
    sd = int(float(range) / float(4))
    num = np.random.normal(mean, sd)
    return int(num)


def generate_big_flows(id, duration, net, log_dir):
    hosts = net.hosts

    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    dst = net.get(str(end_points[1]))

    protocol = random.choice(protocol_list)
    port_argument = str(random.randint(port_min, port_max))
    bandwidth_argument = random.choice(big_bandwidth_list)

    # create cmd
    cmdServ = "iperf -s "
    cmdServ += protocol
    cmdServ += " -p "
    cmdServ += port_argument
    cmdServ += " -i "
    cmdServ += sampling_interval
    cmdServ += " > "
    cmdServ += log_dir + "/big_flow_%003d" % id + ".txt 2>&1 "
    cmdServ += " & "

    cmdClt = "iperf -c "
    cmdClt += dst.IP() + " "
    cmdClt += protocol
    cmdClt += " -p "
    cmdClt += port_argument
    if protocol == "--udp":
        cmdClt += " -b "
        cmdClt += bandwidth_argument
    cmdClt += " -t "
    cmdClt += str(duration)
    cmdClt += " & "

    # send the cmd
    dst.cmdPrint(cmdServ)
    src.cmdPrint(cmdClt)


def generate_small_flows(id, duration, net, log_dir):
    hosts = net.hosts

    # select random src and dst
    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    dst = net.get(str(end_points[1]))

    # select connection params
    protocol = random.choice(protocol_list)
    port_argument = str(random.randint(port_min, port_max))
    bandwidth_argument = random.choice(small_bandwidth_list)

    # create cmd
    cmdServ = "iperf -s "
    cmdServ += protocol
    cmdServ += " -p "
    cmdServ += port_argument
    cmdServ += " -i "
    cmdServ += sampling_interval
    cmdServ += " > "
    cmdServ += log_dir + "/small_flow_%003d" % id + ".txt 2>&1 "
    cmdServ += " & "

    cmdClt = "iperf -c "
    cmdClt += dst.IP() + " "
    cmdClt += protocol
    cmdClt += " -p "
    cmdClt += port_argument
    if protocol == "--udp":
        cmdClt += " -b "
        cmdClt += bandwidth_argument
    cmdClt += " -t "
    cmdClt += str(duration)
    cmdClt += " & "

    # send the cmd
    dst.cmdPrint(cmdServ)
    src.cmdPrint(cmdClt)


def generate_flows(n_big_flows, n_small_flows, duration, net, log_dir):
    if not path.exists(log_dir):
        mkdir(log_dir)

    n_total_flows = n_big_flows + n_small_flows
    interval = duration / n_total_flows

    flow_type = []
    for i in range(n_big_flows):
        flow_type.append('E')
    for i in range(n_small_flows):
        flow_type.append('M')
    random.shuffle(flow_type)

    flow_start_time = []
    for i in range(n_total_flows):
        n = random.randint(1, int(interval))
        if i == 0:
            flow_start_time.append(0)
        else:
            flow_start_time.append(flow_start_time[i - 1] + n)

    flow_end_time = []
    for i in range(n_total_flows):
        s = flow_start_time[i]
        e = int(float(95) / float(100) * float(duration))  # 95% of the duration
        end_time = random_normal_number(s, e)
        while end_time > e:
            end_time = random_normal_number(s, e)
        flow_end_time.append(end_time)

    flow_duration = []
    for i in range(n_total_flows):
        flow_duration.append(flow_end_time[i] - flow_start_time[i])

    print(flow_type)
    print(flow_start_time)
    print(flow_end_time)
    print(flow_duration)
    print("Remaining duration :" + str(duration - flow_start_time[-1]))

    # generating the flows
    for i in range(n_total_flows):
        if i == 0:
            time.sleep(flow_start_time[i])
        else:
            time.sleep(flow_start_time[i] - flow_start_time[i-1])
        if flow_type[i] == 'E':
            generate_big_flows(i, flow_duration[i], net, log_dir)
        elif flow_type[i] == 'M':
            generate_small_flows(i, flow_duration[i], net, log_dir)

    remaining_duration = duration - flow_start_time[-1]
    info("Traffic started, going to sleep for %s seconds...\n " % remaining_duration)
    time.sleep(remaining_duration)

    info("Stopping traffic...\n")
    info("Killing active iperf sessions...\n")

    for host in net.hosts:
        host.cmdPrint('killall -9 iperf')


# Main function
if __name__ == "__main__":
    # Loading default parameter values
    log_dir = "logs"
    topology = StarTopo()
    default_controller = False
    controller_ip = "127.0.0.1"  # localhost
    controller_port = 6633
    debug_flag = False
    debug_host = "localhost"
    debug_port = 6000

    setLogLevel('info')

    # creating log directory
    log_dir = log_dir
    i = 1
    while True:
        if not path.exists(log_dir + str(i)):
            # mkdir(log_dir + str(i))
            log_dir = log_dir + str(i)
            break
        i = i+1

    # starting mininet
    if default_controller:
        net = Mininet(topo=topology, controller=DefaultController, host=CPULimitedHost, link=TCLink,
                      switch=OVSSwitch, autoSetMacs=True)
    else:
        net = Mininet(topo=topology, controller=None, host=CPULimitedHost, link=TCLink,
                      switch=OVSSwitch, autoSetMacs=True)
        net.addController('c1', controller=RemoteController, ip=controller_ip, port=controller_port)

    net.start()

    user_input = "QUIT"

    # run till user quits
    experiment_duration = 1000
    n_big_flows = 10
    n_small_flows = 20

    generate_flows(n_big_flows, n_small_flows, experiment_duration, net, log_dir)
