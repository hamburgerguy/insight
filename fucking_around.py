#import libraries
import hashlib
import math
import string
import datetime
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi
from collections import OrderedDict
from statistics import mean

i = 0
lst = []
holder = 0
n = 19


while i < n:
    i += 1
    lst.append(n-(n-i))
for i in lst:
    print(i, end = '')
