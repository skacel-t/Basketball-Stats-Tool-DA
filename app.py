from constants import PLAYERS, TEAMS
import copy
import random
from statistics import mean


def clean_player_data():
    experienced_players = []
    inexperienced_players = []
    for player in PLAYERS:
        player_info = {}
        player_info['name'] = player['name']
        player_info['guardians'] = player['guardians'].split(' and ')
        player_info['height'] = int(player['height'][0:2])
        if player['experience'] == 'YES':
            player_info['experience'] = True
            experienced_players.append(player_info)
        else:
            player_info['experience'] = False
            inexperienced_players.append(player_info)
    return experienced_players, inexperienced_players


def balance_teams(players):
    teams_dict = {team:[] for team in TEAMS}
    while bool(players):
        for team in teams_dict:
            # this stops errors in case the number of players is not divisible by number of teams
            if not bool(players):
                break
            teams_dict[team].append(players.pop())
    return teams_dict


def display_stats(user_input):
    team_index = TEAMS.index(user_input)
    print(f"\nTeam name: {teams_stats[team_index]['team_name']}\n"
          f"Number of players: {teams_stats[team_index]['num_of_players']}\n"
          f"Player names: {', '.join([player['name'] for player in teams_stats[team_index]['players']])}\n"
          "  Note: players are listed from shortest to tallest.\n"
          f"Number of experienced players: {teams_stats[team_index]['experienced']}\n"
          f"Number of inexperienced players: {teams_stats[team_index]['not_experienced']}\n"
          f"Average height: {teams_stats[team_index]['average_height']} inches\n"
          f"Guardian names: {', '.join([', '.join(player['guardians']) for player in teams_stats[team_index]['players']])}\n")


def menu():
    print(f"{'-'*43}\nTeams: {', '.join([team for team in TEAMS])}.\n{'-'*43}\n"
          f"1. Enter a team name to display team stats. \n2. Enter '2' to re-balance teams.\n3. Enter '3' to quit.\n{'-'*43}")
    while True:
        try:
            user_input = input("Enter one of the menu options:  ")
            user_input = user_input.capitalize()
            if user_input not in TEAMS+['2', '3']:
                raise Exception(f"***\nInvalid input. Please enter one of the following: {', '.join([team for team in TEAMS])}, 2, 3.\nPress enter to try again.\n***")
        except Exception as err:
            input(err)
        else:
            break
    if user_input in TEAMS:
        display_stats(user_input)
        input("Press enter to return to menu.")
        return True
    elif user_input == '2':
        global teams_stats
        teams_stats = run_tool()
        input("New teams created! Press enter to return to menu.")
        return True
    elif user_input == '3':
        print("\nThanks for using the tool! Goodbye!\n")
        return False


def save_stats(made_teams):
    teams_stats = []
    for team in TEAMS:
        team_info = {}
        team_info['team_name'] = team
        team_info['players'] = made_teams[team]
        team_info['num_of_players'] = len(made_teams[team])
        team_info['experienced'] = sum((1 for player in made_teams[team] if player['experience']))
        team_info['not_experienced'] = sum((1 for player in made_teams[team] if not player['experience']))
        team_info['average_height'] = round(mean((player['height'] for player in made_teams[team])), 1)
        teams_stats.append(team_info)
    return teams_stats


def run_tool():
    random.shuffle(experienced_players)
    random.shuffle(inexperienced_players)
    cleaned_players = experienced_players + inexperienced_players
    made_teams = balance_teams(cleaned_players)
    sorted_made_teams = {}
    for team in TEAMS:
        sorted_made_teams[team] = sorted(made_teams[team], key=lambda x: x['height'])
    teams_stats = save_stats(sorted_made_teams)
    return teams_stats


#Running the program:
if __name__ == "__main__":
    experienced_players, inexperienced_players = clean_player_data()
    teams_stats = run_tool()
    running = True
    while running:
        running = menu()
        



