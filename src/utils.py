def is_around(point_a, point_b):
    return abs(point_a[0] - point_b[0]) <= 1 \
           and abs(point_a[1] - point_b[1]) <= 1


def around_block(row, col, min_row, max_row, min_col, max_col):
    block_list = []
    for step in [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
        cur_row, cur_col = row + step[0], col + step[1]
        if min_row <= cur_row <= max_row and min_col <= cur_col <= max_col:
            block_list.append((cur_row, cur_col))
    return block_list

