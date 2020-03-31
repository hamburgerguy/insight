def fib(n,memo):
    if memo[n] != null:
        return memo[n]
    elif n == 1 or n == 2:
        result = 1
    else:
        result = fib(n-1) + fib(n-2)
    memo[n] = result
    return result

print(fib(6,[0,1,1,2,3,5,8]))
