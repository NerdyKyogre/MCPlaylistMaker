'''
Minecraft Playlist Maker 0.0.1
Create a resource pack that replaces Minecraft's built-in music disc with music files of your choice.
Author: NerdyKyogre
'''

import tkinter.filedialog #i have no idea why i have to do this, but it doesn't work if i don't.
import tkinter.font
import tkinter as tk
import os
import shutil
from PIL import ImageTk, Image  

#original song titles and special locations are global constants just for convenience since the main logic loop involves multiple functions due to tkinter limitations
DISC_TITLES = ["5","11","13","blocks","cat","chirp","far","mall","mellohi","otherside","pigstep","relic","stal","strad","wait","ward"] #these constants of the original titles will be useful for the loop
LOCATIONS = {
    "5": "in ancient city chests as fragments to be crafted.",
    "13": "in dungeon, mansion, or ancient city chests.",
    "cat": "in dungeon, mansion, or ancient city chests.",
    "otherside": "in dungeon, ancient city, or stronghold chests.",
    "pigstep": "in bastion chests.",
    "relic": "in suspicious gravel at trail ruins."
}

ROOT_DIR = os.getcwd() #this is convenient in the compression phase when we're not in this directory, which is always once the pack's file structure exists

playlistTitle = "null" #i hate this as much as you do but it's the only way to get name from pack_ver() to compress()

def main():
    '''
    Displays welcome screen and sets name of resource pack
    '''
    #pretty self explanatory, Give The Thing A Name
    label = tk.Label(
        text="Welcome to NerdyKyogre's Minecraft Playlist Maker!\nThis program will create a resource pack that replaces \nMinecraft's built-in music discs with songs or sounds of your choice.\nLet's start with the name of your playlist."
    )
    label.pack(expand=True)
    nameEnt = tk.Entry(font='Consolas 16')
    nameEnt.pack()
    forward = tk.Button(text="Next", command=lambda: pack_ver(nameEnt.get()))
    forward.pack()
    window.mainloop()

'''
Note that all non-looping GUI stages will be formatted as follows:

$logic based on result of previous input
clear_frame()
$GUI for next input

Therefore, function boundaries change in the *middle* of the logic for a task, not at the end of it.
These are all void functions.
'''

def pack_ver(name):
    '''
    Configures resource pack folder directory structure and prompts user to select pack version
    - name: name of pack as string, defined in main
    '''
    global playlistTitle 
    playlistTitle = name
    #check if folder with pack name exists, then make it accordingly
    currentDir = os.getcwd()
    newDir = os.path.join(currentDir, name)
    while os.path.exists(newDir):
        name = name + '(1)' #append 1 rather than recursively overwriting, just for ease of use
        newDir = os.path.join(currentDir, name) #need to update this again since name has changed
    #set up all the directories in standard pack layout
    os.mkdir(newDir)
    os.mkdir(os.path.join(newDir, 'assets'))
    os.mkdir(os.path.join(newDir, 'assets', 'minecraft'))
    os.mkdir(os.path.join(newDir, 'assets', 'minecraft', 'lang'))
    os.mkdir(os.path.join(newDir, 'assets', 'minecraft', 'sounds'))
    os.mkdir(os.path.join(newDir, 'assets', 'minecraft', 'sounds', 'records'))
    os.chdir(newDir)    

    clear_frame()
    
    packVer = 15
    #tool is designed for 1.20 but this will allow smart resource pack creators to use different versions without effort on my part
    label = tk.Label(
        text="Now, let's select a resource pack version.\nIf you don't know what you're doing, leave this empty \nand it will default to 15 (Minecraft 1.20/1.20.1).\nIf you want to use a different Minecraft version, enter the corresponding pack version number."
    )
    label.pack(expand=True)
    verEnt = tk.Entry(font='Consolas 16')
    verEnt.pack()
    forward = tk.Button(text="Next", command=lambda: pack_info(verEnt.get()))
    forward.pack()


def pack_info(ver):
    '''
    Sets pack version, prompts user for description
    - ver: pack version as defined by user, as a string
    '''
    #set pack version if user entered a valid number, otherwise default to 15
    try: 
        ver = int(ver)
    except ValueError:
        ver = 15
    
    clear_frame()

    #now add the description
    label = tk.Label(
        text="Add a short description for your playlist, if you want."
    )
    label.pack(expand=True)
    descEnt = tk.Entry(font='Consolas 16')
    descEnt.pack()
    forward = tk.Button(text="Next", command=lambda: pack_pic(ver, descEnt.get()))
    forward.pack()

def pack_pic(ver, desc):
    '''
    Creates pack.mcmeta file using version and description info, then prompts user to pick a pack.png
    - ver: pack version as defined by user, as a string
    - desc: pack description as defined by user, as a string
    '''
    #make the pack.mcmeta file using the version and description
    meta = open("pack.mcmeta", "x")
    meta.writelines([
        "{\n",
        "  \"pack\": {\n",
        "    \"pack_format\": " + str(ver) + ",\n",
        "    \"description\": \"" + desc + "\"\n",
        "  }\n",
        "}"
    ])
    meta.close()

    clear_frame()
    
    #now optionally upload a photo for pack.png, or simply continue
    label = tk.Label(
        text="If you want, pick a picture to use as pack.png.\nThis picture MUST be a PNG file and it MUST use a square \npower-of-two resolution (i.e. 64x64, 128x128, 256x256, 512x512).\nOnce you've selected a file, click Next to continue."
    )
    label.pack(expand=True)
    picker = tk.Button(text="Choose a picture", command=set_PNG)
    picker.pack()
    forward = tk.Button(text="Next", command=setup_playlist)
    forward.pack()

def setup_playlist():
    '''
    Sets working directory, creates language file to be edited, then hands off to choose_song/add_song loop
    '''
    #get into the assets directory
    os.chdir(os.path.join(os.getcwd(), 'assets', 'minecraft'))

    with open(os.path.join(os.getcwd(), 'lang', 'en_us.json'), "x") as lang: #create lang file to add the titles
        lang.write("{\n")
    
    choose_song(0)

def choose_song(i):
    '''
    Prompts user to choose a song for each disc and enter its title, offering information about the specific disc in the prompt
    Loops until all music discs have been replaced
    - i: position in loop, as int (these two functions are basically a janky for-loop as much as tkinter will allow)
    '''
    song = DISC_TITLES[i]
    imgFileName = "music_disc_" + song + ".png"
    i = i + 1
    clear_frame()
    #add an image of the music disc in question, for the aesthetic
    dimg = Image.open(os.path.join(ROOT_DIR, 'images', imgFileName))
    dimg = dimg.resize((128,128))
    dimgr = ImageTk.PhotoImage(dimg)
    #some discs are special and must be checked
    if song in LOCATIONS:
        location = LOCATIONS[song]
        label = tk.Label(
            text="Time to pick songs!\nThis song will replace the disk " + song + ", which can be found " + location + ".\n Press the button to select an audio file. This MUST be an OGG file.\nThen, enter the song artist and title below, in the format \"Artist - Title\" without quotes.\nWhen you are finished, click Next.",
            image = dimgr,
            compound = 'top'
        )
    #others just come from creepers.
    else: 
        label = tk.Label(
            text="Time to pick songs!\nThis song will replace the disk " + song + ", which can be found rarely as a drop from creepers.\n Press the button to select an audio file. This MUST be an OGG file.\nThen, enter the song artist and title below, in the format \"Artist - Title\" without quotes.\nWhen you are finished, click Next.",
            image = dimgr,
            compound = 'top'
        )
    label.pack(expand=True)
    picker = tk.Button(text="Choose a song", command=lambda: pick_song(song))
    picker.pack()
    titleEnt = tk.Entry(font='Consolas 16')
    titleEnt.pack()
    forward = tk.Button(text="Next", command=lambda: add_song(song, titleEnt.get(), i))
    forward.pack()

def add_song(song, title, i):
    '''
    Updates lang file with the new song
    Then checks if all discs have been replaced and loops or finishes accordingly.
    - song: disc to be replaced, as string
    - title: song title user entered above, as string
    - i: position in loop, as int
    '''
    lang = open(os.path.join(os.getcwd(), 'lang', 'en_us.json'), "a") #add title to lang file
    lang.write("    \"item.minecraft.music_disc_" + song + ".desc\": \"" + title + "\"")
    if i >= len(DISC_TITLES): 
        #decide whether to add another song or finish
        lang.write("\n}")
        lang.close()
        finish()
    else: 
        lang.write(",\n")
        lang.close()
        choose_song(i)

def finish():
    '''
    Saves the pack folder where the user chooses, as a zip archive
    '''
    clear_frame()
    label = tk.Label(
        text="Playlist complete! "
    )
    label.pack(expand=True)
    finish= tk.Button(text="Save and exit", command=compress)
    finish.pack()

def compress():
    '''
    Compresses folder as a zip in location specified by user
    '''
    #had the arguments backwards maybe?
    file = tkinter.filedialog.asksaveasfilename(initialfile = playlistTitle)
    for i in range(3):
        os.chdir("..")
    shutil.make_archive(file, 'zip', os.path.join(os.getcwd(), playlistTitle))
    exit()


def set_PNG():
    '''
    Sets pack.png from a file picked by the user
    '''
    #this will loop until a png is uploaded 
    filename = "null"
    while filename[-4::] != ".png":
        filename = tkinter.filedialog.askopenfilename()
    shutil.copy(filename, os.path.join(os.getcwd(), "pack.png"))

def pick_song(song):
    '''
    Adds a song to the pack based on user's choice in file picker
    song - title of music disc to be replaced, as string
    '''
    #this function is almost identical to set_PNG(), just for OGG files
    filename = "null"
    while filename[-4::] != ".ogg":
        filename = tkinter.filedialog.askopenfilename()
    shutil.copy(filename, os.path.join(os.getcwd(), "sounds", "records", song + ".ogg"))
    

def clear_frame(): 
    '''
    empties the window to add new elements
    '''
    for widgets in window.winfo_children():
        widgets.destroy()
    
#set up main window (needs to be global for fairly obvious reasons)
window = tk.Tk()
window.geometry("1000x500")
window.title("NerdyKyogre's Minecraft Playlist Maker")
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(size=16)

main()