import random

def bubble_sort(array):
    new_arr = array.copy()
    last_item = len(array)-1
    count = 0
    for i in range(last_item):
        for j in range(last_item-i):
            count += 1
            #print(new_arr)
            if new_arr[i] < new_arr[j]:
                new_arr[i], new_arr[j] = new_arr[j], new_arr[i]
    print(count)
    return new_arr

my_list = [random.randint(1,40) for i in range(20)]
print(my_list)
new_arr = bubble_sort(my_list)
print(new_arr)