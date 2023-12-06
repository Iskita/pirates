
from game import location
import game.config as config
from game.display import announce 
from game.events import *
import game.items as items
import random
import game.myis as caveb

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'A'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["trees"] = Trees(self)
        self.locations["riddle_gate"]= Riddle_gate(self)
        self.locations["volcano"] = Volcano(self)
        self.locations["bush"] = Bush(self)
        self.locations["temple"] = Temple(self)
        self.locations["cave"] = Cave(self)

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["trees"]
            """announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False"""
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["riddle_gate"]
        elif (verb == "west"):  
            config.the_player.next_loc = self.main_location.locations["temple"] 
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["bush"]


class Trees (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = items.Cutlass()
        self.item_in_clothes = items.Flintlock()

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")

class Riddle_gate(location.SubLocation):  
    def __init__(self,m):
        super().__init__(m)
        self.name = "ridde_gate"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 10
        self.woord="water"
        self.word=["w","a","t","e","r"]
        self.words=self.word[:]
        self.item_after_puzzle = items.Cutlass()
        self.open_gate = False
        random.shuffle(self.word)
        

    def enter (self):
        if self.open_gate == True:
            announce("the gate's open")
        else:
            announce ("WElcome! You have to rearrange the alphabet to open this gate. ")
            count1 = 0
            count2 = self.event_chance = 10
            while count1 < count2 and not self.open_gate:
                print("rearrange this word:")
                print(self.words)
                user_word=input("your word : ", )

                if user_word != self.woord: 
                    count1 +=1
                    print("incorrect!! better luck next time")
                else:
                    print("correct!you got it ")  
                    item = self.item_after_puzzle
                    config.the_player.add_to_inventory([item])
                    print("yay!!you got a cutlass")
                    self.item_in_puzzle = None
                    self.open_gate = True
                    print("the gate is open")
                
		
   
    def process_verb (self, verb, cmd_list, nouns):
        if self.open_gate == True:
            if (verb == "west" or verb == "north"):
                config.the_player.next_loc = self.main_location.locations["volcano"]
            elif(verb == "east" or verb == "south"):
                config.the_player.next_loc = self.main_location.locations["cave"]
        else:
            if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
                announce ("You return to your ship.")
                config.the_player.next_loc = config.the_player.ship
                config.the_player.visiting = False       
            
class Volcano(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "volcano"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.item_after_quiz = items.Flintlock()
        self.num1 = random.randint(1, 10) 
        self.num2 = random.randint(1, 10)
    def enter (self):
        announce("you entered a volcano !! ")
        
        correct_answer = self.num1 + self.num2

        print(f"Solve the Math Puzzle to get a treaure: {self.num1} + {self.num2}")
        user_answer = int(input("Your answer: "))
        if user_answer == correct_answer:
            print("correct!you got it " )  
            item = self.item_after_quiz
            config.the_player.add_to_inventory([item])
            print("yay!!you got a flintlock")
            self.item_in_quiz = None
            config.the_player.go = True

        else:
           print("Incorrect! Try again")
	

    def process_verb (self, verb, cmd_list, nouns):   
        
        if (verb == "south" or verb == "north" or verb == "west" ):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif(verb == "east" ):
            config.the_player.next_loc = self.main_location.locations["cave"]    

class Cave(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cave"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter (self):
        announce("WElcome to the cave!! you have to fight this creature to get the treasure ")
        chosen = random.choice(config.the_player.get_pirates())

        final_health = caveb.CaveBattle().process(chosen.health)
        damage = chosen.health - final_health
        if damage > 0:
            chosen.inflict_damage(damage,"lost to a creature in a cave")

        else:
            chosen.health = final_health

    def process_verb (self, verb, cmd_list, nouns): 
        if (verb == "south" or verb == "north" or verb == "east" ):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif(verb == "west" ):
            config.the_player.next_loc = self.main_location.locations["volcano"]    

         
            

class Temple(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "volcano"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.item_after_sequence = items.Cutlass()
    def enter (self):
        announce("you arrived at a temple")
        announce("let's see your guessing skills! Guess a sequence from 1 to 5 and try to put them in right order ")
        numbers = list(range(1, 6))
        random.shuffle(numbers)
        correct_sequence = numbers.copy()

        print("guess a sequence from 1 to 6", numbers)
       
        user_sequence = [int(x) for x in input("Enter the sequence separated by spaces: ").split()]

        if user_sequence == correct_sequence:
            print("Great memory!.")
            item = self.item_after_sequence
            config.the_player.add_to_inventory([item])
            print("yay!!you got a cutlass")
            self.item_in_sequence = None
        else:
            print("Oops! Wrong sequence. Try again.")
            config.the_player.go = True
    def process_verb (self, verb, cmd_list, nouns):
            if (verb == "south" or verb == "north" or verb == "east" ):
                announce ("You return to your ship.")
                config.the_player.next_loc = config.the_player.ship
                config.the_player.visiting = False
            elif(verb == "west" ):
                config.the_player.next_loc = self.main_location.locations["bush"] 
class Bush(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "volcano"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.item_after_guess = items.Flintlock()
    def enter (self):
        announce("you fell into a bush")
        announce("Play a number guessing  game through 10 to 20 to get a item")
        correct_number = random.randint(10, 20)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            user_guess = int(input("Your guess: "))

            if user_guess == correct_number:
                    print("congrats!!you got it correct")
                    item = self.item_after_guess
                    config.the_player.add_to_inventory([item])
                    print("yay!!you got a flintlock")
                    self.item_in_guess = None
                    config.the_player.go = True
            else:
                attempts += 1
                print("wrong number !! ")
        print("times up!! try again  ")
        config.the_player.go = True
        
    def process_verb (self, verb, cmd_list, nouns):
            if (verb == "north" or verb == "east" or verb == "west"):
                announce ("You return to your ship.")
                config.the_player.next_loc = config.the_player.ship
                config.the_player.visiting = False
            elif(verb == "south" ):
                config.the_player.next_loc = self.main_location.locations["trees"] 
