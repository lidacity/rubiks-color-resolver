try:
    from json import load as json_load
except ImportError:
    from ujson import load as json_load

from math import sqrt
from rubiks_color_resolver import RubiksColorSolverGeneric
import gc
import logging


# logging.basicConfig(filename='rubiks-rgb-solver.log',
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)5s: %(message)s"
)
log = logging.getLogger(__name__)

# To add a test case:
# - place the cube in the robot, solve it
# - in the log output grab the "RGB json" and save that in a file in test-data
# - in the log output grab the "Final cube for kociema", this is what you put in the entry in the test_cases tuple
test_cases = (
    (
        "3x3x3 solved",
        "test-data/3x3x3-solved.txt",
        "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
    ),
    (
        "3x3x3 checkerboard",
        "test-data/3x3x3-checkerboard.txt",
        "UDUDUDUDURLRLRLRLRFBFBFBFBFDUDUDUDUDLRLRLRLRLBFBFBFBFB",
    ),
    (
        "3x3x3 cross",
        "test-data/3x3x3-cross.txt",
        "DUDUUUDUDFRFRRRFRFRFRFFFRFRUDUDDDUDUBLBLLLBLBLBLBBBLBL",
    ),
    (
        "3x3x3 tetris",
        "test-data/3x3x3-tetris.txt",
        "FFBFUBFBBUDDURDUUDRLLRFLRRLBBFBDFBFFUDDULDUUDLRRLBRLLR",
    ),
    (
        "3x3x3 superflip",
        "test-data/3x3x3-superflip.txt",
        "UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB",
    ),
    (
        "3x3x3 random 01",
        "test-data/3x3x3-random-01.txt",
        "DURUULDBRFDFLRRLFBRLUUFFUFFLRUDDDRRDLBBDLLBBBDFFBBRLUU",
    ),
    (
        "3x3x3 random 02",
        "test-data/3x3x3-random-02.txt",
        "BBRLULRBFDDUURFBULDULRFRUDRFBDFDLUFBUFFRLDRDLFLLRBBDUB",
    ),
    (
        "3x3x3 random 03",
        "test-data/3x3x3-random-03.txt",
        "DFDRULUFDLFLDRBBLRLRFBFLUDURFRRDUUBDFUBBLDLDFBURRBUBLF",
    ),
    (
        "3x3x3 random 04",
        "test-data/3x3x3-random-04.txt",
        "LRBFULUBBDUULRRLBULRRLFDFBBRUDLDDFRFFUBFLBUFDRUDDBDRFL",
    ),
    (
        "3x3x3 random 05",
        "test-data/3x3x3-random-05.txt",
        "BRRDUFDFUBDFFRBDDUBRRRFLLUFUBLRDBBFFULLULBRDFDULLBLRUD",
    ),
    (
        "3x3x3 random 07",
        "test-data/3x3x3-random-07.txt",
        "BUDDUBLDDRURURFBLDULBFFLRDDFRLRDBRDFUFFRLLBFUFRLUBBLBU",
    ),
)

results = []

for (desc, filename, expected) in test_cases:
    log.warning("Test: %s" % desc)
    with open("tests/" + filename, "r") as fh:
        scan_data_str_keys = json_load(fh)
        scan_data = {}
        square_count = 0

        for (key, value) in scan_data_str_keys.items():
            scan_data[int(key)] = value
            square_count += 1

        #square_count_per_side = int(square_count / 6)
        #width = int(sqrt(square_count_per_side))

        cube = RubiksColorSolverGeneric()
        try:
            cube.enter_scan_data(scan_data)
            cube.crunch_colors()
            output = "".join(cube.cube_for_kociemba_strict())
        except Exception as e:
            print(e)
            log.exception(str(e))
            #output = "Exception"
            output = e

        if output == expected:
            results.append("\033[92mPASS\033[0m: %s" % desc)
        else:
            results.append("\033[91mFAIL\033[0m: %s" % desc)
            results.append("   expected %s" % expected)
            results.append("   output   %s" % output)

        cube = None
        gc.collect()

print("\n".join(results))
