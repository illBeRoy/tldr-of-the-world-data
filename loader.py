import sqlite3


if __name__ == '__main__':
    path = 'pantheon.sqlite'

    conn = sqlite3.connect(path)
    conn.execute('CREATE TABLE people (name VARCHAR(80), )')
    conn.execute(
        'CREATE TABLE pair_p (movie_id_1 INT, movie_id_2 INT, cost FLOAT, PRIMARY KEY (movie_id_1, movie_id_2))')
    conn.commit()
