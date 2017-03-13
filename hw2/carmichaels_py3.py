from fermat_primes_py3 import fermat_test, expmod
from fractions import gcd
import sys

def  is_carmichael(n):
    #n has to be a positive integer and is odd
    if n < 2: # 1 is a perfect square so start at 2
        return False;
    elif n % 2 == 0: #all carmichael numbers are odd
        return False;
    else:
        # n cannot be divisible by perfect squares, meaning that
        # it's square free.

        #count the number of prime divisors of n
        factors = 0;
        prime_divisors = 0;
        root = n**(1/2);

        #set b = 2 since carmichael numbers have to satisfy
        #the modular arithmetic relation: b^(n-1) == 1 mod n
        #where all integers 1 < b < n which are prime to n.
        b = 1;
        while(b < n): #1 < b < n
            # all carmichael #'s are square free and have at least 3 prime divisors
            if b > root and not factors:
                    return False;
            if gcd(b,n) > 1: #then there is a factor for n
                factors += 1;
            elif expmod(b,n-1,n) != 1:
                    return False;
            b += 1;
        #if we make it out of the loop full of conditions that disprove carmichael
        #numbers then our number is a carmichael number
        return True;

def find_carmichaels_in_range(x,y):
    #check the input
    if x > y:
        return 0;
    elif x < 0 or y < 0:
        return 0;
    else: #list comprehension
        return set([i for i in range(x,y) if is_carmichael(i)]);


def find_first_n_carmichaels(n):
    if n < 0:
        return 0;
    #we need to have a flag that says when we reach n carmichael
    #numbers
    carmichael_count = 0;
    i = 2;

    result = set();
    while carmichael_count < n:
        if is_carmichael(i):
            carmichael_count += 1;
            print(carmichael_count, ') ', i);
            result.add(i);
        i += 1;

    return result;

def is_prime(n):
    if n < 2:
        return False;
    if n == 2:
        return True;
    for d in range(2, int(n/2.0)+1):
        if n % d == 0:
            return False;
    return True;

if __name__ == '__main__':
    #open up the README file
    f = open('README', 'w');

    #we want the first 34 carmichael's
    n = 34;

    #get the 34 carmichaels in a set to iterate through
    result_set = find_first_n_carmichaels(n);

    #Step2: write the result_set to README
    f.write('First_34_carmichael_numbers:\n');

    count = 1;
    for i in result_set:
        f.write(str(count) + ') ' + str(i) + ',\n');
        count += 1;

    #Step3: check each carmichael with the fermat's primality test
    f.write('\nCarmichael numbers that passed fermat\'s test: \n');

    for i in result_set:
        if fermat_test(i):
            f.write(str(i) + ',\n');


    #Step4: use is_prime to test each carmichael and write which one's pass
    f.write('\nCarmichael numbers that passed is_prime: \n');

    for i in result_set:
        if is_prime(i):
            f.write(str(i) + ',\n');

    #Step5: Write my findings to README
    response = """All of the carmichael's pass fermat's test but aren't actually prime.
    This means that fermat's test could be used to find carmichael numbers
    and it means that fermat's test isn't the best way to find prime numbers.""";

    f.write('\n' + response);

    #close the file.
    f.close();
