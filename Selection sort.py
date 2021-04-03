import random

def find_smallest(array):
    smallest = array[0]
    smallest_index = 0
    for index in range(1, len(array)):
        if array[index] < smallest:
            smallest = array[index]
            smallest_index = index
    return smallest_index

def selection_sort(array):
    new_array = []
    for i in range(len(array)):
        smallest = find_smallest(array)
        new_array.append(array.pop(smallest))
    return new_array

my_list = [random.randint(1,40) for i in range(20)]
print(my_list)
print(selection_sort(my_list))