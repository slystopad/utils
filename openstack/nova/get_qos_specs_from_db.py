#!/usr/bin/env python

import sys
import argparse
import json
import MySQLdb

parser = argparse.ArgumentParser(
  description='Show and modify QoS applied to '
              'Cinder volume attached to the VM')
parser.add_argument(
  '--vm-uuid', required=True,
  help="UUID of the VM")
parser.add_argument(
  '--host', default='',
  help="name of host which serves DB")
parser.add_argument(
  '--port', type=int, default=3306,
  help="TCP port of MySQL server")
parser.add_argument(
  '--db', default='nova',
  help="OpenStack Nova service database name")
parser.add_argument(
  '--user', default='',
  help="DB user user to authenticate as")
parser.add_argument(
  '--password', default='',
  help="DB password password to authenticate with")
parser.add_argument(
  '--write-iops-sec',
  help="Apply write limit to VM's block devices")
parser.add_argument(
  '--read-iops-sec',
  help="Apply read limit to VM's block devices")
parser.add_argument(
  '--clear-qos', action='store_true',
  help="Clear IO limits for VM's block devices")
parser.add_argument(
  '--dry-run', action='store_true',
  help="Lists steps but does not update database")
args = parser.parse_args()

try:
    print(
      'INFO: Working on DB `{}` table `block_device_mapping`'.format(
        args.db))
    db = MySQLdb.connect(
       user=args.user, passwd=args.password, db=args.db,
       host=args.host, port=args.port)
except Exception as e:
    sys.exit(e)

c = db.cursor()
c.execute(
  """select instance_uuid,volume_id,connection_info
  from block_device_mapping where deleted = 0 and instance_uuid=%s""",
  (args.vm_uuid,))
current_data = c.fetchall()

for res_item in current_data:
    volume_id = res_item[1]
    # value in DB is NULL
    if res_item[-1]:
        connection_info = json.loads(res_item[-1])
    else:
        print('INFO: [ {} {} ] connection_info is empty\n'.format(
                args.vm_uuid, volume_id))
        continue
    # sometimes DB field can still have string like 'null'
    try:
        current_specs = connection_info['data']['qos_specs']
    except:
        print('INFO: [ {} {} ] failed to get qos_specs.'
              ' Check VM state\n'.format(args.vm_uuid, volume_id))
        continue
    print(
      'INFO: [ {} {} ] Current QoS state: {}\n'.format(
        args.vm_uuid,
        volume_id,
        json.dumps(current_specs)))

    if args.clear_qos and current_specs:
        connection_info['data']['qos_specs'] = None
        print('INFO: We are going to reset QoS limits')
        print('INFO: New value of block_device_mapping.connection_info:')
        connection_info_string = json.dumps(connection_info)
        print(connection_info_string)

        if not args.dry_run:
            try:
                c.execute(
                  """update block_device_mapping
                  set connection_info=%s
                  where instance_uuid=%s""",
                  (connection_info_string, args.vm_uuid))
                db.commit()
            except Exception as e:
                sys.exit(e)
        sys.exit(0)

    new_specs = {}
    if current_specs:
        for k, v in current_specs.iteritems():
            new_specs[k] = v

    if args.write_iops_sec:
        print(
          'INFO: write_iops_sec is going to be set to {}'.format(
            args.write_iops_sec))
        new_specs['write_iops_sec'] = args.write_iops_sec

    if args.read_iops_sec:
        print(
          'INFO: read_iops_sec is going to be set to {}'.format(
            args.read_iops_sec))
        new_specs['read_iops_sec'] = args.read_iops_sec

    if args.write_iops_sec or args.read_iops_sec:
        connection_info['data']['qos_specs'] = new_specs
        connection_info_string = json.dumps(connection_info)
        print(
          'DEBUG: New value of block_device_mapping.connection_info: '
          '{}'.format(connection_info_string))

        if not args.dry_run:
            try:
                c.execute(
                  """update block_device_mapping
                  set connection_info=%s
                  where instance_uuid=%s""",
                  (connection_info_string, args.vm_uuid))
                db.commit()
            except Exception as e:
                sys.exit(e)
