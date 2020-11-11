from tkinter import *
import re
from typing import OrderedDict
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
        response = "yes"

        #If you put peanut butter it our program counts peanut and butter as two different ingredients
        ingredients = action.split()
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients)}&number={ControlFrame.resultAmnt.get()}")
        responseJSON = response.json()
        #if responsejson is an empy string(ex. no response) then chage the text of the instruction lable
        #print(responseJSON)
        if (responseJSON == []):
            ControlFrame.instructLabel.config(text = "No results or invalid input", fg = "red", font = "helvetica 18 bold")

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
        self.missIng = []
        i = 0
        for ing in recipeJSON["missedIngredients"]:
            if (ing["name"] not in self.missIng):
                self.missIng.append(ing["name"])
            else:
                i+=1
        self.ingMissCnt = recipeJSON["missedIngredientCount"] - i

    def __str__(self):
        return self.title



class RecipeFrame(Frame):
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    def showOptions(self):
        rFrame.pack_forget()
        cFrame.pack(side=TOP, expand=1, fill=BOTH)
        RecipeFrame.dumbFrame.pack_forget()
        RecipeFrame.dumbFrame.pack(side=TOP, fill=X)
        RecipeFrame.OptionBut.pack_forget()


    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        RecipeFrame.dumbFrame = Frame(window)
        RecipeFrame.dumbFrame.pack(side=TOP, fill=X)

        RecipeFrame.instructLabel = Label(RecipeFrame.dumbFrame, text = "Recipes:", font="helvetica 10 bold")
        #RecipeFrame.instructLabel.grid(row=0, column=2)
        RecipeFrame.instructLabel.pack(side=LEFT, pady=6)

        #RecipeFrame.Sort = StringVar(RecipeFrame.dumbFrame)
        #RecipeFrame.SortList = OptionMenu(RecipeFrame.dumbFrame, RecipeFrame.Sort, "Likes", "Used Ingredients", "Missing Ingredients")#, command=rFrame.sortRecipies())
        #RecipeFrame.Sort.set("Likes")
        #RecipeFrame.Sort.trace_add("write", lambda *args: rFrame.sortRecipies())
        #RecipeFrame.SortList.grid(row=0, column=3)
        #RecipeFrame.SortList.pack(side=LEFT, fill=X)

        RecipeFrame.OptionBut = Button(RecipeFrame.dumbFrame, text="Options", command=rFrame.showOptions)
        
        RecipeFrame.instructLabel = Label(RecipeFrame.dumbFrame, text = "Recipes", font="helvetica 10 bold")
        #RecipeFrame.instructLabel.grid(row=0, column=4, ipadx=240)
        #RecipeFrame.instructLabel.pack(fill=X,side=LEFT, ipadx=240)
        
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


    def expandRecipe(self, event):
        #makes this only run if an item is selected
        if (RecipeFrame.myList.curselection()):
            # maybe save RecipeFrame.myList.curselection()[0] so we can ensure we work on the same is the prboem of making another varible that big
            recipe = ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]]
            # delete controls
            cFrame.pack_forget()
            # add option button
            rFrame.OptionBut.pack(side=RIGHT, padx=5)
            #repack the recipie frame
            rFrame.pack(side=TOP, expand=1, fill=BOTH)
            
            RecipeFrame.RecipeSum.pack(anchor = N, side=RIGHT, fill = BOTH, expand=1)
            RecipeFrame.imgLabel.pack(anchor = NW, fill=BOTH, side=TOP)
            RecipeFrame.dumbFrame.pack_forget()
            RecipeFrame.dumbFrame.pack(side=TOP, fill=BOTH, expand=1)
            RecipeFrame.myList.pack_forget()
            RecipeFrame.myList.pack(side=BOTTOM, expand=1, fill=BOTH)

            #make textbox editable
            RecipeFrame.RecipeSum.config(state=NORMAL)
            #clear textbox
            RecipeFrame.RecipeSum.delete("1.0", END)
            instruct = requests.get(f"https://api.spoonacular.com/recipes/{recipe.id}/analyzedInstructions?apiKey={api_key}")
            instructions =  instruct.json()
            steplist = []
            for ins in instructions:
                instuctionlist = ins['steps']
                for steps in instuctionlist:
                    steplist.append(steps['step'])
                
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
                # save photo to og recipe object-
                ControlFrame.Recipies[RecipeFrame.myList.curselection()[0]].photo = photo
                RecipeFrame.imgLabel.config(image=photo)
            #adds missing ingrediends to the desc box
            if (len(recipe.missIng) > 0):
                ingredients = ", ".join(recipe.missIng)
                RecipeFrame.RecipeSum.insert("1.0", f"Missing Ingredients: {ingredients} \n\n")
            
            #adds steps to the description box
            #recstep = ", ".join(steplist)
            linenumber = 3.0
            stepnumber = 1
            listinc = 0
           #adds steps to the desc box 
            for i in steplist:
                RecipeFrame.RecipeSum.insert(f"{linenumber}",f"Step {stepnumber}: {steplist[listinc]} \n\n")
                

                linenumber += 2.0
                stepnumber += 1
                listinc +=1
     
            #RecipeFrame.RecipeSum.insert("2.0", f"\nSteps: {recstep}")
            RecipeFrame.RecipeSum.config(state=DISABLED)
        


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