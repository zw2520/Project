from project2class.game import Person, bcolors
from project2class.Magic import Spell
from project2class.Inventory import Item
import random

#Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
halo = Spell("Halo", 25, 100, "black")
blizzard = Spell("Blizzard", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curga =  Spell("Curaga", 50, 6000, "white")


#create some items
portion = Item("Potion", "potion", "Heals 50 HP", 50)
hiportion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, halo, blizzard, cure, cura]
enemy_spells =  [fire, halo, cure]
enemy_spells2 = [fire, halo, curga]
player_items = [{"item": portion, "quantity": 15}, {"item": hiportion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer,"quantity": 2}, {"item": grenade, "quantity": 5}]
# player and enemy instantiated
player1 = Person("Velos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_spells, player_items)
players = [player1, player2, player3]

enemy1 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 11200, 701, 525, 25, enemy_spells2, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)
# while running:
#     print("")

while running:
    print("=========================")


    print("\n")
    print("name                        HP                                   MP ")

    for player in players:
        player.get_stats()

    # Enemy
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    # play choose attack method
    for player in players:
        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)
            enemies[enemy] .take_dmg(dmg)
            print("You attacked", enemies[enemy].name.replace(" ",""), "for", dmg, "point of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ",""), "has died.")
                del enemies[enemy]
        # if the player choose Magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL, "\nNot Enough MP!\n", bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type_ == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE, "\n", spell.name, "heals for", str(magic_dmg), "HP.", bcolors.ENDC)
            elif spell.type_ == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE+ '\n'+ spell.name, "deals", str(magic_dmg), "points of damage to", enemies[enemy].name.replace(" ",""), bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ",""), "has died.")
                    del enemies[enemy]
        # if the player choose items
        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL, "\n", "None left", bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type_ == "portion":
                player.heal(item.prop)
                print(bcolors.OKGREEN, "\n", item.name, "heals for", item.prop, "HP", bcolors.ENDC)
            elif item.type_ == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN, "\n", item.name, "fully restores HP/MP", bcolors.ENDC)
            elif item.type_ == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.FAIL, "\n", item.name, "deals", str(item.prop), "pints of damage to", enemies[enemy].name.replace(" ",""), bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ",""), "has died.")
                    del enemies[enemy]

    # determine the battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN, 'You win!', bcolors.ENDC)
        running = False
    # check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL, "Your enemy has defeated you!", bcolors.ENDC)
        running = False

    # Enemy attack phase
    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # choose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_dmg()

            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ", ""), "attacked", players[target].name.replace(" ", ""), "for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type_ == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + "heals", enemy.name.replace(" ",""), "for", str(magic_dmg), "HP.", bcolors.ENDC)
            elif spell.type_ == "black":
                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE+ '\n'+ enemy.name.replace(" ", ""), "'s", spell.name, "deals", str(magic_dmg), "points of damage to", players[target].name.replace(" ",""), bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ",""), "has died.")
                    del players[target]
            #print("Enemy Chose", spell, "damage is", magic_dmg)