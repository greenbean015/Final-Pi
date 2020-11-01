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
        # Makes the frame the size of the window
        self.pack(fill=BOTH, expand=1)
        #Create label that tells the user that to put in textbox
        Game.instructLabel = Label(self, text = "What Ingredients do you have?")
        Game.instructLabel.pack(anchor=NW)
        #Creates the Textbox
        Game.player_input = Entry(self, bg="white")
        Game.player_input.bind("<Return>", self.process) #functin that will process input from user 
        Game.player_input.pack(side=TOP, fill=X)
        Game.player_input.focus()
        # Creates response Label
        Game.responseLabel = Label(window, text = "response")
        Game.responseLabel.pack(side=BOTTOM)

    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        response = "invlit input try again"

        words = action.split()
        # Change Response Label
        Game.responseLabel.configure(text = response)


# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Recipies")
window.minsize(WIDTH, HEIGHT)

# create the GUI as a Tkinter Frame inside the window
g = Game(window)
# create GUI elements
g.setupGUI()

# wait for the window to close
window.mainloop()
