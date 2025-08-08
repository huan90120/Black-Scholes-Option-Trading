from source.black_scholes import black_scholes_price, vega

def implied_vol(market_price, S, K, T, r, option_type = 'call', 
                init_vol = 0.2, tol = 1e-6, max_iter = 100, low = 1e-6, high = 5.0):
    """
    Calculate the implied volatility using the Newton-Raphson method.
    Parameters:
    market_price : float : Market price of the option
    S : float : Current stock price
    K : float : Strike price of the option
    T : float : Time to expiration in years
    r : float : Risk-free interest rate (annualized)
    option_type : str : 'call' for call option, 'put' for put option
    init_vol : float : Initial guess for volatility
    tol : float : Tolerance for convergence
    max_iter : int : Maximum number of iterations
    low : float : Lower bound for volatility
    high : float : Upper bound for volatility
    Returns:
    float : Implied volatility
    """
    sigma = max(init_vol, 1e-6)
    for i in range(max_iter):
        price = black_scholes_price(S, K, T, r, sigma, option_type)
        diff = price - market_price
        if abs(diff) < tol:
            return float(sigma)
        v = vega(S, K, T, r, sigma)
        if v < 1e-8:
            break
        sigma -= diff / v
        if sigma <= 0 or sigma != sigma or sigma > 5.0:
            break

    lo, hi = low, high
    for x in range(max_iter):
        mid = 0.5 * (lo + hi)
        pmid = black_scholes_price(S, K, T, r, mid, option_type)
        if abs(pmid - market_price) < tol:
            return float(mid)
        
        if pmid < market_price:
            hi = mid
        else:
            lo = mid
    return float(mid)

