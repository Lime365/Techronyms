'''
2020-02-X
1. Found a website to scrape for acronyms.
2. Set up a sqlite3 database.
3. Wrote a script to scrape the website and add the acronyms and answers to two
   different .txt files. From there i zipped them in a for loope and added them to
   the sqlite3 database. In hindsight it's probably possible to scrape it directly into sqlite.
   This was my first time webscraping and using an SQL database.

   One thing that bothers me is that the website had special utf-8 characters(some wierd box)
   as their "rating". And therefore i got thrown encoding errors. Even with using the correct
   encoder it was hard to get around. Managed to scrape the rest of the info but unfortunately
   not the rating. Will probably add some kind of admin mode to the game where you can adjust the
   rating after you encounter the acronym whilst playing.

   All in all learned a ton about using beautifulsoup to parse HTML, navigate tags
   and also some SQL.

2020-02-X
Started setting up the main menu of the game.
Wasn't to hard but learned how to fetch info from the Sqlite3 database and
effectively converting them to python objects.
The idea is to pull a random acronym from the database, match it with user input,
if correct they score and if they don't they loose a life (start with 3?).


2020-02-17
Finished making scoreboard.
Getting the columns to line up was a challenge.

'''
