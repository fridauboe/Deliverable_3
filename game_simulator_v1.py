# Object-oriented game simulator
# Turid Torheim, NMBU, 2026

from os import name
import random 



# -- Task 1: Character --

# Class representing a character in the game 
class Character:
    """Represents a character in the RPG"""

    # Set the name, maximum HP, damage and optional weapon 
    def __init__(self, name: str, hp_max: int = 100, damage: int = 10, weapon=None) -> None:
        """
        Initialise the Character

        Args:
            name (str): The name of the character.
            hp_max (int): Max hit points (default = 100)
            damage (int): Damage delt when character attacks (default = 10)
        """

        # Store the character's attributes
        self.name = name
        self._hp = hp_max  # Note: _hp indicated private attribute
        self.hp_max = hp_max
        self.damage = damage
        self.weapon = weapon

        # Use weapon damage if the character has a weapon, otherwise use normal damage 
    def attack(self, target) -> None:
        """Attack and deal damage to target character"""
        if self.weapon is not None:
            damage = self.weapon.roll_damage()
        else:
            damage = self.damage

        # Reduce the target's HP
        target.take_damage(damage)
    

    # Reduce HP, but never below 0 
    def take_damage(self, amount: int) -> None:
        """Reduce the character's HP when taking damage"""
        self._hp = max(0, self._hp - amount)

    # Increase HP without exceeding maximum HP
    def heal(self, amount: int) -> None:
         """Heal the character"""
         self._hp = min(self.hp_max, self._hp + amount)

    # Check if the character is alive (HP > 0) 
    @property
    def is_alive(self) -> bool:
        """Check the character is alive"""
        return self._hp > 0

    # Print an introduction of the character 
    def introduce(self) -> None:
        """Creates string that introduces character"""
        print(f"Hi, my name is {self.name}!")

    # Return a detailed description of the character 
    def __repr__(self) -> str:
        """Representation of character object"""
        return f"<Character name={self.name} hp={self.hp} damage={self.damage}>)"

    # Return a readable description of the character 
    def __str__(self) -> str:
        """String representation of character object"""
        return f"Character: {self.name} with {self.hp} HP and {self.damage} damage"

    # Allow HP to be read without changing it directly 
    @property
    def hp(self) -> int:
        """Public read-only property to inspect HP without allowing direct, unsafe edits."""
        return self._hp



# -- Task 2: Dice --

# Class representing a dice 
class Dice:

    # Set the number of sides, default is 6 
    def __init__(self, sides: int = 6) -> None:

        # Check that the dice has at least 2 sides 
        if sides < 2:
            raise ValueError("A dice must have at least 2 sides")
        self.sides = sides

    # Roll a random number between 1 and the number of sides
    def roll(self) -> int:
        """Roll the dice and return a random number"""
        return random.randint(1, self.sides)

    # Return a string showing the number of sides 
    def __repr__(self) -> str:
        """Return a string representation of the dice"""
        return f"Dice(sides={self.sides})"

    # Allow the dice to be rolled by calling the object directly 
    def __call__(self) -> int:
        """Roll the dice when the object is called"""
        return self.roll()


# -- Task 4: Warrior and Mage -- 
# Warrior inherits from Character and has extra protection 
class Warrior(Character):
    # Set the name and armor, with 5 as the default 
    def __init__(self, name: str, armor: int = 5, hp_max: int = 100,
             damage: int = 10, weapon=None):
        super().__init__(name, hp_max, damage, weapon)
        self.armor = armor

    # Reduces the damage by the armor, but never below 0 
    def take_damage(self, amount: int) -> None:
        reduced_damage = max(0, amount - self.armor)
        super().take_damage(reduced_damage)

# Mage inherits from Character and uses Mana for magical attacks 
class Mage(Character):
    #Set the starting Mana and maximum Mana
    def __init__(self, name: str, mana: int = 30, mana_max: int = 30,
             hp_max: int = 100, damage: int = 10, weapon=None):
        super().__init__(name, hp_max, damage, weapon)
        self.mana = mana
        self.mana_max = mana_max


    # Use 10 Mana to deal double damage 
    def attack(self, target) -> None:
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(self.damage * 2)
        # If there is not enough Mana, use a normal wttack and restore 5 Mana 
        else:
            super().attack(target)
            self.mana = min(self.mana_max, self.mana + 5)

# -- Task 5: Battle --

# Class that manages a battle between two characters 
class Battle:

    # Stores the hero and enemy that will fight 
    def __init__(self, hero: Character, enemy: Character):
        self.hero = hero
        self.enemy = enemy

    # Play one round where the hero attacks first  
    def play_round(self) -> None:
        self.hero.attack(self.enemy)

        # The enemy attacks back if it is still alive 
        if self.enemy.is_alive:
            self.enemy.attack(self.hero)

    # Repeat the rounds until one character is defeated 
    def simulate_battle(self) -> None:
        while self.hero.is_alive and self.enemy.is_alive:
            self.play_round()