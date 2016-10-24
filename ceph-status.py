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
            print "255"

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

if __name__ == '__main__':
    main()
