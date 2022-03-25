# probability that two people of n birthday on the same day

import math

people = int(input("Enter a number of people: "))

probability = 1 - math.factorial(365)/(math.factorial(365 - people)*365**people)
print(probability)

