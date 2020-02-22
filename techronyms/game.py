import sqlite3
import os
import sys
import random
from datetime import date

# Set up a connection and cursor to our database. #
database = r"C:/Users/Emil Lilja/github/Techronyms/techronyms/acronyms.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

admin_pass = 'admin'

#-------- Setting up some functions ------------#

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

def fetch_scoreboard():
    cursor.execute('''
    SELECT nick, score, date FROM scoreboard ORDER BY score DESC LIMIT 10;
    ''')
    print('\n\n')
    print('            SCOREBOARD          ')
    print('____________________________________')
    print('    PLAYER    SCORE        DATE\n')
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
    print('____________________________________')
    print('\n\n')

#-------- Admin Functions ------------#

def fetch_difficulty(acronym):
    cursor.execute('''
    SELECT difficulty FROM acronyms WHERE abb = ?
    ''', (acronym, ))
    return cursor.fetchone()[0]

def update_difficulty(acronym, new_diff):
    cursor.execute(
    ''' UPDATE acronyms SET difficulty = ? WHERE abb = ? ''', (new_diff, acronym)
    )
    conn.commit()
    print('Difficulty successfully updated')

def new_entry(entry):

    try:
        new_acr, answer, diff = entry.split(',') #Split the input and remove whitespace incase of user error
    except ValueError:
        return 'Invalid amount of values. Make sure to follow the format\n'

    #Remove whitespace
    new_acr = new_acr.replace(' ', '').upper()
    answer = answer.strip()
    diff = diff.replace(' ','')

    q = (new_acr, answer, diff, date.today())

    try:
        if 0 < int(diff) < 11:
            pass
        else:
            return 'Invalid input. Difficulty must be int between 0-10\n'
    except:
        return 'Invalid input. Difficulty must be int between 0-10\n'

    cursor.execute('''
    SELECT abb FROM acronyms;
    ''')
    acronyms = [acr[0] for acr in cursor.fetchall()]
    if new_acr.upper() in acronyms: #Check for duplicates
        return 'Duplicate entry detected\n'
    else: #Looks good, add the entry
        cursor.execute('''
        INSERT INTO acronyms (abb, answer, difficulty, date_added)
        VALUES (?, ?, ?, ?);
        ''', q)
        conn.commit()
        return 'Entry successfully added\n'

def delete_entry(entry):

    cursor.execute('''
    SELECT abb from acronyms;
    ''')
    acronyms = [acr[0] for acr in cursor.fetchall()]
    if entry.upper() in acronyms:
        cursor.execute('''
        DELETE FROM acronyms WHERE abb=?
        ''', (entry.upper(),) )
        conn.commit()
        print('\nEntry successfully deleted\n')
    else:
        print('\nNo matching entry found\n')

def fetch_database():
    print('\n\n')
    cursor.execute('''
    SELECT * FROM acronyms;
    ''')
    for row in cursor.fetchall():
        id = str(row[0])
        acr = row[1]
        answer = row[2]
        diff = str(row[3])
        date = row[4]

        print(
        id + " "*(5-len(id)) +
        acr + " "*(15-len(acr)) +
        answer + " "*(70-len(answer)) +
        diff + " "*(5-len(diff)) +
        date
        )


print('\n'*40+'Welcome to Techronyms! \n')

def main_menu(admin=False):
    try:
        if admin == True:
            choice = int(input("\nAdmin Mode: On\n\n[1] New Game \n[2] Scoreboard \n[3] Commands \n[4] Turn Off Admin Mode \n[5] Exit \n\n[6] New Entry\n[7] Delete Entry\n[8] Database\n\n"))
        else:
            choice = int(input("\nMake a selection:\n\n[1] New Game \n[2] Scoreboard \n[3] Rules \n[4] Admin mode \n[5] Exit\n\n\n"))
    except:
        print('\n Invalid input \n')
        if admin == True:
            main_menu(admin=True)
        else:
            main_menu()

    if choice == 1: #---------------- Start Game ------------#
        if admin == True:
            admin_game(True)
        else:
            game(True)

    elif choice == 2: #-------------SCOREBOARD---------------#
        fetch_scoreboard()
        if admin == True:
            main_menu(admin=True)
        else:
            main_menu()
    elif choice == 3: #----------------RULES-----------------#
        if admin == True:
            print('''\nr = Reveal answer \nset_diff = set a new difficulty \npass = input correct answer\nhelp = print commands\nquit/exit = terminate session''')
            main_menu(admin=True)
        else:
            print("""On your screen you will ge given an acronym used within the tech world. \n
                    Score points by guessing them correctly, and loose after 3 incorrect guesses. \n
                    Capitalization does not matter, but spacing does! \n
                    Good luck. \n""")
            main_menu()
    elif choice == 4: #--------------------ADMIN MODE----------------#
        if admin == True:
            print('\nAdmin mode: Off\n')
            main_menu()
        else:
            pw = str(input('Password: '))
            if pw == admin_pass:
                main_menu(True)
            else:
                print('\nIncorrect password\n')
                main_menu()
    elif choice == 5: #----------------EXIT GAME-----------------#
        conn.close()
        sys.exit()
    elif choice == 6 and admin == True: #----------- NEW ENTRY ----------#
        while True:
            print('''\nEnter in following format (without quotation marks):\n"acronym, answer, difficulty"\nEnter 'c' to cancel\n''')
            entry = str(input(''))
            if entry == 'c':
                break
            else:
                print(new_entry(entry))

            entry = str(input('Add another entry? Y / N : ' ))
            if entry.lower() == 'y' or entry.lower() == 'yes':
                pass
            else:
                break
        main_menu(admin=True)
    elif choice == 7 and admin == True: #------------ DELETE ENTRY ---------#
        del_entry = str(input('Enter acronym to delete: '))
        delete_entry(del_entry)
        main_menu(admin=True)
    elif choice == 8 and admin == True: #------------- DATABASE ----------#
        fetch_database()
        main_menu(admin=True)

    else:
        print('\n Invalid input \n')
        if admin == True:
            main_menu(admin=True)
        else:
            main_menu()


#--------------- The Game -------------- #

def game(play):

    cursor.execute('''SELECT abb, answer FROM acronyms''') #Query sqlite3 to give us the acronyms and answers
    acr_ls = [acr for acr in cursor.fetchall()] #Store them as tuple pairs in a list
    acr_count = len(acr_ls) #Max score
    score = 0
    lives = 3



    while play:

        if check_lives(lives):
            fetch_scoreboard()
            print('\nGame over!\n')
            print(f'The answer was: {answer} \n\n')
            nick = str(input('Nickname: '))
            if nick == 'c':
                break
            upload_score(nick, score)
            print('\nThank you for playing!')
            break

        if check_win(score, acr_count):
            fetch_scoreboard()
            print('\nCongratulations, you beat the game! \n')
            nick = str(input('Nickname: '))
            upload_score(nick, score)
            print("""\nThank you for playing!\n""")
            break

        #Print out the acronym and prompt the user for a guess
        print('\n\nScore: {}/{}\nLives: {}\n\n\n'.format(score, acr_count, lives))
        acronym, answer = get_acronym(acr_ls)
        print(f'\t{acronym}')
        guess = str(input('Answer: '))

        if guess == 'quit' or guess == 'exit':
            break

        if guess.lower() == answer.lower(): # Correct answer #
            score += 1
            print('Correct!')

        else: # Incorrect anwer #
            lives -= 1
            print('Wrong!')
            print(f'The answer was: {answer} \n\n')

    main_menu()

def admin_game(play):

    cursor.execute('''SELECT abb, answer FROM acronyms''') #Query sqlite3 to give us the acronyms and answers
    acr_ls = [acr for acr in cursor.fetchall()] #Store them as tuple pairs in a list
    acr_count = len(acr_ls) #Max score
    score = 0
    lives = 3

    while play:

        if check_win(score, acr_count):
            fetch_scoreboard()
            print('\nCongratulations, you beat the game! ')
            nick = str(input('Nickname: ')) + ' (admin)'
            if nick == 'c (admin)':
                break
            else:
                upload_score(nick, score)
                print('Thank you for playing!')
                break

        if check_lives(lives):
            fetch_scoreboard()
            print('\nGame over!\n')
            nick = str(input('Nickname: ')) + ' (admin)'
            if nick == 'c (admin)':
                break
            else:
                upload_score(nick, score)
                print('Thank you for playing!')
                break


        #Print out the acronym and prompt the user for a guess
        print('\n\nScore: {}/{}\nLives: {}\n\n\n'.format(score, acr_count, lives))
        acronym, answer = get_acronym(acr_ls)
        print(f'\t{acronym}')
        while True:

            command = str(input('Input: '))

            if command == 'r': #Reveal answer
                print(answer + '\n')

                continue

            if command == 'set_diff':
                print('Current diff: ' + fetch_difficulty(acronym) )
                while True:
                    new_diff = str(input('Set difficulty: '))
                    try:
                        if 0 < int(new_diff) < 11:
                            print('New difficulty set')
                            break
                        else:
                            print('''Wrong input\nEnter int between 1-10 or 'c' to cancel\n''')
                    except:
                        if new_diff == 'c':
                            break
                        else:
                            print('''Wrong input\nEnter int between 1-10 or 'c' to cancel\n''')
                continue

            if command == 'pass':
                print(answer)
                command = answer

            if command == 'help':
                print('\nr = Reveal answer\nset_diff = Set new difficulty\npass = Input correct answer\nquit / exit = Terminate session\nhelp = Print commands\n')

                continue
            if command == 'quit' or command == 'exit':
                play = False
                break


            if command.lower() == answer.lower(): # Correct answer #
                score += 1
                print('Correct!')
                break

            else: # Incorrect anwer #
                lives -= 1
                print('Wrong!')
                print(f'The answer was: {answer} \n\n')
                break



    main_menu(admin=True)

if __name__ == '__main__':
    main_menu()
