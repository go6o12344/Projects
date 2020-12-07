This program simulates the activity of a network of routers. It gets input from the .txt files 
"routers.txt", "network.txt", "packages.txt". "routers.txt" describes the routers in the network,
namely each router has a name and an IP address. "network.txt" describes direct connections between
the routers. It requires two IPs, and the connection is double-ended. "packages.txt" describes
the packages, more specifically packages need to have some content(a string in this case), a sender
IP and a receiver IP. Each separate query should be on a new line, and no empty lines should be left
at the bottom of any document.