# Fork rubiks-color-resolver

## python3 install
```
$ sudo python3 -m pip install git+https://github.com/lidacity/rubiks-color-resolver.git
```

## Changed
- formatting 'RGB Input' in report
- rename packagename
- remove micropython-support (sorry)
- support only rubik's cube 3x3x3
- one-letter color name
- ninja2-report


## Overview
rubiks-color-resolver.py
- accept a JSON string of RGB values for each square of a rubik'ss cube (only 3x3x3 are supported).
- analyzes all RGB values to assign each square one of the six colors of the cube. It then uses a Travelling Salesman algorithm (tsp_solver) to sort the colors.



# Original rubiks-color-resolver

## python3 install
```
$ sudo python3 -m pip install git+https://github.com/dwalton76/rubiks-color-resolver.git
```

## Overview
rubiks-color-resolver.py
- accept a JSON string of RGB values for each square of a rubik'ss cube. 2x2x2, 3x3x3, 4x4x4, 5x5x5, 6x6x6 and 7x7x7 are supported.
- analyzes all RGB values to assign each square one of the six colors of the cube. It then uses a Travelling Salesman algorithm (tsp_solver) to sort the colors.

```
./rubiks-color-resolver.py --filename ./tests/test-data/3x3x3-tetris.txt
Cube

           OR OR Rd
           OR Ye Rd
           OR Rd Rd
 Ye Wh Wh  Bu Gr Gr  Ye Wh Wh  Gr Bu Bu
 Ye Gr Wh  Bu OR Gr  Ye Bu Wh  Gr Rd Bu
 Ye Ye Wh  Bu Bu Gr  Ye Ye Wh  Gr Gr Bu
           Rd Rd OR
           Rd Wh OR
           Rd OR OR

FFBFUBFBBUDDURDUUDRLLRFLRRLBBFBDFBFFUDDULDUUDLRRLBRLLR
```
