"""
  Convenience data class for holding several option strategy screening
  parameters

  author: Sergio Espinoza
  sergio.espinoza.lopez@gmail.com
"""

@dataclass
class StrategyFilters():
    """
    Option strategy filters:
         * pct_under_px_range: .20  scan strikes under this % below market price for underlying
         * num_month_expiries: 3 monthly expires forward
         * max_loss: max loss
         * min_profit: min profit
     """

    #scan strikes under this % below market price for underlying
    pct_under_px_range: float
    #number of monthly expires forward to scan (i.e. if today is 1st Aug
    # then motnhly expiries up to - but not including - November will be
    # scanned )
    num_month_expiries: int
    #Maximum loss allowed, in a vertical spread strategy (like bull put spread)
    #this should influence maximum allowed distance between strikes
    max_loss: float
    #Minimum Profit of the strategy, case of credit spread this would be
    # the minimum premium value.
    min_profit: float
