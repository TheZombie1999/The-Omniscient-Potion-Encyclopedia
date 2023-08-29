
from typing import List, Set
import requests
from bs4 import BeautifulSoup

class Property:

    def __init__(self, name:str, effectType:str) -> None:
        self.name = name
        self.effectType = effectType
        pass

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name and self.effectType == self.effectType
    
    def __hash__(self) -> int:
        return hash((self.name, self.effectType))

class Ingridient:

    def __init__(self, name: str, first:Property, second:Property,third:Property, forth:Property) -> None:
        self.name=name

        self.properties = [first, second, third, forth]

        self.first = self.properties[0]
        self.second = self.properties[1]
        self.third = self.properties[2]
        self.forth = self.properties[3]
        pass

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __hash__(self) -> int:
        return hash((self.name, self.first, self.second, self.third, self.forth))

    def __str__(self) -> str:
        return f'Ingredient({self.name}, {self.first}, {self.second}, {self.third}, {self.forth})'
    
    def __repr__(self) -> str:
        return '\n' + self.__str__()
    
    def get_properties(self):
        return self.properties
    
    def matching_properties(self, other) -> Set[Property]:
        matches:Set[Property] = set()

        for p1 in self.get_properties():
            for p2 in other.get_properties():
                if p1 == p2:
                    matches.add(p1)

        return matches

class Potion:
    
    def __hash__(self) -> int:
        if len(self.ingredients) == 2:
            a = list(self.ingredients)
            return hash((a[0], a[1]))
        else:
            a = list(self.ingredients)
            return hash((a[0], a[1], a[2]))

    def __init__(self, ingredients:Set[Ingridient]):
        if len(ingredients) < 2 or len(ingredients) > 3:
            raise Exception("Invalid Number of Ingridients")
        
        self.ingredients = ingredients
        pass

    def __str__(self) -> str:
        return str(self.get_Properties()) + " : " + str(self.ingredients)
        # return str(self.ingredients)
    
    def __repr__(self) -> str:
        return '\n' + self.__str__()
    
    def __eq__(self, other) -> bool:
        return self.ingredients == other.ingredients

    def get_Properties(self) -> Set[Property]:
        properties:Set[Property] = set()

        for ingredient1 in self.ingredients:
            for ingredient2 in self.ingredients:
                if ingredient1 == ingredient2:
                    continue

                matching_properites = ingredient1.matching_properties(ingredient2)

                for p in matching_properites:
                    if p not in properties:
                        properties.add(p)

        return properties

# There are allways multiple ways to get the same Properties for a Potion.
# A Recipe Contains a list of potions that have a set of Properties.
class Recipe:

    def __init__(self, properties:List[Property], potions:List[Potion]):
        self.properties = properties
        self.potions = potions
        pass

    def __str__(self) -> str:
        erg =  f'Properties: {self.properties} \nNumber of Possiblities: {len(self.potions)}\nPotions: \n'

        for p in self.potions:
            for ingre in p.ingredients:
                erg = erg + ingre.name + ", "
            erg = erg + "\n"

        erg = erg + "\n"
        return erg
    
    def writeToFile(self):

        with open(f"Potion_Recipy_{self.properties}.txt", "w") as file:
            file.writelines(self.__str__())
        pass
    
# Creats all possible potions from a list of ingredients
def permute_ingredients(ingridients:List[Ingridient], all=True)-> Set[Potion]:
    potions:Set[Potion] = set()

    for ingredient1 in ingridients:
        for ingredient2 in ingridients:
            if ingredient1 != ingredient2:
                potions.add(Potion(ingredients={ingredient1, ingredient2}))
    if all:
        for ingredient1 in ingridients:
            for ingredient2 in ingridients:
                for ingredient3 in ingridients:
                    if ingredient1 != ingredient2:
                        potions.add(Potion(ingredients={ingredient1, ingredient2, ingredient3}))
    return potions

def get_list_of_ingrediens(URL = "https://en.uesp.net/wiki/Skyrim:Ingredients"):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find_all("table", class_="wikitable")

    ingridients = list(table)[0].find_all("tr")

    list_of_ingridients: List[Ingridient] = []

    for name, prop in zip(ingridients[1::2], ingridients[2::2]):
        all_props = prop.find_all("td")[0:4]
        list_of_ingridients.append(Ingridient(name=name['id'], 
                first=Property(name=all_props[0].img['alt'], effectType=all_props[0]['class'][0]),
                second=Property(all_props[1].img['alt'], effectType=all_props[1]['class'][0]),
                third=Property(all_props[2].img['alt'], effectType=all_props[2]['class'][0]),
                forth=Property(all_props[3].img['alt'], effectType=all_props[3]['class'][0])))
    return list_of_ingridients

def create_recipe(properties:Set[Property], all=False) -> Recipe:

    list_of_potions = permute_ingredients(get_list_of_ingrediens(), all=all)

    def property_filter(potion:Potion):
        if potion.get_Properties() == properties:
            return True
        return False
    
    return Recipe(properties, set(filter(property_filter, list_of_potions)))

if __name__ == '__main__':
    #print(create_recipe({Property("Slow", "EffectNeg"), Property("")}))
    #print(create_recipe({Property("Fortify Sneak", "EffectPos"), Property("Fortify One-handed", "EffectPos"), Property("Invisibility", "EffectPos")}, all=True))
    #print(get_list_of_ingrediens())
    # print(create_recipe({Property("Fortify One-handed", "EffectPos"), Property("Invisibility", "EffectPos")}, all=True))
    # print(create_recipe({Property("Fortify Block", "EffectPos"), Property("Fortify Heavy Armor", "EffectPos")}, all=True))

    create_recipe({Property("Resist Fire", "EffectPos"), Property("Resist Frost", "EffectPos"), Property("Resist Shock", "EffectPos")}, all=True).writeToFile()