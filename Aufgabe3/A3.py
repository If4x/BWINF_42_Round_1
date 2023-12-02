# Program by Imanuel Fehse
# 42. Bundeswettbewerb Informatik
# Round 1
# Exercise Aufgabe 3

# -*- coding: utf-8 -*-

import heapq


class Building:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_file()
        self.size_y, self.size_x = self.data[0].split(' ')
        self.size_x = int(self.size_x)
        self.size_y = int(self.size_y)
        self.building = []
        self.start_pos = []
        self.end_pos = []
        self.weighted_graph = {}

        # run functions to get result
        self.convert_from_file()
        self.get_weighted_graph()

        # get result
        self.res_graph = []
        res = self.dijkstra(self.start_pos, self.end_pos)
        self.path = res[0]
        self.distance = res[1]
        self.create_path()
        self.save_result()

    # read file
    def read_file(self):
        f = open(self.filename, 'r')
        data = f.read().splitlines()
        f.close()
        return data

    # convert data from file to building
    def convert_from_file(self):
        def get_floor(y_start, y_end, floor):
            # print("get_floor", y_start, y_end, floor)
            c_floor = []
            for y in range(y_start, y_end):
                c_line = []
                for x in range(self.size_x):
                    # if field is a free
                    if self.data[y][x] == '.':
                        c_line.append([x, y - y_start, floor])
                    # if start position
                    elif self.data[y][x] == 'A':
                        c_line.append([x, y - y_start, floor])
                        self.start_pos = [x, y - y_start, floor]
                    # if end position
                    elif self.data[y][x] == 'B':
                        c_line.append([x, y - y_start, floor])
                        self.end_pos = [x, y - y_start, floor]
                    # if field is a wall
                    else:
                        c_line.append([])
                # add current line to current floor
                c_floor.append(c_line)
            return c_floor

        # first floor
        self.building.append(get_floor(1, self.size_y+1, 0))
        # second floor
        self.building.append(get_floor(self.size_y+2, self.size_y*2+2, 1))

    # creates weighted graph
    def get_weighted_graph(self):
        for z in range(len(self.building)):
            for y in range(len(self.building[z])):
                for x in range(len(self.building[z][y])):
                    # if field is not a wall
                    if self.building[z][y][x]:
                        c_connections = []
                        # do not need to check is field is at the end of the building, because outer ring of building
                        # is a wall
                        # check for surrounding fields
                        # check for field in y+ direction
                        if self.building[z][y + 1][x]:
                            c_connections.append([[x, y+1, z], 1])
                        # check for field in x+ direction
                        if self.building[z][y][x + 1]:
                            c_connections.append([[x+1, y, z], 1])
                        # check for field in y- direction
                        if self.building[z][y - 1][x]:
                            c_connections.append([[x, y-1, z], 1])
                        # check for field in x- direction
                        if self.building[z][y][x - 1]:
                            c_connections.append([[x-1, y, z], 1])
                        # check for field in other story
                        if z == 0:
                            if self.building[z+1][y][x]:
                                c_connections.append([[x, y, z+1], 3])
                        else:
                            if self.building[z-1][y][x]:
                                c_connections.append([[x, y, z-1], 3])
                        # add connections to connections dictionary
                        self.weighted_graph[str([x, y, z])] = c_connections

    # Dijkstra's algorithm to find the shortest path
    def dijkstra(self, start, end):
        # use dijkstra's algorithm to find the shortest path and keep track of the path

        # create a dictionary to keep track of the path
        path = {}
        # create a dictionary to keep track of the distance
        distance = {knot: float('inf') for knot in self.weighted_graph}
        distance[str(start)] = 0
        queue = [(0, str(start))]
        while queue:
            # get the current distance and the current knot
            current_distance, current_knot = heapq.heappop(queue)
            # check if the current distance is smaller than the distance in the dictionary
            if current_distance > distance[current_knot]:
                continue

            for neighbour, weight in self.weighted_graph[current_knot]:
                # calculate the new to the neighbour
                distance_to_neighbour = current_distance + weight
                # check if the new distance is smaller than the distance in the dictionary
                if distance_to_neighbour < distance[str(neighbour)]:
                    # update the distance in the dictionary
                    distance[str(neighbour)] = distance_to_neighbour
                    # update the path in the dictionary
                    path[str(neighbour)] = current_knot
                    # add the new distance and the new knot to the queue
                    heapq.heappush(queue, (distance_to_neighbour, str(neighbour)))
        # create a list to keep track of the path
        shortest_path = []
        # get the current knot
        current_knot = str(end)
        # add the current knot to the list
        shortest_path.append(current_knot)
        # loop until the current knot is the start knot
        while current_knot != str(start):
            # update the current knot
            current_knot = path[current_knot]
            # add the current knot to the list
            shortest_path.append(current_knot)
        shortest_path.append(str(start))
        # reverse the list
        shortest_path.reverse()
        # return the list and distance to reach the endpoint
        return [shortest_path, distance[str(end)]]

    # convert path to graph to path to building
    def create_path(self):
        # create graph of building
        # for every floor (z)
        for z in range(len(self.building)):
            c_floor = []
            # for every line (y)
            for y in range(len(self.building[z])):
                c_line = []
                # for every field (x)
                for x in range(len(self.building[z][y])):
                    # if field is not a wall
                    if self.building[z][y][x]:
                        c_line.append('.')
                    # if field is a wall
                    else:
                        c_line.append('#')
                c_floor.append(c_line)
            self.res_graph.append(c_floor)
        # add path to res_graph
        # for every field in path
        for i in range(len(self.path)):
            c_field = []
            for item in self.path[i].strip("[]").split(","):
                c_field.append(int(item))

            # if current field is not the end field
            if i != len(self.path)-1:
                # if path moves in x+ direction
                if c_field[0] < int(self.path[i+1].strip("[]").split(",")[0]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = '>'
                # if path moves in x- direction
                elif c_field[0] > int(self.path[i+1].strip("[]").split(",")[0]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = '<'
                # if path moves in y+ direction
                elif c_field[1] < int(self.path[i+1].strip("[]").split(",")[1]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = 'v'
                # if path moves in y- direction
                elif c_field[1] > int(self.path[i+1].strip("[]").split(",")[1]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = '^'
                # if path moves in z+ direction
                elif c_field[2] < int(self.path[i+1].strip("[]").split(",")[2]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = '!'
                # if path moves in z- direction
                elif c_field[2] > int(self.path[i+1].strip("[]").split(",")[2]):
                    self.res_graph[c_field[2]][c_field[1]][c_field[0]] = '!'
            # if current field is the end field
            else:
                self.res_graph[c_field[2]][c_field[1]][c_field[0]] = 'B'

    # save result to file
    def save_result(self):
        print("save result")
        f = open('result_a3_' + self.filename + '.txt', 'w')
        f.write("distance from A to B: " + str(self.distance) + '\n')
        f.write("building with path:\n")
        for z in range(len(self.res_graph)):
            for y in range(len(self.res_graph[z])):
                line = ""
                for x in range(len(self.res_graph[z][y])):
                    line += str(self.res_graph[z][y][x])
                f.write(line + '\n')
            f.write('\n')
        f.close()


def main():
    while True:
        filename = input("Enter a filename: ")
        if filename == "exit":
            exit(0)
        Test = Building(filename)
        # print(Test.weighted_graph)
        print("path to destination", Test.path)
        print("distance to destination", Test.distance)


# TESTING
main()
