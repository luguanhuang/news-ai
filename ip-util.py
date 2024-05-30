import socket
import os

class IpUtil:
    def get_hostname(self):
        # 查看当前主机名
        hostname = socket.gethostname()
        #print('当前主机名称为 : ' + hostname)
        return hostname

    def get_ipaddr(self):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        gateway = gw[2]
        host = socket.gethostname()
        return ipaddr


if __name__ == '__main__':
    ip_util = IpUtil()
    ipaddr = ip_util.get_ipaddr()
    print(ipaddr)
