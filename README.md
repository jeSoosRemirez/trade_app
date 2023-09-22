### Before the run
$ poetry shell
$ poetry install
If you are going to use the historical_data.py then provide keys in .env file

### How to run
You can test a basic GridStrategy in main.py by using emulate_grid_strategy()

### Some thoughts
1. I used the data that is splited by days and because of that
calculations in strategies can be abnormal. This happens because
the values are not that accurate as data with 1 second or minute
intervals. Also, the reason of some anomalies can be that I used
only the final price on some dates.
2. The main function to do the grid strategy can be rewritten into 
class that inherits from base class Strategy. As I had not enough time
to restructure functionality of emulate_grid_strategy() I left it as it is.
3. There is a itteration on dates in emulate_grid_strategy() that is kinda
gives us the actual data for today. Imagine this like you are jumping
into future by this itteration. If we are going to use the Binance API
most of the functionality inside this function should be rewriten to get
actual data from the binance and to do real orders. In addition, some cases
like stop-loss should be added.
4. I could write some prediction on when to make an order basing on
the previous data, for example if yesterdey was the lowwest price during the 
week then today is a good day to make an order OR our coin is falling
apart. But, as i mentioned before, I had not enough time.
5. This doc can be more informative than just "How to run" but most 
of the key information I described in docstrings.
6. Instead of self-made database could be used any other real database
but to not engage other tecnologies I used regular csv and DataFrames.