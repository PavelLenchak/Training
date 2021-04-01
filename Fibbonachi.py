from functools import lru_cache

@lru_cache(20)
def fido(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fido(num-1) + fido(num-2)


print(fido(10))