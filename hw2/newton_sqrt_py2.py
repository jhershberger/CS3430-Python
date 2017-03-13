from __future__ import division

def average(x, y):
    return (x + y)/2;

def next_guess(n, g):
     return average(g, n/g);

def is_good_enough(n, g, error=0.00001):
    return abs(g**2 - n) <= error;

def newton_square_root(n, g, error):
    if is_good_enough(n, g, error):
        return g;
    else:
       return newton_square_root(n, next_guess(n, g), error);

def newton_sqrt(n):
   return newton_square_root(n, 1, 0.00001);
