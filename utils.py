from random import random, randrange
from bisect import bisect
from datetime import timedelta

# This function aims to provide some control over the
# random generation of elements of the logs by giving
# probability.
# Usage: weighted_choice([(referers[1], 90), (referers[2], 35), ...])
def weighted_choice(choices):
    values, weights = zip(*choices)	# zip returns a list of tuples where the i-th tuple contains
    total = 0 				# the i-th element from each of the argument sequences or iterables.
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]

# Generate a randome date between two specific dates
# Usage:
# d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
# d2 = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')
# print random_date(d1, d2)
def random_date(start, end):
  delta = end - start
  int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
  random_second = randrange(int_delta)
  return start + timedelta(seconds=random_second)

# pick a random row from file
def random_line(file):
  line = next(file)
  for num, aline in enumerate(file):
    if randrange(num + 2): continue
    line = aline
  return line
