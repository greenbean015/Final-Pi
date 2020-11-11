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
        ControlFrame.player_input.pack(side=TOP, fill=X, padx=5)
        ControlFrame.player_input.focus()
        # Makes the frame the size of the window
        self.pack(side=TOP, expand=1, fill=BOTH)

        ControlFrame.resultAmntL = Label(self, font="helvetica 14", text="Number of Results:")
        ControlFrame.resultAmntL.grid(column=0, row=0)
        ControlFrame.resultAmnt = Entry(self, bg="white", font="helvetica 14", width=2)
        ControlFrame.resultAmnt.insert(0, "5")
        ControlFrame.resultAmnt.grid(column=1, row=0)
        
    def process(self, event):
        #resets the recepie list when one a word is entered
        RecipeFrame.myList.delete(0, END)
        #take the input from the input line and sets them all to lower case
        action = ControlFrame.player_input.get().lower()
        response = "invalid input try again"

        #If you put peanut butter it our program counts peanut and butter as two different ingredients
        ingredients = action.split()
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients)}&number={ControlFrame.resultAmnt.get()}")
        responseJSON = response.json()
        #if responsejson is an empy string(ex. no response) then chage the text of the instruction lable
        #this is probably wrong now
        print(responseJSON)
        if (responseJSON == []):
            ControlFrame.instructLabel.config(text = "No results", fg = "red", font = "helvetica 18 bold")

        else:
            ControlFrame.instructLabel.config(text = "What Ingredients do you have?", fg = "black", font = "helvetica 18 bold")
            
        #create list of recipe items
        ControlFrame.Recipies = [Recipe(recipeJSON) for recipeJSON in responseJSON]
        #add recipies to list
        for recipie in ControlFrame.Recipies:
            RecipeFrame.addRecipe(self, recipie)

class Recipe():
    def __init__(self, recipeJSON):
        self.id = recipeJSON["id"]
        self.title = recipeJSON["title"]
        self.img = recipeJSON["image"]
        self.likes = recipeJSON["likes"]
        self.ingUsedCnt = recipeJSON["usedIngredientCount"]
        self.ingMissCnt = recipeJSON["missedIngredientCount"]
        self.missIng = [ing["name"] for ing in recipeJSON["missedIngredients"]]

    def __str__(self):
        return self.title

class RecipeFrame(Frame):
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        dumbFrame = Frame(window)
        dumbFrame.pack(side=TOP, fill=X)

        RecipeFrame.instructLabel = Label(dumbFrame, text = "Recipes:", font="helvetica 10 bold")
        RecipeFrame.instructLabel.pack(anchor=CENTER,fill=X,side=LEFT)

        RecipeFrame.Sort = StringVar(dumbFrame)
        RecipeFrame.SortList = OptionMenu(dumbFrame, RecipeFrame.Sort, "Likes", "Used Ingredients", "Missing Ingredients")
        RecipeFrame.Sort.set("Likes")
        RecipeFrame.SortList.pack(anchor=E, side=RIGHT)

        RecipeFrame.instructLabel = Label(dumbFrame, text = "Sort by:", font="helvetica 10")
        RecipeFrame.instructLabel.pack(anchor=E,side=RIGHT, pady=6)
        
        RecipeFrame.RecipeSum = Text(self, state=DISABLED, wrap=WORD, font='helvetica' , height=10, width=40)
        #RecipeFrame.RecipeSum.pack(side=RIGHT, fill = BOTH, expand=1)

        RecipeFrame.imgLabel = Label(self, height=0, width=0)
        #RecipeFrame.imgLabel.pack(anchor=NW, fill=BOTH)


        # setup scroll bar
        RecipeFrame.scroll = Scrollbar(window)
        RecipeFrame.scroll.pack(side = RIGHT, fill = Y)
        #create list
        RecipeFrame.myList = Listbox(window, font="helvetica")
        RecipeFrame.myList.pack(side=BOTTOM, expand=1, fill=BOTH)
        RecipeFrame.myList.bind('<<ListboxSelect>>', self.expandRecipe)
        #link scroll bar to listbox
        RecipeFrame.myList.config(yscrollcommand=RecipeFrame.scroll.set)
        RecipeFrame.scroll.config(command=RecipeFrame.myList.yview)

    def addRecipe(self, Recipe):
        RecipeFrame.myList.insert(END, f"{Recipe.title}  |  Likes: {Recipe.likes}  |  Missing Ingredients: {Recipe.ingMissCnt}")

    def sortRecipies(self):
        sortVals = []
        if (RecipeFrame.Sort == "Likes"):
            for recipie in ControlFrame.Recipies:
                sortVals.append(int(recipie.likes))
                sortVals.sort(reverse=1)

    def expandRecipe(self, event):
        #makes this only run if an item is selected
        if (RecipeFrame.myList.curselection()):
            # maybe save RecipeFrame.myList.curselection()[0] so we can ensure we work on the same is the prboem of making another varible that big
            recipe = ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]]
            # delete controls and add recipie image widget and textbox
            cFrame.pack_forget()

            RecipeFrame.RecipeSum.pack(anchor = N, side=RIGHT, fill = BOTH, expand=1)
            RecipeFrame.imgLabel.pack(anchor=NW, fill=BOTH, side=TOP)
            #TODO Check if this recipe is already displayed eh i don't think it really matters

            #make textbox editable
            RecipeFrame.RecipeSum.config(state=NORMAL)
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
                RecipeFrame.imgLabel.config(image=Rphoto)
                #RecipeFrame.RecipeSum.config(width=int((800 - Rphoto.width())/12.08))
            else:
                response = requests.get(recipe.img)
                image = Image.open(BytesIO(response.content)).resize((312,231))
                photo = ImageTk.PhotoImage(image)
                # save photo to og recipe object
                ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]].photo = photo
                RecipeFrame.imgLabel.config(image=photo)
            #RecipeFrame.RecipeSum.insert()
            RecipeFrame.RecipeSum.config(state=DISABLED)
            


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