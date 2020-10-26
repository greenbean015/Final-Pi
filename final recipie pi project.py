from tkinter import *


class Game(Frame):
    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def __str__(self):
        pass


# sets up the GUI
    def setupGUI(self):
        # organize the GUI
        self.pack(fill=BOTH, expand=1)
        # setup the player input at the bottom of the GUI
        # the widget is a Tkinter Entry
        # set its background to white and bind the return key to the
        # function process in the class
        # push it to the bottom of the GUI and let it fill
        # horizontally
        # give it focus so the player doesn't have to click on it
        Game.player_input = Entry(self, bg="white")
        Game.player_input.bind("<Return>", self.process) #functin that will process input from user 
        Game.player_input.pack(side=BOTTOM, fill=X)
        Game.player_input.focus()
        
        

        # setup the text to the right of the GUI
        # first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH // 2)
        # the widget is a Tkinter Text
        # disable it by default
        # don't let the widget control the frame's size
        Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)
    def play(self):
        self.setupGUI()
        

    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        response = "invlit input try again"

        words = action.split()
        
        if (action == "quit" or action == "exit"):
            exit(0)
        if (len(words) == 1):
            mainfood = words[0]


            if (mainfood == "meat"):
                print ("ayyyy")
                reponse = "this is a food!"

            else:
                print (response)
        else:
            print ("please use one word")
        



# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Recipies")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()
