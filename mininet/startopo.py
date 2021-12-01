from mininet.topo import Topo  

class StarTopo( Topo ):  
    "Simple star topology with single switch and 12 hosts"
    
    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost( 'h1' )
        Host2 = self.addHost( 'h2' )
        Host3 = self.addHost( 'h3' )
        Host4 = self.addHost( 'h4' )
        Host5 = self.addHost( 'h5' )
        Host6 = self.addHost( 'h6' )
        Host7 = self.addHost( 'h7' )
        Host8 = self.addHost( 'h8' )
        Host9 = self.addHost( 'h9' )
        Host10 = self.addHost( 'h10' )
        Host11 = self.addHost( 'h11' )
        Host12 = self.addHost( 'h12' )
        Switch1 = self.addSwitch('s1')
        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch1 )
        self.addLink( Host3, Switch1 )
        self.addLink( Host4, Switch1 )
        self.addLink( Host5, Switch1 )
        self.addLink( Host6, Switch1 )
        self.addLink( Host7, Switch1 )
        self.addLink( Host8, Switch1 )
        self.addLink( Host9, Switch1 )
        self.addLink( Host10, Switch1 )
        self.addLink( Host11, Switch1 )
        self.addLink( Host12, Switch1 )

topos = { 'startopo': ( lambda: StarTopo() ) }  