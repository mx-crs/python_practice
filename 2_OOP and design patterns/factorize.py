def factorize(x):

    """ Factorize positive integer and return its factors.

    :param x: int, >=0
    :return: tuple[N], N>0
    """
    simples = []
    i = 2

    if x < 0:
        raise ValueError
    elif type(x) == float:
        raise TypeError
    elif x == 1 or x == 0:
        return tuple((x,))
    while i < x+1:
        if x % i == 0:
            x = int(x / i)
            simples.append(i)
        else:
            i += 1
    return tuple(simples)
