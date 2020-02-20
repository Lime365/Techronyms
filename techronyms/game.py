import sqlite3
import os
import sys
import random
from datetime import date

# Set up a connection and cursor to our database. #
database = r"C:/Users/Lime/pyProjects/techronyms/acronyms.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

#An admin pass for playing the game and modify
#the sqlite3 database at the same time
#Also adds a cheat button.
admin_pass = 'admin'
admin = False


#-------- Setting up some basic functions ------------#

def get_acronym(acr_ls): #Pop an entry from the list
    fetch = acr_ls.pop(random.randint(1,len(acr_ls)))
    acr = fetch[0]
    answer = fetch[1]
    return acr, answer

def upload_score(user, score):
    cursor.execute('''INSERT INTO scoreboard (nick, score, date) VALUES (?,?,?)''',
    (user, score, date.today())
    )
    conn.commit()

def check_lives(hp):
    if hp == 0:
        return True

def check_win(score, max_score):
    if score == max_score:
        return True


print('\n'*30+'Welcome to Techronyms! \n')

game_on = False
def main_menu():
    try:
        choice = int(input("Make a selection:\n\n[1] New Game \n[2] Scoreboard \n[3] Rules \n[4] Admin mode \n[5] Exit\n\n\n"))
    except:
        print('\n InVaLiD iNpUt \n')
        main_menu()

    if choice == 1: #---------------- Start Game ------------#

        game(True)

    elif choice == 2: #-------------SCOREBOARD---------------#
        cursor.execute('''
        SELECT nick, score, date FROM scoreboard ORDER BY score DESC LIMIT 10;
        ''')
        print('     PLAYER   SCORE        DATE')
        #WHO NEEDS PRETTYPRINTING ANYWAYS?!
        for pos, player in enumerate(cursor.fetchall()):
            if pos <= 8:
                print(
                str(pos+1)+(" "*3) +
                player[0]+(" "*(10-len(str(player[0]))))+
                str(player[1])+(" "*(10-len(str(player[1]))))+
                player[2]
                )
            elif pos == 9:
                print(
                str(pos+1)+(" "*2) +
                player[0]+(" "*(10-len(str(player[0]))))+
                str(player[1])+(" "*(10-len(str(player[1]))))+
                player[2]
                )
        print('\n\n')
        main_menu()
    elif choice == 3: #----------------RULES-----------------#
        print("""On your screen you will ge given an acronym used within the tech world. \n
                Score points by guessing them correctly, and loose after 3 incorrect guesses. \n
                Capitalization does not matter, but spacing does! \n
                Good luck. \n""")
        main_menu()
    elif choice == 4: #--------------------ADMIN MODE----------------#
    #If admin == True the user can modify the answer or rating of an entry while playing
        if admin == True:
            print('Admin mode: Off')
            admin == False
            main_menu()
        else:
            pw = str(input('Password: '))
            if pw == admin_pass:
                admin == True
                print('\nAdmin mode: On\n')
                main_menu()
            else:
                print('\nIncorrect password\n')
                main_menu()
    elif choice == 5: #----------------EXIT GAME-----------------#
        conn.close()
        sys.exit()
    else:
        print('iNvAlId iNpUt\n')
        main_menu()


#--------------- The Game -------------- #

def game(play):
    cursor.execute('''SELECT abb, answer FROM acronyms''') #Query sqlite3 to give us the acronyms and answers
    acr_ls = [acr for acr in cursor.fetchall()] #Store them as tuple pairs in a list
    acr_count = len(acr_ls) #Max score
    score = 0
    lives = 3
    while play:
        #Print out the acronym and prompt the user for a guess
        print('\n\nScore: {}/{}\nLives: {}\n\n\n'.format(score, acr_count, lives))
        acronym, answer = get_acronym(acr_ls)
        print(f'\t{acronym}')
        guess = str(input('Answer: '))

        if guess.lower() == answer.lower():
            score += 1
            print('Correct!')
            if check_win(score, acr_count):
                print('''Wow, congratulations, rest easy that you inofficially have no life.
                            Bask in the glory of knowing most men are inferior to your supreme
                            knowledge. \n\n''')
                nick = str(input('Nickname: '))
                upload_score(nick, score)
                print("""\nThank you for playing! Check the scoreboard to see if you made the cut!
                Haha kidding. Ofc you did...\n""")
                break



        else:
            lives -= 1
            if check_lives(lives):
                print('Game over!\n')
                print(f'The answer was: {answer} \n\n')
                nick = str(input('Nickname: '))
                print('\nThank you for playing! Check the scoreboard to see if you made the cut!')
                break
            else:
                print('Wrong!')
                print(f'The answer was: {answer} \n\n')

    main_menu()


main_menu()
