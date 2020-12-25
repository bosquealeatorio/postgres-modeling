# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# songplays - records in log data associated with song plays i.e. records with page NextSong
# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""CREATE TABLE songplays (songplay_id int, start_time bigint, user_id int, 
                            level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar,
                            PRIMARY KEY (songplay_id))""")

# users - users in the app
# user_id, first_name, last_name, gender, level
user_table_create = ("""CREATE TABLE users (user_id int, first_name varchar, last_name varchar, gender varchar, level varchar,
                        PRIMARY KEY (user_id))
""")

# songs - songs in music database
# song_id, title, artist_id, year, duration
song_table_create = ("""CREATE TABLE songs (song_id varchar, title varchar, artist_id varchar, year int, duration float,
                        PRIMARY KEY (song_id))""")


# artists - artists in music database
# artist_id, name, location, latitude, longitude
artist_table_create = ("""CREATE TABLE artists (artist_id varchar, name varchar, location varchar, latitude float, longitude float,
                        PRIMARY KEY (artist_id))""")

# time - timestamps of records in songplays broken down into specific units
# start_time, hour, day, week, month, year, weekday
time_table_create = ("""CREATE TABLE time (start_time bigint, hour int, day int, week int, month int, year int, weekday int)""")

# FIND SONGS
# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.
song_select = ("""SELECT song_id, songs.artist_id 
                    FROM songs 
                    LEFT JOIN artists on songs.artist_id = artists.artist_id 
                    WHERE title = %s and name = %s and duration = %s""")

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
