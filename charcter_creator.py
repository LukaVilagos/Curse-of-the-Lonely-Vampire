from classes.Character import Character
from classes.Inventory import Inventory
from constants.character_classes import CHARACTER_CLASSES
from constants.items import *

def create_inventory(character_class):
    items = {}
    max_capacity = 0
    
    match character_class:
        case "Fighter":
            items += {BASIC_SWORD}
            max_capacity = 4
        case "Wizard":
            items += (BASIC_WAND)
            max_capacity = 2
        case "Cleric":
            items += (BASIC_MACE)
            items += (BASIC_HEALING_POTION)
            max_capacity = 3
            
    return Inventory(items, max_capacity)

def create_character():
    print("Create Your Character: ")
    
    name = input("Input character name: ")
    age = input("Input character age: ")
    
    gender_choice = None
    while gender_choice != 'M' and gender_choice != 'F' and gender_choice != 'O':
        gender_choice = input("Choose your gender (M/F/O): ")
    gender = gender_choice
    
    character_class_choice = None
    while character_class_choice not in CHARACTER_CLASSES:
        for character_class in CHARACTER_CLASSES:
            print(f"{CHARACTER_CLASSES.index(character_class) + 1} {character_class}")
            
        choice = int(input("Choose your class: "))
        if choice not in range(len(CHARACTER_CLASSES + 1)):
            continue
        
        character_class_choice = CHARACTER_CLASSES[choice - 1]
                 
    character_class = character_class_choice
    inventory = create_inventory(character_class)
    
    return Character(name, age, gender, character_class, inventory)