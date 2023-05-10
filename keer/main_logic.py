import pygame
import random
import time 
import pandas as pd
import csv_bs
global phase,Score,incorrect,correct,rank
import json
import webbrowser
import sys
pygame.init()
start_time = time.time()
incorrect=0
Score=[0,0,0]
correct=int(sum(Score))
youtube_links = []
rank=0.0
def new_line(s):
    if len(s)<75:
        return s," "
    ind=s.find(" ",75)
    return s[:ind],s[ind:]

def drawing(i,j):
    if not board[i]:
        screen.blit(box,j)
    elif board[i]=="X":
        pygame.draw.line(box, (0,0,0), (36,36),(108,107), width=5)
        pygame.draw.line(box, (0,0,0), (36,107),(108,36), width=5)
        screen.blit(box,j)
    else:
        pygame.draw.circle(box,(0,0,0),(72,72),36,width=5)
        screen.blit(box,j)

def player_wins(board):
    player="X"
    computer_mark="O"
    # check if the player has won horizontally
    if board[0] == board[1] == board[2] == player:
        return "player"
    elif board[3] == board[4] == board[5] == player:
        return "player"
    elif board[6] == board[7] == board[8] == player:
        return "player"
    # check if the player has won vertically
    elif board[0] == board[3] == board[6] == player:
        return "player"
    elif board[1] == board[4] == board[7] == player:
        return "player"
    elif board[2] == board[5] == board[8] == player:
        return "player"
    # check if the player has won diagonally
    elif board[0] == board[4] == board[8] == player:
        return "player"
    elif board[2] == board[4] == board[6] == player:
        return "player"
    # check if the computer has won horizontally
    elif board[0] == board[1] == board[2] == computer_mark:
        return "comp"
    elif board[3] == board[4] == board[5] == computer_mark:
        return "comp"
    elif board[6] == board[7] == board[8] == computer_mark:
        return "comp"
    # check if the computer has won vertically
    elif board[0] == board[3] == board[6] == computer_mark:
        return "comp"
    elif board[1] == board[4] == board[7] == computer_mark:
        return "comp"
    elif board[2] == board[5] == board[8] == computer_mark:
        return "comp"
    # check if the computer has won diagonally
    elif board[0] == board[4] == board[8] == computer_mark:
        return "comp"
    elif board[2] == board[4] == board[6] == computer_mark:
        return "comp"
    else:
        return False

def predict():
    copy=board[:]
    for i in range(len(copy)):
        copy=board[:]
        if copy[i]==None:
            copy[i]='X'
            if player_wins(copy):
                return i+1

#def score_cal(time,correct):
    ##print(time,correct)
    #return 100-int(time)+(int(correct)*10)

# Define the function to calculate scores
def score_cal(time, correct):
    return 100 - int(time) + (int(correct) * 10)

# Read in the scores from scores.csv
scores_df = pd.read_csv('scores.csv')

# Calculate the scores for each row
scores_df['scores'] = scores_df.apply(lambda row: score_cal(row['time'], row['correct']), axis=1)

# Group by username and sum the scores
leaderboard_df = scores_df.groupby('username')['scores'].sum().reset_index()

# Sort by score in descending order
leaderboard_df = leaderboard_df.sort_values(by='scores', ascending=False)

# Add a rank column
leaderboard_df['rank'] = leaderboard_df['scores'].rank(method='dense', ascending=False)

# Write the leaderboard to a new CSV file
leaderboard_df.to_csv('leaderboard.csv', index=False)


#print((csv_bs.best_score("scores.csv",score_cal)))
def save_credentials(username):
    # Create a DataFrame to store the credentials
    df = pd.DataFrame({'rank':[rank],'username': [username], 'scores': [0]})
    
    # Load the existing leaderboard file, or create a new one if it doesn't exist
    try:
        leaderboard = pd.read_csv('leaderboard.csv', index_col=0)
    except FileNotFoundError:
        leaderboard = pd.DataFrame(columns=['rank','username', 'scores'])
    
    ## Check if the username already exists in the leaderboard

    print('Leaderboard file created!')
# Define three sets of questions with varying difficulty levels
def questions():

    global easy_questions,medium_questions,hard_questions
    with open('questions.json') as f:
        questions = json.load(f)

    easy_questions = questions['easy_questions']
    medium_questions = questions['medium_questions']
    hard_questions = questions['hard_questions']
    #READS THE JSON FILE --questions.csv
    

questions()
pygame.init()
pygame.font.init()
screen=pygame.display.set_mode((432,604))
screen.fill((108, 207, 246))

font=pygame.font.SysFont('arial',25) 
small_font=pygame.font.SysFont('arial',15)
large_font=pygame.font.SysFont('arial',45)
vsmall_font=pygame.font.SysFont('arial',20)

board=[None]*9
empty=[i for i in range(9)]
clock=pygame.time.Clock()
box=pygame.Surface((144,142))

#setup for login page
username,password='',''
active=-1
login_rects=[pygame.Rect((108,284),(288,21)),pygame.Rect((108,355),(288,21))]
looks=[pygame.Rect((106,282),(291,24)),pygame.Rect((107,353),(290,24))]
print(login_rects[0].right)
login_box=pygame.Surface((288,21))
login=True
on_top=False
txt=small_font.render("click here!!",True,(0,0,0))
the_rect=txt.get_rect(center=(288,426))
entered=False
login_try=""

get_question=True
option_box=pygame.Surface((432,107))
difficulty=1
phase="login"
wait=False,False
#creating rectangles for the game
box_rects=[]
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,107)))
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,249)))
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,391)))

option_box_rects=[]
for i in range(4):
    option_box_rects.append(option_box.get_rect(topleft=(0,108+i*107)))
while True:
    
    screen.fill((108, 207, 246))
    for i in pygame.event.get():
        if i.type==256:
            pygame.quit()
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE and phase=="end_game":
                Score=[0,0,0]
                difficulty=1
                board=[None]*9
                phase="question"
                wait=False,False
                get_question=True
                incorrect=0
                empty=[i for i in range(9)]
                questions()
            if phase=='login':
                if active==0:
                    if i.key==pygame.K_BACKSPACE:
                        username=username[:-1]
                    else:
                        username+=i.unicode
                if active==1:
                    if i.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        if not i.unicode==r'\r':
                            password+=i.unicode
                if i.key==pygame.K_RETURN and phase=='login':
                    if active==0:
                        username=username[:-1]
                    else:
                        password=password[:-1]
                    entered=True
                    save_credentials(username)
    # pygame.draw.line(screen,(0,0,0),(200,150),(200,750),5)
    # pygame.draw.line(screen,(0,0,0),(400,150),(400,750),5)
    # pygame.draw.line(screen,(0,0,0),(0,150),(600,150),5)
    # pygame.draw.line(screen,(0,0,0),(0,350),(600,350),5)
    # pygame.draw.line(screen,(0,0,0),(0,550),(600,550),5)
    # pygame.draw.line(screen,(0,0,0),(0,150),(600,150),5)
    res=player_wins(board)
    #print(phase,res)
    mouse_buttons=pygame.mouse.get_pressed()
    mouse=pygame.mouse.get_pos()
    if res=="player":
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("You Win!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(2)
        res2=res
        res=''
        board=[None]*9
        phase="end_game"
        continue

    elif res=="comp":
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Computer Wins!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(2)
        res2=res
        res=''
        board=[None]*9
        phase="end_game"
        continue
    # To check for tie
    if not empty:
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Tie!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(3)
        exit()
    if phase=="player":
        move=predict()
        if move:
            txt=font.render(f"hint: You can win by marking position {move} ",True,(0,0,0))
        else:
            txt=font.render(f"hint: No hint available at the moment",True,(0,0,0))
        txt_rect=txt.get_rect(topleft=(21,553))
        screen.blit(txt,txt_rect)
        txt=font.render("Your turn!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        
        #print(mouse_buttons)
        if wait[1] and wait[0]:
            screen.fill((108, 207, 246))
            for i,j in enumerate(box_rects):
                box.fill((52, 84, 209))
                drawing(i,j)
            txt=font.render("Question Time!!",True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,53))
            screen.blit(txt,txt_rect)
            pygame.display.update()
            time.sleep(1)
            wait=False,False
            phase="question"
            continue
        elif not wait[1] and wait[0]:
            screen.fill((108, 207, 246))
            for i,j in enumerate(box_rects):
                box.fill((52, 84, 209))
                drawing(i,j)
            txt=font.render("Invalid!!",True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,53))
            screen.blit(txt,txt_rect)
            pygame.display.update()
            time.sleep(1)
            wait=False,False

        mouse=pygame.mouse.get_pos()
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            print(i,j)
            drawing(i,j)
            if j.collidepoint(mouse):
                #print(i+1)
                box.fill((52, 84, 230))
                drawing(i,j)
                if mouse_buttons[0]:
                    if not board[i]:
                        board[i]='X'
                        empty.remove(i)
                        wait=True,True
                    else:
                        wait=True,False

    elif phase=="comp":
        if empty:
            choice=random.choice(empty)
            board[choice]="O"
            empty.remove(choice)
        phase="question"
        #print(choice)
        screen.fill((108, 207, 246))
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Computers turn!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(1)
    elif phase=="question":
        #print(len(easy_questions))
        if difficulty==1 and get_question:
            question=easy_questions.pop()
            get_question=False
        elif difficulty==2 and get_question:
            question=medium_questions.pop()
            get_question=False
        elif difficulty==3 and get_question:
            question=hard_questions.pop()
            get_question=False
        #print(question)
        #print("in")
        screen.fill((108, 207, 246))
        #print(len(option_box_rects))
        mouse=pygame.mouse.get_pos()
        
        for i,j in enumerate(option_box_rects):
            if j.collidepoint(mouse):
                option_box.fill((52, 84, 230))
            else:
                option_box.fill((52, 84, 209))
            txt=small_font.render(question["options"][i],True,(0,0,0))
            #print(question["options"][i])
            txt_rect=txt.get_rect(midtop=(216,36))
            option_box.blit(txt,txt_rect)
            screen.blit(option_box,j)
            #print(new_line(question["question"]))
            txt=small_font.render(new_line(question["question"])[0],True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,36))
            screen.blit(txt,txt_rect)
            txt=small_font.render(new_line(question["question"])[1],True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,57))
            screen.blit(txt,txt_rect)
            #pygame.display.update()
            
    
        pygame.display.update()
        #time.sleep(2)
        #print(mouse)
        ans=-1
        if mouse_buttons[0]==True:
            for i,j in enumerate(option_box_rects):
                if j.collidepoint(mouse):
                    ans=i
            if ans!=-1:
                phase="result"
                get_question=True
                time.sleep(1)
    elif phase=="result":
     screen.fill((108, 207, 246))
     if question['options'][ans]==question['answer']:
        txt=small_font.render('Correct Answer!!',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,213))
        screen.blit(txt,txt_rect)
        if difficulty<3:
            difficulty+=1
        Score[difficulty-1]+=1
        phase="player"
     else:
        #question['options'][ans] != question["answer"]:
        youtube_links.append(question["youtube_link"])
        txt=small_font.render('Wrong Answer!!',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,213))
        screen.blit(txt,txt_rect)
        if difficulty == 1:
            youtube_link = easy_questions[-1]['youtube_link']
        elif difficulty == 2:
            youtube_link = medium_questions[-1]['youtube_link']
        elif difficulty == 3:
            youtube_link = hard_questions[-1]['youtube_link']
        txt=small_font.render(f'Try this video to  more: {youtube_link}',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,248))
        screen.blit(txt,txt_rect)
        phase="comp"
        incorrect+=1
     pygame.display.update()
     time.sleep(2)

   #CHANGES WERE MADE HERE STARTING
    elif phase=="end_game":
     # youtube_links = []
      #global phase, score, incorrect
      phase="end_game"
      pygame.time.set_timer(pygame.USEREVENT+1,0)
      pygame.time.set_timer(pygame.USEREVENT+2,0)
      screen.fill((108, 207, 246)) 
      if res2=='player':
 #FONTS LOADED FROM THE --assets--font--folder
          font = pygame.font.Font('C:/Users/keert/OneDrive/Desktop/aditi/assets/fonts/OpenSans-SemiBold.ttf', 16)
          small_font = pygame.font.Font('C:/Users/keert/OneDrive/Desktop/aditi/assets/fonts/OpenSans-Regular.ttf', 12)



          txt=small_font.render(f'number of questions answered correctly: {sum(Score)}',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,213))
          screen.blit(txt,txt_rect)
          txt=small_font.render(f'number of questions answered incorrectly: {incorrect}',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,248))
          screen.blit(txt,txt_rect)
          txt=font.render('Press space to try again!!',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,284))
          screen.blit(txt,txt_rect)
          txt=font.render('Press Enter to see history of players',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,350))
          screen.blit(txt,txt_rect)
           # display YouTube links for incorrect answers
          if incorrect > 0:
             txt = font.render("Click the links below to watch video explanations:", True, (0, 0, 0))
             txt_rect = txt.get_rect(center=(216, 400))
             screen.blit(txt, txt_rect)
             y = 450
             for link in youtube_links:
               txt = small_font.render(link, True, (0, 0, 0))
               txt_rect = txt.get_rect(center=(216, y))
               screen.blit(txt, txt_rect)
               #if txt_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
               #    webbrowser.open(link)
               y += 50
          pygame.display.update()
          while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            # Quit the game if the user closes the window
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        display_leaderboard()
                    elif event.key == pygame.K_SPACE:
                            questions()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if a link was clicked
                    pos = pygame.mouse.get_pos()
                    y = 450
                    for link in youtube_links:
                        txt = small_font.render(link, True, (0, 0, 255))
                        txt_rect = txt.get_rect(center=(216, y))
                        if txt_rect.collidepoint(pos):
                            webbrowser.open(link)
                            break
                        y += 50
                pygame.display.update()
         

      elif res2=="comp":
          screen.blit(txt,txt_rect)
          txt=font.render('Computer wins!!',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,241))
          screen.blit(txt,txt_rect)
          txt=font.render('Press space to try again!!',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,241))
          screen.blit(txt,txt_rect)
          txt=font.render('Press Enter to see history of players',True,(0,0,0))
          txt_rect=txt.get_rect(center=(216,350))
          screen.blit(txt,txt_rect)
          pygame.display.update()
          # display YouTube links for incorrect answers
          if incorrect > 0:
             txt = small_font.render("Click the links below to watch video explanations:", True, (0, 0, 0))
             txt_rect = txt.get_rect(center=(216, 400))
             screen.blit(txt, txt_rect)
             y = 450
             for link in youtube_links:
                txt = small_font.render(link, True, (0, 0, 0))
                txt_rect = txt.get_rect(center=(216, y))
                screen.blit(txt, txt_rect)
                #if txt_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                #   webbrowser.open(link)
             pygame.display.update()
           
      pygame.display.update() 

    elif phase=='login':
        #print(username,password)
        screen.fill((108, 207, 246))
        for j,i in enumerate(login_rects):
            if mouse_buttons[0] and not login_rects[1].collidepoint(mouse) and not login_rects[0].collidepoint(mouse):
                active=-1
            if active==j:
                x=(255, 240, 124)
                pygame.draw.rect(screen,(0,0,0),looks[j],2)
                #print(i.right)
            else:
                x=128, 255, 114
            login_box.fill(x)
            if j==0:
                txt=small_font.render(username,True,(0,0,0))
                txt_rect=txt.get_rect(center=(200,15))
                login_box.blit(txt,txt_rect)
            else:
                txt=small_font.render(len(password)*"*",True,(0,0,0))
                txt_rect=txt.get_rect(center=(144,11))
                login_box.blit(txt,txt_rect)
            screen.blit(login_box,i)
            txt=small_font.render("Username",True,(0,0,0))
            screen.blit(txt,(36,284))
            txt=small_font.render("Password",True,(0,0,0))
            screen.blit(txt,(36,355))
            if i.collidepoint(mouse) and mouse_buttons[0]:
                active=j
        if the_rect.collidepoint(mouse):
            color=(230, 57, 70)
            if mouse_buttons[0]:
                phase="new_user"
        else:color=100, 50, 255
        txt=small_font.render("click here!!",True,color)
        screen.blit(txt,the_rect)
        txt=small_font.render("To create a new account",True,(0,0,0))
        txt_rect=txt.get_rect(center=(180,426))
        screen.blit(txt,txt_rect)

        txt=large_font.render("LOGIN",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,142))
        screen.blit(txt,txt_rect)
        txt=small_font.render("press ENTER after filling the details.",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,178))
        screen.blit(txt,txt_rect)
        
        if entered:
            out=csv_bs.login(username,password,"hello.csv")
            if out==-1:login_try="Not a valid username!!"
            elif out==-2:login_try="Wrong password!!"
            elif out==-3:login_try="Username not found!!"
            else:
                login_try="Log in Successful!!"
                txt=small_font.render(login_try,True,(0,0,0))
                txt_rect=txt.get_rect(center=(216,249))
                screen.blit(txt,txt_rect)
                phase="question"
            entered=False
        txt=small_font.render(login_try,True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,249))
        screen.blit(txt,txt_rect)        
        pygame.display.update()

    pygame.display.update()
    clock.tick(60)

    
    #def questions():

    #  global easy_questions,medium_questions,hard_questions
    ##easy_link = "https://www.youtube.com/watch?v=easy_video"
    ##medium_link = "https://www.youtube.com/watch?v=medium_video"
    ##hard_link = "https://www.youtube.com/watch?v=hard_video"
    #  with open('questions.json') as f:
    #    questions = json.load(f)

    #  easy_questions = questions['easy_questions']
    #  medium_questions = questions['medium_questions']
    #  hard_questions = questions['hard_questions']

    def display_leaderboard():
      try:
        scores = pd.read_csv('scores.csv')
        scores['Score'] = scores.apply(lambda row: score_cal(row['time'], row['correct']), axis=1)
        leaderboard = scores.groupby('username')['Score'].sum().reset_index()
        leaderboard = leaderboard.sort_values(by='Score', ascending=False)
        leaderboard['rank'] = range(1, len(leaderboard) + 1) 
        screen.fill((108, 207, 246))
        txt = font.render('Leaderboard', True, (0, 0, 0))
        txt_rect = txt.get_rect(center=(216, 50))
        screen.blit(txt, txt_rect)
        x, y = 30, 100
        count = 0
        for i, row in leaderboard.iterrows():
            rank =row['rank']
            name = row['username']
            score = row['Score']
            txt =font.render(f'{rank}-{name} - {score}', True, (0, 0, 0))
            txt_rect = txt.get_rect(center=(216, 80 + (count * 25)))
            screen.blit(txt, txt_rect)
            count += 1
        pygame.display.update()

        # Handle events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_RETURN:
                        display_leaderboard()
                        #phase = 'leaderboard'
                        #scores = pd.read_csv('scores.csv')
                        #scores['Score'] = scores.apply(lambda row: score_cal(row['time'], row['correct']), axis=1)
                        #leaderboard = scores.groupby('username')['Score'].sum().reset_index()
                        #leaderboard = leaderboard.sort_values(by='Score', ascending=False)
                        #screen.fill((108, 207, 246))
                        #txt = large_font.render('Leaderboard', True, (0, 0, 0))
                        #txt_rect = txt.get_rect(center=(216, 50))
                        #screen.blit(txt, txt_rect)
                        #count = 1
                        #for _, row in leaderboard.iterrows():
                        #    name = row['username']
                        #    score = row['Score']
                        #    rank = row['rank']
                        #    txt = font.render(f'{rank} - {name} - {score}', True, (0, 0, 0))
                        #    txt_rect = txt.get_rect(center=(216, 80 + (count * 25)))
                        #    screen.blit(txt, txt_rect)
                        #    count += 1
                    elif event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE:
                    #elif event.key == pygame.K_SPACE:
                           questions()
                           # pygame.display.update()
            pygame.display.update() 
   

      except Exception as e:
        print(e)
        pass
