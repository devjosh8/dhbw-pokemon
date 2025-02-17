from pokemon import *
import questionary
from time import sleep

playerPokemons = []

def clearScreen():
    print("\033[H\033[J", end="")


def fight(playerPokemon: Pokemon, enemyPokemon: Pokemon):
    global playerPokemons
    # beide Pokemon full hp machen
    playerPokemon._regen()
    enemyPokemon._regen()

    # 0 == Spieler, 1 == Computer
    turn = random.choice([0, 1])

    while True:
        if turn == 0:
            print("\n\n\tDu bist am Zug\n")
            selectedAttack = questionary.select("Wie möchtest du angreifen?", choices=(["Angriff", "Risiko-Angriff"])).ask()
            if selectedAttack == "Angriff":
                attackCritic, attackDamage = playerPokemon.attack(enemyPokemon, 1)
                if attackCritic:
                    print(color.BOLD + "KRITISCH: " + color.END + f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                else:
                    print(f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                print("\n" + color.RED + color.BOLD + f"{enemyPokemon.name}" + color.END + " hat noch " + color.RED + color.BOLD + f"{round(enemyPokemon.currentHealth, 1)}" + color.END + " Leben übrig!")
            else:
                # Risiko Angriff Chance von 1 zu 2, aber doppelter Schaden
                risk = random.choice([0, 1])
                if risk == 0:
                    attackCritic, attackDamage = playerPokemon.attack(enemyPokemon, 2)
                    if attackCritic:
                        print(color.BOLD + "KRITISCHES RISIKO: " + color.END + f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                    else:
                        print(color.BOLD + "RISIKO: " + color.END + f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                    print("\n" + color.RED + color.BOLD + f"{enemyPokemon.name}" + color.END + " hat noch " + color.RED + color.BOLD + f"{round(enemyPokemon.currentHealth, 1)}" + color.END + " Leben übrig!")

                else:
                    print(f">> {playerPokemon.name} hat " + color.RED + "verfehlt!" + color.END)

            if enemyPokemon.currentHealth <= 0:
                break

            turn = 1
            print(f"\n {enemyPokemon.name} ist jetzt am Zug", end = "")
            for i in range(30):
                print(".", end="", flush=True)
                sleep(0.1)
            clearScreen()
        else:
            print(f"\n\n\t{enemyPokemon.name} ist am Zug")
            attackCritic, attackDamage = enemyPokemon.attack(playerPokemon, 1)
            if attackCritic:
                print(color.BOLD + "KRITISCH: " + color.END + f" Du hast " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "erlitten!")
            else:
                print(f" Du hast " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "erlitten!")
            
            if(playerPokemon.currentHealth < 0):
                playerPokemon.currentHealth = 0
                
            print("\nDu hast noch " + color.GREEN + color.BOLD + f"{round(playerPokemon.currentHealth, 1)}" + color.END + " Leben übrig!")
            
            for i in range(30):
                print(".", end="", flush=True)
                sleep(0.1)
            
            turn = 0
            if playerPokemon.currentHealth <= 0:
                break
    
    if enemyPokemon.currentHealth <= 0:
        # Spieler bekommt das Pokemon
        enemyPokemon._regen()
        playerPokemons.append(enemyPokemon)
        clearScreen()
        print(f"\tDu hast den Kampf " + color.GREEN + color.BOLD + "GEWONNEN!!!!" + color.END)
        print("Als Belohnung erhälst du " + color.YELLOW + f"{enemyPokemon.name}" + color.END + " als spielbarer Character.")
        print("\n\n")
        return
    if playerPokemon.currentHealth <= 0:
        print(f"\tDu hast den Kampf " + color.RED + color.BOLD + "verloren..." + color.END)
        print("Kehre zum Menü zurück....\n\n")

def mainLoop():
    global playerPokemons
    while True:
        c = ["Kämpfen", "Verlassen", "Pokemon anschauen"]
        result = questionary.select("Was möchtest du machen?", choices=c).ask()

        if result == "Verlassen":
            break
        
        if result == "Pokemon anschauen":
            pokemon: Pokemon
            clearScreen()
            print("\n\tDeine Pokemon:")
            for pokemon in playerPokemons:
                pokemon.print_stats()
            print("\n\n")

        if result == "Kämpfen":
            pokemonChoice = []
            for pokemon in playerPokemons:
                pokemonChoice.append(pokemon.name)

            pokemonSelect = questionary.select("Mit welchem Pokemon möchtest du kämpfen?", choices=pokemonChoice).ask()
            fightingPokemon = next((obj for obj in playerPokemons if obj.name == pokemonSelect), None)
            
            # Spieler hat fightingPokemon ausgewählt (randomPokemon aus pokemon.py)
            enemy = random.choice(randomPokemon)
            clearScreen()
            print("\n\n" + "Ein wildes " + color.GREEN + color.BOLD + enemy.name + color.END + " des Typs " + color.BOLD + str(enemy.type.name) + color.END + " erscheint!")
            
            fight(fightingPokemon, enemy)

def main():
    # Anfangspokemon auswählen

    basePokemon = [Pokemon("Glumanda", PokemonType.FIRE, 20, 1, 5, 1),
               Pokemon("Schiggy", PokemonType.WATER, 27, 1, 4, 1),
               Pokemon("Bisasam", PokemonType.PLANT, 40, 1, 3, 1)]

    clearScreen()

    basePokemonName = []
    for pokemon in basePokemon:
        basePokemonName.append(pokemon.name)

    selectedPokemon = questionary.select("Welches Start-Pokemon wählst du?", choices=basePokemonName).ask()

    playerPokemons.append( next((obj for obj in basePokemon if obj.name == selectedPokemon), None) )

    print("\n" + f'Du hast {selectedPokemon} ausgewählt.')
    
    print("\n"*2)
    mainLoop()
    pass


main()