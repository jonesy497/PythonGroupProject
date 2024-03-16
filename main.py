import requests
import random
from time import sleep
from operator import itemgetter


# Creates a list of 6 random numbers and assigns the first 3 into one list and the second 3 into a second list
def task_1():
    party = []

    while len(party) < 6:
        selection = random.randint(1, 151)
        if selection not in party:
            party.append(selection)

    return itemgetter(0, 1, 2)(party), itemgetter(3, 4, 5)(party)


# gets pokeAPI data for all 6 pokemon
def task_2():
    parties = task_1()
    dex = []
    for party in parties:
        pokemons = []
        for pokemon in party:
            url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon)
            response = requests.get(url)
            pokedex = response.json()
            pokemons.append(task_3(pokedex))
        dex.append(pokemons)
    return dex


# dictionary for pokemon stats
def task_3(pokedex):
    return {'name': pokedex['name'].title(),
            'id': pokedex['id'],
            'height': pokedex['height'],
            'weight': pokedex['weight'],
            'hp': pokedex['stats'][0]['base_stat'],
            'attack': pokedex['stats'][1]['base_stat'],
            'defense': pokedex['stats'][2]['base_stat'],
            'special attack': pokedex['stats'][3]['base_stat'],
            'special defense': pokedex['stats'][4]['base_stat'],
            'speed': pokedex['stats'][5]['base_stat']}


# displays dictionary content sensibly
def pretty_string(stat_block):
    for key, value in stat_block.items():
        print(f'{key.title()}: {value}')


# gets player pokemon and stat choice
def task_4():
    parties = task_2()
    player_party = parties[0]
    opponent_party = parties[1]
    print('Player Pokemon choice is: ' )
    for pokemon in player_party:
        pretty_string(pokemon)
        print('')
    while True:
        selected_pokemon = input('Selected pokemon name: ')
        if selected_pokemon.title() in player_party[0].values() or selected_pokemon.title() in player_party[1].values() or selected_pokemon.title() in player_party[2].values():
            selected_stat = input('Pick a stat: id, height, weight, hp, attack, defense, special attack, special defense, speed: ')
            while True:
                if selected_stat.lower() not in player_party[0] or selected_stat.lower() == 'name':
                    print('Invalid selection. Try again: ')
                    selected_stat = input('Player pokemon is: ' + selected_pokemon + '.\nPick a stat: id, height, weight, hp, attack, defense, special attack, '
                                                                                     'special defense, speed: ')
                else:
                    break
        else:
            print('Invalid selection. Try again: ')
            continue
        for pokemon in player_party:
            if pokemon['name'] == selected_pokemon.title():
                return task_6(selected_stat, pokemon, opponent_party)


# opponent makes its pokemon choice based on the highest value of the player's selected stat
def task_6(selected_stat, player, opponent_party):
    opponent = {}
    for pokemon in opponent_party:
        if pokemon[selected_stat] > opponent.get(selected_stat, 0):
            opponent = pokemon
    task_7(selected_stat, player, opponent)


# compares stats
def task_7(selected_stat, player, opponent):
    if player[selected_stat] > opponent[selected_stat]:
        print('Opponent drew ' + opponent['name'] + ', with the stat of: ' + str(opponent[selected_stat]) + '. Player wins!')
    elif player[selected_stat] < opponent[selected_stat]:
        print('Opponent drew ' + opponent['name'] + ', with the stat of: ' + str(opponent[selected_stat]) + '. Opponent wins!')
    else:
        print('Opponent drew ' + opponent['name'] + ". It's a draw!")


task_4()

# play again?
while True:
    sleep(1)
    again = input('Again? y/n: ')
    if again == 'y':
        task_4()
    elif again == 'n':
        print('Thanks for playing!')
        break
    else:
        print('Huh?')
