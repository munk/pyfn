""" Calculate xirr based on Libreoffice Algorithm"""
from datetime import timedelta
from math import fabs
import itertools

# Data Creation Functions
def cashflows_list(number_of_payments, daily_payment, investment):
    """Paydown Cash flow"""
    cashflows = [p for p in itertools.repeat(daily_payment, number_of_payments)]
    cashflows[0] = investment
    return cashflows


def date_range(start_date, end_date, increment):
    """Return a series of dates from start_date to end_date"""
    result = []
    nxt = start_date
    delta = timedelta(days=increment)
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result


# XIRR Calculation
def xirr_result(values, dates, guess):
    """Calculates the resulting amount for the passed i
       interest rate and the given XIRR parameters.
        V_0 ... V_n = input values.
        D_0 ... D_n = input dates.
        R           = input interest rate.

        r   := R+1
        E_i := (D_i-D_0) / 365

                    n    V_i                n    V_i
        f(R)  =  SUM   -------  =  V_0 + SUM   ------- .
                   i=0  r^E_i              i=1  r^E_i
    """
    d_0 = dates[0]
    r = guess + 1.0
    result = values[0]
    for v, d  in zip(values[1:], dates[1:]):
        result += v / r**(d - d_0).days / 365.0 
    return result

def xirr_result_prime(values, dates, guess):
    """Calculate first deriviative of xirr_result
        V_0 ... V_n = input values.
        D_0 ... D_n = input dates.
        R           = input interest rate.

        r   := R+1
        E_i := (D_i-D_0) / 365

                             n    V_i
        f'(R)  =  [ V_0 + SUM   ------- ]'
                            i=1  r^E_i

                         n           V_i                 n    E_i V_i
               =  0 + SUM   -E_i ----------- r'  =  - SUM   ----------- .
                        i=1       r^(E_i+1)             i=1  r^(E_i+1)
    """ 
    d_0 = dates[0]
    r = guess + 1.0
    result = 0.0
    for v, d in zip(values[1:], dates[1:]):
        E_i = (d - d_0).days / 365.0
        result -= E_i * v / r ** (E_i + 1.0)
    return result


def get_xirr(values, dates, guess=0.1, maxiter=100, tol=1.48e-8):
    """Calculate XIRR"""
    if len(values) < 2 or len(values) != len(dates):
        raise ValueError("Values too short or Values and Dates don't match!")
    if guess <= -1:
        raise ValueError("Guess must be greater than -1")

    for _ in range(0, maxiter):
        result_value = xirr_result(values, dates, guess)
        new_guess = guess - result_value / xirr_result_prime(values, 
                dates, guess)
        eps = fabs(new_guess - guess)
        guess = new_guess
        if not eps > tol and fabs(result_value) > tol:
            return guess

    if not eps > tol and fabs(result_value) > tol:
        print "Failed to converge after %d iterations" % maxiter

    return guess
