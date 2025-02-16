from __future__ import annotations
from enum import Enum
import math
import random



class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class PokemonType(Enum):
    WATER = 1
    FIRE = 2
    PLANT = 3
    ELECTRIC = 4
    ROCK = 5

class Pokemon:

    def __init__(self, name, type, baseHealth, level, baseDamage, attackSpeed):
        self.name = name
        self.level = level
        self.xp = 0
        self.type = type
        self.baseHealth = baseHealth
        self.baseDamage = baseDamage
        self.attackSpeed = attackSpeed
        self.baseLevelUpXp = 10
        self.currentHealth = self._get_health()

    def print_stats(self):
        print(color.BOLD + f"{self.name:<16}  " + color.END + f"HP: {self.currentHealth:<3}  Schaden: {self._get_damage():<3}   XP: {self.xp:<4}   XP bis nächstes Level: {self._get_damage():<4}  " + color.YELLOW + color.BOLD + f"Level: {self.level:<3}" + color.END)

    def __eq__(self, other):
        return self.name == other.name
    
    def _get_damage(self):
        return round(3*math.sqrt(self.level) + self.baseDamage, 1)
    
    def _get_health(self):
        return round(2*math.pow(self.level, 0.7) + self.baseHealth, 1)
    

    def _get_needed_xp_for_level(self, newLevel):
        return 3*newLevel + self.baseLevelUpXp

    def _add_xp(self, addXp):
        self.xp += addXp
        if self.xp >= self._get_needed_xp_for_level(self.level+1):
            self.xp -= self._get_needed_xp_for_level(self.level+1)
            self.level+=1

    def _regen(self):
        self.currentHealth = self._get_health()    

    def attack(self, other: Pokemon, multiplier):
        damage = self._get_damage()
        critic = False
        
        # Wasser vs Feuer -> Wasser gewinnt
        if self.type == PokemonType.WATER and other.type == PokemonType.FIRE:
            damage = damage * 1.5
            critic = True

        # Feuer vs Pflanze -> Feuer gewinnt
        if self.type == PokemonType.FIRE and other.type == PokemonType.PLANT:
            damage = damage * 1.5
            critic = True

        # Pflanze vs Wasser -> Pflanze gewinnt
        if self.type == PokemonType.PLANT and other.type == PokemonType.WATER:
            damage = damage * 1.5
            critic = True
        
        # Rock vs Fire -> Rock gewinnt gegen Fire
        if self.type == PokemonType.ROCK and other.type == PokemonType.FIRE:
            damage = damage * 1.5
            critic = True

        # Rock vs Electric -> Rock verliert gegen Electric
        if self.type == PokemonType.ROCK and other.type == PokemonType.ELECTRIC:
            damage = damage * 0.5
            critic = True

        # Electric vs Water -> Electric gewinnt gegen Water
        if self.type == PokemonType.ELECTRIC and other.type == PokemonType.WATER:
            damage = damage * 1.5
            critic = True

        # Electric vs Rock -> Electric verliert gegen Rock
        if self.type == PokemonType.ELECTRIC and other.type == PokemonType.ROCK:
            damage = damage * 0.5
            critic = True

        # Zufallsmultiplikator
        randomMultiplier = random.randrange(8, 14) / 10.0
        damage = damage * randomMultiplier
        damage = damage * multiplier

        other.currentHealth -= damage
        self._add_xp(damage)
        return {damage, critic}

    
# danke chatgpt
randomPokemon = [
    Pokemon("Glumanda", PokemonType.FIRE, 20, 1, 5, 1),
    Pokemon("Schiggy", PokemonType.WATER, 27, 1, 4, 1),
    Pokemon("Bisasam", PokemonType.PLANT, 40, 1, 3, 1),
    Pokemon("Pikachu", PokemonType.ELECTRIC, 35, 1, 6, 1),
    Pokemon("Vulpix", PokemonType.FIRE, 28, 1, 4, 1),
    Pokemon("Magmar", PokemonType.FIRE, 45, 1, 6, 1),
    Pokemon("Flamara", PokemonType.FIRE, 50, 1, 7, 1),
    Pokemon("Torkoal", PokemonType.FIRE, 60, 1, 5, 1),
    Pokemon("Karpador", PokemonType.WATER, 15, 1, 2, 1),
    Pokemon("Amonitas", PokemonType.WATER, 40, 1, 4, 1),
    Pokemon("Schwimmbär", PokemonType.WATER, 30, 1, 4, 1),
    Pokemon("Welsar", PokemonType.WATER, 50, 1, 5, 1),
    Pokemon("Tentacha", PokemonType.WATER, 35, 1, 4, 1),
    Pokemon("Bellsprout", PokemonType.PLANT, 30, 1, 3, 1),
    Pokemon("Chlorophyll", PokemonType.PLANT, 38, 1, 4, 1),
    Pokemon("Tangela", PokemonType.PLANT, 42, 1, 5, 1),
    Pokemon("Georok", PokemonType.ROCK, 50, 1, 5, 1),
    Pokemon("Onix", PokemonType.ROCK, 70, 1, 4, 1),
    Pokemon("Kabuto", PokemonType.ROCK, 45, 1, 5, 1),
    Pokemon("Kabutops", PokemonType.ROCK, 55, 1, 6, 1),
    Pokemon("Raikou", PokemonType.ELECTRIC, 65, 1, 8, 1),
    Pokemon("Magnemite", PokemonType.ELECTRIC, 30, 1, 4, 1) 
]

