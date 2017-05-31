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
    if sys.argv[1] == 'throughput_write':
        try:
            print get_cluster_throughput("write")
        except:
            print 0
    if sys.argv[1] == 'throughput_read':
        try:
            print get_cluster_throughput("read")
        except:
            print 0
    if sys.argv[1] == 'total_ops':
        try:
            print get_cluster_total_ops()
        except:
            print 0
    if sys.argv[1] == 'total_pools':
        try:
            print get_cluster_total_pools()
        except:
            print 0
    if sys.argv[1] == 'pools':
        try:
            print get_cluster_pools()
        except:
            print 0
    if sys.argv[1] == 'osds':
        try:
            print get_host_osds()
        except:
            print 0
    if sys.argv[1] == 'osds_mem_use_virt':
        try:
            print get_osd_mem_virt(sys.argv[2],"virt")
        except:
            print 0
    if sys.argv[1] == 'osds_mem_use_res':
#        try:
            print get_osd_mem_virt(sys.argv[2],"res")
#        except:
#            print 0

    if sys.argv[1] == 'osds_cpu_use':
        try:
            print get_osd_cpu(sys.argv[2])
        except:
            print 0
    
#get fio write speed (KB/s)
    if sys.argv[1] == 'fio_write_speed':
        try:
            print get_fio_write_speed()
        except:
            print 0


#get fio write speed (KB/s)
    if sys.argv[1] == 'fio_read_speed':
        try:
            print get_fio_read_speed()
        except:
            print 0


#test unit
    if sys.argv[1] == 'pool_objects':
        try:
            print get_pool_stats(sys.argv[2],"objects")
        except:
            print 0
    if sys.argv[1] == 'pool_bytes_used':
        try:
            print get_pool_stats(sys.argv[2],"used")
        except:
            print 0
    if sys.argv[1] == 'pool_throughput_write':
        try:
            print get_pool_stats(sys.argv[2],"throughput_write")
        except:
            print 0
    if sys.argv[1] == 'pool_throughput_read':
        try:
            print get_pool_stats(sys.argv[2], "throughput_read")
        except:
            print 0
    if sys.argv[1] == 'pool_op_write':
        try:
            print get_pool_stats(sys.argv[2], "op_write")
        except:
            print 0
    if sys.argv[1] == 'pool_op_read':
        try:
            print get_pool_stats(sys.argv[2], "op_read")
        except:
            print 0
    if sys.argv[1] == 'pool_id':
        try:
            print get_pool_config(sys.argv[2],"id")
        except:
            print 0
    if sys.argv[1] == 'pool_size':
        try:
            print get_pool_config(sys.argv[2],"size")
        except:
            print 0
    if sys.argv[1] == 'pool_min_size':
        try:
            print get_pool_config(sys.argv[2], "min_size")
        except:
            print 0
    if sys.argv[1] == 'pool_pg_num':
        try:
            print get_pool_config(sys.argv[2], "pg_num")
        except:
            print 0
    if sys.argv[1] == 'pool_pgp_num':
        try:
            print get_pool_config(sys.argv[2], "pgp_num")
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
#get cluster throughput write and read
def get_cluster_throughput(arg):
    if arg == "write":
        try:
            get_cluster_throughput_write = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null ')
            json_str = json.loads(get_cluster_throughput_write)
            if json_str["pgmap"].has_key('write_bytes_sec') == True:
                return  json_str["pgmap"]["write_bytes_sec"]
            else:
                return 0
        except:
            return 0
    if arg == "read":
        try:
            get_cluster_throughput_read = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null ')
            json_str = json.loads(get_cluster_throughput_read)
            if json_str["pgmap"].has_key('read_bytes_sec') == True:
                return json_str["pgmap"]["read_bytes_sec"]
            else:
                return 0
        except:
            return 0
# get cluster ops (read ,write,promote)
def get_cluster_total_ops():
    ops_list =[]
    try:
        cluster_total_ops = commands.getoutput('timeout 10 ceph -s -f json-pretty 2>/dev/null')
        json_str = json.loads(cluster_total_ops)
        if json_str["pgmap"].has_key('write_op_per_sec') == True:
            ops_list.append(int(json_str["pgmap"]["write_op_per_sec"]))
        if json_str["pgmap"].has_key('read_op_per_sec') == True:
            ops_list.append(int(json_str["pgmap"]["read_op_per_sec"]))
        if json_str["pgmap"].has_key('promote_op_per_sec') == True:
            ops_list.append(int(json_str["pgmap"]["promote_op_per_sec"]))
        return sum(ops_list)
    except:
        return 0
# get cluster total pools (has bug for get pools)
def get_cluster_total_pools():
    try:
        cluster_total_pools = commands.getoutput('timeout 10 ceph osd lspools  -f json-pretty 2>/dev/null')
        json_str = json.loads(cluster_total_pools)
        return len(json_str)
    except:
        return 0
#get all pool name
def get_cluster_pools():
    try:
        pool_list=[]
        data_dic = {}
        cluster_pools = commands.getoutput('timeout 10 ceph df -f json-pretty 2>/dev/null')
        json_str=json.loads(cluster_pools)
        for item in json_str["pools"]:
            pool_dic = {}
            pool_dic['{#POOLNAME}'] = str(item["name"])
            pool_list.append(pool_dic)
        data_dic['data'] = pool_list
        return json.dumps(data_dic,separators=(',', ':'))
    except:
        return 0

def get_host_osds():
    try:
        osd_list=[]
        data_dic={}
        osds=[]
        host_osds = commands.getoutput("mount|grep osd|awk '{print $3}'|cut -f2 -d - 2>/dev/null")
        host_osds = host_osds.splitlines()
        for osd in host_osds:
            osd_dic = {}
            osd_dic['{#OSD}'] = str(osd)
            osd_list.append(osd_dic)
        data_dic['data'] = osd_list
        return json.dumps(data_dic,separators=(',', ':'))
    except:
        return 0


def get_osd_mem_virt(osd,memtype):
#    try:
        pidfile="/var/run/ceph/osd.%s.pid" %osd
        osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
        if not osdpid :
            return 0
        elif memtype == "virt":
            osd_runmemvsz = commands.getoutput('ps -p %s  -o vsz |grep -v VSZ 2>/dev/null' %osdpid)
            return osd_runmemvsz
        elif memtype == "res":
            osd_runmemrsz = commands.getoutput('ps -p %s  -o rsz |grep -v RSZ 2>/dev/null' %osdpid)
            return osd_runmemrsz
        
#    except:
#        return 0
def get_osd_cpu(osd):
    try:
        pidfile="/var/run/ceph/osd.%s.pid" %osd
        osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
        if not osdpid :
            return 0
        osd_cpu = commands.getoutput('''ps -p %s  -o pcpu |grep -v CPU|awk 'gsub(/^ *| *$/,"")' 2>/dev/null''' %osdpid)
        return osd_cpu
    except:
        return 0

def get_fio_write_speed():
    try:
        fio_write_speed = commands.getoutput('''iotop --batch --iter 1 -P -k |grep fio|grep -v fio_write_speed|grep -v grep |awk '{print $6}'  2>/dev/null''')
        if not fio_write_speed:
            return 0
        else:
            return fio_write_speed
    except:
        return 0

def get_fio_read_speed():
    try:
        fio_read_speed = commands.getoutput('''iotop --batch --iter 1 -P -k |grep fio|grep -v fio_read_speed|grep -v grep |awk '{print $4}'  2>/dev/null''')
        if not fio_read_speed:
            return 0
        else:
            return fio_read_speed
    except:
        return 0





#get every pool object,used, throughput,ops
def get_pool_stats(poolname,stats):
    if stats == "objects":
        try:
            pool_objects = commands.getoutput('timeout 10 ceph df -f json-pretty 2>/dev/null')
            json_str = json.loads(pool_objects)
            for item in json_str["pools"]:
                if item["name"] == poolname:
                    return item["stats"]["objects"]
                    break
        except:
            return 0
    elif stats == "used" :
        try:
            pool_bytes_used = commands.getoutput("timeout 10 ceph df -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_bytes_used)
            for item in json_str["pools"]:
                if item["name"] == poolname:
                    return item["stats"]["bytes_used"]
                    break
        except:
            return 0
    elif stats == "throughput_write":
        try:
            pool_throughput_write = commands.getoutput("timeout 10 ceph osd pool stats -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_throughput_write)
            for item in json_str:
                if item["pool_name"] == poolname:
                    if item["client_io_rate"].has_key('write_bytes_sec') == True:
                        return  item["client_io_rate"]["write_bytes_sec"]
                    else:
                        return 0
        except:
            return 0

    elif stats == "throughput_read":
        try:
            pool_throughput_read = commands.getoutput("timeout 10 ceph osd pool stats -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_throughput_read)
            for item in json_str:
                if item["pool_name"] == poolname:
                    if item["client_io_rate"].has_key('read_bytes_sec') == True:
                        return item["client_io_rate"]["read_bytes_sec"]
                    else:
                        return 0
        except:
            return 0

    elif stats == "op_write":
        try:
            pool_op_write = commands.getoutput("timeout 10 ceph osd pool stats -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_op_write)
            for item in json_str:
                if item["pool_name"] == poolname:
                    if item["client_io_rate"].has_key('write_op_per_sec') == True:
                        return item["client_io_rate"]["write_op_per_sec"]
                    else:
                        return 0
        except:
            return 0

    elif stats == "op_read":
        try:
            pool_op_read = commands.getoutput("timeout 10 ceph osd pool stats -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_op_read)
            for item in json_str:
                if item["pool_name"] == poolname:
                    if item["client_io_rate"].has_key('read_op_per_sec') == True:
                        return item["client_io_rate"]["read_op_per_sec"]
                    else:
                        return 0
        except:
            return 0
    elif stats == "size":
        try:
            print stats
            pool_size = commands.getoutput("timeout 10 ceph   osd pool get rbd size -f json-pretty 2>/dev/null")
            json_str = json.loads(pool_size)
            print json_str
        except:
            return 0
#get cluster pool config
def get_pool_config(poolname,config):
    if config == "size":
        try:
            pool_size = commands.getoutput("timeout 10 ceph   osd pool get %s size -f json-pretty 2>/dev/null" %(poolname))
            json_str = json.loads(pool_size)
            return json_str["size"]
        except:
            return 0
    elif config == "id":
        try:
            pool_id = commands.getoutput("timeout 10 ceph   osd pool get %s size -f json-pretty 2>/dev/null" % (poolname))
            json_str = json.loads(pool_id)
            return json_str["pool_id"]
        except:
            return 0
    elif config == "min_size":
        try:
            pool_min_size = commands.getoutput("timeout 10 ceph   osd pool get %s min_size -f json-pretty 2>/dev/null" % (poolname))
            json_str = json.loads(pool_min_size)
            return json_str["min_size"]
        except:
            return 0
    elif config == "pg_num":
        try:
            pool_pg_num = commands.getoutput("timeout 10 ceph   osd pool get %s pg_num -f json-pretty 2>/dev/null" % (poolname))
            json_str = json.loads(pool_pg_num)
            return json_str["pg_num"]
        except:
            return 0
    elif config == "pgp_num":
        try:
            pool_pgp_num = commands.getoutput("timeout 10 ceph   osd pool get %s pgp_num -f json-pretty 2>/dev/null" % (poolname))
            json_str = json.loads(pool_pgp_num)
            return json_str["pgp_num"]
        except:
            return 0

if __name__ == '__main__':
    main()
