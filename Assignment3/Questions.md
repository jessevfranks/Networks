1. A Time to Live (TTL) value, contrary to its name, does not actually represent a time limit, but rather  
a "hop" limit. By incrementing the number of allowed hops, we can incrementally get farther and farther into a  
requests routing path. We can print off each next hop, and view the full path a request makes.
2. Traceroute uses high UDP port numbers for two main reasons. One is to avoid interfering with  
other, common, lower ports that may be in use already. Also, by using a higher port, the destination  
is more unlikely to have a service running on the port, meaning the "port unreachable" response it  
easier to achieve.
3. The responses I received indicate the hostname, IP address, and the RTT, or that a timeout occurred.  
The format I have is "hostname (IP address) RTT". When a timeout occurs, a "*" is printed
4. If a timeout ("*") occurs, that does not mean that subsequent hops will also display "*".  
An individual "*" likely means that the server at that hop chose not to respond to our probe,  
not that there is necessarily an issue of that it doesn't exist. As TTL increments, servers that do respond  
be reached, or at least the destination will.
5. In Windows, ICMP echo requests are used vs UDP datagram probes. When a router is hit, it returns an ICMP  
"Time Exceeded" message that will include its IP and RTT. The idea and result is more or less the  
same, just with a different probe format. I actually ran into some trouble with getting my traceroute to work  
when running on windows, and ended up having to use linux (WSL) in order to successfully receive responses to  
my probes. 