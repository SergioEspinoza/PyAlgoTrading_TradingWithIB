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


  Convenience data class for holding several security screening

"""

from dataclasses import dataclass

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
