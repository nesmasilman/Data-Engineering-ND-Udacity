# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL NOT NULL, start_time timestamp NOT NULL,\
                            user_id int references users(user_id), level varchar NOT NULL, song_id varchar references songs(song_id),\
                                 artist_id varchar references artists(artist_id), session_id int NOT NULL, location varchar NOT NULL,\
                                     user_agent varchar);""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int NOT NULL UNIQUE, first_name varchar, last_name varchar, gender varchar,\
                                                        level varchar, primary key(user_id));""")
                                                          

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar NOT NULL UNIQUE, title varchar NOT NULL, artist_id varchar NOT NULL,\
                                                        year int NOT NULL,duration int NOT NULL, primary key(song_id));""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar NOT NULL UNIQUE, name varchar NOT NULL,  location varchar NOT NULL,\
                                                        latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, primary key(artist_id));""")
                                                           
time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp NOT NULL UNIQUE, hour int NOT NULL, day int NOT NULL, week int NOT NULL,\
                                        month int NOT NULL, year int NOT NULL, weekday varchar NOT NULL, primary key(start_time));""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id,session_id,\
                            location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender,level) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET user_id = EXCLUDED.user_id;""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) DO UPDATE SET song_id = EXCLUDED.song_id;""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (artist_id) DO UPDATE SET artist_id = EXCLUDED.artist_id;""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""SELECT df.song_id, df.artist_id FROM df JOIN df_ns ON df.title = df_ns.song
                        AND df.artist_name = df_ns.artist
                        AND df.duration = df_ns.length;""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]