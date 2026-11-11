""" A simple movie database application """

from flask import Flask, redirect, render_template, request, session, url_for
import movies_sqlite as db

app = Flask(__name__) 


@app.route('/')
def index():
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies ORDER BY release_date DESC LIMIT 5;"
    rows = db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('index.html', rows=rows)

@app.route('/movies')
def movies():
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    query = "SELECT * FROM movies ORDER BY release_date DESC;"
    rows = db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('movies.html', rows=rows)

@app.route('/movie_detail/<int:movie_id>')
def movie_detail(movie_id):
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    # Query to get the movie details
    query = f"SELECT * FROM movies WHERE movies.id = {movie_id};"
    rows = db.retrieve_data_with_query(conn, query)

    # Stars query to get the stars associated with the movie
    query_stars = f"SELECT stars.*, connections.role FROM stars,movies,connections WHERE connections.movie_id = {movie_id} AND connections.star_id = stars.id AND connections.movie_id = movies.id;"
    stars = db.retrieve_data_with_query(conn, query_stars)
    #print(f"Retrieved rows: {stars}")  # Debugging line
    db.close_database(conn)
    return render_template('movie_detail.html', rows=rows, stars=stars)

""" TODO: Add a route to display the list of stars and their details. 
    We hace to create a new template stars.html and star_detail.html to display the list of stars and their details.
    The route should be /stars and /star_detail/<int:star_id> respectively."""
    
@app.route('/stars')
def stars():
    """ Route to display the list of stars """
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    query = "SELECT * FROM stars ORDER BY stage_name DESC;"
    rows = db.retrieve_data_with_query(conn, query)
    db.close_database(conn)
    return render_template('stars.html', rows=rows)

@app.route('/star_detail/<int:star_id>')
def star_detail(star_id):
    """ Route to display the details of a star """
    db_path = 'movies.db'
    conn = db.open_database(db_path)
    # Query to get the star details
    query = f"SELECT * FROM stars WHERE stars.id = {star_id};"
    rows = db.retrieve_data_with_query(conn, query)

    # Movies query to get the movies associated with the star
    query_movies = f"SELECT movies.*, connections.role FROM stars,movies,connections WHERE connections.star_id = {star_id} AND connections.movie_id = movies.id AND connections.star_id = stars.id;"
    related_movies = db.retrieve_data_with_query(conn, query_movies)
    db.close_database(conn)
    #print(related_movies)  # Debugging line
    return render_template('star_detail.html', rows=rows, movies=related_movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Route to handle user login """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid_user = db.user_login(db.open_database('movies.db'), username, password)
        if valid_user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True) 
