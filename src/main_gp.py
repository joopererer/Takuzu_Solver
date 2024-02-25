#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      LI Jiawei
#
# Created:     02/05/2022
# Copyright:   (c) LI Jiawei 2022
# Licence:
#-------------------------------------------------------------------------------

import pathlib
import time
import datetime
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
from tkinter import messagebox

import takuzu_solver

dirPath = ".." #str(pathlib.Path().absolute())

curFrame = 0          # le frame du jeu
list_btns_cases = []  # on a utilisé Widget 'Button' pour les cases
regles_ck = [True]*3  # check des regles, tout est choisi par defaut
valeursDef = [-1, 0, 1]

taille = 0            # taille de Jeu
data = []             # data de Jeu
data_instance = []    # data initiale (from fichier)
tkz_file_path = ""    # fichier (.tkz) lu
tmp_cnf_filename = dirPath + r"/takuzu.cnf"   # fichier .cnf temporaire pour passer au Z3-solver

def load():
    global tkz_file_path
    print("load!")
    tkz_file_path = filedialog.askopenfilename(title="Select file")
    loadJeu(tkz_file_path)

def loadJeu(tkz_file_path):
    global taille, data, data_instance
    print("file_path:", tkz_file_path)

    if(tkz_file_path.endswith(".png")):
        taille, instance = takuzu_solver.loadImgFile(tkz_file_path)
    else:
        taille, instance = takuzu_solver.loadJeuFile(tkz_file_path)

    create(taille)

    data_instance = [-1] * (taille * taille)
    for i in range(len(instance)):
        index = int(instance[i])
        if index < 0:
            data_instance[(-index) - 1] = 0
            # list_cases[(-index)-1].config(text="0", fg="#87CEEB")
        else:
            data_instance[index - 1] = 1
    data = data_instance
    printGrill(data, taille)
    msg_label.config(text=" >> [" + getTimeStamp() + "] File loaded " + tkz_file_path)
    # mettre à jour title
    filename = pathlib.Path(tkz_file_path).name
    root.title("Projet Takuzu (" + filename + ")")

def save():
    print("save!")
    file_path = filedialog.asksaveasfilename(title="Save file", filetypes=[("TKZ", ".tkz")])
    print("file_path:", file_path)
    takuzu_solver.saveJeuFile(data_instance, taille, file_path)
    msg_label.config(text=" >> [" + getTimeStamp() + "] File saved: " + file_path)

def exit_app():
    root.quit()

def btn_click(index):
    global list_btns_cases, data, data_instance
    #print("btn_click:", str(index))
    txt = list_btns_cases[index].cget("text")
    id = 0 if valeursDef.count(data[index])==0 else (valeursDef.index(data[index])+1)%len(valeursDef)
    photo = btn_bg_vide
    if valeursDef[id] == 0:
        photo = btn_bg_0_s
    elif valeursDef[id] == 1:
        photo = btn_bg_1_s
    list_btns_cases[index].config(bg="white", image=photo)
    data[index] = valeursDef[id]
    data_instance[index] = valeursDef[id]

def clean_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create(t_taille):
    # print("create:",str(t_taille),"x",str(t_taille))
    tkz_file_path = ""
    msg_label.config(text=" >> [" + getTimeStamp() + "] Jeu "+str(t_taille)+"x"+str(t_taille)+" est crée.")
    global list_btns_cases, frameTop, data, taille, curFrame, data_instance

    if curFrame != 0:
        frameTop.remove(curFrame)
        curFrame.destroy()
    list_btns_cases.clear()

    curFrame = tk.Frame(frameTop)
    frameTop.add(curFrame)
    curFrame.place(x=(screenW-t_taille*ballSize)//2-25, y=(containerH-t_taille*ballSize)//2-25)
    for i in range(t_taille):
        for j in range(t_taille):
            index = i*t_taille+j
            #list_cases.append(tk.Button(curFrame, text=str(index+1), image=btn_bg_vide, compound=tk.BOTTOM, font=myFontBtn2, fg="#A52A2A", bg="white", command=lambda x=index:btn_click(x)))
            list_btns_cases.append(tk.Button(curFrame, image=btn_bg_vide, bg="white", command=lambda x=index: btn_click(x)))
            list_btns_cases[index].grid(row=i, column=j)

    data = [-1] * (t_taille * t_taille)
    data_instance = [-1] * (t_taille * t_taille)
    taille = t_taille
    # mettre à jour title
    root.title("Projet Takuzu (Jeu "+str(taille)+"x"+str(t_taille)+")")

def solver():
    #print("solver")
    global data, data_instance, taille
    startTime = datetime.datetime.now()
    takuzu_solver.genererCNF(taille, data_instance, tmp_cnf_filename, regles_ck)
    msg_label.config(text=" >> [" + getTimeStamp() + "] CNF file crée: " + tmp_cnf_filename)
    t_data = takuzu_solver.solver(taille, tmp_cnf_filename)
    if len(t_data) == 0:
        print("Il n'y a pas de solution !")
        rslt_label.config(text="Il n'y a pas de solution !", fg="red")
    else:
        endTime = datetime.datetime.now()
        rslt_label.config(text="Résolu ! [time:"+str((endTime-startTime).total_seconds())+"s]", fg="blue")
        printGrill(t_data, taille)
        data = t_data

def printGrill(data, taille):
    for i in range(taille):
        for j in range(taille):
            index = i*taille + j
            #txt = valeursDef[(data[index] + 1) % len(valeursDef)]
            if data_instance[index] != data[index]:
                photo = btn_bg_vide
                if data[index] == 0:
                    photo = btn_bg_0_t
                elif data[index] == 1:
                    photo = btn_bg_1_t
                list_btns_cases[index].config(bg="#B0E0E6", image=photo)
            else:
                if data[index] == -1:
                    list_btns_cases[index].config(bg="white", image=btn_bg_vide)
                else:
                    list_btns_cases[index].config(bg="white", image=btn_bg_1_s if data[index] == 1 else btn_bg_0_s)

def clean():
    global data, data_instance, taille
    data = data_instance
    printGrill(data, taille)
    msg_label.config(text=" >> state")
    rslt_label.config(text="<<result>>")

def reload():
    global tkz_file_path, taille
    if tkz_file_path != "":
        loadJeu(tkz_file_path)
    else:
        create(taille)

def ruleCkChange(id):
    ckbox = eval("btn"+str(id)+"Stat")
    if 1 <= id <= 3:
        regles_ck[id-1] = True if ckbox.get()==1 else False
    #print("ckboxChanged:",str(id),ckbox.get())
    #print(regles_ck)


def getTimeStamp():
    return time.strftime("%H:%M:%S", time.localtime())

def showAbout():
    messagebox.showinfo("About", "Version 0.1 (based on Z3-solver)\n"
                                 "Author: LI Jiawei, PIGNON William, KHALIL Ibrahim\n"
                                 "UGA-DLST INM2 2021-2022",)

def showRules():
    messagebox.showinfo("Règles", "Le jeu suit les 3 règles suivants:\n"
                                  " * sur chaque ligne et sur chaque colonne\n"
                                  "1/ Pas plus de 2 chiffres identiques côté à côté;\n"
                                  "2/ Autant de 1 que de 0;\n"
                                  "3/ 2 lignes ou 2 colonnes ne peuvent pas être identiques.\n"
                                  "https://www.20minutes.fr/services/takuzu")

old_txt = ""
txt_rules = ["Règle 1: Pas plus de 2 chiffres identiques côté à côté",
             "Règle 2: Autant de 1 que de 0",
             "Règle 3: 2 lignes ou 2 colonnes ne peuvent pas être identiques"]

def showRuleTips(event, id):
    global old_txt
    if old_txt == "":
        old_txt = msg_label.cget("text")
    myFontMsg.config(weight='bold')
    msg_label.config(text=(" >> " + txt_rules[id-1]), font=myFontMsg)

def removeRuleTips(event):
    global old_txt
    myFontMsg.config(weight='normal')
    msg_label.config(text=old_txt, font=myFontMsg)
    old_txt = ""

def loadConfig():
    config = {}
    file = open(dirPath+r"/config", "r")
    line = file.readline()
    while line != "":
        key, value = line.split(":")
        config.update({key.strip(): value.strip()})
        line = file.readline()
    file.close()
    return config

#############################
##        Cycle Main       ##
#############################

screenW = 1300
screenH = 1600
ballSize = 70
containerH = 1240
bottomH = 280
btnW = 50
btnFontSize = 18
ckboxFontSize = 14
menuFontSize = 14
smallMode = False

config = loadConfig()
print(config)

root = tk.Tk()
realScreenH = root.winfo_screenheight()
if realScreenH <= 780 or config.get("small_mode") == "1":
    smallMode = True
    screenW = 480  # 650
    screenH = 600  # 783
    ballSize = 50
    containerH = 457  # 620
    bottomH = 120  # 140
    btnW = 23
    btnFontSize = 13
    ckboxFontSize = 9
    menuFontSize = 10

root.geometry(str(screenW)+"x"+str(screenH))
root.title("Projet Takuzu")
#root.iconbitmap(str(pathlib.Path().absolute())+r"/res/takuzu.ico")
#icon = tk.PhotoImage(file='res/takuzu.ico')
#root.iconphoto(True, icon)

# créer Menus
myFontMenu = font.Font(family='Helvetica', size=menuFontSize)
menuBar = tk.Menu(root, font=myFontMenu)

filemenu = tk.Menu(menuBar, tearoff=0)
filemenu.add_command(label="Load (.tkz)", font=myFontMenu, command=load)
filemenu.add_command(label="Save (.tkz)", font=myFontMenu, command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", font=myFontMenu, command=exit_app)
menuBar.add_cascade(label="File", menu=filemenu, font=myFontMenu)

createmenu = tk.Menu(menuBar, tearoff=0)
createmenu.add_command(label="4x4", font=myFontMenu, command= lambda x=4: create(x))
createmenu.add_command(label="6x6", font=myFontMenu, command= lambda x=6: create(x))
createmenu.add_command(label="8x8", font=myFontMenu, command= lambda x=8: create(x))
menuBar.add_cascade(label="Create", menu=createmenu, font=myFontMenu)

helpmenu = tk.Menu(menuBar, tearoff=0)
helpmenu.add_command(label="Rules", font=myFontMenu, command=showRules)
helpmenu.add_command(label="About", font=myFontMenu, command=showAbout)
menuBar.add_cascade(label="Help", menu=helpmenu, font=myFontMenu)

root.config(menu=menuBar)

# Frame
frameTop = tk.PanedWindow(root, width=screenW, height=containerH)
frameBottom = tk.PanedWindow(root, width=screenW, height=bottomH, orient=tk.VERTICAL)

frameTop.grid()
frameBottom.grid()


frameCkboxResult = tk.PanedWindow(frameBottom, orient=tk.HORIZONTAL)
frameBottom.add(frameCkboxResult)

# rule checkbox
myFontCkbox = font.Font(family='microsoft yahei', size=ckboxFontSize)
rulesCkFrame = tk.LabelFrame(frameCkboxResult, text="Règles Check", font=myFontCkbox)
btn1Stat = tk.IntVar(value=1)
btnCk_rule1 = tk.Checkbutton(rulesCkFrame, variable=btn1Stat, text="Règle 1", font=myFontCkbox, command=lambda x=1: ruleCkChange(x))
btnCk_rule1.bind('<Enter>', func=lambda event, x=1: showRuleTips(event, x))
btnCk_rule1.bind('<Leave>', func=removeRuleTips)
btnCk_rule1.grid(row=0, column=2)
btn2Stat = tk.IntVar(value=1)
btnCk_rule2 = tk.Checkbutton(rulesCkFrame, variable=btn2Stat, text="Règle 2", font=myFontCkbox, command=lambda x=2: ruleCkChange(x))
btnCk_rule2.bind('<Enter>', func=lambda event, x=2: showRuleTips(event, x))
btnCk_rule2.bind('<Leave>', func=removeRuleTips)
btnCk_rule2.grid(row=0, column=3)
btn3Stat = tk.IntVar(value=1)
btnCk_rule3 = tk.Checkbutton(rulesCkFrame, variable=btn3Stat, text="Règle 3", font=myFontCkbox, command=lambda x=3: ruleCkChange(x))
btnCk_rule3.bind('<Enter>', func=lambda event, x=3: showRuleTips(event, x))
btnCk_rule3.bind('<Leave>', func=removeRuleTips)
btnCk_rule3.grid(row=0, column=4)
frameCkboxResult.add(rulesCkFrame)

# message-result
rsltFrame = tk.LabelFrame(frameCkboxResult, text="Résultat", font=myFontCkbox)
myFontMsg = font.Font(family='Helvetica', size=12)
rslt_label = tk.Label(rsltFrame, text="<<result>>", bg="#F5DEB3", font=myFontMsg)
rslt_label.pack(fill="both")
frameCkboxResult.add(rsltFrame)

# message-tips (actions)
myFontMsg = font.Font(family='microsoft yahei', size=9)
msg_label = tk.Label(frameBottom, text=" >> state", font=myFontMsg, fg="#A9A9A9", bg="#FFFACD", anchor=tk.NW)
frameBottom.add(msg_label)

# button 'Solver'
'''
myFontBtn = font.Font(family='Helvetica', size=16)
btn_solver = tk.Button(frameBottom, text="Solver", command=solver, fg="#006400", bg="#8FBC8F", font=myFontBtn, relief=tk.GROOVE)
frameBottom.add(btn_solver)'''
btnFrame = tk.PanedWindow(frameBottom, orient='horizontal')
frameBottom.add(btnFrame)
myFontBtn1 = font.Font(family='Helvetica', size=btnFontSize)
myFontBtn2 = font.Font(family='Helvetica', size=btnFontSize-2)
btn_solver = tk.Button(btnFrame, text="⇧ Solver", width=btnW, command=solver, fg="#006400", bg="#8FBC8F", font=myFontBtn1, relief=tk.GROOVE)
btnFrame.add(btn_solver)
btn_clean = tk.Button(btnFrame, text="Clean↩", command=clean, width=10, bg="#ADD8E6", font=myFontBtn2, relief=tk.GROOVE)
btnFrame.add(btn_clean)
btn_reload = tk.Button(btnFrame, text="Reload🔄", command=reload, width=10, font=myFontBtn2, relief=tk.GROOVE)
btnFrame.add(btn_reload)

resDir = dirPath + (r"/res" if smallMode==False else r"/res/small")
btn_bg_0_s = tk.PhotoImage(file=resDir+r"/ball_0_s.png")
btn_bg_0_t = tk.PhotoImage(file=resDir+r"/ball_0_t.png")
btn_bg_1_s = tk.PhotoImage(file=resDir+r"/ball_1_s.png")
btn_bg_1_t = tk.PhotoImage(file=resDir+r"/ball_1_t.png")
btn_bg_vide = tk.PhotoImage(file=resDir+r"/ball_vide.png")

# on crée un nouveau jeu de 4X4 par défaut
create(4)

root.mainloop()