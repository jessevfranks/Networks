![Traceroute output](../images/Spotify%20traceroute%20output.png)  
Here we can see the output of the traceroute when using both a hostname and an IP address.  
Notice how the second run uses the IP address that was printed out from the first.  
We can see that the routes are very similar, with only slight differences. Additionally, since I ran this on campus,  
some of the names are recognizable buildings on campus (Peabody and Boyd).
<br>
<br>
![Wireshark traffic](../images/Spotify%20wireshark%20traffic.png)
Here we can view the wireshark traffic that was captured. There were 9 hops, and we see 9 corresponding UDP probes.  
Two different responses are visible, Tim-to-Live exceeded and Destination Unreachable. TTL exceeded is what we expect  
to see at each hop, as this signifies that the maximum number of hops has been reached. When the request reaches the  
destination, we see the message about the port being unreachable. This is the normal response for when a probe reaches  
the destination.

![TTL value](../images/TTL%203.png)
Here we view the data that was inside a sent probe packet. I chose the 3rd UDP probe sent to inspect. Because this  
is the 3rd UDP probe, we also see that the TTL value (highlighted) is 3.