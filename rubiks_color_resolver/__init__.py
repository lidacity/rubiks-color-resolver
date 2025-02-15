import array
import gc
import os
from math import sqrt
from rubiks_color_resolver.base import (
    LabColor,
    RubiksColorSolverGenericBase,
    Square,
    lab_distance,
    html_color,
    rgb2lab,
)
from rubiks_color_resolver.tsp_solver_greedy import solve_tsp
from rubiks_color_resolver.permutations import (
    even_cube_center_color_permutations,
    len_even_cube_center_color_permutations,
    odd_cube_center_color_permutations,
)

from jinja2 import Environment, FileSystemLoader
import datetime

# from rubiks_color_resolver.profile import timed_function, print_profile_data
import sys

if sys.version_info < (3, 4):
    raise SystemError("Must be using Python 3.4 or higher")


ALL_COLORS = ("B", "G", "O", "R", "W", "Y")
SIDES_COUNT = 6


# @timed_function
def median(list_foo):
    list_foo = sorted(list_foo)
    list_foo_len = len(list_foo)

    if list_foo_len < 1:
        return None

    # Even number of entries
    if list_foo_len % 2 == 0:
        return (
            list_foo[int((list_foo_len - 1) / 2)]
            + list_foo[int((list_foo_len + 1) / 2)]
        ) / 2.0

    # Odd number of entries
    else:
        return list_foo[int((list_foo_len - 1) / 2)]


def tsp_matrix_corners(corners):
    len_corners = len(corners)

    # build a full matrix of color to color distances
    # init the 2d list with 0s
    matrix = [x[:] for x in [[0] * len_corners] * len_corners]
    color_names = set(("W", "Y", "O", "R", "B", "G"))

    for x in range(len_corners):
        x_corner = corners[x]

        for y in range(x + 1, len_corners):
            y_corner = corners[y]

            if (
                x_corner[0].position in color_names
                and y_corner[0].position in color_names
            ):
                distance = 999

            elif (
                x_corner[0].position not in color_names
                and y_corner[0].position not in color_names
            ):
                distance = 999

            else:
                distance_012 = (
                    lab_distance(x_corner[0].lab, y_corner[0].lab)
                    + lab_distance(x_corner[1].lab, y_corner[1].lab)
                    + lab_distance(x_corner[2].lab, y_corner[2].lab)
                )

                distance_201 = (
                    lab_distance(x_corner[0].lab, y_corner[2].lab)
                    + lab_distance(x_corner[1].lab, y_corner[0].lab)
                    + lab_distance(x_corner[2].lab, y_corner[1].lab)
                )

                distance_120 = (
                    lab_distance(x_corner[0].lab, y_corner[1].lab)
                    + lab_distance(x_corner[1].lab, y_corner[2].lab)
                    + lab_distance(x_corner[2].lab, y_corner[0].lab)
                )

                distance = min(distance_012, distance_201, distance_120)

            matrix[x][y] = distance
            matrix[y][x] = distance

    # print("corners matrix")
    # for row in matrix:
    #     print(row)

    return matrix


def corner_distance(corner1, corner2):
    return (
        lab_distance(corner1[0].lab, corner2[0].lab)
        + lab_distance(corner1[1].lab, corner2[1].lab)
        + lab_distance(corner1[2].lab, corner2[2].lab)
    )


def traveling_salesman_corners(corners, desc):
    matrix = tsp_matrix_corners(corners)
    path = solve_tsp(matrix, desc=desc)
    sorted_corners = [corners[x] for x in path]

    for x in range(0, len(sorted_corners), 2):
        corner1 = sorted_corners[x]
        corner2 = sorted_corners[x + 1]

        distance_012 = (
            lab_distance(corner1[0].lab, corner2[0].lab)
            + lab_distance(corner1[1].lab, corner2[1].lab)
            + lab_distance(corner1[2].lab, corner2[2].lab)
        )

        distance_201 = (
            lab_distance(corner1[0].lab, corner2[2].lab)
            + lab_distance(corner1[1].lab, corner2[0].lab)
            + lab_distance(corner1[2].lab, corner2[1].lab)
        )

        distance_120 = (
            lab_distance(corner1[0].lab, corner2[1].lab)
            + lab_distance(corner1[1].lab, corner2[2].lab)
            + lab_distance(corner1[2].lab, corner2[0].lab)
        )

        distance = min(distance_012, distance_201, distance_120)

        if distance == distance_012:
            pass

        elif distance == distance_201:
            sorted_corners[x + 1] = (corner2[2], corner2[0], corner2[1])

        elif distance == distance_120:
            sorted_corners[x + 1] = (corner2[1], corner2[2], corner2[0])

        else:
            raise ValueError(distance)

    while True:
        max_delta = 0
        max_delta_corners_to_swap = None

        for x in range(0, len(sorted_corners), 2):
            corner1 = sorted_corners[x]
            corner2 = sorted_corners[x + 1]
            distance12 = corner_distance(corner1, corner2)

            for y in range(x + 2, len(sorted_corners), 2):
                corner3 = sorted_corners[y]
                corner4 = sorted_corners[y + 1]
                distance34 = corner_distance(corner3, corner4)

                # If we were to swap corner2 with corner4, what would that do to the corner1->corner2 distance plus the corner3->corner4 distance?
                distance14 = corner_distance(corner1, corner4)
                distance32 = corner_distance(corner3, corner2)

                if distance14 + distance32 < distance12 + distance34:
                    delta = (distance12 + distance34) - (distance14 + distance32)

                    if delta > max_delta:
                        max_delta = delta
                        max_delta_corners_to_swap = (x + 1, y + 1)

        if max_delta_corners_to_swap:
            (x, y) = max_delta_corners_to_swap
            orig_x = sorted_corners[x]
            sorted_corners[x] = sorted_corners[y]
            sorted_corners[y] = orig_x

        else:
            break

    return sorted_corners


def tsp_matrix_edge_pairs(edge_pairs):
    len_edge_pairs = len(edge_pairs)

    # build a full matrix of color to color distances
    # init the 2d list with 0s
    matrix = [x[:] for x in [[0] * len_edge_pairs] * len_edge_pairs]
    color_names = set(("W", "Y", "O", "R", "B", "G"))

    for x in range(len_edge_pairs):
        x_edge_pair = edge_pairs[x]

        for y in range(x + 1, len_edge_pairs):
            y_edge_pair = edge_pairs[y]

            if (
                x_edge_pair[0].position in color_names
                and y_edge_pair[0].position in color_names
            ):
                distance = 999

            elif (
                x_edge_pair[0].position not in color_names
                and y_edge_pair[0].position not in color_names
            ):
                distance = 999

            else:
                distance_01 = lab_distance(
                    x_edge_pair[0].lab, y_edge_pair[0].lab
                ) + lab_distance(x_edge_pair[1].lab, y_edge_pair[1].lab)
                distance_10 = lab_distance(
                    x_edge_pair[0].lab, y_edge_pair[1].lab
                ) + lab_distance(x_edge_pair[1].lab, y_edge_pair[0].lab)

                distance = min(distance_01, distance_10)

            matrix[x][y] = distance
            matrix[y][x] = distance

    return matrix


def edge_pair_distance(pair1, pair2, normal):
    if normal:
        return lab_distance(pair1[0].lab, pair2[0].lab) + lab_distance(
            pair1[1].lab, pair2[1].lab
        )
    else:
        return lab_distance(pair1[0].lab, pair2[1].lab) + lab_distance(
            pair1[1].lab, pair2[0].lab
        )


def traveling_salesman_edge_pairs(edge_pairs, desc):
    matrix = tsp_matrix_edge_pairs(edge_pairs)
    path = solve_tsp(matrix, desc=desc)
    sorted_edge_pairs = [edge_pairs[x] for x in path]

    for x in range(0, len(sorted_edge_pairs), 2):
        pair1 = sorted_edge_pairs[x]
        pair2 = sorted_edge_pairs[x + 1]
        distance_01 = edge_pair_distance(pair1, pair2, normal=True)
        distance_10 = edge_pair_distance(pair1, pair2, normal=False)

        if distance_10 < distance_01:
            sorted_edge_pairs[x + 1] = (
                sorted_edge_pairs[x + 1][1],
                sorted_edge_pairs[x + 1][0],
            )

    while True:
        max_delta = 0
        max_delta_edges_to_swap = None

        for x in range(0, len(sorted_edge_pairs), 2):
            pair1 = sorted_edge_pairs[x]
            pair2 = sorted_edge_pairs[x + 1]
            distance12 = edge_pair_distance(pair1, pair2, True)

            for y in range(x + 2, len(sorted_edge_pairs), 2):
                pair3 = sorted_edge_pairs[y]
                pair4 = sorted_edge_pairs[y + 1]
                distance34 = edge_pair_distance(pair3, pair4, True)

                # If we were to swap pair2 with pair4, what would that do to the pair1->pair2 distance plus the pair3->pair4 distance?
                distance14 = edge_pair_distance(pair1, pair4, True)
                distance32 = edge_pair_distance(pair3, pair2, True)

                if distance14 + distance32 < distance12 + distance34:
                    delta = (distance12 + distance34) - (distance14 + distance32)

                    if delta > max_delta:
                        max_delta = delta
                        max_delta_edges_to_swap = (x + 1, y + 1)

        if max_delta_edges_to_swap:
            (x, y) = max_delta_edges_to_swap
            orig_x = sorted_edge_pairs[x]
            sorted_edge_pairs[x] = sorted_edge_pairs[y]
            sorted_edge_pairs[y] = orig_x

        else:
            break

    return sorted_edge_pairs


"""
def path_streak_cost(squares):

    if len(squares) <= 1:
        return 0

    cost = 0
    prev_square = squares[0]

    for square in squares[1:]:
        cost += lab_distance(prev_square.lab, square.lab)
        prev_square = square

    return cost


def best_path_streak(sorted_squares, streak_length, middle_squares, edge_pairs, corners):
    max_cost_start = len(sorted_squares) - streak_length
    min_cost = 999
    min_cost_start = None
    # print(middle_squares)
    len_edge_pairs = len(edge_pairs)

    if len_edge_pairs == 0:
        pass
    elif len_edge_pairs == 12:
        target_edges_in_streak = 4
    else:
        raise ValueError(len_edge_pairs)

    for x in range(0, max_cost_start):
        squares_for_streak = sorted_squares[x:x + streak_length]
        cost = path_streak_cost(squares_for_streak)
        valid = True

        if middle_squares:
            middle_squares_in_streak = [square for square in squares_for_streak if square in middle_squares]
            valid = bool(len(middle_squares_in_streak) == 1)
            # print(middle_squares_in_streak)

        '''
        if valid and edge_pairs:
            for edge_pair in edge_pairs:
                edges_in_pair_in_streak = [square for square in squares_for_streak if square in edge_pair]
                valid = bool(len(edges_in_pair_in_streak) == target_edges_in_streak)
        '''

        if valid and corners:
            # print(f"corners {corners}")
            corners_in_streak = []

            for corner in corners:
                corner_in_streak = [square for square in squares_for_streak if square in corner]
                corners_in_streak.extend(corner_in_streak)
                # print(f"corner_in_streak {len(corner_in_streak)}")
                valid = bool(len(corner_in_streak) <= 1)

                if not valid:
                    break

            if valid:
                valid = bool(len(corners_in_streak) == 4)
            # print(f"corners_in_streak {len(corners_in_streak)}")

        if valid and cost < min_cost:
            min_cost = cost
            min_cost_start = x

    return sorted_squares[min_cost_start : min_cost_start + streak_length]
"""


def tsp_matrix(squares):
    len_squares = len(squares)
    r_len_squares = range(len_squares)

    # build a full matrix of color to color distances
    # init the 2d list with 0s
    matrix = [x[:] for x in [[0] * len_squares] * len_squares]

    for x in r_len_squares:
        x_lab = squares[x].lab

        for y in range(x + 1, len_squares):
            y_lab = squares[y].lab

            distance = lab_distance(x_lab, y_lab)
            matrix[x][y] = distance
            matrix[y][x] = distance

    # convert to tuple of tuples
    for (row_index, row) in enumerate(matrix):
        matrix[row_index] = tuple(row)

    matrix = tuple(matrix)

    return matrix


# @timed_function
def traveling_salesman(squares, desc, middle_squares=[], edge_pairs=[], corners=[]):
    """
    SQUARES_PER_ROW = int(len(squares) / SIDES_COUNT)
    results = []
    _squares = squares[:]

    for x in range(SIDES_COUNT - 1):
        if x == 4:
            matrix = tsp_matrix(_squares)
            path = solve_tsp(matrix, desc=desc)
            path_squares = [_squares[x] for x in path]
            results.extend(path_squares)
        else:
            matrix = tsp_matrix(_squares)
            path = solve_tsp(matrix, desc=desc)
            path_squares = [_squares[x] for x in path]
            results.extend(best_path_streak(path_squares, SQUARES_PER_ROW, middle_squares, edge_pairs, corners))
            _squares = [square for square in squares if square not in results]

    return results
    """
    matrix = tsp_matrix(squares)
    path = solve_tsp(matrix, desc=desc)
    return [squares[x] for x in path]


def traveling_salesman_two_colors(squares, endpoints=None, desc=None):
    matrix = tsp_matrix(squares)

    if endpoints:
        start_index = squares.index(endpoints[0])
        end_index = squares.index(endpoints[1])
        endpoints = (start_index, end_index)
    path = solve_tsp(matrix, endpoints=endpoints, desc=desc)
    return [squares[x] for x in path]


# @timed_function
def get_important_square_indexes(size):
    squares_per_side = size * size
    max_square = squares_per_side * 6
    first_squares = []
    last_squares = []

    for index in range(1, max_square + 1):
        if (index - 1) % squares_per_side == 0:
            first_squares.append(index)
        elif index % squares_per_side == 0:
            last_squares.append(index)

    last_UBD_squares = (last_squares[0], last_squares[4], last_squares[5])
    return (first_squares, last_squares, last_UBD_squares)


# @timed_function
def hex_to_rgb(rgb_string):
    """
    Takes #112233 and returns the RGB values in decimal
    """
    if rgb_string.startswith("#"):
        rgb_string = rgb_string[1:]

    red = int(rgb_string[0:2], 16)
    green = int(rgb_string[2:4], 16)
    blue = int(rgb_string[4:6], 16)
    return (red, green, blue)


# @timed_function
def hashtag_rgb_to_labcolor(rgb_string):
    (red, green, blue) = hex_to_rgb(rgb_string)
    # lab = rgb2lab((red, green, blue))
    # print("LabColor({}, {}, {}, {}, {}, {}),".format(lab.L, lab.a, lab.b, lab.red, lab.green, lab.blue))
    # return lab
    return rgb2lab((red, green, blue))


crayola_colors = {
    # Handy website for converting RGB tuples to hex
    # http://www.w3schools.com/colors/colors_converter.asp
    #
    # These are the RGB values as seen via a webcam
    #   white = (235, 254, 250)
    #   green = (20, 105, 74)
    #   yellow = (210, 208, 2)
    #   orange = (148, 53, 9)
    #   blue = (22, 57, 103)
    #   red = (104, 4, 2)
    #
    # "W": hashtag_rgb_to_labcolor("#FFFFFF"),
    # "G": hashtag_rgb_to_labcolor("#14694a"),
    # "Y": hashtag_rgb_to_labcolor("#FFFF00"),
    # "O": hashtag_rgb_to_labcolor("#943509"),
    # "B": hashtag_rgb_to_labcolor("#163967"),
    # "R": hashtag_rgb_to_labcolor("#680402"),
    "W": LabColor(100.0, 0.00526049995830391, -0.01040818452526793, 255, 255, 255),
    "G": LabColor(
        39.14982168015123, -32.45052099773829, 10.60519920674466, 20, 105, 74
    ),
    "Y": LabColor(
        97.13824698129729, -21.55590833483229, 94.48248544644462, 255, 255, 0
    ),
    "O": LabColor(35.71689493804023, 38.18518746791636, 43.98251678431012, 148, 53, 9),
    "B": LabColor(
        23.92144819784853, 5.28400492805528, -30.63998357385018, 22, 57, 103
    ),
    "R": LabColor(20.18063311070288, 40.48184409611946, 29.94038922869042, 104, 4, 2),
}


# @timed_function
def get_row_color_distances(squares, row_baseline_lab):
    """
    'colors' is list if (index, (red, green, blue)) tuples
    'row_baseline_lab' is a list of Lab colors, one for each row of colors

    Return the total distance of the colors in a row vs their baseline
    """
    results = []
    squares_per_row = int(len(squares) / 6)
    count = 0
    row_index = 0
    distance = 0
    baseline_lab = row_baseline_lab[row_index]

    for square in squares:
        baseline_lab = row_baseline_lab[row_index]
        distance += lab_distance(baseline_lab, square.lab)
        count += 1

        if count % squares_per_row == 0:
            results.append(int(distance))
            row_index += 1
            distance = 0

    return results


# @timed_function
def get_squares_for_row(squares, target_row_index):
    results = []
    squares_per_row = int(len(squares) / 6)
    count = 0
    row_index = 0

    for square in squares:
        if row_index == target_row_index:
            results.append(square)
        count += 1

        if count % squares_per_row == 0:
            row_index += 1

    return results


# @timed_function
def square_list_to_lab(squares):
    reds = array.array("B")
    greens = array.array("B")
    blues = array.array("B")

    for square in squares:
        (red, green, blue) = (square.lab.red, square.lab.green, square.lab.blue)
        reds.append(red)
        greens.append(green)
        blues.append(blue)

    median_red = int(median(reds))
    median_green = int(median(greens))
    median_blue = int(median(blues))

    return rgb2lab((median_red, median_green, median_blue))


class RubiksColorSolverGeneric(RubiksColorSolverGenericBase):

    filename = "rubiks-color-resolver.html"
    ColorNames = {"B": "Blue", "G": "Green", "O": "Orange", "R": "Red", "W": "White", "Y": "Yellow"}


    def write_color_corners(self, desc, corners):
        result = {}
        result["desc"] = desc
        result["corners"] = []

        for row_index in range(3):
            row = []
            for (index, (corner0, corner1, corner2)) in enumerate(corners):

                if row_index == 0:
                    square = corner0
                elif row_index == 1:
                    square = corner1
                elif row_index == 2:
                    square = corner2
                else:
                    raise ValueError(row_index)

                (red, green, blue) = (
                    square.lab.red,
                    square.lab.green,
                    square.lab.blue,
                )

                item = {}
                item["half_square"] = index and index % 2 == 0

                item["color"] = f"{red:0>2x}{green:0>2x}{blue:0>2x}"
                item["RGB"] = f"RGB ({red}, {green}, {blue})"
                item["Lab"] = f"Lab ({int(square.lab.L)}, {int(square.lab.a)}, {int(square.lab.b)})"
                item["Name"] = f"Color ({self.ColorNames[square.color_name]})"
                item["color_name"] = square.color_name
                item["side_name"] = square.side_name #self.color_to_side_name[square.color_name]
                #print(self.color_to_side_name)
                item["position"] = square.position
                row.append(item)
            result["corners"].append(row)

        return result


    def write_color_edge_pairs(self, desc, square_pairs):
        result = {}
        result["desc"] = desc
        result["square_pairs"] = []

        for use_square1 in (True, False):
            pair = []
            for (index, (square1, square2)) in enumerate(square_pairs):

                if use_square1:
                    square = square1
                else:
                    square = square2

                (red, green, blue) = (
                    square.lab.red,
                    square.lab.green,
                    square.lab.blue,
                )

                item = {}
                item["half_square"] = index and index % 2 == 0

                item["color"] = f"{red:0>2x}{green:0>2x}{blue:0>2x}"
                item["RGB"] = f"RGB ({red}, {green}, {blue})"
                item["Lab"] = f"Lab ({int(square.lab.L)}, {int(square.lab.a)}, {int(square.lab.b)})"
                item["Name"] = f"Color ({self.ColorNames[square.color_name]})"
                item["side_name"] = square.side_name
                item["position"] = square.position
                pair.append(item)

            result["square_pairs"].append(pair)

        return result


    # @timed_function
    def write_colors(self, desc, squares):
        result = {}
        squares_per_row = int(len(squares) / 6)
        result["desc"] = desc
        result["squares"] = []

        count = 0
        for square in squares:
            item = {}
            (red, green, blue) = (square.lab.red, square.lab.green, square.lab.blue)
            item["color"] = f"{red:0>2x}{green:0>2x}{blue:0>2x}"
            item["RGB"] = f"RGB ({red}, {green}, {blue})"
            item["Lab"] = f"Lab ({int(square.lab.L)}, {int(square.lab.a)}, {int(square.lab.b)})"
            item["Name"] = f"Color ({self.ColorNames[square.color_name]})"
            item["side_name"] = square.side_name
            item["position"] = square.position

            count += 1

            item["br"] = count % squares_per_row == 0

            result["squares"].append(item)

        return result


    scan_data = None


    # @timed_function
    def enter_scan_data(self, scan_data):

        for (position, (red, green, blue)) in scan_data.items():
            position = int(position)
            side = self.pos2side[position]
            side.set_square(position, red, green, blue)


#            self.www_header()

            self.scan_data = scan_data

        self.calculate_pos2square()


    # @timed_function
    def html_cube(self, desc, use_html_colors, div_class):
        cube = ["dummy"]

        for side in (
            self.sideU,
            self.sideL,
            self.sideF,
            self.sideR,
            self.sideB,
            self.sideD,
        ):
            for position in range(side.min_pos, side.max_pos + 1):
                square = side.squares[position]

                if use_html_colors:
                    red = html_color[square.color_name]["red"]
                    green = html_color[square.color_name]["green"]
                    blue = html_color[square.color_name]["blue"]
                else:
                    red = square.lab.red
                    green = square.lab.green
                    blue = square.lab.blue

                cube.append((red, green, blue, square.color_name, square.lab))

        col = 1
        squares_per_side = self.width * self.width
        max_square = squares_per_side * 6

        sides = ("upper", "left", "front", "right", "back", "down")
        side_index = -1
        (first_squares, last_squares, last_UBD_squares) = get_important_square_indexes(
            self.width
        )

        html = {}
        html["div_class"] = div_class
        html["desc"] = desc
        html["side_index"] = {}
        for index in range(1, max_square + 1):
            if index in first_squares:
                side_index += 1
                html["side_index"][sides[side_index]] = []

            (red, green, blue, color_name, lab) = cube[index]

            item = {}
            item["col"] = col
            item["RGB"] = f"RGB ({red}, {green}, {blue})"
            item["Lab"] = f"Lab ({int(lab.L)}, {int(lab.a)}, {int(lab.b)})"
            if color_name is not None:
                item["Name"] = f"Color ({self.ColorNames[color_name]})"
            item["color"] = f"{red:0>2x}{green:0>2x}{blue:0>2x}"
            item["index"] = f"{index:0>2}"
            item["last_UBD_squares"] = index in last_UBD_squares
            item["first_squares"] = index in first_squares
            item["last_squares"] = index in last_squares

            html["side_index"][sides[side_index]].append(item)

            col += 1

            if col == self.width + 1:
                col = 1

        return html


    def _write_colors(self, desc, box):
        result = {}
        result["desc"] = desc
        result["color_name"] = []

        for color_name in ("W", "Y", "G", "B", "O", "R"):
            lab = box[color_name]

            item = {}
            item["color"] = f"{lab.red:0>2x}{lab.green:0>2x}{lab.blue:0>2x}"
            item["RGB"] = f"RGB ({lab.red}, {lab.green}, {lab.blue})"
            item["Lab"] = f"Lab ({int(lab.L)}, {int(lab.a)}, {int(lab.b)})"
            item["Name"] = f"Color ({self.ColorNames[color_name]})"
            item["color_name"] = color_name
            result["color_name"].append(item)

        return result


    # @timed_function
    def write_crayola_colors(self):
        return self._write_colors("crayola box", crayola_colors)


    # @timed_function
    def write_color_box(self):
        return self._write_colors("color box", self.color_box)


    # @timed_function
    def set_state(self):
        self.state = []

        # odd cube
        if self.sideU.mid_pos is not None:

            # Assign a color name to each center square. Compute
            # which naming scheme results in the least total color distance in
            # terms of the assigned color name vs. the colors in crayola_colors.
            min_distance = None
            min_distance_permutation = None

            # Build a list of all center squares
            center_squares = []
            for side in (
                self.sideU,
                self.sideL,
                self.sideF,
                self.sideR,
                self.sideB,
                self.sideD,
            ):
                square = side.squares[side.mid_pos]
                center_squares.append(square)
            # desc = "middle center"
            # log.info("center_squares: %s".format(center_squares))

            for permutation in odd_cube_center_color_permutations:
                distance = 0

                for (index, center_square) in enumerate(center_squares):
                    color_name = permutation[index]
                    color_obj = crayola_colors[color_name]
                    distance += lab_distance(center_square.lab, color_obj)

                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    min_distance_permutation = permutation
                    """
                    log.info("{} PERMUTATION {}, DISTANCE {:,} (NEW MIN)".format(desc, permutation, int(distance)))
                else:
                    log.info("{} PERMUTATION {}, DISTANCE {}".format(desc, permutation, distance))
                    """
            self.color_to_side_name = {
                min_distance_permutation[0]: "U",
                min_distance_permutation[1]: "L",
                min_distance_permutation[2]: "F",
                min_distance_permutation[3]: "R",
                min_distance_permutation[4]: "B",
                min_distance_permutation[5]: "D",
            }
            # log.info("{} FINAL PERMUTATION {}".format(desc, min_distance_permutation))

        # even cube
        else:
            self.color_to_side_name = {
                "W": "U",
                "O": "L",
                "G": "F",
                "R": "R",
                "B": "B",
                "Y": "D",
            }

        for side in (
            self.sideU,
            self.sideR,
            self.sideF,
            self.sideD,
            self.sideL,
            self.sideB,
        ):
            for x in range(side.min_pos, side.max_pos + 1):
                square = side.squares[x]
                square.side_name = self.color_to_side_name[square.color_name]


    # @timed_function
    def cube_for_json(self):
        """
        Return a dictionary of the cube data so that we can json dump it
        """
        data = {}
        data["kociemba"] = "".join(self.cube_for_kociemba_strict())
        data["sides"] = {}
        data["squares"] = {}

        for side in (
            self.sideU,
            self.sideR,
            self.sideF,
            self.sideD,
            self.sideL,
            self.sideB,
        ):
            for x in range(side.min_pos, side.max_pos + 1):
                square = side.squares[x]
                color = square.color_name
                side_name = self.color_to_side_name[color]

                if side_name not in data["sides"]:
                    data["sides"][side_name] = {}
                    data["sides"][side_name]["colorName"] = color
                    data["sides"][side_name]["colorHTML"] = {}
                    data["sides"][side_name]["colorHTML"]["red"] = html_color[color][
                        "red"
                    ]
                    data["sides"][side_name]["colorHTML"]["green"] = html_color[color][
                        "green"
                    ]
                    data["sides"][side_name]["colorHTML"]["blue"] = html_color[color][
                        "blue"
                    ]

                data["squares"][square.position] = {"finalSide": side_name}

        return data


    # @timed_function
    def assign_color_names(
        self, desc, squares_lists_all, color_permutations, color_box
    ):
        """
        Assign a color name to each square in each squares_list. Compute
        which naming scheme results in the least total color distance in
        terms of the assigned color name vs. the colors in color_box.
        """
        ref_even_cube_center_color_permutations = even_cube_center_color_permutations
        # print("\n\n\n")
        # print("assign_color_names '{}' via {}".format(desc, color_permutations))

        def get_even_cube_center_color_permutation(permutation_index):
            LINE_LENGTH = 12
            start = permutation_index * LINE_LENGTH
            end = start + LINE_LENGTH
            return ref_even_cube_center_color_permutations[start:end].split()

        ref_ALL_COLORS = ALL_COLORS

        # squares_lists_all is sorted by color. Split that list into 6 even buckets (squares_lists).
        squares_per_row = int(len(squares_lists_all) / 6)
        squares_lists = []
        square_list = []

        for square in squares_lists_all:
            square_list.append(square)

            if len(square_list) == squares_per_row:
                squares_lists.append(tuple(square_list))
                square_list = []

        # Compute the distance for each color in the color_box vs each squares_list
        # in squares_lists. Store this in distances_of_square_list_per_color
        distances_of_square_list_per_color = {}

        for color_name in ref_ALL_COLORS:
            color_lab = color_box[color_name]
            distances_of_square_list_per_color[color_name] = []

            for (index, squares_list) in enumerate(squares_lists):
                distance = 0
                for square in squares_list:
                    distance += lab_distance(square.lab, color_lab)
                distances_of_square_list_per_color[color_name].append(int(distance))
            distances_of_square_list_per_color[
                color_name
            ] = distances_of_square_list_per_color[color_name]

        min_distance = 99999
        min_distance_permutation = None

        if color_permutations == "even_cube_center_color_permutations":

            # before sorting
            """
            print("\n".join(map(str, squares_lists)))
            for color_name in ref_ALL_COLORS:
                print("pre  distances_of_square_list_per_color {} : {}".format(color_name, distances_of_square_list_per_color[color_name]))
            print("")
            """

            # Move the squares_list row that is closest to B to the front, then G, O, R, W, Y.
            # This will allow us to skip many more entries later.
            for (insert_index, color_name) in enumerate(ref_ALL_COLORS):
                min_color_name_distance = 99999
                min_color_name_distance_index = None

                for (index, distance) in enumerate(
                    distances_of_square_list_per_color[color_name]
                ):
                    if distance < min_color_name_distance:
                        min_color_name_distance = distance
                        min_color_name_distance_index = index

                tmp_square_list = squares_lists[min_color_name_distance_index]
                squares_lists.pop(min_color_name_distance_index)
                squares_lists.insert(insert_index, tmp_square_list)

                for color_name in ref_ALL_COLORS:
                    blue_distance = distances_of_square_list_per_color[color_name][
                        min_color_name_distance_index
                    ]
                    distances_of_square_list_per_color[color_name].pop(
                        min_color_name_distance_index
                    )
                    distances_of_square_list_per_color[color_name].insert(
                        insert_index, blue_distance
                    )

            # after sorting
            """
            print("\n".join(map(str, squares_lists)))
            for color_name in ref_ALL_COLORS:
                print("post distances_of_square_list_per_color {} : {}".format(color_name, distances_of_square_list_per_color[color_name]))
            print("")
            """

            permutation_len = len_even_cube_center_color_permutations
            permutation_index = 0
            # total = 0
            # skip_total = 0
            r = range(6)

            while permutation_index < permutation_len:
                permutation = get_even_cube_center_color_permutation(permutation_index)
                distance = 0
                skip_by = 0

                for x in r:
                    distance += distances_of_square_list_per_color[permutation[x]][x]

                    if distance > min_distance:

                        if x == 0:
                            skip_by = 120
                        elif x == 1:
                            skip_by = 24
                        elif x == 2:
                            skip_by = 6
                        elif x == 3:
                            skip_by = 2

                        # if skip_by:
                        #    print("{} PERMUTATION {} - {}, x {} distance {:,} > min {}, skip_by {}".format(
                        #        desc, permutation_index, permutation, x, distance, min_distance, skip_by))
                        break

                if skip_by:
                    permutation_index += skip_by
                    # skip_total += skip_by
                    continue

                if distance < min_distance:
                    # print("{} PERMUTATION {} - {}, DISTANCE {:,} vs min {} (NEW MIN)".format(desc, permutation_index, permutation, distance, min_distance))
                    # log.info("{} PERMUTATION {}, DISTANCE {:,} (NEW MIN)".format(desc, permutation, int(distance)))
                    min_distance = distance
                    min_distance_permutation = permutation
                # else:
                #    print("{} PERMUTATION {} - {}, DISTANCE {} vs min {}".format(desc, permutation_index, permutation, distance, min_distance))
                #    #log.info("{} PERMUTATION {}, DISTANCE {}".format(desc, permutation, distance))

                # total += 1
                permutation_index += 1

            # print("total {}".format(total))
            # print("skip total {}".format(skip_total))
            # print("")

        elif color_permutations == "odd_cube_center_color_permutations":
            p = odd_cube_center_color_permutations

            for permutation in p:
                distance = (
                    distances_of_square_list_per_color[permutation[0]][0]
                    + distances_of_square_list_per_color[permutation[1]][1]
                    + distances_of_square_list_per_color[permutation[2]][2]
                    + distances_of_square_list_per_color[permutation[3]][3]
                    + distances_of_square_list_per_color[permutation[4]][4]
                    + distances_of_square_list_per_color[permutation[5]][5]
                )

                if distance < min_distance:
                    min_distance = distance
                    min_distance_permutation = permutation
                #    print("{} PERMUTATION {} -  {}, DISTANCE {:,} (NEW MIN)".format(desc, permutation_index, permutation, int(distance)))
                #    log.info("{} PERMUTATION {}, DISTANCE {:,} (NEW MIN)".format(desc, permutation, int(distance)))
                # else:
                #    print("{} PERMUTATION {}, DISTANCE {}".format(desc, permutation, distance))
                #    log.info("{} PERMUTATION {}, DISTANCE {}".format(desc, permutation, distance))

        # Assign the color name to the Square object
        for (index, squares_list) in enumerate(squares_lists):
            color_name = min_distance_permutation[index]

            for square in squares_list:
                square.color_name = color_name


    def get_squares_by_color_name(self):
        white_squares = []
        yellow_squares = []
        orange_squares = []
        red_squares = []
        green_squares = []
        blue_squares = []

        for side in (
            self.sideU,
            self.sideR,
            self.sideF,
            self.sideD,
            self.sideL,
            self.sideB,
        ):
            for square in side.center_squares + side.corner_squares + side.edge_squares:
                if square.color_name == "W":
                    white_squares.append(square)
                elif square.color_name == "Y":
                    yellow_squares.append(square)
                elif square.color_name == "O":
                    orange_squares.append(square)
                elif square.color_name == "R":
                    red_squares.append(square)
                elif square.color_name == "G":
                    green_squares.append(square)
                elif square.color_name == "B":
                    blue_squares.append(square)

        return (
            white_squares,
            yellow_squares,
            orange_squares,
            red_squares,
            green_squares,
            blue_squares,
        )


    # @timed_function
    def resolve_color_box(self):
        """
        Temporarily assign names to all squares, use crayola colors as reference point.

        We use these name assignments to build our "color_box" which will be our
        references W, Y, O, R, G, B colors for assigning color names to edge
        and center squares.
        """

        # If we are solving a 3x3x3 then we are most likely on an
        # underpowered platform like a LEGO EV3.  Save a lot of CPU cycles by only using the
        # corner squares to create the color box.
        corner_squares = []

        for side in (
            self.sideU,
            self.sideR,
            self.sideF,
            self.sideD,
            self.sideL,
            self.sideB,
        ):
            for square in side.corner_squares:
                corner_squares.append(square)

        sorted_corner_squares = traveling_salesman(corner_squares, "corner")

        self.assign_color_names(
            "corner squares for color box",
            sorted_corner_squares,
            "even_cube_center_color_permutations",
            crayola_colors,
        )

        result = self.write_colors("corners for color box", sorted_corner_squares)

        (
            white_squares,
            yellow_squares,
            orange_squares,
            red_squares,
            green_squares,
            blue_squares,
        ) = self.get_squares_by_color_name()
        self.color_box = {}
        self.color_box["W"] = square_list_to_lab(white_squares)
        self.color_box["Y"] = square_list_to_lab(yellow_squares)
        self.color_box["O"] = square_list_to_lab(orange_squares)
        self.color_box["R"] = square_list_to_lab(red_squares)
        self.color_box["G"] = square_list_to_lab(green_squares)
        self.color_box["B"] = square_list_to_lab(blue_squares)

        self.orange_baseline = self.color_box["O"]
        self.red_baseline = self.color_box["R"]

        # Nuke all color names (they were temporary)
        for side in (
            self.sideU,
            self.sideR,
            self.sideF,
            self.sideD,
            self.sideL,
            self.sideB,
        ):
            for square in side.center_squares + side.corner_squares + side.edge_squares:
                square.color_name = None

        color_box = self.write_color_box()

        return result, color_box


    # @timed_function
    def resolve_corner_squares(self):
        """
        Assign names to the corner squares
        """
        white = Square(
            None,
            "W",
            self.color_box["W"].red,
            self.color_box["W"].green,
            self.color_box["W"].blue,
        )
        yellow = Square(
            None,
            "Y",
            self.color_box["Y"].red,
            self.color_box["Y"].green,
            self.color_box["Y"].blue,
        )
        orange = Square(
            None,
            "O",
            self.color_box["O"].red,
            self.color_box["O"].green,
            self.color_box["O"].blue,
        )
        red = Square(
            None,
            "R",
            self.color_box["R"].red,
            self.color_box["R"].green,
            self.color_box["R"].blue,
        )
        green = Square(
            None,
            "G",
            self.color_box["G"].red,
            self.color_box["G"].green,
            self.color_box["G"].blue,
        )
        blue = Square(
            None,
            "B",
            self.color_box["B"].red,
            self.color_box["B"].green,
            self.color_box["B"].blue,
        )

        white.color_name = "W"
        yellow.color_name = "Y"
        orange.color_name = "O"
        red.color_name = "R"
        green.color_name = "G"
        blue.color_name = "B"

        target_corners = [
            (white, green, orange),
            (white, red, green),
            (white, orange, blue),
            (white, blue, red),
            (yellow, orange, green),
            (yellow, green, red),
            (yellow, blue, orange),
            (yellow, red, blue),
        ]

        from rubiks_color_resolver.cube_333 import corner_tuples

        corners = []

        for corner_tuple in corner_tuples:
            corners.append(
                [
                    self.pos2square[corner_tuple[0]],
                    self.pos2square[corner_tuple[1]],
                    self.pos2square[corner_tuple[2]],
                ]
            )

        sorted_corners = traveling_salesman_corners(target_corners + corners, "corners")

        # assign color names
        for x in range(0, len(sorted_corners), 2):
            corner1 = sorted_corners[x]
            corner2 = sorted_corners[x + 1]
            corner2[0].color_name = corner1[0].position
            corner2[1].color_name = corner1[1].position
            corner2[2].color_name = corner1[2].position

        return self.write_color_corners("corners", sorted_corners)


    # @timed_function
    def resolve_edge_squares(self):
        """
        Use traveling salesman algorithm to sort the colors
        """

        from rubiks_color_resolver.cube_333 import edge_orbit_id

        white = Square(
            None,
            "W",
            self.color_box["W"].red,
            self.color_box["W"].green,
            self.color_box["W"].blue,
        )
        yellow = Square(
            None,
            "Y",
            self.color_box["Y"].red,
            self.color_box["Y"].green,
            self.color_box["Y"].blue,
        )
        orange = Square(
            None,
            "O",
            self.color_box["O"].red,
            self.color_box["O"].green,
            self.color_box["O"].blue,
        )
        red = Square(
            None,
            "R",
            self.color_box["R"].red,
            self.color_box["R"].green,
            self.color_box["R"].blue,
        )
        green = Square(
            None,
            "G",
            self.color_box["G"].red,
            self.color_box["G"].green,
            self.color_box["G"].blue,
        )
        blue = Square(
            None,
            "B",
            self.color_box["B"].red,
            self.color_box["B"].green,
            self.color_box["B"].blue,
        )

        white.color_name = "W"
        yellow.color_name = "Y"
        orange.color_name = "O"
        red.color_name = "R"
        green.color_name = "G"
        blue.color_name = "B"

        result = []

        for target_orbit_id in range(self.orbits):
            edge_pairs = []

            for side in (self.sideU, self.sideD, self.sideL, self.sideR):
                for square in side.edge_squares:
                    orbit_id = edge_orbit_id[square.position]

                    if orbit_id == target_orbit_id:
                        partner_index = side.get_wing_partner(square.position)
                        partner = self.pos2square[partner_index]
                        edge_pair = (square, partner)

                        if (
                            edge_pair not in edge_pairs
                            and (edge_pair[1], edge_pair[0]) not in edge_pairs
                        ):
                            edge_pairs.append(edge_pair)

            if len(edge_pairs) == 12:
                target_edge_pairs = [
                    (white, orange),
                    (white, red),
                    (white, green),
                    (white, blue),
                    (green, orange),
                    (green, red),
                    (blue, orange),
                    (blue, red),
                    (yellow, orange),
                    (yellow, red),
                    (yellow, green),
                    (yellow, blue),
                ]

            elif len(edge_pairs) == 24:
                target_edge_pairs = [
                    (white, orange),
                    (white, orange),
                    (white, red),
                    (white, red),
                    (white, green),
                    (white, green),
                    (white, blue),
                    (white, blue),
                    (green, orange),
                    (green, orange),
                    (green, red),
                    (green, red),
                    (blue, orange),
                    (blue, orange),
                    (blue, red),
                    (blue, red),
                    (yellow, orange),
                    (yellow, orange),
                    (yellow, red),
                    (yellow, red),
                    (yellow, green),
                    (yellow, green),
                    (yellow, blue),
                    (yellow, blue),
                ]
            else:
                raise ValueError("found {} edge pairs".format(len(edge_pairs)))

            sorted_edge_pairs = traveling_salesman_edge_pairs(
                target_edge_pairs + edge_pairs, "edge pairs"
            )

            # assign color names
            for x in range(0, len(sorted_edge_pairs), 2):
                pair1 = sorted_edge_pairs[x]
                pair2 = sorted_edge_pairs[x + 1]
                pair2[0].color_name = pair1[0].position
                pair2[1].color_name = pair1[1].position

            item = self.write_color_edge_pairs("edges - orbit %d" % target_orbit_id, sorted_edge_pairs)
            result.append(item)
        return result


    # @timed_function
    def resolve_center_squares(self):
        """
        Use traveling salesman algorithm to sort the squares by color
        """

        from rubiks_color_resolver.cube_333 import center_groups

        for (desc, centers_squares) in center_groups:
            # log.debug("\n\n\n\n")
            # log.info("Resolve {}".format(desc))
            center_squares = []

            for position in centers_squares:
                square = self.pos2square[position]
                center_squares.append(square)

            if desc == "centers":
                sorted_center_squares = center_squares[:]
                permutations = "odd_cube_center_color_permutations"
            else:
                sorted_center_squares = traveling_salesman(center_squares, desc)
                permutations = "even_cube_center_color_permutations"

            self.assign_color_names(
                desc, sorted_center_squares, permutations, self.color_box
            )

            return self.write_colors(desc, sorted_center_squares)


    # @timed_function
    def crunch_colors(self):
        html_init_cube = self.html_cube("Initial RGB values", False, "initial_rgb_values")
        crayola = self.write_crayola_colors()

        gc.collect()
        corner_color_box, color_box = self.resolve_color_box()

       # corners
        gc.collect()
        corner_squares = self.resolve_corner_squares()

        # centers
        gc.collect()
        center_squares = self.resolve_center_squares()

        # edges
        gc.collect()
        edge_squares = self.resolve_edge_squares()
        gc.collect()
        self.set_state()
        gc.collect()
        self.sanity_check_edge_squares()
        gc.collect()
        self.validate_all_corners_found()
        gc.collect()
        self.validate_odd_cube_midge_vs_corner_parity()
        gc.collect()

        html_final_cube = self.html_cube("Final Cube", True, "final_cube")

        if self.write_debug_file:
            Env = Environment(loader=FileSystemLoader(__name__))
            Template = Env.get_template("report.html")
            #scan_data = {int(key): self.scan_data[key] for key in self.scan_data.keys()}
            HTML = Template.render(DateTime=datetime.datetime.now(), side_margin=10, square_size=40, size=self.width, scan_data=self.scan_data, init=html_init_cube, crayola=crayola, corner_color_box=corner_color_box, color_box=color_box, corner_squares=corner_squares, center_squares=center_squares, edge_squares=edge_squares, final=html_final_cube)
            with open(self.filename, "w") as File:
                File.write(HTML)


    def print_profile_data(self):
        # print_profile_data()
        pass


# @timed_function
def resolve_colors(argv):
    help_string = """usage: rubiks-color-resolver.py [-h] [-j] [--filename FILENAME] [--rgb RGB]

    optional arguments:
      -h, --help           show this help message and exit
      -j, --json           Print json results
      --filename FILENAME  Print json results
      --rgb RGB            RGB json
    """
    filename = None
    rgb = None
    use_json = False
    argv_index = 1

    while argv_index < len(argv):

        if argv[argv_index] == "--help":
            print(help_string)
            sys.exit(0)

        elif argv[argv_index] == "--filename":
            filename = argv[argv_index + 1]
            argv_index += 2

        elif argv[argv_index] == "--rgb":
            rgb = argv[argv_index + 1]
            argv_index += 2

        elif argv[argv_index] == "--json" or argv[argv_index] == "-j":
            use_json = True
            argv_index += 1

        else:
            print(help_string)
            sys.exit(1)

    if filename:
        with open(filename, "r") as fh:
            rgb = "".join(fh.readlines())
    elif rgb:
        pass
    else:
        print("ERROR: Neither --filename or --rgb was specified")
        sys.exit(1)

    argv = None
    scan_data = eval(rgb)

    for key, value in scan_data.items():
        scan_data[key] = tuple(value)

    #square_count = len(list(scan_data.keys()))
    #square_count_per_side = int(square_count / 6)
    #width = int(sqrt(square_count_per_side))

    cube = RubiksColorSolverGeneric()
    #cube.filename = "Report.html"
    cube.write_debug_file = True
    cube.enter_scan_data(scan_data)
    cube.crunch_colors()
    cube.print_profile_data()
    cube.print_cube()

    if use_json:
        from json import dumps as json_dumps

        result = json_dumps(cube.cube_for_json(), indent=4, sort_keys=True)
    else:
        result = "".join(cube.cube_for_kociemba_strict())

    print(result)
    return result
