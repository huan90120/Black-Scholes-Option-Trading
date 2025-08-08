from math import log, sqrt, exp
from scipy.stats import norm

def check_inputs(S, K, T, r, sigma):
    """
    Validate the inputs for the Black-Scholes model.

    Parameters:
    S : float : Current stock price
    K : float : Strike price of the option
    T : float : Time to expiration in years
    r : float : Risk-free interest rate (annualized)
    """
    S = float(S); K = float(K); T = float(T); r = float(r); sigma = float(sigma)
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive")
    if T <= 0:
        T = 1.0/365.0
    if sigma <= 0 or sigma != sigma:
        sigma = 1e-6
    return S, K, T, r, sigma 

def d1_d2(S, K, T, r, sigma):
    d1 = (log(S/K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return d1, d2 

def black_scholes_price(S, K, T, r, sigma, option_type = 'call'):
    """
    Calculate the Black-Scholes option price.

    Parameters:
    S : float : Current stock price
    K : float : Strike price of the option
    T : float : Time to expiration in years
    r : float : Risk-free interest rate (annualized)
    sigma : float : Volatility of the underlying stock (annualized)
    option_type : str : 'call' for call option, 'put' for put option

    Returns:
    float : Price of the option
    """
    S, K, T, r, sigma = check_inputs(S, K, T, r, sigma)
    d1, d2 = d1_d2(S, K, T, r, sigma)

    if option_type == 'call':
        return (S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2))
    elif option_type == 'put':
        return (K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def delta(S, K, T, r, sigma, option_type = 'call'):
    S, K, T, r, sigma = check_inputs(S, K, T, r, sigma)
    d1, _ = d1_d2(S, K, T, r, sigma)
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1.0

def vega(S, K, T, r, sigma):
    S, K, T, r, sigma = check_inputs(S, K, T, r, sigma)
    d1, _ = d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * sqrt(T)

