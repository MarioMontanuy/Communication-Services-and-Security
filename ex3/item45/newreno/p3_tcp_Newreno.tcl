#################################################
#
#   Problema 3 
#   Alumnes: Mario Montanuy, Chaymaa Dkouk
#
#################################################

# Start with agent: RFC793 with slow start
set trailer .tcp_Newreno_ss

# Define output files
set tracefile sor$trailer
set cwfile cw$trailer

# Creating the simulator object
set ns [new Simulator]

#file to store results
set nf [open $tracefile  w]
$ns trace-all $nf

set nff [open $cwfile  w]


#Finishing procedure
proc finish {} {
    global ns nf nff tracefile cwfile trailer 
    $ns flush-trace
    # Process "sor.tr" to get sent packets
    #exec awk {{ if ($1=="-" && $3==1 && $4=2) print $2, 49}}  $tracefile > tx$trailer
    # Process "sor.tr" to get dropped packets
    #exec awk {{ if ($1=="d" && $3==2 && $4=3) print $2, 44}}  $tracefile  > drop$trailer
    #exec awk {{  print $2,$3}}  $tracefile  > out$trailer
    close $nf
    close $nff
    exit 0
}

# TCP times recording procedure
proc record { } {
	global ns tcp1 nff
	# Getting the congestion window
    set cw  [$tcp1 set cwnd_] 
    set rtt  [expr [$tcp1 set rtt_]  * [$tcp1 set tcpTick_]]
    # set rto [expr [$tcp1 set rto_] * [$tcp1 set tcpTick_]]
	set now [$ns now]
#	puts $nff "$now $cw $rtt $rto"
	puts $nff "$now $cw $rtt"
	$ns at [expr $now+0.1] "record"
}

# Create 4 nodes
#
#  n0
#  \
#   \
#    n2--------n3
#   /
#  /
# n1
 
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

# Duplex lines between nodes
$ns duplex-link $n0 $n2 0.25Mb 20ms DropTail
$ns duplex-link $n1 $n2 0.25Mb 20ms DropTail
$ns duplex-link $n2 $n3 0.05Mb 500ms DropTail

# Set node 2 buffer size
$ns queue-limit $n2 $n3 20


# Node 0: UDP agent
set udp0 [new Agent/UDP]
$udp0 set class_ 0
$ns attach-agent $n0 $udp0

# UDP agent: Exponential traffic generator
set cbr0 [new Application/Traffic/Exponential]
$cbr0 set rate_ 0.05Mbps
$cbr0 attach-agent $udp0


# Node 3: null agent for UDP
set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

# Connect node 0 to node 3
$ns connect $udp0 $null0

# UDP traffic activates 20 s after start and ends 20 s before ending simulation
$ns at 20.0 "$cbr0 start"
$ns at 180.0 "$cbr0 stop"

# Node 1: RFC793 with slow start
set tcp1 [new Agent/TCP/Newreno]
$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1
$tcp1 set tcpTick_ 0.01
$tcp1 set window_ 10
$tcp1 set packetSize_ 1000

# TCP agent: CBR traffic generator
set cbr1 [new Application/Traffic/CBR]
$cbr1 set rate_ 0.05Mbps
$cbr1 attach-agent $tcp1
$ns at 0.0 "$cbr1 start"
$ns at 0.0 "record"

# Node 3: tcp sink for TCP
set null1 [new Agent/TCPSink]
$ns attach-agent $n3 $null1

# Connect node 1 to node 3
$ns connect $tcp1 $null1 

# Stop simulation at  20 s.
$ns at 200.0 "finish"


#Run simulation
$ns run
