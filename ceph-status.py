#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import json

def main():
    if sys.argv[1] == 'health':
        try:
            print get_cluster_health()
        except:
            print 255
    if sys.argv[1] == 'used_percent':
        try:
            print get_cluster_used_percent()
        except:
            print 0
    if sys.argv[1] == 'total_objects':
        try:
            print get_cluster_total_objects()
        except:
            print 0
    if sys.argv[1] == 'total_pgs':
        try:
            print get_cluster_total_pgs()
        except:
            print 0
    if sys.argv[1] == 'commit_latency':
        try:
            print get_cluster_latency("ave_commit")
        except:
            print 0
    if sys.argv[1] == 'apply_latency':
        try:
            print get_cluster_latency("ave_apply")
        except:
            print 0

##get ceph cluster status
def get_cluster_health() :
    cluster_health = commands.getoutput('timeout 10 ceph health -f json-pretty 2>/dev/null')
    try:
        json_str = json.loads(cluster_health)
        if json_str["overall_status"] == "HEALTH_OK":
            return 1
        elif  json_str["overall_status"] == "HEALTH_WARN":
            return 2
        elif  json_str["overall_status"] == "HEALTH_ERR":
            return 3
        else:
            return 255
    except:
        return 255
##get cluster used percent
def get_cluster_used_percent():
    try:
        cluster_used_percent = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null')
        json_str = json.loads(cluster_used_percent)
        cluster_used = int(json_str["pgmap"]["bytes_used"])
        cluster_total = int(json_str["pgmap"]["bytes_total"])
        return    "%.3f"   %(cluster_used/float(cluster_total))
    except:
        return 0
##get cluster total objects(has bug for get objects)
def get_cluster_total_objects():
    get_cluster_total_objects = commands.getoutput('timeout 10 ceph -s  2> /dev/null|grep pgmap|awk \'{print $10}\'')
    try:
        if len(get_cluster_total_objects) != 0:
            return get_cluster_total_objects
        else:
            return 0
    except:
        return 0
#get cluster total pg
def get_cluster_total_pgs():
    try:
        get_cluster_total_pgs = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null')
        json_str = json.loads(get_cluster_total_pgs)
        return json_str["pgmap"]["num_pgs"]
    except:
        return 0
#get cluster average latency
def get_cluster_latency(arg):
    if arg =="ave_commit":
        osd_commit_list = []
        try:
            get_cluster_latency_commit = commands.getoutput('timeout 10 ceph osd perf -f json-pretty 2>/dev/null')
            json_str = json.loads(get_cluster_latency_commit)
            for item in json_str["osd_perf_infos"]:
                osd_commit_list.append(int(item["perf_stats"]["commit_latency_ms"]))
            return sum(osd_commit_list)/len(osd_commit_list)
        except:
            return 0
    if arg =="ave_apply":
        osd_apply_list = []
        try:
            get_cluster_latency_apply = commands.getoutput('timeout 10 ceph osd perf -f json-pretty 2>/dev/null')
            json_str = json.loads(get_cluster_latency_apply)
            for item in json_str["osd_perf_infos"]:
                osd_apply_list.append(int(item["perf_stats"]["apply_latency_ms"]))
            return sum(osd_apply_list)/len(osd_apply_list)
        except:
            return 0

if __name__ == '__main__':
    main()
