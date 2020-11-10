from tkinter import *
import re
import requests
import ImageTk
from io import BytesIO
from PIL import Image

class ControlFrame(Frame):
    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def __str__(self):
        pass

# sets up the GUI
    def setupGUI(self):
        #Create label that tells the user that to put in textbox
        ControlFrame.instructLabel = Label(window, text = "What Ingredients do you have?", font="helvetica 18 bold")
        ControlFrame.instructLabel.pack(anchor=N)
        
        #Creates the Textbox
        ControlFrame.player_input = Entry(window, bg="white", font="helvetica 16")
        #functin that will process input from user
        ControlFrame.player_input.bind("<Return>", self.process)  
        ControlFrame.player_input.pack(side=TOP, fill=X)
        ControlFrame.player_input.focus()
        # Makes the frame the size of the window
        self.pack(side=TOP, expand=1, fill=BOTH)

        ControlFrame.resultAmount = Entry(self, bg="white", font="helvetica 16", width=8)
        ControlFrame.resultAmount.pack(anchor=S)
        
    def process(self, event):
        #resets the recepie list when one a word is entered
        RecipeFrame.myList.delete(0, END)
        #take the input from the input line and sets them all to lower case
        action = ControlFrame.player_input.get().lower()
        response = "invalid input try again"

        #If you put peanut butter it our program counts peanut and butter as two different ingredients
        ingredients = action.split()
        response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={','.join(ingredients)}&number=2&fillIngredients=true&addRecipeInformation=true")
        responseJSON = response.json()
        #if responsejson is an empy string(ex. no response) then chage the text of the instruction lable
        #this is probably wrong now
        #print(responseJSON)
        if (responseJSON == []):
            print ("invalid input")
            ControlFrame.instructLabel.config(text = "invalid input!!!!!!!, please try again.", fg = "red", font = "helvetica 18 bold")

        else:
            ControlFrame.instructLabel.config(text = "What Ingredients do you have?", fg = "black", font = "helvetica 18 bold")
            
        #create list of recipe items
        ControlFrame.Recipies = [Recipe(recipeJSON) for recipeJSON in responseJSON["results"]]
        #add recipies to GUI
        for recipe in ControlFrame.Recipies:
            rFrame.addRecipe(recipe)

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
        RecipeFrame.instructLabel = Label(self, text = "Recipes")
        RecipeFrame.instructLabel.pack(side=BOTTOM)

        RecipeFrame.RecipeSum = Text(self, state=DISABLED, wrap=WORD, font='helvetica' , height=10, width=40)
        #RecipeFrame.RecipeSum.pack(side=RIGHT, fill = BOTH, expand=1)

        RecipeFrame.imgLabel = Label(self, height=0, width=0)
        #RecipeFrame.imgLabel.pack(anchor=NW, fill=BOTH)

        # setup scroll bar
        RecipeFrame.scroll = Scrollbar(window)
        RecipeFrame.scroll.pack(side = RIGHT, fill = Y)
        #create list
        RecipeFrame.myList = Listbox(window, font="helvetica")
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
            # maybe save RecipeFrame.myList.curselection()[0] so we can ensure we work on the same is the prboem of making another varible that big
            recipe = ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]]
            # delete controls and add recipie image widget and textbox
            cFrame.pack_forget()
            RecipeFrame.RecipeSum.pack(side=RIGHT, fill = BOTH, expand=1)
            RecipeFrame.imgLabel.pack(anchor=NW, fill=BOTH)
            #TODO Check if this recipe is already displayed eh i don't think it really matters

            #make textbox editable
            RecipeFrame.RecipeSum.config(state=NORMAL)
            #looks at all the ingredients and subtracs the one you entered and gives you the missing ingredienants
            missingIngrediants = requests.get(f"https://api.spoonacular.com/recipes/{recipe.id}/ingredientWidget.json?apiKey={api_key}")
            missingJSON = missingIngrediants.json()
            ingredientsmis = missingJSON['ingredients']
            #print (ingredientsmis)
            misname = []
            for misingredients in ingredientsmis:
                #print (misingredients['name'])
                have = ControlFrame.player_input.get().lower()
                misname.append(misingredients['name'])
                    

                

            misname.remove(have)
            print(misname)
            #so we don't get more informaiton ona recipe more than once
            #if (hasattr(recipe, "summary")):
                ##clear textbox
                #RecipeFrame.RecipeSum.delete("1.0", END)
                #cleanSum = recipe.summary.replace("<b>", "").replace("</b>", "")
                #RecipeFrame.RecipeSum.insert(END, f"{recipe.title}\n\n{cleanSum}")
                #RecipeFrame.formatSummary(self, recipe)
            #else:
                #response = requests.get(f"https://api.spoonacular.com/recipes/{recipe.id}/information?apiKey={api_key}")
                #responseJSON = response.json()
                ##clear textbox
                #RecipeFrame.RecipeSum.delete("1.0", END)
                ##convert response to JSON object
                #sumarry = responseJSON["summary"]
                ##remove similar recipies, maybe we can do something with them
                #sumarry = sumarry[0:sumarry.rfind("Try <a href=")]
                #ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]].summary = sumarry
                #cleanSum = sumarry.replace("<b>", "").replace("</b>", "")
                #RecipeFrame.RecipeSum.insert(END, f"{recipe.title}\n\n{cleanSum}")
                ## Gives the summary box bold text
                #RecipeFrame.formatSummary(self, ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]])
                
            ##check if recipe already has the image downloaded
            #set image to image thing and image with the image with and image
            if (hasattr(ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]], "photo")):
                Rphoto = ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]].photo
                RecipeFrame.imgLabel.config(image=Rphoto, height=Rphoto.height(), width=Rphoto.width())
                #RecipeFrame.RecipeSum.config(width=int((800 - Rphoto.width())/12.08))
            else:
                response = requests.get(recipe.img)
                image = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(image)
                # save photo to og recipe object
                ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]].photo = photo
                RecipeFrame.imgLabel.config(image=photo, height=photo.height(), width=photo.width())
                #RecipeFrame.RecipeSum.pack(side=RIGHT, fill = BOTH, expand=1)

    def formatSummary(self, recipe):
        word_concord=re.finditer(r"<b>(.+?)<\/b>",recipe.summary)
        i = 0
        for word_found in word_concord:
            start = RecipeFrame.RecipeSum.index(f"1.0+{word_found.start()+len(recipe.title) + 2 - i*7} chars")
            end = RecipeFrame.RecipeSum.index(f"1.0+{word_found.end()+len(recipe.title) + 2 - (i+1)*7} chars")
            RecipeFrame.RecipeSum.tag_add('bold', start, end)
            i += 1
        RecipeFrame.RecipeSum.tag_configure("bold", font='Helvetica 14 bold')
        


##################################################################################
api_key = "b29344da13414323bac320e823e7736a"
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 480

# create the window
window = Tk()
window.title("Recipies")
window.geometry(f"{WIDTH}x{HEIGHT}")
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