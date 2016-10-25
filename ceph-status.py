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
    except:
        return 255
##get cluster used percent
def get_cluster_used_percent():
    cluster_used_percent = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null')
    try:
        json_str = json.loads(cluster_used_percent)
        cluster_used = int(json_str["pgmap"]["bytes_used"])
        cluster_total = int(json_str["pgmap"]["bytes_total"])
        return    "%.3f"   %(cluster_used/float(cluster_total))
    except:
        return 0

if __name__ == '__main__':
    main()
