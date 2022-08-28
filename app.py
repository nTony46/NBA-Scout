from flask import Flask, render_template, request, flash, send_file
from main import *
import urllib.parse

app = Flask(__name__)
app.secret_key = "super secret key"

last_searched_name = []

@app.route("/home")
def index():
	flash("Enter a player or team")
	return render_template("landing.html")

@app.route("/search", methods=["POST", "GET"])
def search():
	searched_stats = get_player_stats(str(request.form['team_input']))
	searched_team_stats = get_team_stats(str(request.form['team_input']))

	if searched_stats:
		first_name = searched_stats[0][0]
		last_name = searched_stats[0][1]
		if last_searched_name:
			last_searched_name.pop()
		player_name = first_name + " " + last_name
		last_searched_name.append(player_name)
		flash("Here are the most recent stats for " + first_name + " " + last_name)
		print(searched_stats)
		return render_template("search.html", data=searched_stats) 
	elif searched_team_stats:
		team_name = searched_team_stats[0][0] + " " + searched_team_stats[0][1]
		flash("Here are the most recent stats for " + team_name)
		return render_template("search-team.html", data=searched_team_stats)
	else:
		flash("Invalid Player/Team - Try Again")
		return render_template("landing.html")
	
@app.route("/random-search-player", methods=["POST", "GET"])
def random_search_player():
	stats = get_random_player_stats()
	first_name = stats[0][0]
	last_name = stats[0][1]
	if last_searched_name:
		last_searched_name.pop()
	name = first_name + " " + last_name
	last_searched_name.append(name)

	flash("The random player is " + name)
	return render_template("search.html", data=stats)

@app.route("/random-search-team", methods=["POST", "GET"])
def random_search_team():
	stats = get_random_team_stats()
	team_name = stats[0][0] + " " + stats[0][1]
	flash("The random team is " + team_name)
	return render_template("search-team.html", data=stats)

@app.route('/visualize-shot-chart')
def visualize():
	plot = display_player_chart(last_searched_name[0], "2021-22")

	img=io.BytesIO()
	plot.savefig(img, format='png')
	img.seek(0)
	plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
	#return send_file(img, mimetype='image/png')
	return render_template('shotchart.html', plot_url=plot_data)


if __name__ == "__main__":
	app.config['SECRET_KEY'] = 'super secret key'
	app.run(debug=True)
