# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# TODO: add foreign keys

# CREATE TABLES
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                            (songplay_id int, start_time bigint, user_id int, level varchar, song_id varchar, 
                            artist_id varchar, session_id int, location varchar, user_agent varchar,
                            PRIMARY KEY (songplay_id))
                            """)

user_table_create = ("""CREATE TABLE users 
                        (user_id int, first_name varchar, last_name varchar, gender varchar, level varchar,
                        PRIMARY KEY (user_id, level))""")

song_table_create = ("""CREATE TABLE songs 
                        (song_id varchar, title varchar, artist_id varchar, year int, duration float,
                        PRIMARY KEY (song_id))""")

artist_table_create = ("""CREATE TABLE artists 
                        (artist_id varchar, name varchar, location varchar, latitude float, longitude float,
                        PRIMARY KEY (artist_id))""")

time_table_create = ("""CREATE TABLE time 
                        (start_time bigint, hour int, day int, week int, month int, year int, weekday int)""")

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create,
                        time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
