import os
import pathlib
import math
import numpy as np

__all__ = ['GOLDEN_RATIO', 'time_format', 'getfiles', 'get_prime_factors',
           'profiling_app', 'sign', 'is_prime']

GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def time_format(timevalue: (int, float),
                prefix: str = "",
                suffix: str = "") -> str:
    """
    Format the input time interval in seconds as a string in the format:
    'days d, hours h, minutes m, seconds s'
    For time intervals smaller than 1 second, the output is formatted in milliseconds:
    'milliseconds ms'

    Args:
        timevalue (int, float): input time in seconds
        prefix (str): string appended before the formatted time
        suffix (str): string appended after the formatted time

    Returns:
        str: formatted string in the appropriate time units

    Examples:
    >>> time_format(0)
    ''
    >>> time_format(12345678)
    '142d 21h 21m 18s'
    >>> time_format(123456)
    '1d 10h 17m 36s'
    >>> time_format(1234, prefix="Total time: ")
    'Total time: 20m 34s'
    >>> time_format(1234, suffix=" elapsed")
    '20m 34s elapsed'
    >>> time_format(0.0234)
    '23.4 ms'
    >>> time_format(0.00000000456)
    '4.56 ns'
    >>> time_format(0.00000000000000567)
    '5.67 fs'
    >>> time_format(0.00000000000000000000000678)
    '6.78 ys'
    >>> time_format(-1.5)
    """
    return_message = ""
    si_prefix = {-3: 'm', -6: 'u', -9: 'n', -12: 'p', -15: 'f', -18: 'a', -21: 'z', -24: 'y',
                 3: 'k', 6: 'M', 9: 'G', 12: 'T', 15: 'P', 18: 'E', 21: 'Z', 24: 'Y'}
    _prefix = {'y': 1e-24,  # yocto
               'z': 1e-21,  # zepto
               'a': 1e-18,  # atto
               'f': 1e-15,  # femto
               'p': 1e-12,  # pico
               'n': 1e-9,  # nano
               'u': 1e-6,  # micro
               'm': 1e-3,  # mili
               'c': 1e-2,  # centi
               'd': 1e-1,  # deci
               'k': 1e3,  # kilo
               'M': 1e6,  # mega
               'G': 1e9,  # giga
               'T': 1e12,  # tera
               'P': 1e15,  # peta
               'E': 1e18,  # exa
               'Z': 1e21,  # zetta
               'Y': 1e24,  # yotta
               }
    if abs(timevalue) >= 1:
        days, rest = divmod(timevalue, 86400)
        hours, rest = divmod(rest, 3600)
        minutes, seconds = divmod(rest, 60)

        days_str = f'{int(days):g}d' if days > 0 else ''
        hours_str = f' {int(hours):g}h' if hours > 0 else ''
        minutes_str = f' {int(minutes):g}m' if minutes > 0 else ''
        seconds_str = f' {int(seconds):g}s'
        time_message = f'{days_str}{hours_str}{minutes_str}{seconds_str}'.strip()
        return_message = prefix + time_message + suffix

    if 0 < timevalue < 1:
        number_of_significant_digits = math.floor(math.log10(timevalue))
        closest_si_prefix = np.argmin(abs(number_of_significant_digits - np.array(list(si_prefix.keys()))))
        time_message = f"{round(timevalue * 10 ** (-list(si_prefix.keys())[closest_si_prefix]), 3)} " \
                       f"{si_prefix.get(list(si_prefix.keys())[closest_si_prefix])}s"
        return_message = prefix + time_message + suffix

    return return_message


def getfiles(sourcedir: (str, pathlib.Path),
             extensions: tuple = None,
             exclusions: tuple = None) -> list:
    """
    Get all files within the given source folder and all its subfolders.
    The list can be filtered by selecting and excluding extensions.

    Args:
        sourcedir (str, os.PathLike): input source folder to start the files search
        extensions (tuple): list of included extensions
        exclusions (tuple): list of excluded extensions

    Returns:
        list: files matching the extension filters in the source folder and subfolders

    Examples:
    >>> getfiles("./")
    ['./_utils.py', './__init__.py', './__pycache__\\\\main.cpython-38.pyc', './__pycache__\\\\__init__.cpython-38.pyc']
    >>> getfiles("./", extensions=('.py',))
    ['./_utils.py', './__init__.py']
    >>> getfiles("./", exclusions=('.pyc',))
    ['./_utils.py', './__init__.py']
    """
    if not sourcedir:
        raise TypeError("Path should be string, bytes, os.PathLike or integer, not NoneType")
    if not isinstance(sourcedir, (str, pathlib.Path)):
        raise TypeError(f"Path should be string, bytes, os.PathLike or integer, not {type(sourcedir)}")

    sourcedir = str(sourcedir)

    if not os.path.isdir(sourcedir):
        raise TypeError("Path does not exist")

    if extensions == exclusions:
        return [os.path.join(root, f) for root, dirs, files in os.walk(sourcedir) for f in files]

    if extensions and exclusions:
        return [os.path.join(root, f) for root, dirs, files in os.walk(sourcedir) for f in files if
                f.endswith(extensions) and not f.endswith(exclusions)]

    if extensions:
        return [os.path.join(root, f) for root, dirs, files in os.walk(sourcedir) for f in files if
                f.endswith(extensions)]

    if exclusions:
        return [os.path.join(root, f) for root, dirs, files in os.walk(sourcedir) for f in files if
                not f.endswith(exclusions)]

    return [os.path.join(root, f) for root, dirs, files in os.walk(sourcedir) for f in files]


def get_prime_factors(number: int) -> list:
    """
    Get all prime factors of an number

    Args:
        number (int): input number. If the number is not an integer, the closest
            integer smaller than the input number will be used. If the number is
            negative, `-1` is added to the list of prime factors, and the absolute
            value of the input number will be used to calculate the prime factors.

    Returns:
        list: prime factors of input number.

    Examples:
    >>> get_prime_factors(270)
    [2, 3, 3, 3, 5]
    >>> get_prime_factors(-270)
    [-1, 2, 3, 3, 3, 5]
    >>> get_prime_factors(270.34)
    [2, 3, 3, 3, 5]
    """
    prime_factors = []
    if number < 0:
        number = abs(number)
        prime_factors.append(-1)

    if not isinstance(number, int):
        number = math.floor(number)

    while number % 2 == 0:
        prime_factors.append(2)
        number //= 2

    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while number % i == 0:
            prime_factors.append(int(i))
            number //= i

    if number > 2:
        prime_factors.append(int(number))

    return prime_factors


def profiling_app(function, parameters):
    """
    Profile application performance

    Args:
        function (function): function to test
        parameters (list): parameters used to run the function

    Returns:
        printout of application's performance

    Examples:
    >>> profiling_app(time_format, [1234])
             6 function calls in 0.000 seconds
    <BLANKLINE>
       Ordered by: internal time
    <BLANKLINE>
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 F:/Python/utils/utils/_utils.py:14(time_format)
            3    0.000    0.000    0.000    0.000 {built-in method builtins.divmod}
            1    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    <BLANKLINE>
    <BLANKLINE>
    >>> profiling_app(get_prime_factors, [270])
             9 function calls in 0.000 seconds
    <BLANKLINE>
       Ordered by: internal time
    <BLANKLINE>
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 F:/Python/utils/utils/_utils.py:146(get_prime_factors)
            1    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
            5    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
            1    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    <BLANKLINE>
    <BLANKLINE>
    """
    import cProfile
    import pstats
    pr = cProfile.Profile()
    pr.enable()
    function(*parameters)
    pr.disable()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


def sign(x):
    """
    Get the sign of a number
    Args:
        x (float): input number

    Returns:
        int: -1 if x < 0
             0 if x = 0
             1 if x > 0

    Examples:
    >>> sign(1)
    1
    >>> sign(-1)
    -1
    >>> sign(0)
    0
    >>> import random
    >>> a = random.randint(1, 1000000)
    >>> sign(a)
    1
    >>> sign(-1*a)
    -1
    >>> sign([1, -1, 0, 1, -1])
    [1, -1, 0, 1, -1]
    """
    if isinstance(x, list):
        return [bool(element > 0) - bool(element < 0) for element in x]
    return bool(x > 0) - bool(x < 0)


def is_prime(n):
    """
    Calculate if a number is prime
    Args:
        n (int): input number

    Returns:
        bool: True if number is prime, False otherwise

    Examples:
    >>> is_prime(5)
    True
    >>> is_prime(6)
    False
    """
    from math import sqrt
    from itertools import count, islice
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))
