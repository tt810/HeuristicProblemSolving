what to do?
The mint problem is to design a set of coin denominations, such that the Exchange Number of coins required for a purchase is minimized given the constraints.

How to run it:

$ python mint.py 3.0

where 3.0 is N, which can be any float.

This program contains three crucial functions:
  exactChange(denomination) 
  exchangeNumber(denomination, N)
  mint(N)

exact change number:
given the set of 5 coin denominations, the expected number of coins required to give exact change for a purchase is called the Exact Change Number. Using the U.S. denominations, the Exact Change Number for 43 cents can be realized by one quarter, one dime, one nickel, and three pennies, thus giving a total of 6. 

exchange number:
the Exchange Number of a purchase is the number of coins given from the buyer to the seller plus the number given in change to the buyer from the seller. For an item costing 43 cents using the U.S. denominations, the Exchange Number can be realized by having the buyer pay 50 cents and receiving a nickel and two pennies in return, giving a total of only 4. You can assume the availability of 1 dollar. So, the Exchange Number for 99 cents is 1 since a penny is returned after handing the seller 1 dollar. 

scoring:
Score is sum of the costs of all non-multiples of 5 + sum of N * costs of the multiples of 5. For example, if the cost of every entry were 2. Then the total score would be (99-19)*2 + (19*N*2).
