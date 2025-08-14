#Names: Anthony Eryan, Lakysha Motiani, Sotiris Ploumbis
#pledge: We pledge our honor we have abided by the stevens honor system
import os

file = './musicrecplus.txt'

def CheckIfFileExists(file):
    '''checks if a file exists, if it doesnt it creates it-sotiris'''
    if os.path.isfile(file):
        DatabaseLoad(file)
    else:
        open(file,"w")

def DatabaseLoad(file):
    '''puts the contents of a file into a dictionary so further functiosn iterate through it-sotiris'''
    database = {}
    with open(file, "r") as file:
        for line in file:
            line = line.strip().split(':')
            if len(line) ==2:
                username = line[0].rstrip()
                artists = sorted(set(line[1].split(',')))
                database[username] = artists
    return database


def check(database, userInput):
    "checks if the user is in the database - sotiris"
    T = 0
    if userInput in database:
        T = 1
    else:
        T=0
    return T

def enter_preferences(userName, database, file):
    '''enteres the preferences of a user, works for new useraswell-sotiris'''
    listofprefernce = []
    while True:
        print("Enter an artist that you like (Press Enter to finish): ")
        artist = input().strip()
        if artist == '':
            break
        if artist not in listofprefernce:
            listofprefernce.append(artist)

    listofprefernce.sort()
    listofprefernce = [artist.title() for artist in listofprefernce]
    listofprefernce = set(listofprefernce)
    correctedUserName = userName.title()
    database[correctedUserName] = listofprefernce

    with open(file, "r") as f:
        doc = f.readlines()

    new_entry = f'{correctedUserName}:{",".join(listofprefernce)}\n'
    found = False
    for i, line in enumerate(doc):
        if line.startswith(correctedUserName + ":"):
            doc[i] = new_entry
            found = True
            break

    if not found:
        doc.append(new_entry)

    doc.sort()

    with open(file, "w") as f:
        f.writelines(doc)

    print("Preferences have been updated")




def Menu(inputOfUser,userInput, database,file):
    '''pops up the menu for the user to choose what actions he wants- sotiris'''
    if inputOfUser == 'e':
        enter_preferences(userInput, database,file)
    elif inputOfUser == 'r':
      user = userInput
      get_recommendations(user, database)
    elif inputOfUser == 'p':
      top_3_popular_artists(file)

    elif inputOfUser == 'h':
      count_artist_likes(file)

    elif inputOfUser == 'm':
      current_user = userInput
      find_user_likes_mostartists(database, current_user)


    elif inputOfUser =='q':
      save_and_quit(file)







def Main():
    '''main function of the program-sotiris'''
    inputOfUser = ''
    userInput = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ")
    CheckIfFileExists(file)
    while  inputOfUser != 'q':
        database = DatabaseLoad(file)
        if check(database,userInput) == 0:
            print('welcome newcomer!')
            enter_preferences(userInput, database,file)
        inputOfUser = input('''
            e - Enter preferences
            r - Get recommendations
            p - Show most popular artists
            h - How popular is the most popular
            m - Which user has the most likes
            q - Save and quit
            ''')
        Menu(inputOfUser,userInput,database, file)
    print('program terminated')



def top_3_popular_artists(file):
    '''Print the artists that are liked by the most users.
    by Anthony Eryan
    '''
    artist_counts = {}  # key: artist value: likes

    with open(file, 'r') as f:
        for line in f:
            sides = line.strip().split(':')  # splits between two sides, user and artist(s)
            if len(sides) >= 2 and not sides[0].endswith('$'):  # Check if sides has at least two elements and user does not end with '$'
                artist_preferences = [artist.strip() for artist in sides[1].split(',')]  # right side of collective artists

                for artist in artist_preferences:
                    artist_counts[artist] = artist_counts.get(artist, 0) + 1  # increment artist_count by get()

    if not artist_counts:
        print('Sorry, no artists found.')
        return

    # find the top 3 artists (or all if fewer than 3)
    top_artists = sorted(artist_counts, key=lambda x: artist_counts[x], reverse=True)[:3]

    print("Top 3 Popular Artists:")
    for artist in top_artists:
        print(artist)






def count_artist_likes(file):  # 4
    '''Print the number of likes the most popular artist received.
    by Anthony Eryan'''
    artist_counts = {}  # key: artist value: likes
    with open(file, 'r') as f:
        for line in f:
            sides = line.strip().split(':')  # splits between two sides, user and artist(s)
            if len(sides) >= 2:  # Check if sides has at least two elements
                user_name = sides[0].strip()  # side[0] represents the left side
                artist_preferences = [artist.strip() for artist in sides[1].split(',')]  # right side of collective artists
                if not user_name.endswith('$'):  # non-anon users
                    for artist in artist_preferences:
                        artist_counts[artist] = artist_counts.get(artist, 0) + 1  # by default artist goes to 0, increments by get
    if not artist_counts:  # post-loop check if all artists in the file are unique
        print('Sorry, no artists found.')
        return
    max_likes = max(artist_counts.values())  # value of max likes accumulated from the loop
    print(f"The most popular artist received {max_likes} likes.")


# Rest of your code remains unchanged

def find_user_likes_mostartists(database, current_user): #5
    if not database:
        print("Sorry, no user found.")
        return

    eligible_users = [user for user in database if not user.endswith("$")] 

    user_like_count = {}
    for user in eligible_users:
        user_like_count[user] = 0
        for artist in database[user]: 
            user_like_count[user] += 1

    max_liker = max(user_like_count.values())
    top_user = [user for user, likes in user_like_count.items() if likes == max_liker]

    print("User(s) who likes the most artists goes to: ")
    for user in sorted(top_user):
        print(user)


''' 
lakshya motiani
'''

def save_and_quit(file): #6
  '''When the user chooses to quit, the current database should be written
to the musicrecplus.txt, replacing old contents (if any).
by Anthony Eryan'''
  CheckIfFileExists(file)
  with open(file, 'w') as f:
      f.write('')
  print('Saved and quit')
#Function to get recommendations for the user

def get_recommendations(user, database):

  #ensure user is in the database
  if user not in database:
    print("User not found in database. Please enter preferences first!")
    return

#find user with the most similarity
  the_most_similar_user = find_most_similar_user(user, database) 

#check if similar user was found
  if the_most_similar_user == None:
    print("No recommendations available at this time.")
    return

  #Get the recommendations for the user based on the most similar user
  recommendations = generate_recommendations(user, the_most_similar_user, database)

#display recommendations to the user
  print("Recommendations:")
  for artist in recommendations:
    print(artist)
    '''
    lakshya motiani'''

#Function to find the most similar user
def find_most_similar_user(user, database):
  #exclude users in private mode
  eligible_users = [other_user for other_user in database if not other_user.endswith("$")]

#initalize variable to track most similar user as well as overlap
  most_similar_user = None
  max_overlap = -1

  #iterate through eligible users to find the most similar one
  for other_user in eligible_users:
    #skip same user
    if other_user == user:
      continue

#calculate the overlap of preferences
    overlap = len(set(database[user]) & set(database[other_user]))

#check if other user = better match
    if overlap > max_overlap and overlap > 0: 
      most_similar_user = other_user
    max_overlap = overlap

  return find_most_similar_user


#function to generate recommendations based on similar user

def generate_recommendations(user, similar_user, database):
  recommendations = set(database[similar_user]) - set(database[user])

  return sorted(recommendations)

'''
Lakshya Motiani
'''

Main()
