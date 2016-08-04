# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import time
import commands
import operator

import topology_parser as tp
'''import topology_structure as ts'''
import html_create as hc
import dictionary_structure as ds

#=======Global variable========
TOPO_LIST = []

timestamp = time.strftime("%c")

all_topo_file = "topology_listing"
summaryfile = "topology_summary"
dashfile = "topology_dashboard"
optifile = "topology_optimization"

# change number of results to display in the dashboard
results_count = 3


def update_dic_top(dic_topo, new_top):
    # Parameters: existing dic_topology and same topology
    # Function: copy over the test name and vm/host OS type
    for test_name in new_top.testnames:
        dic_topo.testnames.append(test_name)
        dic_topo.testfilecount = dic_topo.testfilecount + 1
    dic_topo.testcount = dic_topo.testcount + new_top.testcount
    for host in new_top.hosts:
        if host in dic_topo.hosts:
            dic_topo.hosts[host] = dic_topo.hosts[host] + new_top.hosts[host]
        else:
            dic_topo.hosts[host] = new_top.hosts[host]
    for feat in new_top.feat:
        if feat in dic_topo.feat:
            dic_topo.feat[feat] = dic_topo.feat[feat] + new_top.feat[feat]
        else:
            dic_topo.feat[feat] = new_top.feat[feat]
    if len(dic_topo.pic) < len(new_top.pic):
        dic_topo.pic[:] = []
        for line in new_top.pic:
            dic_topo.pic.append(line)
    dic_topo.total_ixia = dic_topo.testfilecount * dic_topo.ixia_count
    dic_topo.total_switch = dic_topo.testfilecount * dic_topo.switches_count
    dic_topo.total_vm = dic_topo.testfilecount * dic_topo.vm_count


def copy_newtop_to_dic_top(dic_topo, new_top, num):
    # Parameters: new dictionary topology and new topology to be copied
    # Function: to copy brand new topology into main dictionary
    name = (str(new_top.switches_count) + "sw_" + str(new_top.ixia_count) +
            "ixia_" + str(new_top.link_count) + "link_" + str(new_top.vm_count)
            + "host")
    dic_topo.topology_name = name
    dic_topo.link_count = new_top.link_count
    dic_topo.ixia_count = new_top.ixia_count
    dic_topo.switches_count = new_top.switches_count
    dic_topo.vm_count = new_top.vm_count
    for test_name in new_top.testnames:
        dic_topo.testnames.append(test_name)
        dic_topo.testfilecount = dic_topo.testfilecount + 1
    dic_topo.testcount = dic_topo.testcount + new_top.testcount
    for host in new_top.hosts:
        if host in dic_topo.hosts:
            dic_topo.hosts[host] = dic_topo.hosts[host] + new_top.hosts[host]
        else:
            dic_topo.hosts[host] = new_top.hosts[host]
    for feat in new_top.feat:
        if feat in dic_topo.feat:
            dic_topo.feat[feat] = dic_topo.feat[feat] + new_top.feat[feat]
        else:
            dic_topo.feat[feat] = new_top.feat[feat]
    for line in new_top.pic:
        dic_topo.pic.append(line)
    dic_topo.total_ixia = dic_topo.testfilecount * dic_topo.ixia_count
    dic_topo.total_switch = dic_topo.testfilecount * dic_topo.switches_count
    dic_topo.total_vm = dic_topo.testfilecount * dic_topo.vm_count


def compare_topologies(dict_top, new_top):
    # Parameters: a dictionary topology and a new topology
    # Returns: 0 if not same, 1 if it exists already
    if dict_top.link_count != new_top.link_count:
        return 0
    if dict_top.ixia_count != new_top.ixia_count:
        return 0
    if dict_top.switches_count != new_top.switches_count:
        return 0

    # for testing
    # print("dict_top.vm_count" + str(dict_top.vm_count))
    # print("new_top.vm_count" + str(new_top.vm_count))

    if dict_top.vm_count != new_top.vm_count:
        return 0
    return 1


def check_top_empty(new_top):
    # if topology is empty, discard it
    # returns 0 if not empty, return 1 if empty
    if ((new_top.link_count is 0 and new_top.ixia_count is 0 and
            new_top.switches_count is 0 and new_top.vm_count is 0) or
            new_top.testcount is 0):
        return 1
    return 0


#======Adding entry to the topology dictionary====
def populate_dic(new_top):
    # Parameters: a parsed topology
    # Function: either creates a new entry into the dictionary
    #           or adds data to an existing topology
    global TOPO_LIST

    add_flag = 0

    for d_topology in TOPO_LIST:
        if add_flag is 0:
            if compare_topologies(d_topology, new_top):
                update_dic_top(d_topology, new_top)
                add_flag = 1
                break
    if add_flag is 0:
        new_dic_topo = ds.Topology_Dict()
        copy_newtop_to_dic_top(new_dic_topo, new_top, len(TOPO_LIST) + 1)
        TOPO_LIST.append(new_dic_topo)


#=========Traverse dir and subdir===
def get_all_pytests(walk_dir):
    # Parameters: path of the direcotry to go through
    # Function: recursivley runs through a folder to find tests
    # that start with "test" and end in "py"
    #Creates the TOPO_LIST dictionary with all the topologies

    for root, dirs, files in os.walk(walk_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.startswith("test") and filename.endswith(".py"):
                new_top = tp.parse_main(file_path)
                if check_top_empty(new_top):
                    continue
                populate_dic(new_top)


def find_max(atr):
    #returns the list of topologies with most hosts
    global results_count
    temp = []
    temp1 = []
    for topology in (sorted(TOPO_LIST, key=operator.attrgetter(atr),
            reverse=True)):
        temp.append(topology)

    for x in range(results_count):
        temp1.append(temp[x])
    return temp1


def calc_percent_w_sign(var1, var2):
    percent = '{percent:.2%}'.format(percent=float(var1)
                / float(var2))
    return percent


def calc_percent(var1, var2):
    fract = float(var1) / float(var2)
    percent = '{0:.2f}'.format(fract * 100)
    return percent


def write_summary(git_repo):
    #Parameter: list of the git repos
    #Writes HTML files for summary, dashboard, optimization and full topology
    print(">Creating HTML summary, dashboard, optimization, and topology")
    totalfile = 0
    totaltest = 0
    inputID = 0
    boxID = 0
    scriptID = 0
    dictBoxID = {}
    num = 0

    #======Optimization===
    #===by feature ====
    nix_total = 0
    nix_test = 0
    nix_sw = 0
    nix_ix = 0
    nix_vm = 0
    nix_total_sw = 0
    nix_total_ix = 0
    nix_total_vm = 0

    ix_total = 0
    ix_test = 0
    ix_sw = 0
    ix_ix = 0
    ix_vm = 0
    ix_total_sw = 0
    ix_total_ix = 0
    ix_total_vm = 0

    #=== by topology =====
    nix_test_t = 0
    nix_sw_t = 0
    nix_ix_t = 0
    nix_vm_t = 0

    ix_test_t = 0
    ix_sw_t = 0
    ix_ix_t = 0
    ix_vm_t = 0

    for topology in TOPO_LIST:
        totalfile = topology.testfilecount + totalfile
        totaltest = topology.testcount + totaltest

    # =========All topology html file===========
    hc.html_intro(all_topo_file, "All Topologies")
    hc.html_main_head(all_topo_file, "Listing", dashfile,
            summaryfile, optifile, all_topo_file)

    hc.html_pagetitle(all_topo_file, "Full Topology Listing")
    hc.html_line(all_topo_file)
    hc.html_paragraph(all_topo_file, "Report generated on: " + timestamp, 0)
    for repo in git_repo:
        hc.html_paragraph(all_topo_file, "Using repository: " + repo, 0)
    hc.html_paragraph(all_topo_file, "Total test file count: " + str(totalfile), 0)
    hc.html_paragraph(all_topo_file, "Total test count: " + str(totaltest), 0)
    hc.html_paragraph(all_topo_file, "Total topology count: "
                + str(len(TOPO_LIST)), 0)
    for topology in (sorted(TOPO_LIST, key=operator.attrgetter("testfilecount"),
                reverse=True)):
        topology.write_html(all_topo_file, num)
        num = num + 1

          # =======if no ixia in topology ==========
        if topology.ixia_count is 0:
            nix_test_t = nix_test_t + topology.testfilecount - 1
            nix_sw_t = (nix_sw_t +
                    topology.switches_count * (topology.testfilecount - 1))
            nix_ix_t = (nix_ix_t + topology.ixia_count * (topology.testfilecount
                    - 1))
            nix_vm_t = (nix_vm_t + topology.vm_count * (topology.testfilecount
                    - 1))

            nix_total = nix_total + topology.testfilecount
            nix_total_sw = (nix_total_sw +
                    topology.switches_count * topology.testfilecount)
            nix_total_ix = (nix_total_ix +
                    topology.ixia_count * topology.testfilecount)
            nix_total_vm = nix_total_vm + topology.vm_count * topology.testfilecount
            # print("----------Topology: " + topology.topology_name)
            for feat in topology.feat:
                if topology.feat[feat] > 1:
                    # print("    feat [" + feat + "]: "
                        #+ str(topology.feat[feat]))
                    nix_test = nix_test + (topology.feat[feat] - 1)
                    nix_sw = nix_sw + (topology.switches_count
                        * (topology.feat[feat] - 1))
                    nix_ix = nix_ix + (topology.ixia_count
                        * (topology.feat[feat] - 1))
                    nix_vm = nix_vm + (topology.vm_count
                        * (topology.feat[feat] - 1))
        # ====== if ixia in topology ===========
        else:
            ix_test_t = ix_test_t + topology.testfilecount - 1
            ix_sw_t = (ix_sw_t +
                    topology.switches_count * (topology.testfilecount - 1))
            ix_ix_t = (ix_ix_t + topology.ixia_count * (topology.testfilecount
                    - 1))
            ix_vm_t = (ix_vm_t + topology.vm_count * (topology.testfilecount
                    - 1))

            ix_total = ix_total + topology.testfilecount
            ix_total_sw = (ix_total_sw +
                    topology.switches_count * topology.testfilecount)
            ix_total_ix = (ix_total_ix +
                    topology.ixia_count * topology.testfilecount)
            ix_total_vm = ix_total_vm + topology.vm_count * topology.testfilecount
            # print("----------Topology: " + topology.topology_name)
            for feat in topology.feat:
                if topology.feat[feat] > 1:
                    # print("    feat [" + feat + "]: "
                        #+ str(topology.feat[feat]))
                    ix_test = ix_test + (topology.feat[feat] - 1)
                    ix_sw = ix_sw + (topology.switches_count
                        * (topology.feat[feat] - 1))
                    ix_ix = ix_ix + (topology.ixia_count
                        * (topology.feat[feat] - 1))
                    ix_vm = ix_vm + (topology.vm_count
                        * (topology.feat[feat] - 1))
    hc.html_end(all_topo_file)

    # ===== Optimization html file =========
    hc.html_intro(optifile, "Potential Optimization")
    hc.html_main_head(optifile, "Optimization", dashfile, summaryfile,
        optifile, all_topo_file)

    hc.html_pagetitle(optifile, "Potential Optimization")
    hc.html_line(optifile)
    hc.html_paragraph(optifile, "Report generated on: " + timestamp, 0)
    for repo in git_repo:
        hc.html_paragraph(optifile, "Using repository: " + repo, 0)
    hc.html_paragraph(optifile, "Total test file count: " + str(totalfile), 0)
    hc.html_paragraph(optifile, "Total test count: " + str(totaltest), 0)

    hc.html_line(optifile)

    # =======================By Feature ===================
    hc.html_header(optifile, "By Feature", 1, 1)
    #-----------------------Non Ixia topologies------------
    hc.html_header(optifile, "Non Ixia Topologies", 2, 0)
    # hc.html_paragraphCenter(optifile, "Total tests with Ixia count: "
    #        + str(nix_total))

    list1 = []
    arGraph1a = []
    arGraph2a = []

    list1.append("Total Non Ixia Test Files")
    list1.append("Estimated Provisioning Time")
    list1.append("Estimated Parallel Test Run Time")
    list1.append("Total Switches")
    list1.append("Total Ixia")
    list1.append("Total Hosts")

    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, nix_total, boxID)
    arGraph1a.append("Test files")
    arGraph1a.append(nix_total)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, 0, 0, inputID, scriptID, 0, 4)  # time edit
    hc.html_table_mid2(optifile, nix_total, 1, inputID, scriptID, boxID, 4)
    dictBoxID[boxID] = nix_total
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_sw, boxID)
    arGraph1a.append("Switch")
    arGraph1a.append(nix_total_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_ix, boxID)
    arGraph1a.append("Ixia")
    arGraph1a.append(nix_total_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_vm, boxID)
    arGraph1a.append("Host")
    arGraph1a.append(nix_total_vm)
    boxID = boxID + 1
    hc.html_table_end(optifile)
    hc.html_break(optifile)

    list1 = []
    list1.append("Collapsable Test Files")
    list1.append("Percent of Total Non Ixia Tests")
    list1.append("Potential Time Saving (minute)")
    list1.append("Switch Saving")
    list1.append("Ixia Saving")
    list1.append("Host Saving")
    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, nix_test, boxID)
    arGraph2a.append("Test files")
    arGraph2a.append(nix_total - nix_test)
    boxID = boxID + 1
    percent = calc_percent_w_sign(nix_test, nix_total)
    hc.html_table_mid(optifile, percent, boxID)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, nix_test, 1, inputID, scriptID, boxID, 4)
    dictBoxID[boxID] = nix_test
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_sw, boxID)
    arGraph2a.append("Switch")
    arGraph2a.append(nix_total_sw - nix_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_ix, boxID)
    arGraph2a.append("Ixia")
    arGraph2a.append(nix_total_ix - nix_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_vm, boxID)
    arGraph2a.append("Host")
    arGraph2a.append(nix_total_vm - nix_vm)
    boxID = boxID + 1
    hc.html_table_script(optifile, scriptID, inputID, dictBoxID)
    inputID = inputID + 1
    scriptID = scriptID + 1
    hc.html_table_end(optifile)

    hc.html_break(optifile)
    hc.html_graph(optifile, 1, 300, 60)

    hc.html_line(optifile)
    hc.html_collapse_start(optifile, "Show non-ixia topology tests", num, None)
    num = num + 1
    for topology in (sorted(TOPO_LIST, key=operator.attrgetter("testfilecount"),
                reverse=True)):
        if topology.ixia_count is 0:
            first_flag = 1
            for feat in (sorted(topology.feat.items(),
                    key=operator.itemgetter(1), reverse=True)):
                feat = feat[0]
                if topology.feat[feat] > 1:
                    if first_flag:
                        hc.html_header(optifile, topology.topology_name, 3, 0)
                        hc.html_collapse_start(optifile, "Show Features", num, None)
                        num = num + 1
                        first_flag = 0
                    fcs = topology.feat[feat] - 1  # feat count saving
                    feat_str = ("[Test file count: " + str(topology.feat[feat]) +
                            "] [Time saving: " + str(fcs * 4) +
                            " mins] [Switch saving: " + (str(fcs *
                            topology.switches_count) + "] [Ixia saving: " +
                            str(fcs * topology.ixia_count) + "] [VM saving: "
                            + str(fcs * topology.vm_count) + "]"))
                    hc.html_break(optifile)
                    hc.html_collapse_start(optifile, feat, num, feat_str)
                    num = num + 1
                    for test in topology.testnames:
                        #parse the filename to avoid Ping capturing Ping6
                        test_name = test.split("_", 1)[1]
                        if "_" in test_name:
                            test_name = test_name.split("_", 1)[0]
                        else:
                            test_name = test_name.split(".", 1)[0]
                        test_name = test_name.lower()
                        if feat == test_name:
                            hc.html_paragraph_color(optifile, test, 1)
                    hc.html_collapse_end(optifile)
                '''else:
                    for test in topology.testnames:
                        #parse the filename to avoid Ping capturing Ping6
                        test_name = test.split("_", 1)[1]
                        if "_" in test_name:
                            test_name = test_name.split("_", 1)[0]
                        else:
                            test_name = test_name.split(".", 1)[0]
                        test_name = test_name.lower()
                        if feat == test_name:
                            hc.html_paragraph(optifile, test, 1)'''
            if not first_flag:
                hc.html_break(optifile)
                hc.html_collapse_end(optifile)

    hc.html_collapse_end(optifile)
    #hc.html_line(optifile)

    #-----------------------Ixia topologies------------
    hc.html_header(optifile, "Ixia Topologies", 2, 0)
    # hc.html_paragraphCenter(optifile, "Total tests with Ixia count: "
            #+ str(ix_total))
    dictBoxID.clear()
    arGraph1b = []
    arGraph2b = []
    list1 = []
    list1.append("Total Ixia Test Files")
    list1.append("Estimated Provisioning Time")
    list1.append("Estimated Parallel Test Run Time")
    list1.append("Total Switches")
    list1.append("Total Ixia")
    list1.append("Total Hosts")

    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, ix_total, boxID)
    arGraph1b.append("Test files")
    arGraph1b.append(ix_total)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, 0, 0, inputID, scriptID, 0, 8)  # time edit
    hc.html_table_mid2(optifile, ix_total, 1, inputID, scriptID, boxID, 8)
    dictBoxID[boxID] = ix_total
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_sw, boxID)
    arGraph1b.append("Switch")
    arGraph1b.append(ix_total_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_ix, boxID)
    arGraph1b.append("Ixia")
    arGraph1b.append(ix_total_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_vm, boxID)
    arGraph1b.append("Hosts")
    arGraph1b.append(ix_total_vm)
    boxID = boxID + 1
    hc.html_table_end(optifile)
    hc.html_break(optifile)

    list1 = []
    list1.append("Collapsable Test Files")
    list1.append("Percent of Total Ixia Tests")
    list1.append("Potential Time Saving (minute)")
    list1.append("Switch Saving")
    list1.append("Ixia Saving")
    list1.append("Host Saving")
    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, ix_test, boxID)
    arGraph2b.append("Test files")
    arGraph2b.append(ix_total - ix_test)
    boxID = boxID + 1
    percent = calc_percent_w_sign(ix_test, ix_total)
    hc.html_table_mid(optifile, percent, boxID)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, ix_test, 1, inputID, scriptID, boxID, 8)
    dictBoxID[boxID] = ix_test
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_sw, boxID)
    arGraph2b.append("Switch")
    arGraph2b.append(ix_total_sw - ix_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_ix, boxID)
    arGraph2b.append("Ixia")
    arGraph2b.append(ix_total_ix - ix_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_vm, boxID)
    arGraph2b.append("Host")
    arGraph2b.append(ix_total_vm - ix_vm)
    boxID = boxID + 1
    hc.html_table_script(optifile, scriptID, inputID, dictBoxID)
    inputID = inputID + 1
    scriptID = scriptID + 1
    hc.html_table_end(optifile)

    hc.html_break(optifile)

    hc.html_graph(optifile, 2, 300, 60)

    hc.html_line(optifile)
    hc.html_collapse_start(optifile, "Show ixia topology tests", num, None)
    num = num + 1

    for topology in (sorted(TOPO_LIST, key=operator.attrgetter("testfilecount"),
                reverse=True)):
        if topology.ixia_count is not 0:
            first_flag = 1
            for feat in (sorted(topology.feat.items(),
                    key=operator.itemgetter(1), reverse=True)):
                feat = feat[0]
                if topology.feat[feat] > 1:
                    if first_flag:
                        hc.html_header(optifile, topology.topology_name, 3, 0)
                        hc.html_collapse_start(optifile, "Show Features",
                            num, None)
                        num = num + 1
                        first_flag = 0
                    fcs = topology.feat[feat] - 1  # feat count saving
                    feat_str = ("[Test file count: " + str(topology.feat[feat]) +
                            "] [Time saving: " + str(fcs * 8) +
                            " mins] [Switch saving: " + (str(fcs *
                            topology.switches_count) + "] [Ixia saving: " +
                            str(fcs * topology.ixia_count) + "] [VM saving: "
                            + str(fcs * topology.vm_count) + "]"))
                    hc.html_break(optifile)
                    hc.html_collapse_start(optifile, feat, num, feat_str)
                    num = num + 1
                    for test in topology.testnames:
                        #parse the filename to avoid Ping capturing Ping6
                        test_name = test.split("_", 1)[1]
                        if "_" in test_name:
                            test_name = test_name.split("_", 1)[0]
                        else:
                            test_name = test_name.split(".", 1)[0]
                        test_name = test_name.lower()
                        if feat == test_name:
                            hc.html_paragraph_color(optifile, test, 1)
                    hc.html_collapse_end(optifile)
            if not first_flag:
                hc.html_break(optifile)
                hc.html_collapse_end(optifile)

    hc.html_collapse_end(optifile)

    hc.html_line(optifile)
    #=============By Topology =================

    hc.html_header(optifile, "By Topology", 1, 1)

    hc.html_header(optifile, "Non Ixia Topologies", 2, 0)
    # hc.html_paragraphCenter(optifile, "Total tests with Ixia count: "
    #        + str(nix_total))

    list1 = []
    arGraph3a = []
    arGraph3b = []

    list1.append("Total Non Ixia Test Files")
    list1.append("Estimated Provisioning Time")
    list1.append("Estimated Parallel Test Run Time")
    list1.append("Total Switches")
    list1.append("Total Ixia")
    list1.append("Total Hosts")

    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, nix_total, boxID)
    arGraph3a.append("Test files")
    arGraph3a.append(nix_total)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, 0, 0, inputID, scriptID, 0, 4)  # time edit
    hc.html_table_mid2(optifile, nix_total, 1, inputID, scriptID, boxID, 4)
    dictBoxID[boxID] = nix_total
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_sw, boxID)
    arGraph3a.append("Switch")
    arGraph3a.append(nix_total_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_ix, boxID)
    arGraph3a.append("Ixia")
    arGraph3a.append(nix_total_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_total_vm, boxID)
    arGraph3a.append("Host")
    arGraph3a.append(nix_total_vm)
    boxID = boxID + 1
    hc.html_table_end(optifile)
    hc.html_break(optifile)

    list1 = []
    list1.append("Collapsable Test Files")
    list1.append("Percent of Total Non Ixia Test Files")
    list1.append("Potential Time Saving (minute)")
    list1.append("Switch Saving")
    list1.append("Ixia Saving")
    list1.append("Host Saving")
    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, nix_test_t, boxID)
    arGraph3b.append("Test files")
    arGraph3b.append(nix_total - nix_test_t)
    boxID = boxID + 1
    percent = calc_percent_w_sign(nix_test_t, nix_total)
    hc.html_table_mid(optifile, percent, boxID)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, nix_test_t, 1, inputID, scriptID, boxID, 4)
    dictBoxID[boxID] = nix_test_t
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_sw_t, boxID)
    arGraph3b.append("Switch")
    arGraph3b.append(nix_total_sw - nix_sw_t)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_ix_t, boxID)
    arGraph3b.append("Ixia")
    arGraph3b.append(nix_total_ix - nix_ix_t)
    boxID = boxID + 1
    hc.html_table_mid(optifile, nix_vm_t, boxID)
    arGraph3b.append("Host")
    arGraph3b.append(nix_total_vm - nix_vm_t)
    boxID = boxID + 1
    hc.html_table_script(optifile, scriptID, inputID, dictBoxID)
    inputID = inputID + 1
    scriptID = scriptID + 1
    hc.html_table_end(optifile)

    hc.html_break(optifile)
    hc.html_graph(optifile, 3, 300, 60)

    hc.html_line(optifile)
    hc.html_collapse_start(optifile, "Show non-ixia topology test files", num, None)
    num = num + 1
    for topology in (sorted(TOPO_LIST, key=operator.attrgetter("testfilecount"),
                reverse=True)):
        if topology.ixia_count is 0:
            hc.html_header(optifile, topology.topology_name, 3, 0)
            fcs = topology.testfilecount - 1
            topo_str = ("[Test file count: " + str(topology.testfilecount) +
                            "] [Time saving: " + str(fcs * 4) +
                            " mins] [Switch saving: " + (str(fcs *
                            topology.switches_count) + "] [Ixia saving: " +
                            str(fcs * topology.ixia_count) + "] [VM saving: "
                            + str(fcs * topology.vm_count) + "]"))
            hc.html_collapse_start(optifile, "Show Test Files", num, topo_str)
            num = num + 1
            hc.html_break(optifile)
            for test in topology.testnames:
                hc.html_paragraph_color(optifile, test, 1)
            hc.html_collapse_end(optifile)

            hc.html_break(optifile)
    hc.html_collapse_end(optifile)
    #hc.html_line(optifile)

    #-----------------------Ixia topologies------------
    hc.html_header(optifile, "Ixia Topologies", 2, 0)
    # hc.html_paragraphCenter(optifile, "Total tests with Ixia count: "
            #+ str(ix_total))
    dictBoxID.clear()
    arGraph4a = []
    arGraph4b = []
    list1 = []
    list1.append("Total Ixia Test Files")
    list1.append("Estimated Provisioning Time")
    list1.append("Estimated Parallel Test Run Time")
    list1.append("Total Switches")
    list1.append("Total Ixia")
    list1.append("Total Hosts")

    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, ix_total, boxID)
    arGraph4a.append("Test files")
    arGraph4a.append(ix_total)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, 0, 0, inputID, scriptID, 0, 8)  # time edit
    hc.html_table_mid2(optifile, ix_total, 1, inputID, scriptID, boxID, 8)
    dictBoxID[boxID] = ix_total
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_sw, boxID)
    arGraph4a.append("Switch")
    arGraph4a.append(ix_total_sw)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_ix, boxID)
    arGraph4a.append("Ixia")
    arGraph4a.append(ix_total_ix)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_total_vm, boxID)
    arGraph4a.append("Hosts")
    arGraph4a.append(ix_total_vm)
    boxID = boxID + 1
    hc.html_table_end(optifile)
    hc.html_break(optifile)

    list1 = []
    list1.append("Collapsable Test Files")
    list1.append("Percent of Total Ixia Test Files")
    list1.append("Potential Time Saving (minute)")
    list1.append("Switch Saving")
    list1.append("Ixia Saving")
    list1.append("Host Saving")
    hc.html_table_start(optifile, list1)
    hc.html_table_mid(optifile, ix_test_t, boxID)
    arGraph4b.append("Test files")
    arGraph4b.append(ix_total - ix_test_t)
    boxID = boxID + 1
    percent = calc_percent_w_sign(ix_test_t, ix_total)
    hc.html_table_mid(optifile, percent, boxID)
    boxID = boxID + 1
    hc.html_table_mid2(optifile, ix_test_t, 1, inputID, scriptID, boxID, 8)
    dictBoxID[boxID] = ix_test_t
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_sw_t, boxID)
    arGraph4b.append("Switch")
    arGraph4b.append(ix_total_sw - ix_sw_t)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_ix_t, boxID)
    arGraph4b.append("Ixia")
    arGraph4b.append(ix_total_ix - ix_ix_t)
    boxID = boxID + 1
    hc.html_table_mid(optifile, ix_vm_t, boxID)
    arGraph4b.append("Host")
    arGraph4b.append(ix_total_vm - ix_vm_t)
    boxID = boxID + 1
    hc.html_table_script(optifile, scriptID, inputID, dictBoxID)
    inputID = inputID + 1
    scriptID = scriptID + 1
    hc.html_table_end(optifile)

    hc.html_break(optifile)
    hc.html_graphStart(optifile)
    hc.html_graphScript(optifile, 1, arGraph1a, "Before Optimization",
            arGraph2a, "After Optimization", "Tests without Ixia", "column")
    hc.html_graphScript(optifile, 2, arGraph1b, "Before Optimization",
            arGraph2b, "After Optimization", "Tests Using Ixia", "column")
    hc.html_graphScript(optifile, 3, arGraph3a, "Before Optimization",
            arGraph3b, "After Optimization", "Tests without Ixia", "column")
    hc.html_graphScript(optifile, 4, arGraph4a, "Before Optimization",
            arGraph4b, "After Optimization", "Tests Using Ixia", "column")
    hc.html_graphEnd(optifile)
    hc.html_graph(optifile, 4, 300, 60)

    hc.html_line(optifile)
    hc.html_collapse_start(optifile, "Show ixia topology test files", num, None)
    num = num + 1

    for topology in (sorted(TOPO_LIST, key=operator.attrgetter("testfilecount"),
                reverse=True)):
        if topology.ixia_count is not 0:
            hc.html_header(optifile, topology.topology_name, 3, 0)
            fcs = topology.testfilecount - 1
            topo_str = ("[Test file count: " + str(topology.testfilecount) +
                            "] [Time saving: " + str(fcs * 4) +
                            " mins] [Switch saving: " + (str(fcs *
                            topology.switches_count) + "] [Ixia saving: " +
                            str(fcs * topology.ixia_count) + "] [VM saving: "
                            + str(fcs * topology.vm_count) + "]"))
            hc.html_collapse_start(optifile, "Show Test files", num, topo_str)
            num = num + 1
            hc.html_break(optifile)
            for test in topology.testnames:
                hc.html_paragraph_color(optifile, test, 1)
            hc.html_collapse_end(optifile)

            hc.html_break(optifile)
    hc.html_collapse_end(optifile)

    hc.html_end(optifile)

    '''print("======Non Ixia=====")
    print("Total tests: " + str(nix_total))
    print("Test count: " + str(nix_test))
    print("Switch count: " + str(nix_sw))
    print("Ixia count: " + str(nix_ix))
    print("Vm count: " + str(nix_vm))
    print("")
    print("======Ixia=====")
    print("Total tests: " + str(ix_total))
    print("Test count: " + str(ix_test))
    print("Switch count: " + str(ix_sw))
    print("Ixia count: " + str(ix_ix))
    print("Vm count: " + str(ix_vm))'''

    # ======Dash html file========

    hc.html_intro(dashfile, "Dashboard Summary")
    hc.html_main_head(dashfile, "Dashboard", dashfile, summaryfile,
        optifile, all_topo_file)

    hc.html_pagetitle(dashfile, "Dashboard")
    hc.html_line(dashfile)
    hc.html_paragraph(dashfile, "Report generated on: " + timestamp, 0)
    for repo in git_repo:
        hc.html_paragraph(dashfile, "Using repository: " + repo, 0)
    hc.html_paragraph(dashfile, "Total test file count: " + str(totalfile), 0)
    hc.html_paragraph(dashfile, "Total test count: " + str(totaltest), 0)

    hc.html_line(dashfile)
    hc.html_header(dashfile, "Top 3 Most Common Topologies", 2, 0)
    arGraph3 = []
    max_topo_list = find_max("testfilecount")
    count = 0
    for topo in max_topo_list:
        arGraph3.append(topo.topology_name)
        p3 = calc_percent(topo.testfilecount, totalfile)
        arGraph3.append(str(p3))
        count = count + topo.testfilecount
        topo.html_table(dashfile, totalfile, boxID)
        hc.html_break(dashfile)
        hc.html_line(dashfile)
        hc.html_break(dashfile)
    arGraph3.append("Other")
    p3 = calc_percent((totalfile - count), totalfile)
    arGraph3.append(str(p3))
    hc.html_graph(dashfile, 3, 300, 60)

    hc.html_header(dashfile, "Top 3 Topologies with Most Switches", 2, 0)
    arGraph4 = []
    max_sw_list = find_max("total_switch")
    count = 0
    for topo in max_sw_list:
        arGraph4.append(topo.topology_name)
        p4 = calc_percent(topo.total_switch, ix_total_sw + nix_total_sw)
        arGraph4.append(str(p4))
        count = count + topo.total_switch
        topo.html_table(dashfile, totalfile, boxID)
        hc.html_break(dashfile)
        hc.html_line(dashfile)
        hc.html_break(dashfile)
    arGraph4.append("Other")
    p4 = calc_percent(ix_total_sw + nix_total_sw - count,
                ix_total_sw + nix_total_sw)
    arGraph4.append(str(p4))
    hc.html_graph(dashfile, 4, 300, 60)

    hc.html_header(dashfile, "Top 3 Topologies with Most Ixia Ports", 2, 0)
    arGraph5 = []
    max_ixia_list = find_max("total_ixia")
    count = 0
    for topo in max_ixia_list:
        arGraph5.append(topo.topology_name)
        p5 = calc_percent(topo.total_ixia, ix_total_ix + nix_total_ix)
        arGraph5.append(str(p5))
        count = count + topo.total_ixia
        topo.html_table(dashfile, totalfile, boxID)
        hc.html_break(dashfile)
        hc.html_line(dashfile)
        hc.html_break(dashfile)
    arGraph5.append("Other")
    p5 = calc_percent(ix_total_ix + nix_total_ix - count,
                ix_total_ix + nix_total_ix)
    arGraph5.append(str(p5))
    hc.html_graph(dashfile, 5, 300, 60)

    hc.html_header(dashfile, "Top 3 Topologies with Most Hosts", 2, 0)
    arGraph6 = []
    max_host_list = find_max("total_vm")
    count = 0
    for topo in max_host_list:
        arGraph6.append(topo.topology_name)
        p6 = calc_percent(topo.total_vm, ix_total_vm + nix_total_vm)
        arGraph6.append(str(p6))
        count = count + topo.total_vm
        topo.html_table(dashfile, totalfile, boxID)
        hc.html_break(dashfile)
        hc.html_line(dashfile)
        hc.html_break(dashfile)
    arGraph6.append("Other")
    p6 = calc_percent(ix_total_vm + nix_total_vm - count,
                ix_total_vm + nix_total_vm)
    arGraph6.append(str(p6))
    hc.html_graph(dashfile, 6, 300, 60)

    hc.html_graphStart(dashfile)
    hc.html_graphScript(dashfile, 3, arGraph3, "Test file count",
            None, None, "Top 3 Topology vs Other", "pie")
    hc.html_graphScript(dashfile, 4, arGraph4, "Switches",
            None, None, "Top 3 Topology with Most Switches vs Other", "pie")
    hc.html_graphScript(dashfile, 5, arGraph5, "Ixia",
            None, None, "Top 3 Topology with Most Ixia vs Other", "pie")
    hc.html_graphScript(dashfile, 6, arGraph6, "Host",
            None, None, "Top 3 Topology with Most Host vs Other", "pie")
    hc.html_graphEnd(dashfile)

    hc.html_end(dashfile)
    # ======Summary html file========
    hc.html_intro(summaryfile, "Summary")
    hc.html_main_head(summaryfile, "Summary", dashfile, summaryfile,
            optifile, all_topo_file)

    hc.html_pagetitle(summaryfile, "Summary Listing")
    hc.html_line(summaryfile)
    hc.html_paragraph(summaryfile, "Report generated on: " + timestamp, 0)
    for repo in git_repo:
        hc.html_paragraph(summaryfile, "Using repository: " + repo, 0)
    # hc.html_break(summaryfile)
    hc.html_paragraph(summaryfile, "Total test file count: " + str(totalfile), 0)
    hc.html_paragraph(summaryfile, "Total test count: " + str(totaltest), 0)

    hc.html_line(summaryfile)
    hc.html_header(summaryfile, "Top 3 Most Common Topologies", 2, 0)
    max_topo_list = find_max("testfilecount")
    for topo in max_topo_list:
        topo.write_html(summaryfile, num)
        num = num + 1

    hc.html_line(summaryfile)
    hc.html_header(summaryfile, "Top 3 Topologies with Most Switches", 2, 0)
    max_sw_list = find_max("total_switch")
    for topo in max_sw_list:
        topo.write_html(summaryfile, num)
        num = num + 1

    hc.html_line(summaryfile)
    hc.html_header(summaryfile, "Top 3 Topologies with Most Ixia Ports", 2, 0)
    max_ixia_list = find_max("total_ixia")
    for topo in max_ixia_list:
        topo.write_html(summaryfile, num)
        num = num + 1

    hc.html_line(summaryfile)
    hc.html_header(summaryfile, "Top 3 Topologies with Most Hosts", 2, 0)
    max_host_list = find_max("total_vm")
    for topo in max_host_list:
        topo.write_html(summaryfile, num)
        num = num + 1
    hc.html_end(summaryfile)

    print(">Done!")
    print("")


def setup_test_files(git_repo):
    #Parameter: takes in the hpe-enterprise git repo with ft stress tests
    #Returns the folder created with all the copied tests
    test_folder = "topology_script_tests_folder"
    if os.path.exists(test_folder):
        print("Updating hpe-enterprise-tests..")
        subprocess.call(["cd " + test_folder + "/hpe-enterprise-tests "
        + "&& git pull "], shell=True)
    else:
        subprocess.call(["mkdir " + test_folder], shell=True)
        subprocess.call(["cd " + test_folder + "&& git clone "
                    + git_repo], shell=True)
    return test_folder


def setup_ops_repo(test_folder, ops_repo):
    #Parameters: takes the tests folder and the ops-main repo
    #Returns the list of all the sub feature repos that it copied
    ar = []
    path_ops = test_folder + "/ops-build"

    if not os.path.exists(path_ops):
        ar.append("make configure genericx86-64")
        ar.append("make devenv_init")
        subprocess.call(["cd " + test_folder + "&& git clone "
                    + ops_repo], shell=True)
    else:
        print("Updating all existing repos...")
        subprocess.call(["cd " + path_ops + " && make git_pull "
                    + ops_repo], shell=True)
    ar.append("make devenv_list_all")

    files = ""
    for cmd in ar:
        print("")
        print("Executing: " + str(cmd))
        if "list_all" in cmd:
            files = commands.getstatusoutput("cd " + path_ops + " && " + cmd)[1]
            print(files)
            continue
        subprocess.call(["cd " + path_ops + " && " + cmd], shell=True)

    while "*" in files:
        list1 = files.split("*", 1)
        if "*" in list1[1]:
            list2 = list1[1].split("*", 1)
            files = "*" + list2[1]
            cmd = list2[0]
            cmd = cmd.strip()
            if "opennsl-cdp" in cmd:
                continue
            print("Adding: " + cmd)
            subprocess.call(["cd " + path_ops + " && " + "make devenv_add "
                    + cmd], shell=True)
        else:
            cmd = list1[1]
            cmd = cmd.strip()
            print("Adding: " + cmd)
            subprocess.call(["cd " + path_ops + " && " + "make devenv_add "
                    + cmd], shell=True)
            files = list1[1]



def clean_up(test_folder):
    #Parameter: the folder with the tests
    #Function: recursivley deletes the folder and the tests
    if os.path.exists(test_folder):
        subprocess.call(["rm -rf " + test_folder], shell=True)


def process_folders(git_repo, test_folder):
    for repo in git_repo:
        folder = repo.rsplit("/", 1)
        print(folder)


# =========Main ==============
def main():
    # ========Define git repo=======
    git_repo = []
    git_repo.append("git://git-nos.rose.rdlabs.hpecorp.net/hpe/hpe-"
        "enterprise-tests")
    git_repo.append("https://git.openswitch.net/openswitch/ops-build")

    test_folder = "topology_script_tests_folder"
    #Setting up the test folder
    test_folder = setup_test_files(git_repo[0])
    print("")
    print(">Copied folder: " + git_repo[0])

    setup_ops_repo(test_folder, git_repo[1])
    print("")
    print(">Copied folder: " + git_repo[1])

    process_folders(git_repo, test_folder)

    #process all the test files in the test folder
    get_all_pytests(test_folder)
    print(">Dictionary topology created")

    #clean_up(test_folder)
    print(">Cleaning up files")
    #report the data
    write_summary(git_repo)
    #subprocess.call(["firefox " + summaryfile + ".html"], shell=True)

# =========Call Main==========
main()
