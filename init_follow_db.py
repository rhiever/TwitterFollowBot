# Copyright 2014 Sebastian Raschka

import sqlite3

def create_blank_db(db_file):
    """ Creates a new SQLite database with one field as primary key 
    Args:
        db_file (str): file name for the new database
    Returns the total number of changes made to the data base.

    """ 
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('CREATE TABLE twitter_db (user_id TEXT PRIMARY KEY)')
    # TEXT because some IDs have trailing 0s
    changes = conn.total_changes 
    conn.commit()
    conn.close()
    return changes
    
def add_existing_ids(db_file, text_file):
    """ Adds IDs from a 1-col text file to existing database. 
        Entries must be unique! 
    Args:
        text_file (str): name of the input 1-col text file
        db_file (str): file name for of the SQLite database
    Returns the total number of changes made to the data base.

    """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    with open(text_file, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            c.execute('INSERT INTO twitter_db (user_id) VALUES ("%s")' %line)
    changes = conn.total_changes 
    conn.commit()
    conn.close()
    return changes


if __name__ == '__main__':
    create_blank_db('./follow_db.sqlite')
    #add_existing_ids('./follow_db.sqlite', './already_followed.txt')
