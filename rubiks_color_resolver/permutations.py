def permutations(iterable, r=None):
    """
    From https://github.com/python/cpython/blob/master/Modules/itertoolsmodule.c
    """
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    indices = list(range(n))
    cycles = list(range(n - r + 1, n + 1))[::-1]
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(list(range(r))):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1 :] + indices[i : i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


odd_cube_center_color_permutations = (
    ("W", "O", "G", "R", "B", "Y"),
    ("W", "G", "R", "B", "O", "Y"),
    ("W", "B", "O", "G", "R", "Y"),
    ("W", "R", "B", "O", "G", "Y"),
    ("Y", "B", "R", "G", "O", "W"),
    ("Y", "G", "O", "B", "R", "W"),
    ("Y", "R", "G", "O", "B", "W"),
    ("Y", "O", "B", "R", "G", "W"),
    ("O", "Y", "G", "W", "B", "R"),
    ("O", "W", "B", "Y", "G", "R"),
    ("O", "G", "W", "B", "Y", "R"),
    ("O", "B", "Y", "G", "W", "R"),
    ("G", "Y", "R", "W", "O", "B"),
    ("G", "W", "O", "Y", "R", "B"),
    ("G", "R", "W", "O", "Y", "B"),
    ("G", "O", "Y", "R", "W", "B"),
    ("R", "Y", "B", "W", "G", "O"),
    ("R", "W", "G", "Y", "B", "O"),
    ("R", "B", "W", "G", "Y", "O"),
    ("R", "G", "Y", "B", "W", "O"),
    ("B", "W", "R", "Y", "O", "G"),
    ("B", "Y", "O", "W", "R", "G"),
    ("B", "R", "Y", "O", "W", "G"),
    ("B", "O", "W", "R", "Y", "G"),
)

# even_cube_center_color_permutations = list(sorted(permutations(ALL_COLORS)))
even_cube_center_color_permutations = """B G O R W Y
B G O R Y W
B G O W R Y
B G O W Y R
B G O Y R W
B G O Y W R
B G R O W Y
B G R O Y W
B G R W O Y
B G R W Y O
B G R Y O W
B G R Y W O
B G W O R Y
B G W O Y R
B G W R O Y
B G W R Y O
B G W Y O R
B G W Y R O
B G Y O R W
B G Y O W R
B G Y R O W
B G Y R W O
B G Y W O R
B G Y W R O
B O G R W Y
B O G R Y W
B O G W R Y
B O G W Y R
B O G Y R W
B O G Y W R
B O R G W Y
B O R G Y W
B O R W G Y
B O R W Y G
B O R Y G W
B O R Y W G
B O W G R Y
B O W G Y R
B O W R G Y
B O W R Y G
B O W Y G R
B O W Y R G
B O Y G R W
B O Y G W R
B O Y R G W
B O Y R W G
B O Y W G R
B O Y W R G
B R G O W Y
B R G O Y W
B R G W O Y
B R G W Y O
B R G Y O W
B R G Y W O
B R O G W Y
B R O G Y W
B R O W G Y
B R O W Y G
B R O Y G W
B R O Y W G
B R W G O Y
B R W G Y O
B R W O G Y
B R W O Y G
B R W Y G O
B R W Y O G
B R Y G O W
B R Y G W O
B R Y O G W
B R Y O W G
B R Y W G O
B R Y W O G
B W G O R Y
B W G O Y R
B W G R O Y
B W G R Y O
B W G Y O R
B W G Y R O
B W O G R Y
B W O G Y R
B W O R G Y
B W O R Y G
B W O Y G R
B W O Y R G
B W R G O Y
B W R G Y O
B W R O G Y
B W R O Y G
B W R Y G O
B W R Y O G
B W Y G O R
B W Y G R O
B W Y O G R
B W Y O R G
B W Y R G O
B W Y R O G
B Y G O R W
B Y G O W R
B Y G R O W
B Y G R W O
B Y G W O R
B Y G W R O
B Y O G R W
B Y O G W R
B Y O R G W
B Y O R W G
B Y O W G R
B Y O W R G
B Y R G O W
B Y R G W O
B Y R O G W
B Y R O W G
B Y R W G O
B Y R W O G
B Y W G O R
B Y W G R O
B Y W O G R
B Y W O R G
B Y W R G O
B Y W R O G
G B O R W Y
G B O R Y W
G B O W R Y
G B O W Y R
G B O Y R W
G B O Y W R
G B R O W Y
G B R O Y W
G B R W O Y
G B R W Y O
G B R Y O W
G B R Y W O
G B W O R Y
G B W O Y R
G B W R O Y
G B W R Y O
G B W Y O R
G B W Y R O
G B Y O R W
G B Y O W R
G B Y R O W
G B Y R W O
G B Y W O R
G B Y W R O
G O B R W Y
G O B R Y W
G O B W R Y
G O B W Y R
G O B Y R W
G O B Y W R
G O R B W Y
G O R B Y W
G O R W B Y
G O R W Y B
G O R Y B W
G O R Y W B
G O W B R Y
G O W B Y R
G O W R B Y
G O W R Y B
G O W Y B R
G O W Y R B
G O Y B R W
G O Y B W R
G O Y R B W
G O Y R W B
G O Y W B R
G O Y W R B
G R B O W Y
G R B O Y W
G R B W O Y
G R B W Y O
G R B Y O W
G R B Y W O
G R O B W Y
G R O B Y W
G R O W B Y
G R O W Y B
G R O Y B W
G R O Y W B
G R W B O Y
G R W B Y O
G R W O B Y
G R W O Y B
G R W Y B O
G R W Y O B
G R Y B O W
G R Y B W O
G R Y O B W
G R Y O W B
G R Y W B O
G R Y W O B
G W B O R Y
G W B O Y R
G W B R O Y
G W B R Y O
G W B Y O R
G W B Y R O
G W O B R Y
G W O B Y R
G W O R B Y
G W O R Y B
G W O Y B R
G W O Y R B
G W R B O Y
G W R B Y O
G W R O B Y
G W R O Y B
G W R Y B O
G W R Y O B
G W Y B O R
G W Y B R O
G W Y O B R
G W Y O R B
G W Y R B O
G W Y R O B
G Y B O R W
G Y B O W R
G Y B R O W
G Y B R W O
G Y B W O R
G Y B W R O
G Y O B R W
G Y O B W R
G Y O R B W
G Y O R W B
G Y O W B R
G Y O W R B
G Y R B O W
G Y R B W O
G Y R O B W
G Y R O W B
G Y R W B O
G Y R W O B
G Y W B O R
G Y W B R O
G Y W O B R
G Y W O R B
G Y W R B O
G Y W R O B
O B G R W Y
O B G R Y W
O B G W R Y
O B G W Y R
O B G Y R W
O B G Y W R
O B R G W Y
O B R G Y W
O B R W G Y
O B R W Y G
O B R Y G W
O B R Y W G
O B W G R Y
O B W G Y R
O B W R G Y
O B W R Y G
O B W Y G R
O B W Y R G
O B Y G R W
O B Y G W R
O B Y R G W
O B Y R W G
O B Y W G R
O B Y W R G
O G B R W Y
O G B R Y W
O G B W R Y
O G B W Y R
O G B Y R W
O G B Y W R
O G R B W Y
O G R B Y W
O G R W B Y
O G R W Y B
O G R Y B W
O G R Y W B
O G W B R Y
O G W B Y R
O G W R B Y
O G W R Y B
O G W Y B R
O G W Y R B
O G Y B R W
O G Y B W R
O G Y R B W
O G Y R W B
O G Y W B R
O G Y W R B
O R B G W Y
O R B G Y W
O R B W G Y
O R B W Y G
O R B Y G W
O R B Y W G
O R G B W Y
O R G B Y W
O R G W B Y
O R G W Y B
O R G Y B W
O R G Y W B
O R W B G Y
O R W B Y G
O R W G B Y
O R W G Y B
O R W Y B G
O R W Y G B
O R Y B G W
O R Y B W G
O R Y G B W
O R Y G W B
O R Y W B G
O R Y W G B
O W B G R Y
O W B G Y R
O W B R G Y
O W B R Y G
O W B Y G R
O W B Y R G
O W G B R Y
O W G B Y R
O W G R B Y
O W G R Y B
O W G Y B R
O W G Y R B
O W R B G Y
O W R B Y G
O W R G B Y
O W R G Y B
O W R Y B G
O W R Y G B
O W Y B G R
O W Y B R G
O W Y G B R
O W Y G R B
O W Y R B G
O W Y R G B
O Y B G R W
O Y B G W R
O Y B R G W
O Y B R W G
O Y B W G R
O Y B W R G
O Y G B R W
O Y G B W R
O Y G R B W
O Y G R W B
O Y G W B R
O Y G W R B
O Y R B G W
O Y R B W G
O Y R G B W
O Y R G W B
O Y R W B G
O Y R W G B
O Y W B G R
O Y W B R G
O Y W G B R
O Y W G R B
O Y W R B G
O Y W R G B
R B G O W Y
R B G O Y W
R B G W O Y
R B G W Y O
R B G Y O W
R B G Y W O
R B O G W Y
R B O G Y W
R B O W G Y
R B O W Y G
R B O Y G W
R B O Y W G
R B W G O Y
R B W G Y O
R B W O G Y
R B W O Y G
R B W Y G O
R B W Y O G
R B Y G O W
R B Y G W O
R B Y O G W
R B Y O W G
R B Y W G O
R B Y W O G
R G B O W Y
R G B O Y W
R G B W O Y
R G B W Y O
R G B Y O W
R G B Y W O
R G O B W Y
R G O B Y W
R G O W B Y
R G O W Y B
R G O Y B W
R G O Y W B
R G W B O Y
R G W B Y O
R G W O B Y
R G W O Y B
R G W Y B O
R G W Y O B
R G Y B O W
R G Y B W O
R G Y O B W
R G Y O W B
R G Y W B O
R G Y W O B
R O B G W Y
R O B G Y W
R O B W G Y
R O B W Y G
R O B Y G W
R O B Y W G
R O G B W Y
R O G B Y W
R O G W B Y
R O G W Y B
R O G Y B W
R O G Y W B
R O W B G Y
R O W B Y G
R O W G B Y
R O W G Y B
R O W Y B G
R O W Y G B
R O Y B G W
R O Y B W G
R O Y G B W
R O Y G W B
R O Y W B G
R O Y W G B
R W B G O Y
R W B G Y O
R W B O G Y
R W B O Y G
R W B Y G O
R W B Y O G
R W G B O Y
R W G B Y O
R W G O B Y
R W G O Y B
R W G Y B O
R W G Y O B
R W O B G Y
R W O B Y G
R W O G B Y
R W O G Y B
R W O Y B G
R W O Y G B
R W Y B G O
R W Y B O G
R W Y G B O
R W Y G O B
R W Y O B G
R W Y O G B
R Y B G O W
R Y B G W O
R Y B O G W
R Y B O W G
R Y B W G O
R Y B W O G
R Y G B O W
R Y G B W O
R Y G O B W
R Y G O W B
R Y G W B O
R Y G W O B
R Y O B G W
R Y O B W G
R Y O G B W
R Y O G W B
R Y O W B G
R Y O W G B
R Y W B G O
R Y W B O G
R Y W G B O
R Y W G O B
R Y W O B G
R Y W O G B
W B G O R Y
W B G O Y R
W B G R O Y
W B G R Y O
W B G Y O R
W B G Y R O
W B O G R Y
W B O G Y R
W B O R G Y
W B O R Y G
W B O Y G R
W B O Y R G
W B R G O Y
W B R G Y O
W B R O G Y
W B R O Y G
W B R Y G O
W B R Y O G
W B Y G O R
W B Y G R O
W B Y O G R
W B Y O R G
W B Y R G O
W B Y R O G
W G B O R Y
W G B O Y R
W G B R O Y
W G B R Y O
W G B Y O R
W G B Y R O
W G O B R Y
W G O B Y R
W G O R B Y
W G O R Y B
W G O Y B R
W G O Y R B
W G R B O Y
W G R B Y O
W G R O B Y
W G R O Y B
W G R Y B O
W G R Y O B
W G Y B O R
W G Y B R O
W G Y O B R
W G Y O R B
W G Y R B O
W G Y R O B
W O B G R Y
W O B G Y R
W O B R G Y
W O B R Y G
W O B Y G R
W O B Y R G
W O G B R Y
W O G B Y R
W O G R B Y
W O G R Y B
W O G Y B R
W O G Y R B
W O R B G Y
W O R B Y G
W O R G B Y
W O R G Y B
W O R Y B G
W O R Y G B
W O Y B G R
W O Y B R G
W O Y G B R
W O Y G R B
W O Y R B G
W O Y R G B
W R B G O Y
W R B G Y O
W R B O G Y
W R B O Y G
W R B Y G O
W R B Y O G
W R G B O Y
W R G B Y O
W R G O B Y
W R G O Y B
W R G Y B O
W R G Y O B
W R O B G Y
W R O B Y G
W R O G B Y
W R O G Y B
W R O Y B G
W R O Y G B
W R Y B G O
W R Y B O G
W R Y G B O
W R Y G O B
W R Y O B G
W R Y O G B
W Y B G O R
W Y B G R O
W Y B O G R
W Y B O R G
W Y B R G O
W Y B R O G
W Y G B O R
W Y G B R O
W Y G O B R
W Y G O R B
W Y G R B O
W Y G R O B
W Y O B G R
W Y O B R G
W Y O G B R
W Y O G R B
W Y O R B G
W Y O R G B
W Y R B G O
W Y R B O G
W Y R G B O
W Y R G O B
W Y R O B G
W Y R O G B
Y B G O R W
Y B G O W R
Y B G R O W
Y B G R W O
Y B G W O R
Y B G W R O
Y B O G R W
Y B O G W R
Y B O R G W
Y B O R W G
Y B O W G R
Y B O W R G
Y B R G O W
Y B R G W O
Y B R O G W
Y B R O W G
Y B R W G O
Y B R W O G
Y B W G O R
Y B W G R O
Y B W O G R
Y B W O R G
Y B W R G O
Y B W R O G
Y G B O R W
Y G B O W R
Y G B R O W
Y G B R W O
Y G B W O R
Y G B W R O
Y G O B R W
Y G O B W R
Y G O R B W
Y G O R W B
Y G O W B R
Y G O W R B
Y G R B O W
Y G R B W O
Y G R O B W
Y G R O W B
Y G R W B O
Y G R W O B
Y G W B O R
Y G W B R O
Y G W O B R
Y G W O R B
Y G W R B O
Y G W R O B
Y O B G R W
Y O B G W R
Y O B R G W
Y O B R W G
Y O B W G R
Y O B W R G
Y O G B R W
Y O G B W R
Y O G R B W
Y O G R W B
Y O G W B R
Y O G W R B
Y O R B G W
Y O R B W G
Y O R G B W
Y O R G W B
Y O R W B G
Y O R W G B
Y O W B G R
Y O W B R G
Y O W G B R
Y O W G R B
Y O W R B G
Y O W R G B
Y R B G O W
Y R B G W O
Y R B O G W
Y R B O W G
Y R B W G O
Y R B W O G
Y R G B O W
Y R G B W O
Y R G O B W
Y R G O W B
Y R G W B O
Y R G W O B
Y R O B G W
Y R O B W G
Y R O G B W
Y R O G W B
Y R O W B G
Y R O W G B
Y R W B G O
Y R W B O G
Y R W G B O
Y R W G O B
Y R W O B G
Y R W O G B
Y W B G O R
Y W B G R O
Y W B O G R
Y W B O R G
Y W B R G O
Y W B R O G
Y W G B O R
Y W G B R O
Y W G O B R
Y W G O R B
Y W G R B O
Y W G R O B
Y W O B G R
Y W O B R G
Y W O G B R
Y W O G R B
Y W O R B G
Y W O R G B
Y W R B G O
Y W R B O G
Y W R G B O
Y W R G O B
Y W R O B G
Y W R O G B"""
len_even_cube_center_color_permutations = 720
