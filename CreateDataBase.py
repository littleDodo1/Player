import sqlite3


def create():
    connection = sqlite3.connect('Likedbd.sqlite')
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Liked(
						"title" TEXT 
          			)"""
    )

    connection.commit()
    connection.close()
