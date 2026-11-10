from game_simulator_v1 import Dice

# -- Task 3: Weapons and items --

# Class representing a weapon in the game 
class Weapon:

    # Store the weapon's name and the dice used for damage 
    def __init__(self, name: str, damage_dice: Dice) -> None:
        self.name = name
        self.damage_dice = damage_dice
    
    # Roll the dice to calculate the weapon's damage 
    def roll_damage(self) -> int:
        """Roll the weapon's damage dice"""
        return self.damage_dice.roll()