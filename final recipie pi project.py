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
        ControlFrame.responseLabel.pack(side = TOP, fill = BOTH)
        
        #Creates the Textbox
        ControlFrame.player_input = Entry(self, bg="white")
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
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients)}&number=5&ranking=2")
        responseJSON = response.json()
        #create list of recipe items
        ControlFrame.Recipies = [Recipe(recipeJSON) for recipeJSON in responseJSON]

        #add recipies to GUI
        for recipe in ControlFrame.Recipies:
            rFrame.addRecipe(recipe)

        #change response label text
        ControlFrame.responseLabel.configure(text = response.elapsed)

class Recipe():
    def __init__(self, recipeJSON):
        self.id = recipeJSON["id"]
        self.title = recipeJSON["title"]
        self.img = recipeJSON["image"]
        self.likes = recipeJSON["likes"]
        self.ingUsed = recipeJSON["usedIngredientCount"]
        self.ingMiss = recipeJSON["missedIngredientCount"]

    def __str__(self):
        return self.title

class RecipeFrame(Frame):
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        RecipeFrame.RecipeInfo = Text(self, state=DISABLED)
        RecipeFrame.RecipeInfo.pack(side=TOP, fill = BOTH)

        RecipeFrame.instructLabel = Label(self, text = "Recipes")
        RecipeFrame.instructLabel.pack(anchor=N)

        # setup scroll bar
        RecipeFrame.scroll = Scrollbar(window)
        RecipeFrame.scroll.pack(side = RIGHT, fill = Y)
        #create list
        RecipeFrame.myList = Listbox(window)
        RecipeFrame.myList.pack(side=TOP, expand=1, fill=BOTH)
        RecipeFrame.myList.bind('<<ListboxSelect>>', self.expandRecipe)
        #link scroll bar to listbox
        RecipeFrame.myList.config(yscrollcommand=RecipeFrame.scroll.set)
        RecipeFrame.scroll.config(command=RecipeFrame.myList.yview)

    def addRecipe(self, Recipe):
        RecipeFrame.myList.insert(END, f"{Recipe.title}  |  Likes: {Recipe.likes}  |  Missing Ingredients: {Recipe.ingMiss}")

    def expandRecipe(self, event):
        #makes this only run if an item is selected
        if (RecipeFrame.myList.curselection()):
            recipe = ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]]
            #TODO Check if this recipe is already displayed
            response = requests.get(f"https://api.spoonacular.com/recipes/{recipe.id}/information?apiKey={api_key}")
            responseJSON = response.json()
            RecipeFrame.RecipeInfo.config(state=NORMAL)
            RecipeFrame.RecipeInfo.delete("1.0", END)
            sumarry = responseJSON["summary"]
            RecipeFrame.RecipeInfo.insert(END, f"{recipe.title}\n\n{sumarry}")
            #print(RecipeFrame.myList.curselection()[0])

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
#window.maxsize(WIDTH, HEIGHT)

# create the controls GUI as a Tkinter Frame inside the window
cFrame = ControlFrame(window)
cFrame.setupGUI()

# create the recipe display frame inside the window
rFrame = RecipeFrame(window)
rFrame.setupGUI()

# wait for the window to close
window.mainloop()