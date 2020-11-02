from tkinter import *
import requests

class ControlFrame(Frame):
    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def __str__(self):
        pass

# sets up the GUI
    def setupGUI(self):
        # Makes the frame the size of the window
        self.pack(side=TOP, expand=1, fill=BOTH)
        
        #Create label that tells the user that to put in textbox
        ControlFrame.instructLabel = Label(self, text = "What Ingredients do you have?")
        ControlFrame.instructLabel.pack(anchor=N)
        
        # Creates response Label
        ControlFrame.responseLabel = Label(self, text = "response", bg = "white")
        ControlFrame.responseLabel.pack(side = TOP, fill = BOTH, ipady=100)
        
        #Creates the Textbox
        ControlFrame.player_input = Entry(self, bg="white", text="bread peanut butter jelly")
        #functin that will process input from user
        ControlFrame.player_input.bind("<Return>", self.process)  
        ControlFrame.player_input.pack(side=BOTTOM, fill=X)
        ControlFrame.player_input.focus()
        
    def process(self, event):
        #take the input from the input line and sets them all to lower case
        action = ControlFrame.player_input.get().lower()
        response = "invalid input try again"

        #If you put peanut butter it our program counts peanut and butter as two different ingredients
        ingredients = action.split()
        #response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}")
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients)}&number=1&ranking=2")

        responseJSON = response.json()
        #create list of recipe items
        Recipies = [Recipe(recipeJSON) for recipeJSON in responseJSON]

        #add recipies to GUI
        for recipe in Recipies:
            rFrame.addRecipe(recipe)

        #change response label text
        ControlFrame.responseLabel.configure(text = response)

class Recipe():
    def __init__(self, recipeJSON):
        self.img = recipeJSON["image"]

    def __str__(self):
        pass

class RecipeFrame(Frame):
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        # setup scroll bar
        RecipeFrame.scroll = Scrollbar(self)
        RecipeFrame.scroll.pack(side = RIGHT, fill = Y)
        RecipeFrame.instructLabel = Label(self, text = "Recipes")
        RecipeFrame.instructLabel.pack(anchor=N)

    def addRecipe(self, Recipe):
        # Download and encode the image to base64 (dosen't work)
        dlimage = requests.get(Recipe.img).text()
        print(dlimage)

##################################################################################
api_key = "b29344da13414323bac320e823e7736a"
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Recipies")
#window.geometry(f"{WIDTH}x{HEIGHT}")
window.minsize(WIDTH, HEIGHT)

# create the controls GUI as a Tkinter Frame inside the window
cFrame = ControlFrame(window)
cFrame.setupGUI()

# create the recipe display frame inside the window
rFrame = RecipeFrame(window)
rFrame.setupGUI()

# wait for the window to close
window.mainloop()
