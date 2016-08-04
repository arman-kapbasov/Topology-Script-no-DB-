# -*- coding: utf-8 -*-

import topology_structure as ts
import html_create as hc


class Topology_Dict(ts.Topology):

    def __init__(self):
        ts.Topology.__init__(self, None)
        self.topology_name = "."
        self.total_switch = 0
        self.total_ixia = 0
        self.total_vm = 0

    def print_topology_information(self):
        print("Topology name: " + self.topology_name)
        print("    Tests:")
        for test in self.testnames:
            print("        Testname: " + test)
        print("    Switch count: " + str(self.switches_count))
        print("    Ixia count: " + str(self.ixia_count))
        print("    Link count: " + str(self.link_count))
        print("    VM count: " + str(self.vm_count))
        for host in self.hosts:
            print("        Host [" + host + "]: " + str(self.hosts[host]))
        print("    Test count: " + str(self.testfilecount))
        for key in self.feat:
            print(key + ": " + str(self.feat[key]))
        #print("Topology:")
        #for line in self.pic:
            #print(line)

    #def html_opti(filename):

    def write_html(self, filename, num):
        hc.html_line(filename)
        hc.html_header(filename, "Topology name: " + self.topology_name, 3, 0)

        hc.html_break(filename)
        for line in self.pic:
            if line in ['\n', '\r\n'] or not line.strip():
                continue
            hc.html_pI(filename, line, 0)
        hc.html_break(filename)

        hc.html_paragraph(filename, "Switch count: "
                            + str(self.switches_count), 0)

        hc.html_paragraph(filename, "Ixia count: "
                            + str(self.ixia_count), 0)

        hc.html_paragraph(filename, "Link count: "
                            + str(self.link_count), 0)

        hc.html_paragraph(filename, "VM count: "
                            + str(self.vm_count), 0)

        for host in self.hosts:
            hc.html_paragraph(filename, "Host [" + host + "]: "
                            + str(self.hosts[host]), 1)

        hc.html_paragraph(filename, "Test file count: "
                            + str(self.testfilecount), 0)

        hc.html_break(filename)
        hc.html_collapse_start(filename, "Show test files:", num, None)

        for test in self.testnames:
            hc.html_collapse_middle(filename, "Testname: " + test)
            hc.html_break(filename)
        hc.html_collapse_end(filename)

    def html_table(self, filename, totaltest, boxID):
        list1 = []
        list1.append("Test file count")
        list1.append("Switch count")
        list1.append("Ixia count")
        list1.append("Link count")
        list1.append("Host count")

        hc.html_header(filename, self.topology_name, 3, 1)

        hc.html_table_start(filename, list1)
        hc.html_table_mid(filename, self.testfilecount, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.switches_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.ixia_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.link_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.vm_count, boxID)
        boxID = boxID + 1
        hc.html_table_end(filename)

        hc.html_break(filename)

        list2 = []
        list2.append("Percentage of total test files")
        list2.append("Total topology switch count")
        list2.append("Total topology ixia count")
        list2.append("Total topology link count")
        list2.append("Total topology host count")

        percent = '{percent:.2%}'.format(percent=float(self.testfilecount)
                / float(totaltest))
        hc.html_table_start(filename, list2)
        hc.html_table_mid(filename, str(percent), boxID)
        hc.html_table_mid(filename, self.testfilecount * self.switches_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.testfilecount * self.ixia_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.testfilecount * self.link_count, boxID)
        boxID = boxID + 1
        hc.html_table_mid(filename, self.testfilecount * self.vm_count, boxID)
        boxID = boxID + 1
        hc.html_table_end(filename)
