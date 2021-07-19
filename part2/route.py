#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: {Kethamakka.Karthikeya,kketham}
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
from typing import TextIO
from heapq import (heappop, heappush, heapify)
import numpy as np
from collections import defaultdict
import math
from decimal import *


def data_dict_generate():
    file = open('road-segments.txt', 'r')
    lines = file.read().splitlines()
    roads = defaultdict(list)
    for i in lines:
        k = i.split(" ")

        city_strt = k[0].strip()

        city_end = k[1].strip()

        distance = (k[2].strip())
        speed_limit = (k[3].strip())
        time = int(distance) / int(speed_limit)
        highway_name = k[4].strip()
        if "I-" in highway_name:
            acc_rate = 1 * int(distance) * 0.000001
        else:
            acc_rate = 2 * int(distance) * 0.000001
        roads[city_strt].append(
            city_end + ":" + distance + ":" + speed_limit + ":" + highway_name + ":" + str.format('{0:.5f}',
                                                                                                  time) + ":" + str(
                acc_rate))
        roads[city_end].append(
            city_strt + ":" + distance + ":" + speed_limit + ":" + highway_name + ":" + str(
                np.round(time, 8)) + ":" + str(acc_rate))
    return roads


def file_gps(city):
    loc = {}
    # f: TextIO
    with open('city-gps.txt', 'r') as f:
        for line in f.readlines():
            gps_data = line.split()
            city1 = gps_data[0]
            if gps_data[0] != "":
                if gps_data[1] == "" or gps_data[2] == "":
                    loc[city1] = (0, 0)
                else:
                    latitude = float(gps_data[1])
                    longitude = float(gps_data[2])
                    loc[city1] = (latitude, longitude)
    if city in loc:
        return loc[city]
    else:
        return (0, 0)


def succesor(roads, city):
    data_list = []
    for i in roads[city]:
        i = i.split(":")
        data_list.append((1, i[1], i[4], i[5], i[3], i[2], i[0]))
    return data_list


def get_route(start, end, cost):
    travelled = []
    fringe = []
    heapify(fringe)
    heappush(fringe,
             (0, 0, 0, 0, 0, "", "", 0,
              start))  # Priority, segments,distance,time,acc-rate,h-name,path,speed,current_city
    roads = data_dict_generate()

    if cost == "distance":
        route_taken = []

        while fringe:
            p = 0
            (priority, total_segment, total_dist, total_time, total_acc_rate, full_path, tot_h_info, tot_speed,
             current_city) = heappop(fringe)

            (lat1, long1) = file_gps(current_city)
            (lat2, long2) = file_gps(end)
            h_fun = abs(lat2 - lat1) + abs(long2 - long1)

            for (seg, distance, time, acc_rate, h_info, speed, city) in succesor(roads, current_city):

                if current_city == end:
                    temp_path = full_path.split(' ')
                    temp_h_info = tot_h_info.split(' ')
                    s = start
                    for k in range(1, len(temp_path)):
                        z = roads[temp_path[k]]
                        # I am in start, I have to go to temp_path[k] and start is in z
                        # find distance of start and update start = temp_path[k]
                        for x in z:
                            x = x.split(':')
                            if s in x:
                                d = x[1]
                                # print(s, temp_path[k], d)
                                s = temp_path[k]
                        if (temp_path[k] != '') or temp_h_info[k] != '':
                            route_taken.append((temp_path[k], temp_h_info[k] + " for " + str(d) + " miles"))
                    return {"total-segments": int(total_segment), "total-miles": float(format((total_dist))),
                            "total-hours": float(format((total_time))),
                            "total-expected-accidents": float(total_acc_rate), "route-taken": route_taken}
                getcontext().prec = 30

                if city not in travelled:
                    p = float(distance) + float(total_dist) + h_fun
                    current_distance = float(distance) + float(total_dist)
                    current_segement = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)
                    current_acc_rate = float(total_acc_rate) + float(acc_rate)
                    current_speed = float(tot_speed) + float(speed)

                    heappush(fringe, (p, current_segement, current_distance, current_time, current_acc_rate,
                                      str(full_path) + str(' ') + str(city), str(tot_h_info) + str(' ') + str(h_info),
                                      current_speed, city))

                    travelled.append(city)



    elif cost == "time":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_dist, total_time, total_acc_rate, full_path, tot_h_info, tot_speed,
             current_city) = heappop(fringe)

            (lat1, long1) = file_gps(current_city)
            (lat2, long2) = file_gps(end)
            R = 3963
            ll1, ll2 = math.radians(lat1), math.radians(lat2)
            dlat = math.radians(lat2 - lat1)
            dlong = math.radians(long2 - long1)
            a = math.sin(dlat / 2) ** 2 + math.cos(ll1) * math.cos(ll2) * math.sin(dlong / 2) ** 2
            # h_fun = 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))   #Use this if computing long paths
            h_fun = abs(lat2 - lat1) + abs(long2 - long1)  # use for shorter paths
            # h_fun=0    #Use this if no test case gives desired result

            for (seg, distance, time, acc_rate, h_info, speed, city) in succesor(roads, current_city):

                if current_city == end:
                    temp_path = full_path.split(' ')
                    temp_h_info = tot_h_info.split(' ')
                    s = start
                    for k in range(1, len(temp_path)):
                        z = roads[temp_path[k]]
                        # I am in start, I have to go to temp_path[k] and start is in z
                        # find distance of start and update start = temp_path[k]
                        for x in z:
                            x = x.split(':')
                            if s in x:
                                d = x[1]
                                # print(s, temp_path[k], d)
                                s = temp_path[k]
                        if (temp_path[k] != '') or temp_h_info[k] != '':
                            route_taken.append((temp_path[k], temp_h_info[k] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_dist),
                            "total-hours": float(total_time),
                            "total-expected-accidents": float(total_acc_rate), "route-taken": route_taken}

                if city not in travelled:
                    current_distance = float(distance) + float(total_dist)
                    current_segement = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)
                    current_acc_rate = float(total_acc_rate) + float(acc_rate)
                    current_speed = float(tot_speed) + float(speed)
                    p = current_time * float(speed) + h_fun

                    heappush(fringe, (p, current_segement, current_distance, current_time, current_acc_rate,
                                      str(full_path) + str(' ') + str(city), str(tot_h_info) + str(' ') + str(h_info),
                                      current_speed, city))
                    travelled.append(city)
    elif cost == "safe":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_dist, total_time, total_acc_rate, full_path, tot_h_info, tot_speed,
             current_city) = heappop(fringe)

            (lat1, long1) = file_gps(current_city)
            (lat2, long2) = file_gps(end)

            R = 3959.8743
            ll1, ll2 = math.radians(lat1), math.radians(lat2)
            dlat = math.radians(lat2 - lat1)
            dlong = math.radians(long2 - long1)
            a = math.sin(dlat / 2) ** 2 + math.cos(ll1) * math.cos(ll2) * math.sin(dlong / 2) ** 2
            # h_fun = 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            # h_fun=abs(lat2-lat1)+abs(long2-long1)
            #h_fun=0
            # R = 3959.8743
            # ll1, ll2 = math.radians(lat1), math.radians(lat2)
            # dlat = math.radians(lat2 - lat1)
            # dlong = math.radians(long2 - long1)
            # a = math.sin(dlat / 2) ** 2 + math.cos(ll1) * math.cos(ll2) * math.sin(dlong / 2) ** 2
            # h_fun = 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            h_fun = abs(lat2 - lat1) + abs(long2 - long1)
            # h_fun=0

            for (seg, distance, time, acc_rate, h_info, speed, city) in succesor(roads, current_city):

                if current_city == end:
                    temp_path = full_path.split(' ')
                    temp_h_info = tot_h_info.split(' ')
                    s = start
                    for k in range(1, len(temp_path)):
                        z = roads[temp_path[k]]
                        # I am in start, I have to go to temp_path[k] and start is in z
                        # find distance of start and update start = temp_path[k]
                        for x in z:
                            x = x.split(':')
                            if s in x:
                                d = x[1]
                                # print(s, temp_path[k], d)
                                s = temp_path[k]
                        if (temp_path[k] != '') or temp_h_info[k] != '':
                            route_taken.append((temp_path[k], temp_h_info[k] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_dist),
                            "total-hours": float(total_time),
                            "total-expected-accidents": float(total_acc_rate), "route-taken": route_taken}

                if city not in travelled:
                    current_distance = float(distance) + float(total_dist)
                    current_segement = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)
                    current_acc_rate = float(total_acc_rate) + float(acc_rate)
                    current_speed = float(tot_speed) + float(speed)
                    p = current_acc_rate + h_fun

                    heappush(fringe, (p, current_segement, current_distance, current_time, current_acc_rate,
                                      str(full_path) + str(' ') + str(city), str(tot_h_info) + str(' ') + str(h_info),
                                      current_speed, city))
                    travelled.append(city)

    elif cost == "segments":
        route_taken = []
        p = 0
        while fringe:
            (priority, total_segment, total_dist, total_time, total_acc_rate, full_path, tot_h_info, tot_speed,
             current_city) = heappop(fringe)

            (lat1, long1) = file_gps(current_city)
            (lat2, long2) = file_gps(end)
            h_fun = abs(lat2 - lat1) + abs(long2 - long1)

            for (seg, distance, time, acc_rate, h_info, speed, city) in succesor(roads, current_city):

                if current_city == end:
                    temp_path = full_path.split(' ')
                    temp_h_info = tot_h_info.split(' ')
                    s = start
                    for k in range(1, len(temp_path)):
                        z = roads[temp_path[k]]
                        # I am in start, I have to go to temp_path[k] and start is in z
                        # find distance of start and update start = temp_path[k]
                        for x in z:
                            x = x.split(':')
                            if s in x:
                                d = x[1]
                                # print(s, temp_path[k], d)
                                s = temp_path[k]
                        if (temp_path[k] != '') or temp_h_info[k] != '':
                            route_taken.append((temp_path[k], temp_h_info[k] + " for " + str(d) + " miles"))

                    return {"total-segments": int(total_segment), "total-miles": float(total_dist),
                            "total-hours": float(total_time),
                            "total-expected-accidents": float(total_acc_rate), "route-taken": route_taken}

                if city not in travelled:
                    current_distance = float(distance) + float(total_dist)
                    current_segement = float(total_segment) + float(seg)
                    current_time = float(total_time) + float(time)
                    current_acc_rate = float(total_acc_rate) + float(acc_rate)
                    current_speed = float(tot_speed) + float(speed)
                    p = float(current_segement)+h_fun

                    heappush(fringe, (p, current_segement, current_distance, current_time, current_acc_rate,
                                      str(full_path) + str(' ') + str(city), str(tot_h_info) + str(' ') + str(h_info),
                                      current_speed, city))
                    travelled.append(city)


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])
