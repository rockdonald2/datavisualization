import numpy as np

'''
a = np.array([1, 2, 3])

a + a # output: array([2, 4, 6]) '''

# ezt a függvényt fogjuk használni a 3 tulajdonság kiírására
def print_array_details(a):
    print('Dimensions: {}, shape: {}, dtype: {}'.format(a.ndim, a.shape, a.dtype))

''' a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(a)
print_array_details(a)
# output:
# [1 2 3 4 5 6 7 8 9]
# Dimensions: 1, shape: (9,), dtype: int32

a = a.reshape([3, 3])
print(a)
print_array_details(a)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
# Dimensions: 2, shape: (3, 3), dtype: int32

b = np.array([1, 2, 3, 4, 5, 6, 7, 8])
b = b.reshape([2, 2, 2])
print(b)
print_array_details(b)
# [[[1 2]
#   [3 4]]
# 
#  [[5 6]
#   [7 8]]]
# Dimensions: 3, shape: (2, 2, 2), dtype: int32 '''

''' x = np.array([[1, 2, 3], [4, 5, 6]], np.int64)
print(x.shape) # output: (2, 3)
print(x.dtype) # output: int64

x.shape = (6, )
x = x.astype('int32')
print(x.shape) # output: (6, )
print(x.dtype) # output: int32 '''

''' a = np.zeros([2, 3])
print(a)
print(a.dtype)
# output:
# [[0. 0. 0.]
#  [0. 0. 0.]]
# float64

b = np.ones([2, 3])
print(b)
print(b.dtype)
# output:
# [[1. 1. 1.]
#  [1. 1. 1.]]
# float64

empty_arr = np.empty([2, 3])
print(empty_arr)
# output: 
# [[1. 1. 1.]
#  [1. 1. 1.]]
# az output változhat, attól függően éppen mi volt a memóriaterületen

rand_arr = np.random.random([2, 3])
print(rand_arr)
# output:
# [[0.16112766 0.76956209 0.28967126]
#  [0.17799395 0.11935788 0.83240867]] '''

''' # létrehozunk egy 5 elemből álló egyenlő-eloszlású tömböt 2 és 10 között
a = np.linspace(2, 10, 5)
print(a)


# létrehozunk egy tömböt 2 és 10 között, kettesével lépegetve
b = np.arange(2, 10, 2)
print(b)

# output:
# [ 2.  4.  6.  8. 10.]
# [2 4 6 8]
# az arange a felső határral kizáró, míg a linspace megengedő '''

''' a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]) '''
''' print(a[5]) '''
''' print(a[1:3]) '''
''' print(a[::-1]) '''
''' a[::4] = -1 '''
''' print(a) '''
'''  '''
''' # output: '''
''' # 6 '''
''' # [2 3] '''
''' # [9 8 7 6 5 4 3 2 1] '''
''' # [-1  2  3  4 -1  6  7  8 -1] '''

''' a = np.arange(16, dtype='int64')
a = a.reshape([2, 2, 4])
# print(a)
# print(a[0, 1])
print(a[0, :, 2:3])
print(a[0, :, :])
print(a[0, ...])

# output:
# [[2]
#  [6]]
# [[0 1 2 3]
#  [4 5 6 7]]
# [[0 1 2 3]
#  [4 5 6 7]] '''

''' a = np.arange(1, 7, dtype='int64')
print(a)
a = a.reshape([2, 3])
print(a)
print(a + 2)
print(a * 2)
print(a / 2.0)
# a fenti osztás esetében, implicit módon, amikor float számmal osztunk, a tömb átalakításra kerül float64 típusúvá

# output:
# [1 2 3 4 5 6]
# [[1 2 3]
#  [4 5 6]]
# [[3 4 5]
#  [6 7 8]]
# [[ 2  4  6]
#  [ 8 10 12]]
# [[0.5 1.  1.5]
#  [2.  2.5 3. ]]

print(a < 4)
# output:
# [[ True  True  True]
# [False False False]] '''

''' a = np.arange(10).reshape([2, 5])

print(a.min(axis=1))
# output: [0 5]

print(a.sum(axis=0))
# output: [ 5  7  9 11 13]

print(a.sum(axis=1))
# output: [10 35]

print(a.mean(axis=1))
# output: [2. 7.]

# szórás
print(a.std(axis=1))
# output: [1.41421356 1.41421356]

# az axis = 0 esetén, függölegesen, a dimenziók között, összegzi (pl.) az elemeket 
# az axis = 1 esetén, vízszintesen, a dimenziókon belül, összegzi az elemeket '''

''' pi = np.pi
a = np.array([pi, pi/2, pi/4, pi/6])
print(np.degrees(a)) # átalakítja radiánból fokba a megadott tömb elemeit
# output: [180.  90.  45.  30.]

sin_a = np.sin(a) # visszatéríti a radiánok szinusz értékét
print(sin_a)
# output: [1.22464680e-16 1.00000000e+00 7.07106781e-01 5.00000000e-01]

print(np.round(sin_a, 7)) # kerekíti 7 tizedespontosággal
# output: [0.        1.        0.7071068 0.5      ]

a = np.arange(8).reshape([2, 4])

print(np.cumsum(a, axis=1))
# halmozott összeg a második tengely mentén, tehát jelenesetben vízszintesen, dimenziókon belül

print(np.cumsum(a))
# a tengelymeghatározás nélkül a tömb kisimul, tehát egy-dimenzióssá alakul

# output:
# [[ 0  1  3  6]
#  [ 4  9 15 22]]
# [ 0  1  3  6 10 15 21 28] '''

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

print(moving_average(np.arange(6)))
# output: [1. 2. 3. 4.]