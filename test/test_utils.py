# import math
import pytest
import random
from utils import time_format, getfiles, \
    GOLDEN_RATIO, get_prime_factors, sign, is_prime


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
                           ['F:\\Python\\utils\\utils\\_utils.py',
                            'F:\\Python\\utils\\utils\\__init__.py',
                            'F:\\Python\\utils\\utils\\__pycache__\\main.cpython-38.pyc',
                            'F:\\Python\\utils\\utils\\__pycache__\\__init__.cpython-38.pyc'
                            ]),
                          (r'F:\Python\cmsutils\cmsutils', {'extensions': ('.py')},
                           ['F:\\Python\\utils\\utils\\_utils.py',
                            'F:\\Python\\utils\\utils\\__init__.py'
                            ]),
                          (r'F:\Python\cmsutils\cmsutils', {'exclusions': ('.py',)},
                           ['F:\\Python\\utils\\utils\\__pycache__\\main.cpython-38.pyc',
                            'F:\\Python\\utils\\utils\\__pycache__\\__init__.cpython-38.pyc',
                            ])
                          ]
                         )
def test_getfiles(input_data):
    # print(len(input_data), input_data)
    if len(input_data) > 2:
        assert getfiles(input_data[0], **input_data[1]) == input_data[-1]
    else:
        assert getfiles(input_data[0]) == input_data[1]


@pytest.mark.parametrize("input_data",
                         [(270, [2, 3, 3, 3, 5]),
                          (-270, [-1, 2, 3, 3, 3, 5]),
                          (270.34, [2, 3, 3, 3, 5])]
                         )
def test_get_prime_factors(input_data):
    assert get_prime_factors(input_data[0]) == input_data[1]


@pytest.mark.parametrize("input_data",
                         [random.choices(
                             [c for c in [random.randint(2, 19) for _ in range(1000)] if is_prime(c)],
                             k=random.randint(3, 7)) for _ in range(10)]
                         )
def test_get_prime_factors_random(input_data):
    import math
    input_data.sort()
    assert get_prime_factors(math.prod(input_data)) == input_data


@pytest.mark.parametrize("input_data",
                         [(random.random()*s*10**random.randint(0, 23), s)
                          for s in random.choices(
                             [1 if random.random() > 0.5 else -1 for _ in range(500)], k=25)] +
                         [(-1, -1),
                          (1, 1),
                          (0, 0)]
                         )
def test_sign_random(input_data):
    assert sign(input_data[0]) == input_data[1]


@pytest.mark.parametrize("input_data",
                         [([-1, 0, 1], [-1, 0, 1]),
                          ([1, 1, 0, -1, -1], [1, 1, 0, -1, -1]),
                          ([0, 0, 0], [0, 0, 0])]
                         )
def test_sign_list(input_data):
    assert sign(input_data[0]) == input_data[1]
