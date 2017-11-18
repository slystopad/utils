# utils
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
