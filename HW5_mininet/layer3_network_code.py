from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI

def setup_net():
    """
    A function that sets up mininet topography
    3 switches with 2 hosts each and 1 router/host connecting everything
    """
    net = Mininet(controller=Controller, waitConnected=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    r1 = net.addHost('r1')
    h1 = net.addHost('h1', ip='20.10.172.1/26', defaultRoute='via 20.10.172.62')
    h2 = net.addHost('h2', ip='20.10.172.2/26', defaultRoute='via 20.10.172.62')
    h3 = net.addHost('h3', ip='20.10.172.65/25', defaultRoute='via 20.10.172.126')
    h4 = net.addHost('h4', ip='20.10.172.66/25', defaultRoute='via 20.10.172.126')
    h5 = net.addHost('h5', ip='20.10.172.193/27', defaultRoute='via 20.10.172.222')
    h6 = net.addHost('h6', ip='20.10.172.194/27', defaultRoute='via 20.10.172.222')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s3)
    net.addLink(h6, s3)

    net.addLink(r1, s1)
    net.addLink(r1, s2)
    net.addLink(r1, s3)

    info('*** Starting network\n')
    net.start()

    r1.cmd('ifconfig r1-eth0 20.10.172.62/26')
    r1.cmd('ifconfig r1-eth1 20.10.172.126/25')
    r1.cmd('ifconfig r1-eth2 20.10.172.222/27')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    #info('*** Running CLI\n')
    #CLI(net)
    net.pingAll()
    info('*** Stopping network')
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    setup_net()