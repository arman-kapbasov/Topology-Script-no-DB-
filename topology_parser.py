# -*- coding: utf-8 -*-

import topology_structure as ts
import os


def parse_main(filepath):
    # Parameters: takes in filepath and creates a new topology object
    #Returns the new topology object
    new_topology = ts.Topology(filepath)
    file_parse(new_topology)
    #new_topology.print_topology_information()
    return new_topology


def file_parse(new_top):
    # Parameters: new empty topology with only filepath
    # Function: populates the objects attributes based on
    #           the parsing of filepath
    flag_top = 0
    link_flag = 0
    flag_pic = 0
    ar_ixia = []
    # print(">>Parsing pathfile right now: " + str(new_top.filepath))
    new_top.testnames.append(os.path.split(new_top.filepath)[1])
    new_top.testfilecount = new_top.testfilecount + 1
    if "_" in new_top.testnames[0]:
        feature = new_top.testnames[0].split("_", 1)[1]
        if "_" in feature:
            feature = feature.split("_", 1)[0]
        else:
            feature = feature.split(".", 1)[0]
    else:
        feature = new_top.testnames[0].split(".", 1)[0]
    feature = feature.lower()
    new_top.feat[feature] = 1
    with open(new_top.filepath, "r") as content:
        for line in content:
            if "TOPOLOGY" in line:
                flag_top = 1
                flag_pic = 1
                continue
            if flag_top:
                #=======Capture the topology picture====
                if "Node" in line:
                    flag_pic = 0
                if line.isspace():
                    continue
                if flag_pic and line.startswith("#"):
                    new_top.pic.append(line.replace("#", ""))
                if flag_pic:
                    continue
                #========Picture Topology======
                if '"""' in line:
                    flag_top = 0
                    link_flag = 0
                    continue
                if "type=ixia" in line and not line.startswith("#"):
                    split_line = line.split("]", 1)
                    ar_ixia.append(split_line[1].strip())
                    continue
                elif "type=openswitch" in line and not line.startswith("#"):
                    new_top.switches_count = new_top.switches_count + 1
                    continue
                elif "type=host" in line and not line.startswith("#"):
                    new_top.vm_count = new_top.vm_count + 1

                    if "image" not in line:
                        image = "Ubuntu"
                    else:
                        seperated_line = line.rsplit("\"", 2)
                        image = seperated_line[1]
                        image = image.replace(":", "/")
                    if image in new_top.hosts:
                        new_top.hosts[image] = new_top.hosts[image] + 1
                        continue
                    else:
                        new_top.hosts[image] = 1
                        continue
                elif "Links" in line:
                    link_flag = 1
                    continue
                if link_flag and flag_top:
                    if "--" in line and not line.startswith("#"):
                        new_top.link_count = new_top.link_count + 1
                    for ixia in ar_ixia:
                        if ixia in line and not line.startswith("#"):
                            new_top.ixia_count = new_top.ixia_count + 1
                    continue
            #========Parsing test cases ===========
            if "def test_" in line:
                new_top.testcount = new_top.testcount + 1
                continue