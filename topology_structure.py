# -*- coding: utf-8 -*-


class Topology():

    def __init__(self, path):
        self.filepath = path
        self.switches_count = 0
        self.ixia_count = 0
        self.link_count = 0
        self.vm_count = 0
        self.testfilecount = 0
        self.testcount = 0
        self.hosts = {}
        self.feat = {}
        self.testnames = []
        self.pic = []

    def print_topology_information(self):
        for test in self.testnames:
            print("Testname: " + test)
        print("    Switches count: " + str(self.switches_count))
        print("    Ixia count: " + str(self.ixia_count))
        print("    Link count: " + str(self.link_count))
        print("    VM count: " + str(self.vm_count))
        for host in self.hosts:
            print("        Host [" + host + "]: " + str(self.hosts[host]))
        print("    Test file count: " + str(self.testfilecount))
        print("    Test cases count: " + str(self.testcount))
        print("    PAth: " + str(self.filepath))
        #for key in self.feat:
        #    print(key + ": " + str(self.feat[key]))
        #print("Topology:")
        #for line in self.pic:
            #print(line)
