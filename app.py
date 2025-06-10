from flask import Flask, render_template, request
import pandas as pd
from data_analysis import filter_data_and_plot

app = Flask(__name__)

# Load the dataset once globally
df = pd.read_csv(r'C:\Users\nandi\olympics_data_analysis\olympics_data.csv')

# Extract unique player names and countries
unique_players = df['Athlete'].unique().tolist()
unique_countries = df['Country'].unique().tolist()

@app.route('/', methods=['GET', 'POST'])
def home():
    filters = {
        'player': '',
        'country': '',
        'year': '',
        'medal': ''
    }
    if request.method == 'POST':
        filters['player'] = request.form.get('player', '').strip()
        filters['country'] = request.form.get('country', '').strip()
        filters['year'] = request.form.get('year', '').strip()
        filters['medal'] = request.form.get('medal', '').strip()

    active_filters = {k: v for k, v in filters.items() if v}
    filter_data_and_plot(df, active_filters)

    return render_template('index.html', filters=filters, players=unique_players, countries=unique_countries)

if __name__ == '__main__':
    app.run(debug=True)
