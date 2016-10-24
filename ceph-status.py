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
            print "unknown"

##获取集群的状态
def get_cluster_health() :
    cluster_health = commands.getoutput('ceph health -f json-pretty 2>/dev/null')
    json_str = json.loads(cluster_health)
    return json_str["overall_status"]

if __name__ == '__main__':
    main()