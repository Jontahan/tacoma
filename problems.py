import functools
import numpy as np

import lib


def tacoma(l=6, m=2500, d=0.01, omega=2 * np.pi * (38 / 60), W=0):
    a = 0.2
    c = 1000 / (m * a)

    def f(t, y):
        s = np.sin(y[2, 0])
        a1 = np.exp(a * (y[0, 0] - l * s))
        a2 = np.exp(a * (y[0, 0] + l * s))

        return np.matrix([
            [y[1, 0]],
            [-d * y[1, 0] - c * (a1 + a2 - 2) + 0.2 * W * np.sin(omega * t)],
            [y[3, 0]],
            [-d * y[3, 0] + c * (3 * np.cos(y[2, 0]) / l) * (a1 - a2)]
        ])

    return f


def tacoma_over_w(l, t, iv, tolerance, reduce_fn_gen):
    def f(W):
        results = lib.variable_euler(tacoma(W=W, l=l), t=t, iv=(0, iv), tolerance=tolerance)

        reduce_fn, initializer = reduce_fn_gen(W)
        return functools.reduce(reduce_fn, results, initializer)

    return f


def tacoma_over_iv_theta(l, t, W, tolerance, reduce_fn_gen):
    def f(p):
        iv = np.matrix([
            [0],
            [0],
            [10 ** p],
            [0]
        ])

        results = lib.variable_euler(tacoma(W=W, l=l), t=t, iv=(0, iv), tolerance=tolerance)

        reduce_fn, initializer = reduce_fn_gen(p)
        return functools.reduce(reduce_fn, results, initializer)

    return f

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    l = 6

    iv = np.matrix([
        [0],
        [0],
        [1e-3],
        [0]
    ])


    def reduce(W):
        def r(max_so_far, result):
            return max(max_so_far, np.abs(result['w'][2, 0]))

        return r, 0

    max_theta = tacoma_over_w(l, 1000, iv, 1e-10, reduce)
    f = lambda x: max_theta(x) / iv[2, 0]

    print(lib.secant_method(f, 58, 59, y=100, tolerance=1e-10))

    # ws = range(-10, -2)
    #
    # lib.plot_gen((f(w) for w in ws), x_keys=[0], y_keys=[2])
    # plt.show()