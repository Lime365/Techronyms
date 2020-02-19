import sqlite3
import os
import sys
import random

# Set up a connection and cursor to our database. #
database = r"C:/Users/Lime/pyProjects/tech_abs_quiz/abbs.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()
# Fetch list with acronyms #
cursor.execute(
'''SELECT abb FROM abbs'''
)
ls = (acr[0] for acr in cursor.fetchall())
print(list(ls))

#An admin pass for playing the game and modify
#the sqlite3 database at the same time
admin_pass = 'admin'
print('Welcome to Tech Abs! \n')
def main_menu():
    try:
        choice = int(input("Make a selection:\n[1] New Game \n[2] Scoreboard \n[3] Rules \n[4] Admin mode \n[5] Exit\n"))
    except:
        print('InVaLiD iNpUt \n')
        main_menu()

    if choice == 1: #---------------- Start Game ------------#
        pass
    elif choice == 2: #-------------SCOREBOARD---------------#
        cursor.execute('''
        SELECT nick, score, date FROM scoreboard ORDER BY score DESC LIMIT 10;
        ''')
        print('    PLAYER   SCORE    DATE')
        #WHO NEEDS PRETTYPRINTING ANYWAYS?!
        for pos, player in enumerate(cursor.fetchall()):
            if pos <= 8:
                print(
                str(pos+1)+(" "*3) +
                player[0]+(" "*(10-len(str(player[0]))))+
                str(player[1])+(" "*(6-len(str(player[1]))))+
                player[2]
                )
            elif pos == 9:
                print(
                str(pos+1)+(" "*2) +
                player[0]+(" "*(10-len(str(player[0]))))+
                str(player[1])+(" "*(6-len(str(player[1]))))+
                player[2]
                )
        print('\n\n')
        main_menu()
    elif choice == 3: #----------------RULES-----------------#
        print("""On your screen you will ge given an acronym used within the tech world. \n
                    You score points by guessing them correctly, and loose after 3 incorrect guesses. \n
                    Capitalization does not matter, but spacing does! \n
                    Good luck. \n""")
        main_menu()
    elif choice == 4: #--------------------ADMIN MODE----------------#
                      #With admin mode activated you can modify an acronym's rating
                      #or delete it after encountering it.
        pw = string(input('Enter Password: '))
        if pw == admin_pass:
            #admin mode == True
            pass
        else:
            print('Incorrect password.')
            main_menu()
    elif choice == 5: #----------------EXIT GAME-----------------#
        conn.close()
        sys.exit()
    else:
        print('iNvAlId iNpUt\n')
        main_menu()


#def get_acronym():


if __name__ == '__main__':
    main_menu()
