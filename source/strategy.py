def trading_strategy(market_price, model_price, threshold = 0.05):
    """
    Decide whether to buy, sell, or hold based on the difference between market price and model price
    
    Parameters:
    market_price: float
    model_price: float
    threshold: float - minimum percentage difference to trigger a trade (set 5% default)
    
    Returns:
    str - 'buy', 'short', or 'hold'
    """

    #Calculate the % difference between model and market
    diff_percent = (market_price - model_price) / model_price

    if diff_percent < -threshold:
        return 'buy' #market is undervaluing it so buy
    elif diff_percent > threshold:
        return 'short' #market is overvaluating it so sell
    else:
        return 'hold' #no clear signal to trade
    
