"""
  Convenience data class for holding several security screening
  parameters

  author: Sergio Espinoza
  sergio.espinoza.lopez@gmail.com
"""

from dataclass import dataclass

@dataclass
class SecurityFilters:

    #minimum market capital in USD Millions Dollars
    min_market_cap : float

    # After minimum market cap ordering
    # and filtering scan up to to this number of securities.
    # Manly used for testing purposes
    constituents_slice : float

    #minimum average daily option volume
    min_option_volume : float

    #min 52 weeks Implied Volatility Rank (%)
    min_iv_rank : int

    #minimum days to next earnings report
    min_days_to_earnings : int
