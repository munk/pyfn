from finance import cashflows_list, date_range, xirr_result, xirr_result_prime, get_xirr
from datetime import datetime
from math import fabs

def test_xirr_result():
    values = cashflows_list(5, 1.0, 10.0)
    start = datetime(2013, 10, 8)
    end = datetime(2013, 10, 11)
    dates = date_range(start, end, 1)
    expected = 10.0068132931
    actual = xirr_result(values, dates, 0.1)
    eps = 1e-8
    print expected, actual, expected - actual
    assert fabs(expected - actual) < eps

def test_xirr_result_prime():
    values = cashflows_list(5, 1.0, 10.0)
    start = datetime(2013, 10, 8)
    end = datetime(2013, 10, 11)
    dates = date_range(start, end, 1)
    expected = -0.0149348580177 
    actual = xirr_result_prime(values, dates, 0.1)
    eps = 1e-6
    print expected, actual, expected - actual
    assert fabs(expected - actual) < eps

def test_get_xirr():
    values = cashflows_list(5, 1.0, 10.0)
    start = datetime(2013, 10, 8)
    end = datetime(2013, 10, 12)
    dates = date_range(start, end, 1)
    expected = 0 # ??
    actual = get_xirr(values, dates, 0.1)
    
def test_cashflows_list():
    expected = [10.0, 1.0, 1.0, 1.0, 1.0]
    actual = cashflows_list(5, 1.0, 10.0)
    assert expected == actual

def test_date_range():
    start = datetime(2013, 10, 8)
    end = datetime(2013, 10, 11)
    expected = [datetime(2013, 10, 8),
                datetime(2013, 10, 9),
                datetime(2013, 10, 10),
                datetime(2013, 10, 11)]
    actual = date_range(start, end, 1)
    for e, a in zip(expected, actual):
        assert e == a
