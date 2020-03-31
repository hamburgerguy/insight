import matplotlib.pyplot as plt
from random import randint

iter = 1000
seed = 0.5
spacing = .0001
res = 8

#init x and y maps
rlist = []
xlist = []

#define logmap fn
def logmap(x,r):
    return x*r*(1-x)

#return nth interation of logmap
def iterate(n,x,r):

    for i in range(1,n):
        x = logmap(x,r)
    return x
#list values, iterate over each r val
for r in [i*spacing for i in range(int(1/spacing),int(4/spacing))]:
    rlist.append(r)
    xlist.append(iterate(randint(iter-res/2,iter+res/2),seed,r))

plt.scatter(rlist,xlist, s = .01)
plt.xlim(0.9,4.1)
plt.ylim(-0.1,1.1)
plt.show()
