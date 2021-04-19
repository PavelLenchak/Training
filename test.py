import numpy as np

'''
module for testing
'''

class Character():
    def __init__(self, race, damage=10):
        self.race = race
        self.damage = damage
        self.health = 100

    def __str__(self):
        return "The Character's race is {} and he has {} damage".format(self.race, self.damage)

    def hit(self, damage):
        self.health -= damage
        return self.health

    def is_dead(self):
        return self.health <= 0


c = Character('Elf')

my_list = [-1,0,4,2,1,2]
answer = np.median(my_list)
print(answer)