import os
import pathlib
import random
import time
import math
import numpy as np

__all__ = ['GOLDEN_RATIO', 'time_format', 'getfiles']

GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def time_format(timevalue: (int, float),
                prefix: str = "",
                suffix: str = "") -> str:
    """
    Format the input time interval in seconds as a string in the format:
    'days d, hours h, minutes m, seconds s'
    >>> time_format(123456)
        '1d 10h 17m 36s'
    For time intervals smaller than 1 second, the output is formatted in milliseconds:
    'milliseconds ms'
    >>> time_format(0.0234)

    :param timevalue:
    :param prefix:
    :param suffix:
    :return:
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
    if timevalue >= 1:
        days, rest = divmod(timevalue, 86400)
        hours, rest = divmod(rest, 3600)
        minutes, seconds = divmod(rest, 60)

        days_str = f'{int(days):g}d' if days > 0 else ''
        hours_str = f' {int(hours):g}h' if hours > 0 else ''
        minutes_str = f' {int(minutes):g}m' if minutes > 0 else ''
        seconds_str = f' {int(seconds):g}s'
        time_message = f'{days_str}{hours_str}{minutes_str}{seconds_str}'.strip()
        return_message = prefix + time_message + suffix

    elif timevalue < 1:
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
    :param sourcedir: input source folder to start the files search
    :param extensions: list of extensions
    :param exclusions:
    :return:
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
