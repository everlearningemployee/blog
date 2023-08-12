```yaml
network:
  ethernets:
    eth0:
      addresses:
      - 172.23.154.144/20
      gateway4: 172.23.144.1
      nameservers:
        addresses:
        - 8.8.8.8
  version: 2
```

```bash
$ ip -j addr show scope global | jq '.[0].ifname'
"eth0"
```

```bash
$ ip route | awk '/^default/{print $3}'
172.23.144.1
```

```bash
$ ip -j route | jq '.[] | select(.dst=="default").gateway'
"172.23.144.1"
```

```bash
$ ip addr show scope global | awk '/inet/{print $2}'
172.23.154.144/20
```

```bash
$ ip -j addr show scope global | jq '.[0].addr_info[0] | .local + "/" + (.prefixlen|tostring)'
"172.23.154.144/20"
```

```bash
$ ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 52:54:00:f3:ae:dc brd ff:ff:ff:ff:ff:ff
    inet 172.23.154.144/20 brd 172.23.159.255 scope global dynamic eth0
       valid_lft 86273sec preferred_lft 86273sec
    inet6 fe80::5054:ff:fef3:aedc/64 scope link
       valid_lft forever preferred_lft forever
```

```bash
$ ip route
default via 172.23.144.1 dev eth0 proto dhcp src 172.23.154.144 metric 100
172.23.144.0/20 dev eth0 proto kernel scope link src 172.23.154.144
172.23.144.1 dev eth0 proto dhcp scope link src 172.23.154.144 metric 100       
```

```json
$ ip -j addr show scope global | jq
[
  {
    "ifindex": 2,
    "ifname": "eth0",
    "flags": [
      "BROADCAST",
      "MULTICAST",
      "UP",
      "LOWER_UP"
    ],
    "mtu": 1500,
    "qdisc": "mq",
    "operstate": "UP",
    "group": "default",
    "txqlen": 1000,
    "link_type": "ether",
    "address": "52:54:00:0b:eb:81",
    "broadcast": "ff:ff:ff:ff:ff:ff",
    "addr_info": [
      {
        "family": "inet",
        "local": "172.23.151.6",
        "prefixlen": 20,
        "broadcast": "172.23.159.255",
        "scope": "global",
        "dynamic": true,
        "label": "eth0",
        "valid_life_time": 72084,
        "preferred_life_time": 72084
      },
      {}
    ]
  }
]
```

```json
$ ip -j route | jq
[
  {
    "dst": "default",
    "gateway": "172.23.144.1",
    "dev": "eth0",
    "protocol": "dhcp",
    "prefsrc": "172.23.151.6",
    "metric": 100,
    "flags": []
  },
  {
    "dst": "172.23.144.0/20",
    "dev": "eth0",
    "protocol": "kernel",
    "scope": "link",
    "prefsrc": "172.23.151.6",
    "flags": []
  },
  {
    "dst": "172.23.144.1",
    "dev": "eth0",
    "protocol": "dhcp",
    "scope": "link",
    "prefsrc": "172.23.151.6",
    "metric": 100,
    "flags": []
  }
]
```

## 기타

- [WSL2 활용도를 높여주는 고정 IP 설정 | 요즘IT (wishket.com)](https://yozm.wishket.com/magazine/detail/1386/?fbclid=IwAR0jHhB3R60Pn-mlauxao4pSvRwDuHRuQNTO5cytFDqkHjhZSMMfZe3N-cA)
