import test_matplotlib.pyplot as plt
from scipy.integrate import quad, cumtrapz, trapz
import numpy as np


###################################################################################
######################            TOOLKIT FUNCTIONS           #####################
###################################################################################

def get_integral_func(**kwargs) -> float:
    """
    Integrate func from a to b.

    :param kwargs:
        func: Union[function, LowLevelCallable],
        a: float,
        b: float,
        args: Union[Iterable, tuple, None] = (),

    :return: The integral of func from a to b.
    """
    return quad(**kwargs)[0]


def get_integral_value(**kwargs) -> float:
    """
    Integrate along the given axis using the composite trapezoidal rule.

    :param kwargs:
        y: Union[ndarray, Iterable, int, float],
        x: Union[ndarray, Iterable, int, float, None] = None,
        dx: Union[int, float, complex, None] = 1.0,
        axis: Optional[int] = -1

    :return: The integral of data samples.
    """
    return trapz(**kwargs)


def get_integral_array(**kwargs) -> np.ndarray:
    """
    Cumulatively integrate y(x) using the composite trapezoidal rule.

    :param kwargs:
        y: Union[ndarray, Iterable, int, float],
        x: Union[ndarray, Iterable, int, float, None] = None,
        dx: Optional[float] = 1.0,
        axis: Optional[int] = -1,
        initial: Union[int, float, complex, None] = None

    :return: The result of cumulative integration of y.
    """

    return cumtrapz(**kwargs)


def sum_data(*args) -> float:
    """
    Sum of variable number of arguments

    :param args:
    :return:
    """

    total = 0.

    for arg in args:
        total += np.sum(arg)

    return total


def cumsum_data(arg: np.ndarray) -> np.ndarray:
    """
    Cumulative sum of numpy array argument

    :param arg:
    :return:
    """

    return np.cumsum(arg)


###################################################################################
######################            TESTING FUNCTIONS           #####################
###################################################################################

def test_integral():
    # # examples of how to use the above functions
    # # integral of cosine function from 0 to PI/2
    # integral_value = integral_func(func=np.cos, a=0., b=np.pi / 2., args=None)
    # print(f'integral value of func: {integral_value}')
    #
    # integral_value = integral_data(y=np.cos(np.linspace(start=0.0, stop=np.pi / 2, num=100, endpoint=False)),
    #                                x=np.linspace(start=0.0, stop=np.pi / 2, num=100, endpoint=False))
    # print(f'integral value of data: {integral_value}')
    #
    # integral_value = integral_data(y=np.cos(np.linspace(start=0.0, stop=np.pi / 2, num=100, endpoint=False)),
    #                                dx=np.pi / 2 / 100)
    # print(f'integral value of data: {integral_value}')
    #
    integral_value = get_integral_value(y=np.cos(np.linspace(start=0.0, stop=1., num=100, endpoint=True)),
                                        x=np.linspace(start=0.0, stop=1., num=100, endpoint=True))
    print(f'integral value of data: {integral_value}')

    x = np.linspace(start=0., stop=100, num=100, endpoint=True)
    x = np.linspace(start=0.0, stop=1., num=100, endpoint=True)

    y1 = x[:50]
    y1 = np.cos(x[:50])
    y1i = get_integral_array(y=y1, x=x[:50], initial=0)

    y2 = x[49:]
    y2 = np.cos(x[49:])
    y2i = get_integral_array(y=y2, x=x[49:], initial=0) + y1i[-1]
    print(y2i[-1])

    plt.plot(x[:50], y1,
             x[:50], y1i,
             x[49:], y2,
             x[49:], y2i)
    plt.show()


def test_sum():
    print(f'data:\n {np.array([[1, 2, 3], [11, 22, 33]])}')
    print(f'total:\n {sum_data(np.array([[1, 2, 3], [11, 22, 33]]))}')
    print()

    print(f'data:\n {[1, 2, 3], [4, 5, 6]}')
    print(f'total:\n {sum_data([1, 2, 3], [4, 5, 6])}')
    print()

    print(f'data:\n {np.array([.23]), np.array([1, 2])}')
    print(f'total:\n {sum_data(np.array([.23]), np.array([1, 2]))}')
    print()

    print(f'data:\n {3.14, np.array([1, 2])}')
    print(f'total:\n {sum_data(3.14, np.array([1, 2]))}')
    print()

    print(f'data:\n {3.14, [1, 2]}')
    print(f'total:\n {sum_data(3.14, [1, 2])}')
    print()

    print(f'data:\n {3.14, (1, 2)}')
    print(f'total:\n {sum_data(3.14, (1, 2))}')
    print()


def test_cumsum():
    print(f'data array:\n {np.array([[1, 2, 3, 4]])}')
    print(f'cumulative sum array:\n {cumsum_data(np.array([1, 2, 3, 4]))}')
    print()


def main():
    test_integral()
    # test_sum()
    # test_cumsum()


if __name__ == '__main__':
    main()
