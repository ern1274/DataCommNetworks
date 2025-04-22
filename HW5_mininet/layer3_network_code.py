from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI

def subnet():
    net = Mininet(controller=Controller, waitConnected=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='20.10.172.0')
    h2 = net.addHost('h2', ip='20.10.172.1')
    h3 = net.addHost('h3', ip='20.10.172.64')
    h4 = net.addHost('h4', ip='20.10.172.65')
    h5 = net.addHost('h5', ip='20.10.172.193')
    h6 = net.addHost('h6', ip='20.10.172.194')

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
    h1.setIP('20.10.172.0/26')
    h2.setIP('20.10.172.1/26')
    h3.setIP('20.10.172.64/25')
    h4.setIP('20.10.172.65/25')
    h5.setIP('20.10.172.193/27')
    h6.setIP('20.10.172.194/27')


    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    subnet()