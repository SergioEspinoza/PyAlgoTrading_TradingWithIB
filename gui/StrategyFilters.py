"""
Copyright 2020 Sergio Espinoza Lopez sergio.espinoza.lopez@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

  Convenience data class for holding several option strategy screening
  parameters
"""

from dataclasses import dataclass

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
