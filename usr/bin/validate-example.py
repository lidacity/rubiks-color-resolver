#!/usr/bin/env python

"""
This is an example of how to use RubiksColorSolverGenericBase to
determine if the state of your cube is valid
"""

from rubiks_color_resolver.base import RubiksColorSolverGenericBase

cube = RubiksColorSolverGenericBase()
cube.enter_cube_state("FFBFUBFBBUDDURDUUDRLLRFLRRLBBFBDFBFFUDDULDUUDLRRLBRLLR")
cube.sanity_check_edge_squares()
cube.validate_all_corners_found()
cube.validate_odd_cube_midge_vs_corner_parity()
cube.print_cube()
print("".join(cube.cube_for_kociemba_strict()))
