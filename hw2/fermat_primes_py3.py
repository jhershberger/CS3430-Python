import sys
import random
from newton_sqrt_py3 import newton_sqrt

def is_even(x):
    # if the remainder of x / 2 is 0 then it is an even number
    if x % 2 == 0:
        return True
    else:
        return False;

def expmod(b,e,m):
    if e == 0:
        return 1
    elif is_even(e):
        x = expmod(b, e/2, m)
        return (x*x % m)  #return the remainder
    else: #e is odd
        return ((b*expmod(b,e-1,m)) % m)

def fermat_test(n):
    if (n -1) < 2:
        return False
    elif n == 2:
        return True
    else:
        a = random.randint(2,n-1)
        return expmod(a,n,n) == a

def is_fermat_prime(n,num_times):
    if num_times == 0:
        return True
    elif n < 2:
        return False
    elif n == 2:
        return True
    else:
         for t in range(2, num_times+1):
             if not fermat_test(n):
                 return False
         return True

def is_prime(n):
    if n<2:
        return False
    elif n == 2:
        return True
    else:
        for d in range(2, int(newton_sqrt(n))+1):
            if n % d == 0:
                return False
        return True

def sum_of_fermat_primes(x,y,num_times):
    summ = 0
    #iterate through the range provided, if we run into a prime add it to the summ variable
    for i in range(x, y):
        if is_fermat_prime(i, num_times):
             summ += i
    return summ

def sum_of_primes(x,y):
    summ = 0
    for i in range(x,y):
        if is_prime(i):
            summ += i
    return summ

def test_sum_diff_in_range(n):
    sp = sum_of_primes(0, n)
    sfp = sum_of_fermat_primes(0, n, 10)
    print('sum of primes = ', sp)
    print('sum of fermat primes = ', sfp)
    print('sum diff = ', sfp - sp)

if __name__ == '__main__':
    prime = int(sys.argv[1])

    test_sum_diff_in_range(prime)
