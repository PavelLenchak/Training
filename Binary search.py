import random

def binary_search(array, item):
    low = 0
    hight = len(array) - 1

    while low <= hight:
        mid = int((low + hight) / 2)
        guess = array[mid]
        if guess == item:
            return 'The position of item in array is {}'.format(mid)
        elif guess < item:
            low = mid + 1
        else:
            hight = mid -1

    return None

my_array = [i for i in range(20, 40)]
print(my_array)
print(binary_search(my_array, 22))