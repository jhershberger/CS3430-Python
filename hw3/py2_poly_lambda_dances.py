import sys
import random
from datetime import datetime

def make_2nd_deg_poly(k2,k1,k0):
    #anonymous function that returns a tuple
    return lambda x: (('p(x) = ' + str(k2) + 'x^2 + ' + str(k1) + 'x + ' + str(k0)),
                    (k2 * x**2 + k1 * x + k0), ('x = ' + str(x)))

#this function will take a list of 3 tuples and return a list of anonymous second
#degree polynomials
def make_2nd_deg_polys(coeffs):
    poly_list = []
    for tup in coeffs:
        poly_list.append(lambda x, tup=tup: (('p(x) = ' + str(tup[0]) + 'x^2 + '
         + str(tup[1]) + 'x + ' + str(tup[2])), (tup[0] * x**2 + tup[1] * x + tup[2]),
         ('x = ' + str(x))))
    return poly_list

def map_polys(polys, numbers):
    map_list = [];
    for tup in polys:
        map_list.append(map(lambda x: tup(x) , numbers))
    return map_list

def display_poly_maps(poly_maps):
    for tup in poly_maps:
        for li in tup:
            px, val, xval = li
            print px, "=", val, ", at", xval

def poly_dance(coeffs, xvals):
    polys = make_2nd_deg_polys(coeffs)
    poly_maps = map_polys(polys, xvals)
    return poly_maps

def make_nth_deg_rand_poly(n, a, b):
    i = 0
    rand = []
    while i < n + 1:
        rand.append(gen_rand_coeff(a,b))
        i += 1

    list_polys = [('p(x) = ')] + [(str(rand[deg]) + 'x^' + str(deg) + ' + ') if deg > 0 else str(rand[deg]) for deg in range(n,-1,-1)]

    return lambda x: ((''.join(list_polys)), (sum((x**coeff) * rand[coeff] for coeff in range(n, -1, -1))), ('x = ' + str(x)))

def make_nth_deg_rand_polys(num_polys,n,a,b):
    result_list = [(make_nth_deg_rand_poly(n,a,b)) for i in range(num_polys)]
    return result_list

def rand_poly_dance(num_polys,n,a,b,xvals):
    polys = make_nth_deg_rand_polys(num_polys, n, a, b)
    poly_maps = map_polys(polys, xvals)
    return poly_maps

def sorted_rand_poly_dance(num_polys, n, a, b, xvals):
    polys = rand_poly_dance(num_polys, n, a, b, xvals)

    #I use list comprehension to take the list of lists of tuples
    #to concatenate it to just a list of tuples so that we can
    #sort the entire list by the sum value in each tuple
    concat_list = [tup for poly in polys for tup in poly]

    #the second element of each tuple is the value we want to sort by
    concat_list.sort(key=lambda x: x[1], reverse = True)
    return concat_list

def display_sorted_polys(sorted_polys):
    for tup in sorted_polys:
        print tup[0] , ' = ',  tup[1] , ', at ', tup[2]

def gen_rand_coeff(a, b):
    sign = random.randint(1, 1000)
    if sign < 500:
        return -random.randint(a, b)
    else:
        return random.randint(a, b)

if __name__ == '__main__':
    start = datetime.now()
    top_10 = sorted_rand_poly_dance(10000,5,1,10,xrange(0,3))[:10]
    end = datetime.now()
    duration = end = start
    print 'start = ', start
    print 'end = ', end
    print 'duration = ', duration
    display_sorted_polys(top_10)
