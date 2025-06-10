import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI usage
import matplotlib.pyplot as plt
import pandas as pd
import os

# Ensure static folder exists for plots
static_dir = 'static'
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

def plot_medals_by_country(df):
    medals_by_country = df['Country'].value_counts()
    plt.figure(figsize=(10,6))
    medals_by_country.head(10).plot(kind='bar', color='deepskyblue')
    plt.title('Top 10 Countries by Medal Count')
    plt.xlabel('Country')
    plt.ylabel('Medal Count')
    plt.tight_layout()
    plt.savefig(os.path.join(static_dir, 'medals_by_country.png'))
    plt.close()

def plot_medals_by_player(df):
    # Count medals by player
    if 'Athlete' not in df.columns:
        raise ValueError("Column 'Athlete' not in dataframe")
    medals_by_player = df['Athlete'].value_counts()
    plt.figure(figsize=(10,6))
    medals_by_player.head(10).plot(kind='bar', color='coral')
    plt.title('Top 10 Athletes by Medal Count')
    plt.xlabel('Athlete')
    plt.ylabel('Medal Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(static_dir, 'medals_by_player.png'))
    plt.close()

def plot_medals_by_year(df):
    medals_by_year = df['Year'].value_counts().sort_index()
    plt.figure(figsize=(12,6))
    medals_by_year.plot(kind='line', marker='o', color='mediumseagreen')
    plt.title('Total Medals Awarded Each Year')
    plt.xlabel('Year')
    plt.ylabel('Medal Count')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(static_dir, 'medals_by_year.png'))
    plt.close()

def plot_medals_by_country_year(df):
    # Create pivot table: country by year medal count
    pivot = df.pivot_table(index='Year', columns='Country', values='Medal', aggfunc='count', fill_value=0)

    # For simplicity, plot top 5 countries with most total medals
    top_countries = df['Country'].value_counts().head(5).index.tolist()

    plt.figure(figsize=(12,7))
    for country in top_countries:
        if country in pivot.columns:
            plt.plot(pivot.index, pivot[country], marker='o', label=country)

    plt.title('Medals by Top 5 Countries across Years')
    plt.xlabel('Year')
    plt.ylabel('Medal Count')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(static_dir, 'medals_by_country_year.png'))
    plt.close()

def filter_data_and_plot(df: pd.DataFrame, filters: dict):
    filtered_df = df.copy()
    filtered_df.columns = filtered_df.columns.str.strip()

    for col in ['Athlete', 'Country', 'Year', 'Medal']:
        if col not in filtered_df.columns:
            raise ValueError(f"Expected column '{col}' not found")

    if 'player' in filters and filters['player'].strip():
        val = filters['player'].strip().lower()
        filtered_df = filtered_df[filtered_df['Athlete'].str.lower().str.contains(val, na=False)]

    if 'country' in filters and filters['country'].strip():
        val = filters['country'].strip().lower()
        filtered_df = filtered_df[filtered_df['Country'].str.lower().str.contains(val, na=False)]

    if 'year' in filters and filters['year'].strip():
        try:
            year_int = int(filters['year'].strip())
            filtered_df = filtered_df[filtered_df['Year'] == year_int]
        except ValueError:
            pass

    if 'medal' in filters and filters['medal'].strip():
        val = filters['medal'].strip().lower()
        filtered_df = filtered_df[filtered_df['Medal'].str.lower().str.contains(val, na=False)]

    print(f"Filter result count: {len(filtered_df)}")

    if not filtered_df.empty:
        plot_medals_by_country(filtered_df)
        plot_medals_by_player(filtered_df)
        plot_medals_by_year(filtered_df)
        plot_medals_by_country_year(filtered_df)
    else:
        for fname in ['medals_by_country.png','medals_by_player.png','medals_by_year.png','medals_by_country_year.png']:
            filepath = os.path.join(static_dir, fname)
            plt.figure(figsize=(8,6))
            plt.text(0.5,0.5,'No data available for this filter', horizontalalignment='center', verticalalignment='center', fontsize=16)
            plt.axis('off')
            plt.savefig(filepath)
            plt.close()


