from requests import get
from pprint import PrettyPrinter
from random import random, randrange

import sys
import numpy as np 
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch

import io
import base64

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

		if team_input.split()[-1].upper() == team_name.split()[-1].upper():
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

def get_player_shotchartdetail(player_name, season_id):
	nba_players = players.get_players()
	player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
	print(player_dict)
	print('\n')

	career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
	career_df = career.get_data_frames()[0]
	print(career_df)
	print('\n')

	team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID'].astype(int)
	print(team_id)
	print('\n')

	shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
													player_id=int(player_dict['id']),
													season_type_all_star='Regular Season',
													season_nullable=season_id,
													context_measure_simple="FGA").get_data_frames()
	
	return shotchartlist[0], shotchartlist[1]

def draw_court(ax=None, color="blue", lw=1, outer_lines=False):
	if ax is None:
		ax = plt.gca()

	hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

	backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)

	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

	corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

	if outer_lines:
		outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
		court_elements.append(outer_lines)

	for element in court_elements:
		ax.add_patch(element)

# Shot Chart Function
def shot_chart(data, title="", color="b", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
			   court_color="white", court_lw=2, outer_lines=False,
			   flip_court=False, gridsize=None,
			   ax=None, despine=False):

	if ax is None:
		ax = plt.gca()

	if not flip_court:
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
	else:
		ax.set_xlim(xlim[::-1])
		ax.set_ylim(ylim[::-1])

	ax.tick_params(labelbottom="off", labelleft="off")
	ax.set_title(title, fontsize=18)

	draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

	# separate color by make or miss
	x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
	y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

	x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
	y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

	ax.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidths=3)
	ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker='o', s=100, linewidths=3)

	for spine in ax.spines:
		ax.spines[spine].set_lw(court_lw)
		ax.spines[spine].set_color(line_color)

	if despine:
		ax.spines["top"].set_visible(False)
		ax.spines["bottom"].set_visible(False)
		ax.spines["right"].set_visible(False)
		ax.spines["left"].set_visible(False)

	return ax

def display_player_chart(player_name, season_id):
	roster_players = get_links()['leagueRosterPlayers']
	players = get(BASE_URL + roster_players).json()['league']['standard']

	player_name_split = player_name.split()
	#print(player_name_split)

	for player in players:
		if player['firstName'].upper() == player_name_split[0].upper() and player['lastName'].upper() == player_name_split[1].upper():
			player_name = player['firstName'] + " " + player['lastName']

	# title
	title = player_name + " Shot Chart " + season_id

	# Get Shotchart Data using nba_api
	player_shotchart_df, league_avg = get_player_shotchartdetail(player_name, season_id)

	# Draw Court and plot Shot Chart
	shot_chart(player_shotchart_df, title=title)
	# Set the size for our plots
	plt.rcParams['figure.figsize'] = (36, 33)
	return plt

	
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
	#display_player_chart("Draymond Green", "2021-22")



if __name__ == '__main__':
	main()