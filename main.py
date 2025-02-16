from pokemon import *
import questionary
from time import sleep

playerPokemon = []

def clearScreen():
    print("\033[H\033[J", end="")


def fight(playerPokemon: Pokemon, enemyPokemon: Pokemon):
    # beide Pokemon full hp machen
    playerPokemon._regen()
    enemyPokemon._regen()

    # 0 == Spieler, 1 == Computer
    turn = random.choice([0, 1])

    while True:
        if turn == 0:
            print(">> \tDu bist am Zug")
            selectedAttack = questionary.select("Wie möchtest du angreifen?", choices=(["Angriff", "Risiko-Angriff"])).ask()
            if selectedAttack == "Angriff":
                attackCritic, attackDamage = playerPokemon.attack(enemyPokemon, 1)
                if attackCritic:
                    print(color.BOLD + "KRITISCH: " + color.END + f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                else:
                    print(f" Du hast {enemyPokemon.name} " + color.RED + color.BOLD + f"{round(attackDamage, 1)} Schaden " + color.END + "gemacht!")
                print("\n" + color.RED + color.BOLD + f"{enemyPokemon.name}" + color.END + " hat noch " + color.RED + color.BOLD + f"{round(enemyPokemon.currentHealth, 1)}" + color.END + " Leben übrig!")

        else:
            pass
    pass

def mainLoop():
    global playerPokemon
    while True:
        c = ["Kämpfen", "Verlassen", "Pokemon anschauen"]
        result = questionary.select("Was möchtest du machen?", choices=c).ask()

        if result == "Verlassen":
            break
        
        if result == "Pokemon anschauen":
            pokemon: Pokemon
            for pokemon in playerPokemon:
                pokemon.print_stats()

        if result == "Kämpfen":
            pokemonChoice = []
            for pokemon in playerPokemon:
                pokemonChoice.append(pokemon.name)

            pokemonSelect = questionary.select("Mit welchem Pokemon möchtest du kämpfen?", choices=pokemonChoice).ask()
            fightingPokemon = next((obj for obj in playerPokemon if obj.name == pokemonSelect), None)
            
            # Spieler hat fightingPokemon ausgewählt (randomPokemon aus pokemon.py)
            enemy = random.choice(randomPokemon)
            print("\n\n" + ">> Ein wildes " + color.GREEN + color.BOLD + enemy.name + color.END + " des Typs " + color.BOLD + str(enemy.type.name) + color.END + " erscheint!")
            
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

    playerPokemon.append( next((obj for obj in basePokemon if obj.name == selectedPokemon), None) )

    print("\n" + f'Du hast {selectedPokemon} ausgewählt.')
    
    print("\n"*2)
    mainLoop()
    pass


main()