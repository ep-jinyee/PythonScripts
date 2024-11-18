## _04_mac_whisper.py

If you're using this script, you need to run it as root, e.g. use the following command

```
sudo python _04_mac_whisper.py --interface=enp6s0 --dst-mac=88:97:df:ff:ff:ff --payload='{"model":"EDGELPR","mac":"88:97:DF
:FF:FF:FF","ipv4":"192.168.88.247","subnet":"255.255.255.0","dns":["8.8.8.8","8.8.4.4"],"gateway":"192.168.88.1","arp_resp":"192.168.88.169"}'
```