import os
import time
import keyboard
import json
import time
import numpy as np
from array import *
import random

def main():

    add_keybindings()
    render()

    while True:
        continue

class Question:
    def __init__(self, question, answers, correct):
        self.question = question
        self.answers = answers
        self.correct = correct
        self.answered = []
        for answer in answers:
            self.answered.append(False)
    def getPoints(self, answer):
        incorrect = 0
        for answer in self.answered:
            if answer:
                incorrect+=1
        return len(self.answers)-incorrect
    def render(self):
        global curr_action
        for answer in range(len(self.answers)):
            if self.answered[answer]:
                print("     "+"(X)"+self.answers[answer])
            elif curr_action == answer:
                print("     "+"(*)"+self.answers[answer])
            else:
                print("     "+"( )"+self.answers[answer])

class Control_point:
    def __init__(self, name, coord, water, info, questions, game):
        self.name = name
        self.coord = coord
        self.water = water
        self.info = info
        self.questions = []
        for question in questions:
            self.questions.append(Question(question["question"], question["answers"], question["answer"]))
        self.curr_question = 0
        self.finished = False
        self.game = game
    def render(self):
        global actions
        clear()
        print(self.name.center(width))
        print("")
        if self.water != "":
            print("Ūdens krātuve: " + self.water)
            print("")
       
        print(f"koordinātas: {self.coord[0]}, {self.coord[1]}")
        print("")
        print(self.info)
        print("")
        if not self.finished:
            self.finished = len(self.questions) == 0 and self.game == ""
        if self.finished:
            actions = ["Atpakaļ"]
        else:
            actions = ["Sākt"]
        render_actions()
    def render_question(self):
        global actions
        if self.game != "":
            play_game(self.game)
            self.finished = True
            return;
        clear()
        actions= []
        for answer in self.questions[self.curr_question].answered:
            if answer:
                actions.append("")
            else:
                actions.append("1")
        print("("+str(self.curr_question+1)+"/"+str(len(self.questions))+")"+self.questions[self.curr_question].question)
        self.questions[self.curr_question].render()
    def answer(self, answer):
        global WINDOW, actions, curr_action, game
        
        if answer != self.questions[self.curr_question].correct:
            self.questions[self.curr_question].answered[answer] = True
            actions[answer] = ""
            
            curr_action = 0
            while actions[curr_action] == "" or curr_action > len(actions):
                curr_action += 1
            render()
        else:
            clear()
            score = self.questions[self.curr_question].getPoints(answer);
            game.score += score
            print("Pareizi!".center(width))
            print(("Tu ieguvi "+str(score)+" punktus!").center(width))
            print(("Kopā: " + str(game.score)).center(width))
            
            self.curr_question+=1
            if self.curr_question >= len(self.questions):
                WINDOW = "point_end"
                print("(*)Atpakaļ".center(width))
            else:
                self.finished = True
                WINDOW = "question_end"
                print("(*)Nākamais".center(width))


class Game:
    def __init__(self, file):
        f = open('questions.json',  encoding="utf8")
        data = json.load(f)
        self.points = []
        for point in data["control points"]:
            self.points.append(Control_point(point["name"], point["coord"], point["water"], point["info"], point["questions"], point["game"]))
        self.score = 10
        self.curr_point = self.points[0]
        self.starttime = time.time()
        self.endtime = time.time()
        f.close()
    def render(self):
        global actions, curr_action, WINDOW
        clear()
        finished = 0
        for point in self.points:
            if point.finished:
                finished+=1
        if finished==len(self.points):
            self.endtime = time.time()
            self.render_end()
            WINDOW = "game_end"
            return
        print("Kontrolpunkti:")
        actions = []
        for point in self.points:
            if point.finished:
                actions.append("")
            else:
                actions.append(point.name)
        while actions[curr_action] == "" or curr_action > len(actions):
            curr_action += 1

        for point in range(len(self.points)):
            if self.points[point].finished:
                print("    (+)"+self.points[point].name)
            elif curr_action == point:
                 print("    (*)"+self.points[point].name)
            else:
                print("    ( )"+self.points[point].name)
                
        
        
    def render_end(self):
        clear()
        global actions
        actions = ["Sākums"]
        print("Spēles beigas!".center(width))
        print(f"Tu ieguvi {self.score} punktus!")
        timer = time.strftime("%M:%S", time.gmtime(self.endtime-self.starttime))
        print(f"Laiks: {timer}")
        print("")
        render_actions()


width=20

WINDOW = "menu"

actions = []
curr_question = 0
curr_action = 0
game = 0

def clear():
    os.system('cls')

def key_up():
    global curr_action, actions
    curr_action-=1
    if curr_action < 0:
        curr_action = len(actions)-1
    if actions[curr_action] == "":
        key_up()
    else:
        render()

def key_down():
    global curr_action, actions
    curr_action+=1
    if curr_action > len(actions)-1:
        curr_action = 0
    if actions[curr_action] == "":
        key_down()
    else:
        render()

def select():
    global WINDOW, game, curr_action
    action = curr_action
    curr_action = 0
    if WINDOW == "menu":
        if action==0:
            WINDOW = "game"
            game = Game("questions.json");
            curr_action=0;
            render()
            return
        if action==1:
            WINDOW = "instructions"
            render()
            return
    if WINDOW == "instructions":
        WINDOW = "menu"
        render()
        return

    if WINDOW == "game":
        game.curr_point = game.points[action];
        WINDOW = "point"
        render()
        return;

    if WINDOW == "point":
        if actions[action] == "Sākt":
            WINDOW = "question"
            render()
            return
        if actions[action] == "Atpakaļ":
            WINDOW = "game";
            render()
            return
        

    if WINDOW == "question":
        game.curr_point.answer(action)
        return

    if WINDOW == "question_end":
        WINDOW = "question"
        render()
        return
    if WINDOW == "point_end":
        WINDOW = "point"
        render()
        return
    if WINDOW == "game_end":
        if action==0:
            WINDOW = "menu"
            render()
            return

def render():
    global WINDOW, game, curr_action, actions
    if WINDOW == "menu":
        main_menu()
    elif WINDOW == "game":
        game.render()
    elif WINDOW == "game_end":
        game.render_end()
    elif WINDOW == "point":
        game.curr_point.render()
    elif WINDOW == "question":
        game.curr_point.render_question()
    elif WINDOW == "instructions":
        instructions()

def main_menu():
    global actions
    clear()
    print("Liepājas ceļojums".center(width))
    actions = ["Sākt", "Instrukcijas"]
    render_actions()
    print("")
    print("kontroles: \n   augšējā bultiņa\n   apakšējā bultiņa\n   enter")
    print("")
    print("Autori: Kārlis, Toms, Norlands".center(width))
    

            
def render_actions():
    global actions
    for action in range(len(actions)):
        if action == curr_action:
            print("     "+"(*)"+actions[action])
        else:
            print("     "+"( )"+actions[action])

def instructions():
    global actions
    clear()
    print("Instrukcijas".center(width))
    print("kontroles: \n   augšējā bultiņa\n   apakšējā bultiņa\n   enter")
    print("Spēles mērķis ir apmeklēt visus kontrolpunktus, un izpildīt tajā jautājumu vai uzdevumu.\nSPēle beidzas, kad tika apmeklēti visi kontrolpunkti.")
    actions = ["Atpakaļ"]
    render_actions()

def remove_keybindings():
    keyboard.unhook_all_hotkeys()

def add_keybindings():
    keyboard.add_hotkey('up', key_up)
    keyboard.add_hotkey('down', key_down)
    keyboard.add_hotkey('enter', select)
    keyboard.add_hotkey('space', select)

def play_game(name):
    global WINDOW, game
    score = 0
    if name == "makšķernieks":
        remove_keybindings()
        score = catchafish()
        clear()
        add_keybindings()
    game.score += score
    print("Uzvara!".center(width))
    print(("Tu ieguvi "+str(score)+" punktus!").center(width))
    print(("Kopā: " + str(game.score)).center(width))
    print("(*)Atpakaļ".center(width))
    WINDOW = "point_end"

def sayfish(temp, nowy, nowx):
    os.system("cls")
    for i in range(0, 5):
        for j in range(0,5):
            if(nowy==i and nowx == j):
                print("#",end="")
            else:
                if(temp[i][j]==0):
                    print("*",end="")
                else:
                    print(temp[i][j],end="")
        print()
    print("")
    print("kusties ar bultiņām un ar atstarpi ķer zivi, ja nenoķēri, tad parādīsies attālums līdz zivij.\nPamēģini noķert zivi ar vismazāk gājieniem!")
        

def catchafish():
    board =[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    sayfish(board, 0, 0)
    x = random.randint(0,4)
    y = random.randint(0,4)
    moves = 0

    nowx=0
    nowy=0

    while(True):

        if(keyboard.is_pressed("up")==0 and keyboard.is_pressed("down")==0 and (keyboard.is_pressed("space")==0 or keyboard.is_pressed("enter")==0) and keyboard.is_pressed("left")==0 and keyboard.is_pressed("right")==0  ):
            t=0
        if(t==1):
            continue

        if(keyboard.is_pressed("up")):
            nowy=nowy-1
            t=1
            if(nowy==-1):
                nowy=4
            sayfish(board, nowy, nowx)
        if(keyboard.is_pressed("down")):
            nowy=nowy+1
            t=1
            if(nowy==5):
                nowy=0
            sayfish(board, nowy, nowx)
        if(keyboard.is_pressed("left")):
            nowx=nowx-1
            t=1
            if(nowx==-1):
                nowx=4
            sayfish(board, nowy, nowx)
        if(keyboard.is_pressed("right")):
            nowx=nowx+1
            t=1
            if(nowx==5):
                nowx=0
            sayfish(board, nowy, nowx)

        if((keyboard.is_pressed("space") or keyboard.is_pressed("enter")) and board[nowy][nowx]==0):
            moves+=1
            if(nowx==x and nowy==y):
                return 25-moves
            

            board[nowy][nowx]= (abs(nowx-x)+abs(y-nowy))
            t=1
            j=0
            for i in range(0, 5):
                for j in range(0,5):
                    if(board[i][j]==0):
                        nowy=i
                        nowx=j
                        j=1
                        break
                if(j==1):
                    break

            sayfish(board, nowy, nowx)


if __name__ == "__main__":
    main()
