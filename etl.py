import os
import glob
import psycopg2
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def get_files(filepath):
    """
    return a list with all json files on the filepath folder
    
    params
    filepath: path of parent folder
    """

    all_files = []

    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files


def insert_df_to_table(df, temp_file, connection, table_name):
    """
    insert a dataframe into a postgres table
    
    params
    df: dataframe with data
    temp_file: local path to checkpoint the dataframe
    connection: connection object to the database
    table_name: table to insert the data
        
    based on the implementation of Naysan Saran
    https://naysan.ca/2020/06/21/pandas-to-postgresql-using-psycopg2-copy_from/
    """

    # using a string to flag null values (numpy NaNs throw errors when copying)
    df = df.fillna('NULL')

    # save values to temp file
    df.to_csv(temp_file, header=False, index=False, sep='\t')

    # load temp file
    file = open(temp_file, 'r')

    # getting the cursor
    cursor = connection.cursor()

    try:

        # copy data from file to postgres table
        cursor.copy_from(file, table_name, sep='\t', null='NULL')

    except (Exception, psycopg2.DatabaseError) as error:

        # print error if completed
        print(f"Error({table_name}): %s" % error)

        # remove temp file, rollback and close cursor
        os.remove(temp_file)
        connection.rollback()
        cursor.close()

        return None

    # print message if completed
    print(f"copy_from_file({table_name}) done")

    # remove temp file and close cursor
    cursor.close()
    os.remove(temp_file)

    return 1


def process_song_files(connection, filepath):
    """
    insert into the postgres tables the data from songs filepath

    params
    connection: connection object to postgres
    filepath: parent folder of json files
    """

    # get all files in filepath
    all_files = get_files(filepath)

    # report files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # concat all files into one dataframe
    df = pd.concat([pd.read_json(file, lines=True) for file in all_files])

    song_data = df.get(['song_id', 'title', 'artist_id', 'year', 'duration'])
    insert_df_to_table(song_data, 'tables/songs.csv', connection, 'songs')

    artist_data = df.get(['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude'])
    artist_data = artist_data.drop_duplicates()
    insert_df_to_table(artist_data, 'tables/artists.csv', connection, 'artists')


def process_log_files(connection, filepath):
    """
    insert into the postgres tables the data from logs filepath

    params
    connection: connection object to postgres
    filepath: parent folder of json files
    """

    # get all files in filepath
    all_files = get_files(filepath)

    # report files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # concat all files into one dataframe
    df = pd.concat([pd.read_json(file, lines=True) for file in all_files])
    df = df.query("page == 'NextSong'")

    # prepare time data for table
    t = pd.to_datetime(df['ts'])
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.isocalendar()['week'], t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame({col: values for col, values in zip(column_labels, time_data)})
    # insert time table data
    insert_df_to_table(time_df, 'tables/time.csv', connection, 'time')

    # load user table
    user_df = df.get(['userId', 'firstName', 'lastName', 'gender', 'level'])
    user_df['userId'] = user_df['userId'].astype(int)
    user_df = user_df.drop_duplicates(['userId', 'level'])
    # insert users table data
    insert_df_to_table(user_df, 'tables/users.csv', connection, 'users')

    # prepare songplays data
    artists = pd.read_sql('select * from artists', connection)
    songs = pd.read_sql('select * from songs', connection)
    full_songs = pd.merge(songs, artists, on='artist_id').get(['song_id', 'artist_id', 'title', 'name', 'duration'])

    songplays = pd.merge(df, full_songs, left_on=['song', 'artist', 'length'], right_on=['title', 'name', 'duration'], how='left')
    songplays = songplays.reset_index()
    songplays_data = songplays.get(
        ['index', 'ts', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent'])

    # insert songplays into fact table
    insert_df_to_table(songplays_data, 'tables/songplays.csv', connection, 'songplays')


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)

    process_song_files(connection=conn, filepath='data/song_data')
    process_log_files(connection=conn, filepath='data/log_data')

    conn.close()


if __name__ == "__main__":
    main()
