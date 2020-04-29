from flask import Flask, render_template
import random
import pandas as pd
from string import Template

url = "/Users/ayushi/Downloads/title.basics.tsv"

load_all = True # make it False to load faster
load_all = False
if load_all:
    # let df itself be df_ten, if we are loading all anyways
    df_ten = pd.read_csv(url, sep='\t', dtype='unicode')
else:
    if False: # we can avoid creating df so it loads even faster
        df = pd.read_csv(url, sep='\t', dtype='unicode')
        df_ten = df.head(10)
    else:
        df_ten = pd.read_csv(url, sep='\t', dtype='unicode').head(10)
    
df_genres = df_ten['genres'].str.get_dummies(sep=',')
df_new = pd.concat([df_ten, df_genres], axis=1)

is_excited = lambda genres: 'Action' in genres or 'Adventure' in genres or 'Thriller' in genres or 'Mystery' in genres or 'Sport' in genres 
is_scared = lambda genres: 'Horror' in genres
is_humored = lambda genres: 'Comedy' in genres
is_educated = lambda genres: 'Documentary' in genres or 'Biography' in genres or 'History' in genres
is_romanced = lambda genres: 'Romance' in genres
is_young = lambda genres: ('Adult' not in genres) and ('Animation' in genres or 'Short' in genres or 'Comedy' in genres)
is_explorative = lambda genres: 'Fantasy' in genres or 'Sci-Fi' in genres or 'War' in genres

def label_moods_lambda(df):
    for index, row in df.iterrows():
        if is_excited(row['genres']): 
            df.at[index, 'mood'] = "Excited"
        elif is_scared(row['genres']):
            df.at[index, 'mood'] = "Scared"
        elif is_humored(row['genres']):
            df.at[index, 'mood'] = "Humored"
        elif is_educated(row['genres']):
            df.at[index, 'mood'] = "Educated"
        elif is_romanced(row['genres']):
            df.at[index, 'mood'] = "Romanced"
        elif is_young(row['genres']):
            df.at[index, 'mood'] = "Young"
        elif is_explorative(row['genres']):
            df.at[index, 'mood'] = "Explorative"
        else:
            df.at[index, 'mood'] = "Unknown"

label_moods_lambda(df_ten)

def random_movie_with_mood(mood):
    entries = df_ten[df_ten['mood'].str.lower() == mood.lower()]
    titles = list(entries.primaryTitle)
    if not titles:
        return "Could not find any title matching mood %s" % (mood)
    return random.choice(titles)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mood.html')
def mood():
    return render_template('mood.html', mood="excited")

@app.route('/<some_mood>')
def some_mood_page(some_mood):
    print(some_mood)
    show = random_movie_with_mood(some_mood)
    return render_template('mood.html', mood=some_mood, show=show)

if __name__ == "__main__":
    app.run(debug=True)
