# Program by Imanuel Fehse
# 42. Bundeswettbewerb Informatik
# Round 1
# Exercise Aufgabe 4

# -*- coding: utf-8 -*-

import pandas as pd


# Lamp Input Brick
class LampInput:
    def __init__(self, number):
        self.type = "lamp_in"
        self.number = number
        self.state = None


# Lamp Output Brick
class LampOutput:
    def __init__(self, number):
        self.type = "lamp_out"
        self.number = number
        self.state = None


# Red Sensor Brick
class Red:
    def __init__(self, sensor_position):
        self.type = "red"
        self.sensor_position = sensor_position
        self.output_0 = None
        self.output_1 = None

    def input(self, input):
        if input == 1:
            self.output_0 = 0
            self.output_1 = 0
        else:
            self.output_0 = 1
            self.output_1 = 1


# White Sensor Brick
class White:
    def __init__(self):
        self.type = "white"
        self.output_0 = None
        self.output_1 = None

    def input(self, input_1, input_2):
        if input_1 == 1 and input_2 == 1:
            self.output_0 = 0
            self.output_1 = 0
        else:
            self.output_0 = 1
            self.output_1 = 1


# Blue Sensor Brick
class Blue:
    def __init__(self):
        self.type = "blue"
        self.output_0 = None
        self.output_1 = None

    def input(self, input_1, input_2):
        if input_1 == 1:
            self.output_0 = 1
        else:
            self.output_0 = 0
        if input_2 == 1:
            self.output_1 = 1
        else:
            self.output_1 = 0


# Construction
class Construction:
    # initialisation
    def __init__(self, filename):
        # read file
        self.filename = filename
        self.data = self.read_file()
        # x = width (n) and y = height (m)
        self.x, self.y = self.data[0].split()
        self.x = int(self.x)
        self.y = int(self.y)
        # create construction from file
        self.construction = []
        self.create_construction_from_file()
        # get inputs
        self.inputs = self.get_inputs()
        # get outputs
        self.outputs = self.get_outputs()
        # get combinations of inputs
        self.combinations_of_inputs = self.get_combinations_of_inputs()
        # results
        self.results = []
        self.get_results()

        # read file
    def read_file(self):
        f = open(self.filename, "r")
        data = f.read().splitlines()
        # if there's an empty line in the file, remove it
        f.close()
        return data

    # create construction from file (convert file to objects in coordinate system = construction)
    def create_construction_from_file(self):
        # for each line (y-value) of the construction
        for line in self.data[1:self.y+1]:
            line = line.split()
            current_line_construction = []
            # convert file to objects
            i = 0
            while i < self.x:
                # if position is empty
                if line[i] == "X":
                    current_line_construction.append(None)
                # if position in a lamp (start)
                elif line[i][0] == "Q":
                    current_line_construction.append(LampInput(int(line[i][1:])))
                # if position is a white sensor
                elif line[i] == "W":
                    current_line_construction.append(White())
                    current_line_construction.append(current_line_construction[-1])
                    i += 1
                # if position is a blue sensor
                elif line[i] == "B":
                    current_line_construction.append(Blue())
                    current_line_construction.append(current_line_construction[-1])
                    i += 1
                # if position is a lamp (end)
                elif line[i][0] == "L":
                    current_line_construction.append(LampOutput(int(line[i][1:])))
                elif i+1 < self.x:
                    # if position is a red sensor with sensor position 0
                    if line[i] == "R" and line[i+1] == "r":
                        current_line_construction.append(Red(0))
                        current_line_construction.append(current_line_construction[-1])
                        i += 1
                    # if position is a red sensor with sensor position 1
                    elif line[i] == "r" and line[i+1] == "R":
                        current_line_construction.append(Red(1))
                        current_line_construction.append(current_line_construction[-1])
                        i += 1

                # go to next position
                i += 1
            # add line to construction
            self.construction.append(current_line_construction)

    def print_construction(self):
        print("Construction:", self.filename)
        for line in self.construction:
            print(len(line), line)

    # get list of inputs (lamp inputs)
    def get_inputs(self):
        inputs = []
        # search for lamp inputs
        for line in self.construction:
            for brick in line:
                # if position is a lamp input
                if brick is not None and brick.type == "lamp_in":
                    inputs.append(brick)
        return inputs

    # get list of outputs (lamp outputs)
    def get_outputs(self):
        outputs = []
        # search for lamp outputs
        for line in self.construction:
            for brick in line:
                # if position is a lamp output
                if brick is not None and brick.type == "lamp_out":
                    outputs.append(brick)
        return outputs

    # get all combinations of inputs
    def get_combinations_of_inputs(self):
        combinations = []
        for i in range(2**len(self.inputs)):
            c_combination = list(bin(i)[2:].zfill(len(self.inputs)))
            c_combination = [int(x) for x in c_combination]
            combinations.append(c_combination)
        return combinations

    # get output of brick in line above (same x-value, y-value - 1)
    def get_output_of_brick_in_line_above(self, x, y):
        # if brick is in first line of construction
        if y == 0:
            return None
        # if brick is not in first line of construction
        else:
            # if brick above is a red sensor
            if self.construction[y-1][x].type == "red":
                return self.construction[y-1][x].output_0

            # if brick above is a white sensor
            elif self.construction[y-1][x].type == "white":
                return self.construction[y-1][x].output_0

            # if brick above is a blue sensor
            elif self.construction[y-1][x].type == "blue":
                # if c_pos is on the left side of the current sensor
                if self.get_c_side_of_sensor(x, y) == 0:
                    return self.construction[y-1][x].output_0
                # if c_pos is on the right of the current sensor
                elif self.get_c_side_of_sensor(x, y) == 1:
                    return self.construction[y-1][x].output_1
                # if c_pos is on the lamp output of the blue brick above
                elif self.get_c_side_of_sensor(x, y) == 2:
                    # if left side of blue brick above is over lamp output
                    if self.get_c_side_of_sensor(x, y-1) == 0:
                        return self.construction[y-1][x].output_0
                    # if right side of blue brick above is over lamp output
                    elif self.get_c_side_of_sensor(x, y-1) == 1:
                        return self.construction[y-1][x].output_1

            # if brick above is a lamp input
            elif self.construction[y-1][x].type == "lamp_in":
                return self.construction[y-1][x].state

            # if brick above is none (empty)
            elif self.construction[y-1][x] is None:
                return 0

    # get current side of the red sensor (0= left, 1 = right)
    def get_c_side_of_sensor(self, x, y):
        # if c position in on the right
        if x - 1 >= 0:
            if self.construction[y][x] == self.construction[y][x - 1]:
                # print("get_c_pos is on the right")
                return 1
        # if c position in on the left
        if x + 1 < self.x:
            if self.construction[y][x] == self.construction[y][x + 1]:
                # print("get_c_pos is on the left")
                return 0
        # if the c brick is a lamp output
        if self.construction[y][x].type == "lamp_out":
            return 2
        return None

    # get result for specific combination of the state of the lamp inputs
    def get_res(self, combination):
        # set inputs to combination
        for i in range(len(self.inputs)):
            self.inputs[i].state = combination[i]

        # calculate outputs
        # for each line in the construction (y-value)
        for y in range(self.y):
            # for each position in line (x-value)
            for x in range(self.x):
                # if brick is None (empty)
                if self.construction[y][x] is None:
                    pass

                # if brick is a lamp input
                elif self.construction[y][x].type == "lamp_in":
                    pass

                # if brick is a red sensor
                elif self.construction[y][x].type == "red":
                    # get position of the sensor in the red sensor block
                    sensor_position = self.construction[y][x].sensor_position
                    # get current side of the red sensor
                    current_side = self.get_c_side_of_sensor(x, y)
                    # if sensor of the sensor block is on the current side
                    if sensor_position == current_side:
                        # set output of the sensor
                        self.construction[y][x].input(self.get_output_of_brick_in_line_above(x, y))
                    else:
                        pass

                # if brick is a white sensor
                elif self.construction[y][x].type == "white":
                    current_side = self.get_c_side_of_sensor(x, y)
                    # if c_pos is on the left
                    if current_side == 0:
                        self.construction[y][x].input(self.get_output_of_brick_in_line_above(x, y),
                                                      self.get_output_of_brick_in_line_above(x+1, y))
                    # if c_pos is on the right
                    elif current_side == 1:
                        self.construction[y][x].input(self.get_output_of_brick_in_line_above(x-1, y),
                                                      self.get_output_of_brick_in_line_above(x, y))
                # if brick is a blue sensor
                elif self.construction[y][x].type == "blue":
                    current_side = self.get_c_side_of_sensor(x, y)
                    # if c_pos is on the left
                    if current_side == 0:
                        self.construction[y][x].input(self.get_output_of_brick_in_line_above(x, y),
                                                      self.get_output_of_brick_in_line_above(x+1, y))
                    # if c_pos is on the right
                    elif current_side == 1:
                        self.construction[y][x].input(self.get_output_of_brick_in_line_above(x-1, y),
                                                      self.get_output_of_brick_in_line_above(x, y))
                # if brick is a lamp output
                elif self.construction[y][x].type == "lamp_out":
                    self.construction[y][x].state = self.get_output_of_brick_in_line_above(x, y)

        # get outputs of the construction (lamp outputs)
        outputs = []
        for output in self.outputs:
            outputs.append(output.state)
        return outputs

    # get individual result for all combinations and add them to a list with all the results
    def get_results(self):
        for combination in self.combinations_of_inputs:
            self.results.append(self.get_res(combination))

    # save results to file
    def save_results(self):
        # text file with table
        # create table with pandas
        data = {}
        # get values of input i and add input i to data
        for i in range(len(self.inputs)):
            c_q = "Q" + str(self.inputs[i].number)
            c_ins = []
            for j in range(len(self.combinations_of_inputs)):
                c_ins.append(self.combinations_of_inputs[j][i])
            data[c_q] = c_ins
        # get values of output i and add output i to data
        for i in range(len(self.outputs)):
            c_l = "L" + str(self.outputs[i].number)
            c_outs = []
            for j in range(len(self.results)):
                c_outs.append(self.results[j][i])
            data[c_l] = c_outs
        # create table
        # print("data:", data)
        df = pd.DataFrame(data)
        # save dataframe to txt file without index in line
        f = open("result_a4_" + self.filename + "_table.txt", "w")
        f.write(df.to_string(index=False))
        f.close()


def main():
    while True:
        # get filename
        filename = input("Enter a filename: ")
        if filename == "exit":
            exit(0)

        # create construction (object
        construction = Construction(filename)
        print("results")
        for i in range(len(construction.combinations_of_inputs)):
            print(construction.combinations_of_inputs[i], construction.results[i])
        # save results
        construction.save_results()


# RUN
main()
