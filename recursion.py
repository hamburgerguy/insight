import os

lst = [1,2,3,5,7,11,12,13,14,15,17,18,19,20,21,23,27,34]

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def draw_line(tick_length,tick_label=''):
    line = '-'*tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)

def draw_interval(center_length):
    if center_length > 0:
        draw_interval(center_length -1)
        draw_line(center_length)
        draw_interval(center_length -1)

def draw_ruler(num_inches, major_length):
    draw_line(major_length,'0')
    for j in range(1,1+num_inches):
        draw_interval(major_length-1)
        draw_line(major_length,str(j))

def binary_search(data,target,low,high):
    """return true if target is found in indicated portion of list"""
    if low > high:
        return False
    else:
        mid = (low+high)//2
        if target == data[mid]:
            return mid
        elif target < data[mid]:
            return binary_search(data,target,low,mid-1)
        else:
            return binary_search(data,target,mid+1,high)

def disk_usage(path):
    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            childpath = os.path.join(path,filename)
            total += disk_usage(childpath)
    print('{0:<7}'.format(total),path)
    return total
S = [2,3,5,7,11,13,17,19]

def unique(S,start,stop):
    if stop - start <= 1:
        return True
    elif not unique(S,start,stop-1):
        return False
    elif not unique(S,start+1,stop):
        return False
    else:
        return S[start] != S[stop-1]

def bad_fibonacci(n):
    if n <= 1:
        return n
    else:
        return bad_fibonacci(n-2) + bad_fibonacci(n-1)

def good_fib(n):
    if n <= 1:
        return (n,0)
    else:
        (a,b) = good_fib(n-1)
        return (a+b,a)

def linear_sum(S,n):

    if n == 0:
        return 0
    else:
        return linear_sum(S,n-1) + S[n-1]

def reverse(S,start,stop):
    if start < stop-1:
        S[start],S[stop-1] = S[stop-1],S[start]
        reverse(S,start+1,stop-1)


def power(x,n):
    if n == 0:
        return 1
    else:
        return x*power(x,n-1)

def power_fast(x,n):
    if n == 0:
        return 1
    else:
        partial = power(x,n//2)
        result = partial*partial
        if n % 2 == 1:
            result *= x
        return result

def binary_sum(S,start,stop):
    if start >= stop:
        return 0
    elif start == stop-1:
        return S[start]
    else:
        mid = (start+stop)//2
        return binary_sum(S,start,mid) + binary_sum(S,mid,stop)

def it_bin_search(data,target):
    low = 0
    high = len(data)-1
    while low <= high:
        mid = (low+high)//2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            high = mid-1
        else:
            low = mid+1
    return False

def it_reverse(S):
    start,stop = 0,len(S)
    while start < stop-1:
        S[start],S[stop-1] = S[stop-1],S[start]
        start,stop = start+1, stop-1
primes = array('i', [2,3,5,7,11,13,17,19])
