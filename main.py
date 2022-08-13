from requests import get
from pprint import PrettyPrinter
from random import random, randrange

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()



def get_links():
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    return links


def get_scoreboard():
    scoreboard = get_links()['currentScoreboard']
    data = get(BASE_URL + scoreboard).json()
    printer.pprint(data)


def get_team_stats_leader():
    team_stats_leader = get_links()['leagueTeamStatsLeaders']
    
    # 'vegas' is the Summer League. Change to 'regularSeason' for Regular Season stats
    data = get(BASE_URL + team_stats_leader).json()['league']['vegas']['regularSeason']['teams']

    # Delete/Comment out this line to sort by name instead of points-per-game
    data.sort(key=lambda x: int(x['ppg']['rank']))

    for team in data:
        team_name_abbrv = team['abbreviation']
        team_city = team['name']
        team_name = team['nickname']
        ppg = team['ppg']['avg']
        apg = team['apg']['avg']

        print(f"{team_name_abbrv} || {team_city} {team_name} || PPG: {ppg} || APG: {apg}\n")


def get_all_player_stats():
    roster_players = get_links()['leagueRosterPlayers']
    players = get(BASE_URL + roster_players).json()['league']['standard']

    for player in players:
        fname = player['firstName']
        lname = player['lastName']
        p_id = player['personId']
        height_feet = player['heightFeet']
        height_inches = player['heightInches']
        

        gamelog = get_links()['playerProfile']
        gamelog_new = gamelog.replace('{{personId}}', p_id)

        log_resp = get(BASE_URL + gamelog_new).json()['league']['standard']['stats']['regularSeason']['season']
        if log_resp and height_feet != '-':
            latest_stats = log_resp[0]['total']

            mins = latest_stats['mpg']
            ppg = latest_stats['ppg']
            apg = latest_stats['apg']
            
            printer.pprint(log_resp[0])
            print(f"{fname} {lname} - {height_feet}\'{height_inches}\"")
            print(f"MINS: {mins} || PPG: {ppg} || APG: {apg}\n")

def get_team_stats(team_input):
    team_stats_leader = get_links()['leagueTeamStatsLeaders']

    # 'vegas' is the Summer League. Change to 'regularSeason' for Regular Season stats
    teams = get(BASE_URL + team_stats_leader).json()['league']['vegas']['regularSeason']['teams']

    #print(teams[0]['fgp'].keys())
    stats = []
    for team in teams:
        team_city = team['name']
        team_name = team['nickname']

        if team_input.split()[-1].upper() == team_name.upper():
            ppg = team['ppg']['avg']
            apg = team['apg']['avg']
            fpg = team['fgp']['avg']
            orpg = team['orpg']['avg']
            drpg = team['drpg']['avg']
            spg = team['spg']['avg']
            bpg = team['bpg']['avg']
            
            stats = [[team_city, team_name], [ppg, apg, fpg, orpg, drpg, spg, bpg]]
            return stats

    return stats
          
def get_random_team_stats():
    team_stats_leader = get_links()['leagueTeamStatsLeaders']

    # 'vegas' is the Summer League. Change to 'regularSeason' for Regular Season stats
    teams = get(BASE_URL + team_stats_leader).json()['league']['vegas']['regularSeason']['teams']

    team_num = randrange(len(teams))

    team = teams[team_num]
    team_city = team['name']
    team_name = team['nickname']

    ppg = team['ppg']['avg']
    apg = team['apg']['avg']
    fpg = team['fgp']['avg']
    orpg = team['orpg']['avg']
    drpg = team['drpg']['avg']
    spg = team['spg']['avg']
    bpg = team['bpg']['avg']
    
    stats = [[team_city, team_name], [ppg, apg, fpg, orpg, drpg, spg, bpg]]
    return stats



def get_player_stats(player_name):
    roster_players = get_links()['leagueRosterPlayers']
    players = get(BASE_URL + roster_players).json()['league']['standard']

    #printer.pprint(players[0].keys())

    player_name_split = player_name.split()
    #print(player_name_split)

    for player in players:
        stats = []
        if player['firstName'].upper() == player_name_split[0].upper() and player['lastName'].upper() == player_name_split[1].upper():
            p_id = player['personId']
            
            height_feet = player['heightFeet']
            height_inches = player['heightInches']



            gamelog = get_links()['playerProfile']
            gamelog_new = gamelog.replace('{{personId}}', p_id)
            log_resp = get(BASE_URL + gamelog_new).json()['league']['standard']['stats']['regularSeason']['season']

            if log_resp and height_feet != '-':
                latest_stats = log_resp[0]['total']

                print(latest_stats.keys())
                print()

                fname = player['firstName']
                lname = player['lastName']

                height = str(height_feet) + '\'' + str(height_inches) + "\""
                weight = str(player['weightPounds'])
                nba_debut_year = str(player['nbaDebutYear'])
                pos = player['pos']

                year = log_resp[0]['seasonYear']
                gp = latest_stats['gamesPlayed']
                mins = latest_stats['mpg']
                ppg = latest_stats['ppg']
                apg = latest_stats['apg']
                rpg = latest_stats['rpg']

                stats = [[fname, lname],[height, weight, nba_debut_year, pos],[year, gp, mins, ppg, apg, rpg]]
                
                print(f"{player_name_split[0]} {player_name_split[1]} - {height_feet}\'{height_inches}\"")
                print(f"GAMES PLAYED: {gp} || MINS: {mins}")
                print(f"PPG: {ppg} || APG: {apg} || RPG: {rpg}\n")
                return stats

    return stats

def get_random_player_stats():
    roster_players = get_links()['leagueRosterPlayers']
    players = get(BASE_URL + roster_players).json()['league']['standard']

    valid_player = False

    while (not valid_player):
        random_num = randrange(len(players))

        player = players[random_num]
        p_id = player['personId']
        
        height_feet = player['heightFeet']
        height_inches = player['heightInches']

        gamelog = get_links()['playerProfile']
        gamelog_new = gamelog.replace('{{personId}}', p_id)
        log_resp = get(BASE_URL + gamelog_new).json()['league']['standard']['stats']['regularSeason']['season']

        if log_resp and height_feet != '-':
            latest_stats = log_resp[0]['total']

            #print(latest_stats.keys())
            #print()

            fname = player['firstName']
            lname = player['lastName']

            height = str(height_feet) + '\'' + str(height_inches) + "\""
            weight = str(player['weightPounds'])
            nba_debut_year = str(player['nbaDebutYear'])
            pos = player['pos']

            year = log_resp[0]['seasonYear']
            gp = latest_stats['gamesPlayed']
            mins = latest_stats['mpg']
            ppg = latest_stats['ppg']
            apg = latest_stats['apg']
            rpg = latest_stats['rpg']

            stats = [[fname, lname],[height, weight, nba_debut_year, pos],[year, gp, mins, ppg, apg, rpg]]          
            valid_player = True
            return stats
    
def test():
    test_str = 'leagueRosterPlayers'
    test = get_links()[test_str]
    print("\n")

    # printing links
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    print("LINKS AVAILABLE ARE:\n")
    printer.pprint(links)


def main():
    test()
    print()
    #get_team_stats_leader()
    #get_all_player_stats()
    #print(get_player_stats("Steven Adams"))
    #print(get_team_stats("Los Angeles Lakers"))
    #print(get_random_player_stats())
    #print(get_random_team_stats())



if __name__ == '__main__':
    main()