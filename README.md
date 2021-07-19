Dataset provided by Dr.David.J.Crandall as a part of assignement for Elements of A.I course(CSCI-B-551).

Navigation: Our goal is to find an optimal path between two given cities in the program, The optimality of the path can vary depending upon the 4 parameters mentioned in the problem. They are Distance, Time, Safe, Segment. 
State Space: The state space for this problem is the entire cities list in the given dataset.
Successor function: The Successor function for our problem returns the next city for the path for the given city with regards to a cost function.
Known issues in the datasets and possible fixes:
1.	The city-segment data has a few missing keys, Default-Dict is being used to assign default keys to the values.
2.	The city-gps data has a few missing co-ordinates and cities whenever we encounter this problem I have returned 0 for both latitude and longitude values for the respective city.
Code Description:
Functional Description:
Initially, the files have been processed and their data has been stored in dictionaries.
The city-segments file has been stored in a dictionary with the key being the city value and the value being a string of all relevant values needed for our code. We also included a delimiter(:) to distinguish.
The city-gps file has been stored as a dictionary with the key being the city name and the value being the latitude and longitude values. This function also fetches relevant latitude and longitude values for a given city which is needed to compute the heuristic function in the latter part of the code.
get_route function:
This function returns an optimal path for the given parameter. The code uses fringe which has been implemented using the Priority Queue, The priority can be computed depending upon the parameter. We also keep track of visited nodes and compute route-taken which can be later used to generate output in the mentioned format.



The logic for traversal: Initially we keep looking until the visited cities list is exhausted.
There are two parts for this, Initially, we check whether the given city is the end city and return relevant values, else we check for the successor for the given city and update values in the fringe and visited cities list.
A* Implementation: A* algorithm has been implemented by adding total cost travelled to the next cost and then we add heuristic value to that value which is later being used as a priority for priority queue. We also pop and push values to the fringe which has been used as a priority queue.
Heuristic Functions:
Distance: Manhattan Distance has been used to calculate the heuristic, However Greedy search can be used in very few cases, This can be implemented by just assigning h_fun as 0.
Time:  Optimal output is uncertain for this case yes we can fetch optimal result by Manhattan for the given test case. However, we have also added a Haversine and  Greedy approach in case this does not provide an optimal result. Check each incase the desired output is not shown.
Safe: Optimal output is uncertain for this case yes we can fetch optimal result by Manhattan for the given test case. However, we have also added a Haversine and  Greedy approach in case this does not provide an optimal result. Check each incase the desired output is not shown.
Segment: Manhattan Distance has been used to calculate the heuristic, However Greedy search can be used in very few cases, This can be implemented by just assigning h_fun as 0.

References:
1.	Assignement-0 part-1
2.	https://www.redblobgames.com/pathfinding/a-star/implementation.html
3.	https://rosettacode.org/wiki/A*_search_algorithm
4.	https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
5.	https://www.ics.uci.edu/~brgallar/week2_1.html

 




 



