'''
module for testing
'''

class Character():
    def __init__(self, race, damage=10):
        self.race = race
        self.damage = damage
        self.health = 100

    def hit(self, damage):
        self.health -= damage
        return self.health

    def is_dead(self):
        return self.health <= 0


c = Character('Elf')
print(c.health)
print(c.is_dead())

c.hit(99)
print(c.health)
print(c.is_dead())