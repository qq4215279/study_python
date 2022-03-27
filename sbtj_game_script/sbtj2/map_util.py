def index_to_x_y(index):
    return index / 1200, index % 1200


def x_y_to_index(x, y):
    return x * 1200 + y
