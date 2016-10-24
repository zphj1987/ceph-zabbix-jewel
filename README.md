ceph-zabbix-jewel

是基于https://github.com/thelan/ceph-zabbix的修改版本，在整体思路一致的情况下,进行一些优化和新的适配，方便扩展

##安装

将 zabbix_agent_ceph_plugin.conf 拷贝到 /etc/zabbix/zabbix_agentd.d/ 路径下面



将 ceph-status.py 拷贝到可执行的路径下面，现在先规定为 /sbin/ceph-status.py

##模板

模板目前还处于开发节点，一个个添加

