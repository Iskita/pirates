import random

class CaveBattle:
    
     
    def __init__(self): 
        self.battle_continue = True
       
        
    def attack(self):
        if self.attack_choice == 1:
            attack_points = random.randint(18,25)
            return attack_points 
        elif self.attack_choice == 2: 
            attack_points = random.randint(10,35) 
            return attack_points
    def creatureattack(self):
        if self.creature_choice == 1:
            creature_points = random.randint(18,25)
            return creature_points 
        elif self.creature_choice == 2: 
           creature_points = random.randint(10,35)
           return creature_points
        
    def heal(self):
        if self.attack_choice == 3:
            
            heal_points = random.randint(18,25) 
            return heal_points
    def creatureheal(self):
        if self.creature_choice == 3:
            
            creatureheal_points = random.randint(18,25) 
            return creatureheal_points     
       
        
    def checkHealth(self):
        if self.user_health > 100:
            self.user_health = 100 
        elif self.user_health <= 0: 
            self.user_health = 0
            self.battle_continue = False
        
        if self.creature_health > 100: 
            self.creature_health = 100 
        elif self.creature_health <= 0: 
            self.creature_health = 0 
            self.battle_continue = False 
        
             
        
    def playGame(self):
        if self.attack_choice == 1 or self.attack_choice == 2:
            self.damage_to_creature = self.attack()
            self.heal_self = 0
            if self.creature_choice == 1:
                print("creature used close range attack")
            elif self.creature_choice == 2:
                print("creature used far range attack")
            else:
                print("creature healed itself")
            print("You dealt",self.damage_to_creature,"damage.")
            self.creature_health = (self.creature_health) - self.damage_to_creature
            self.checkHealth()
                
        if self.creature_choice == 1 or self.creature_choice == 2:
            self.damage_to_user = self.creatureattack()
            self.heal_creature = 0
            print("CREATURE dealt", self.damage_to_user, "damage.")
            self.user_health = self.user_health - self.damage_to_user
            self.checkHealth()
                
        if self.attack_choice == 3:
            self.heal_self = self.heal() 
            self.damage_to_creature = 0
            if self.creature_choice == 1:
                print("creature used close range attack")
            elif self.creature_choice == 2:
                print("creature used far range attack")
            else:
                print("creature healed itself")
            print("You dealt",self.damage_to_creature,"damage.")
            print("You healed",self.heal_self,"health points.")
            self.user_health = self.user_health + self.heal_self
            self.checkHealth()
                
        if self.creature_choice == 3:
            self.heal_creature = self.creatureheal() 
            self.damage_to_user = 0 
            print("creature healed", self.heal_creature, "health points ")
            
            self.creature_health = self.creature_health + self.heal_creature
            self.checkHealth()
        
    def process(self, starting_health):    
        self.user_health = starting_health
        self.creature_health = 100
        while self.battle_continue == True:
            print("----------------------------------")
            print("Your current health is", self.user_health)
            print("creature's current health is", self.creature_health)  
            print("\nATTACK CHOICES\n1. Close range attack\n2. Far range attack\n3. Heal")
            self.attack_choice = int(input("\nSelect an attack: "))
            if self.creature_health == 100:
                self.creature_choice = random.randint(1,2)
            else:
                self.creature_choice = random.randint(1,3)
                   
            self.playGame()
            self.checkHealth()
            

            
              
        if self.user_health < self.creature_health: 
            print("\nYou lost! Better luck next time!")
        else:
            print("\nYou won against creature!")
        return self.user_health     
                
                       
 
    
            
if __name__== "__main__":
    game = CaveBattle()
    game.process()
