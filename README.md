# Some helper scripts

##### ./mcp - tools usefull with Mirantis MCP
```
usage: ip_inventory.py [-h] [--cidr CIDR] [--networks]

List IP address inventory based on Salt grains

optional arguments:
  -h, --help   show this help message and exit
  --cidr CIDR  Show only specified network
  --networks   Show available networks

  Reads YAML from STDIN and outputs IP to minion mapping

  EXAMPLES:
    > salt '*' grains.get ipv4 --out yaml | ip_inventory.py
    > salt '*' grains.get ipv4 --out yaml | ip_inventory.py --cind 192.168.0.0/24
```
##### ./openstack - OpenStack related utils
```
usage: get_qos_specs_from_db.py [-h] --vm-uuid VM_UUID [--host HOST]
                                [--port PORT] [--db DB] [--user USER]
                                [--password PASSWORD]
                                [--write-iops-sec WRITE_IOPS_SEC]
                                [--read-iops-sec READ_IOPS_SEC]
                                [--clear-qos] [--dry-run]

Show and modify QoS applied to Cinder volume attached to the VM

optional arguments:
  -h, --help            show this help message and exit
  --vm-uuid VM_UUID     UUID of the VM
  --host HOST           name of host which serves DB
  --port PORT           TCP port of MySQL server
  --db DB               OpenStack Nova service database name
  --user USER           DB user user to authenticate as
  --password PASSWORD   DB password password to authenticate with
  --write-iops-sec WRITE_IOPS_SEC
                        Apply write limit to VM's block devices
  --read-iops-sec READ_IOPS_SEC
                        Apply read limit to VM's block devices
  --clear-qos           Clear IO limits for VM's block devices
  --dry-run             Lists steps but does not update database

```
**EXAMPLES:**

Look at current limits:
```
root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b {"write_iops_sec": "555", "read_iops_sec": "333"}

```

Look what `--clear` would do:
```
root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90 --clear --dry
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b {"write_iops_sec": "555", "read_iops_sec": "333"}

INFO: We are going to reset QoS limits
INFO: New value of block_device_mapping.connection_info:
{"driver_volume_type": "nfs", "mount_point_base": "/var/lib/cinder/mnt", "serial": "06e2b8b9-32da-47c4-9344-530a6262419b", "data": {"device_path": "/var/lib/nova/mnt/9b279265fe46ef47b940e5519d84a673/volume-06e2b8b9-32da-47c4-9344-530a6262419b", "name": "volume-06e2b8b9-32da-47c4-9344-530a6262419b", "encrypted": false, "qos_specs": null, "export": "172.18.52.245:/vol_cin3", "access_mode": "rw", "options": null}, "connector": {"initiator": "iqn.1993-08.org.debian:01:dbcdd584e44", "ip": "192.168.0.11", "platform": "x86_64", "host": "node-11.domain.tld", "os_type": "linux2", "multipath": false}}

```

Clear current limits and check result:
```
root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90 --clear
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b {"write_iops_sec": "555", "read_iops_sec": "333"}

INFO: We are going to reset QoS limits
INFO: New value of block_device_mapping.connection_info:
{"driver_volume_type": "nfs", "mount_point_base": "/var/lib/cinder/mnt", "serial": "06e2b8b9-32da-47c4-9344-530a6262419b", "data": {"device_path": "/var/lib/nova/mnt/9b279265fe46ef47b940e5519d84a673/volume-06e2b8b9-32da-47c4-9344-530a6262419b", "name": "volume-06e2b8b9-32da-47c4-9344-530a6262419b", "encrypted": false, "qos_specs": null, "export": "172.18.52.245:/vol_cin3", "access_mode": "rw", "options": null}, "connector": {"initiator": "iqn.1993-08.org.debian:01:dbcdd584e44", "ip": "192.168.0.11", "platform": "x86_64", "host": "node-11.domain.tld", "os_type": "linux2", "multipath": false}}

root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b null

```

Set limits and check result:
```
root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90 --write 99 --read 88
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b null

INFO: write_iops_sec is going to be set to 99
INFO: read_iops_sec is going to be set to 88
DEBUG: New value of block_device_mapping.connection_info: {"driver_volume_type": "nfs", "mount_point_base": "/var/lib/cinder/mnt", "serial": "06e2b8b9-32da-47c4-9344-530a6262419b", "data": {"device_path": "/var/lib/nova/mnt/9b279265fe46ef47b940e5519d84a673/volume-06e2b8b9-32da-47c4-9344-530a6262419b", "name": "volume-06e2b8b9-32da-47c4-9344-530a6262419b", "encrypted": false, "qos_specs": {"write_iops_sec": "99", "read_iops_sec": "88"}, "export": "172.18.52.245:/vol_cin3", "access_mode": "rw", "options": null}, "connector": {"initiator": "iqn.1993-08.org.debian:01:dbcdd584e44", "ip": "192.168.0.11", "platform": "x86_64", "host": "node-11.domain.tld", "os_type": "linux2", "multipath": false}}

root@host:~# ./get_qos_specs_from_db.py --pass P@ssw0rd --vm 6a480ebd-05e7-4364-837c-69d95a9b9e90
INFO: Working on DB `nova` table `block_device_mapping`
INFO: Current QoS state: 06e2b8b9-32da-47c4-9344-530a6262419b {"write_iops_sec": "99", "read_iops_sec": "88"}

```
