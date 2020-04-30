# Routing-via-Multi-Commodity-Flow
We explore the problem of routing in a quantum internet using multi-commodity flow. In this project, we assume that all of the repeaters are based on atomic ensemble and linear optics. Moreover, we assume that any node in the network can act as an end node as well as a repeater node.

Here the file Surfnet.graphml.xml contains the .graphml file corresponding to the SURFnet topology. The file lp_routing_testing.py takes the .graphml file as input and then generates random demands (s,e,l), where s is the source, e is the destination, and l is the upper bound on the length of the path.

On the basis of this demand, we compute the modified network and in order to get a total achievable rate, we construct a linear program (LP). Later we feed this LP formulation to an LP solver and get the optimal total achievable rate for all of the demands. 
