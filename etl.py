import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
        
    """Takes in a Postgesql cursor and a filepath to files in the "song_data" folder, and inserts the data of files     
    into the corresponding tables using the insert commands prepared in the "sql_queries.py" file

    Keyword arguments:
    cur -- Postgesql cursor
    filepath -- filepath to "song_data" files required for analysis
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df2 = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]

    # insert song record
    song_data = list(df2)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    df3 = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].replace({pd.np.nan: 0})
    artist_data = list(df3.values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """Takes in a Postgesql cursor and a filepath to files in the "log_data" folder, and inserts the data of files     
    into the corresponding tables using the insert commands prepared in the "sql_queries.py" file

    Keyword arguments:
    cur -- Postgesql cursor
    filepath -- filepath to "log_data" files required for analysis
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    df['timestamp']=t
    df['hour']=t.dt.hour
    df['day']=t.dt.day
    df['week of year']=t.dt.weekofyear
    df['month']=t.dt.month
    df['year']=t.dt.year
    df['weekday']=t.dt.weekday
    df4=df[['timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday']]
    time_data = list(df4.values[0])
    column_labels = df4.columns
    time_df = df4

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data =(pd.to_datetime(row.timestamp, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    
    """Takes in a Postgesql cursor, connection, a filepath in our data folders, and a function of the 2 functions created above     
    and runs the function on each of the files in the filepaths.
    
    Keyword arguments:
    cur -- Postgesql cursor
    conn  -- Postgesql connection
    filepath -- filepath to files in our "data" folder
    function -- a pre-defined function of the 2 created above.
    
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
        
    """Connects to our "sparkify" database and uses the function defined above "process_data" to process the data
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()