from flask import render_template, request
import requests
from .forms import LoginForm
from app import app

# ROUTES
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/students', methods = ['GET'])
def students():
    my_students = ['Scarlett', 'Aydee', 'Patrick', 'Armani', 'Jalen']
                                                # var_name in Jinja = var name in python
    return render_template('students.html.j2', students = my_students)


@app.route('/ergast', methods=['GET','POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        round = request.form.get('round')

        url =  f'https://ergast.com/api/f1/{year}/{round}/driverStandings.json'
        response = requests.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('ergast.html.j2', error=error_string)

        if not response.json()["MRData"]["StandingsTable"]["StandingsLists"]:
            error_string = "We had an error loading your data most likely because the year/round combo is not in the database"
            return render_template('ergast.html.j2', error=error_string)

        data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        new_data = []
        for racer in data:
            racer_dict={}
            racer_dict={
                "last_name":racer['Driver']['familyName'],
                "first_name":racer['Driver']['givenName'],
                "position":racer['position'],
                "wins":racer['wins'],
                "DOB":racer['Driver']['dateOfBirth'],
                "nationality":racer['Driver']['nationality'],
                "constructor":racer['Constructors'][0]['name']
            }
            new_data.append(racer_dict)
        
        return render_template('pokemon.html.j2', racers=new_data)


    return render_template('pokemon.html.j2')

@app.route('/pokemon', methods = ['GET', 'POST'])

def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')

        url =f"https://pokeapi.co/api/v2/pokemon/{name}"
        response =requests.get(url)
        
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokemon.html.j2', error=error_string)

        if not response.json():
            error_string = "We had an error loading your data most likely because the year/round combo is not in the database"
            return render_template('pokemon.html.j2', error=error_string)
        new_data=[]
        pokemon = response.json()  
        character_dict={
            'p_name':pokemon['name'],
            'ability_name':pokemon['abilities'][0]['ability']['name'],
            'base_experience':pokemon['base_experience'],
            'sprite_url':pokemon['sprites']['back_default'],
            'attack_stat':pokemon['stats'][1]['base_stat'],
            'hp_power':pokemon['stats'][0]['base_stat'],
            'defense':pokemon['stats'][2]['base_stat']
    }
        new_data.append(character_dict)
      
        return render_template('pokemon.html.j2', racers=new_data)
    return render_template('pokemon.html.j2')

if __name__ == '_main_':
    app.run(debug=True)