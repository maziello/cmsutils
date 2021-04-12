import pytest
from cmsutils.main import time_format, getfiles, GOLDEN_RATIO

__all__ = ['test_time_format', 'test_getfiles', 'test_GOLDEN_RATIO']


def test_GOLDEN_RATIO():
    assert GOLDEN_RATIO == (1 + 5 ** 0.5) / 2, f"Golden ratio value is {GOLDEN_RATIO}, " \
                                               f"should be {(1 + 5 ** 0.5) / 2}"


@pytest.mark.parametrize("input_data",
                         [(8075, '2h 14m 35s'),
                          (2374, '39m 34s'),
                          (2294, '38m 14s'),
                          (7072, '1h 57m 52s'),
                          (6246, '1h 44m 6s'),
                          (7295, '2h 1m 35s'),
                          (7003, '1h 56m 43s'),
                          (7234, '2h 34s'),
                          (8380, 'prefix', '2h 19m 40s'),
                          (3141, 'prefix', 'suffix', '52m 21s'),
                          (1.82266e-09, '1.823 ns'),
                          (23563.5, '6h 32m 43s'),
                          (4.357e-05, '43.57 us'),
                          (76910.7, '21h 21m 50s'),
                          (76207.8, '21h 10m 7s'),
                          (166.457, '2m 46s'),
                          (2561.54, '42m 41s'),
                          (6.1851e-08, '61.851 ns'),
                          (0.00585611, 'prefix', '5.856 ms'),
                          (6.5962e-13, 'prefix', 'suffix', '0.66 ps')
                          ]
                         )
def test_time_format(input_data):
    t = input_data[0]
    result = input_data[-1]
    if len(input_data) > 2:
        if len(input_data) == 4:
            result = f"{input_data[1]}{input_data[-1]}{input_data[2]}"
        else:
            result = f"{input_data[1]}{input_data[-1]}"
        assert time_format(input_data[0],
                           *input_data[1:-1]) == result, f"time_format({t}) should be {result}, not {time_format(t)}"
    else:
        assert time_format(input_data[0]) == result, f"time_format({t}) should be {result}, not {time_format(t)}"


@pytest.mark.parametrize("input_data",
                         [(r'F:\Python\cmsutils\cmsutils',
                           ['F:\\Python\\cmsutils\\cmsutils\\main.py',
                            'F:\\Python\\cmsutils\\cmsutils\\__init__.py',
                            'F:\\Python\\cmsutils\\cmsutils\\__pycache__\\main.cpython-38.pyc',
                            'F:\\Python\\cmsutils\\cmsutils\\__pycache__\\__init__.cpython-38.pyc'
                            ]),
                          (r'F:\Python\cmsutils\cmsutils', {'extensions': ('.py')},
                           ['F:\\Python\\cmsutils\\cmsutils\\main.py',
                            'F:\\Python\\cmsutils\\cmsutils\\__init__.py'
                            ]),
                          (r'F:\Python\cmsutils\cmsutils', {'exclusions': ('.py')},
                           ['F:\\Python\\cmsutils\\cmsutils\\__pycache__\\main.cpython-38.pyc',
                            'F:\\Python\\cmsutils\\cmsutils\\__pycache__\\__init__.cpython-38.pyc',
                            ])
                          ]
                         )
def test_getfiles(input_data):
    if len(input_data) > 2:
        assert getfiles(input_data[0], **input_data[1]) == input_data[-1]
    else:
        assert getfiles(input_data[0]) == input_data[-1]
