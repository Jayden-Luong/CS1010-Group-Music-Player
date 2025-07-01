import tkinter as tk
from tkinter import filedialog
import pygame
import os
import customtkinter as ctk
import time
from mutagen.mp3 import MP3
import random
import os

class MusicPlayer():
    selected = 0
    shuffle = False
    queue = []
    originalQueue = []
    playing = False
    paused = False
    audio = None
    isMuted = False
    volume = 100
    previous_vol = 100
    seek_pos_offset = 0


pygame.init()
project_path = "/".join(os.path.realpath(__file__).split("\\")[:-1])
default_songs = [["Pu Uoy Evig Annog Reven",f"{project_path}/assets/songs/Pu Uoy Evig Annog Reven.mp3"]]
groot = tk.Tk()
groot.iconbitmap(project_path + "/assets/images/icon.ico")
groot.title("Harmony Hub")
groot.geometry("600x400")
groot.minsize(600, 400)

pygame.mixer.init()
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)


topFrame = tk.Frame(groot)
topFrame.pack(fill="both", expand=True)
player = MusicPlayer()

def shuffle():
    if player.shuffle:
        player.shuffle = False
        shuffleButton.configure(image=shuffleButtonImage)
        player.queue = list(player.originalQueue)
        #print("Here`")
        return
    else:
        player.shuffle = True
        shuffleButton.configure(image=shuffleButtonOnImage)
        #print("Here 1")
    if not player.queue: # If queue is empty it does not continue
        #print("Here 2")
        return

    print("Before",player.queue)
    temp = player.queue.pop(player.selected) # Removes the current playing song
    random.shuffle(player.queue) # Shuffles the songs
    player.queue.insert(player.selected, temp ) # Add song back into the list
    print("After",player.queue)


def create_database(files):
    data = default_songs
    for file in files:
        data.append([file.split("/")[-1][:-4], file]) # This creates a 2d list for the database of songs. Index 0 is the name and 1 is the full path.
    return data


def get_names(database):
    return [item[0] for item in database]

def get_folder():
    files = filedialog.askopenfilenames(parent=groot, title="Select Music Files", multiple=True) # Opens up the file dialog to ask for music files, might add more types
    global database
    if files: # Makes sure files are selected or it will throw errors :(
        # print(files)
        database = create_database(files)
        songsVar.set(get_names(database))
        if player.paused:
            pygame.mixer.music.stop()
            player.paused = False
            player.playing = False

def playMusic(index,reload=False):
    if reload: # If this function is called by the event it will reset the paused and load the new song
        player.paused = False
        player.playing = False
    if not player.playing:
        if not player.shuffle:
            player.selected = index # Get the index of selected song
            player.queue = list(database) # Sets the queue to the position of the songs onwards
            player.originalQueue = list(player.queue)
        selected_file = player.queue[player.selected][1]
        pygame.mixer.music.load(selected_file)
        player.audio = MP3(selected_file) 
        pygame.mixer.music.play() 
        playButton.configure(image=pauseButtonImage)
        player.playing = True 
        player.paused = True
        update_progressbar()
    else: 
        if player.paused:
            pygame.mixer.music.pause() 
            playButton.configure(image=playButtonImage) 
            player.paused = False
        else: 
            player.paused = True 
            pygame.mixer.music.unpause()
            playButton.configure(image=pauseButtonImage)

def moveForward():
    if (player.selected >= len(player.queue)-1):
        return

    player.seek_pos_offset = 0
    original_index = player.originalQueue.index(player.queue[player.selected]) # Gets the original index in the Listbox to adapt for shuffles
    player.selected += 1
    songList.selection_clear(original_index) # Clears the previous selection

    songList.selection_set(player.originalQueue.index(player.queue[player.selected])) # Selects the currently playing song
    groot.after(100,playMusic(player.selected, True))

def moveBackwards():
    if (player.selected <= 0):
        return
    player.seek_pos_offset = 0
    original_index = player.originalQueue.index(player.queue[player.selected]) # Gets the original index in the Listbox to adapt for shuffles
    songList.selection_clear(original_index) # Clears the previous selection
    player.selected -= 1

    songList.selection_set(player.originalQueue.index(player.queue[player.selected])) # Selects the currently playing song
    groot.after(100,playMusic(player.selected, True))
    
songsVar = tk.Variable()
songList = tk.Listbox(topFrame, listvariable=songsVar, activestyle="none")
songList.pack(fill="both", expand=True, side="left")
songList.bind("<Double-Button-1>", lambda e: playMusic(songList.curselection()[0], True))
scrollbar = tk.Scrollbar(topFrame, command=songList.yview)
scrollbar.pack(fill="y", side="left")
database = create_database([])
songsVar.set(get_names(database))
songList.selection_set(0)

playButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/playButton.png")
pauseButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/pauseButton.png")
nextButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/nextButton.png")
reverseButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/previousButton.png")
shuffleButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/shuffleButton.png")
shuffleButtonOnImage = tk.PhotoImage(file = f"{project_path}/assets/images/shuffleButtonOn.png")
openButtonImage = tk.PhotoImage(file=f"{project_path}/assets/images/openButton.png")
bottomFrame = tk.Frame(groot)
bottomFrame.pack(fill="both", expand=True)


playButton = tk.Button(bottomFrame, image=playButtonImage, borderwidth=0,command=lambda: playMusic(songList.curselection()[0]))
nextButton = tk.Button(bottomFrame, image=nextButtonImage, borderwidth=0, command=moveForward)
reverseButton = tk.Button(bottomFrame, image=reverseButtonImage, borderwidth=0, command=moveBackwards)     
shuffleButton = tk.Button(bottomFrame, image=shuffleButtonImage, borderwidth=0, command=shuffle)
addFolder = tk.Button(
    bottomFrame, image=openButtonImage, borderwidth=0, command=get_folder
)
# Use the place manager with relativity so the location will scale with the window
addFolder.place(relx=0.20, rely=0.25, anchor="e", width=50, height=50)
shuffleButton.place(relx=0.35, rely=0.25, anchor="e", width=50, height=50)
reverseButton.place(relx=0.45, rely=0.25, anchor="e", width=50, height=50)
playButton.place(relx=0.50, rely=0.25, anchor="center", width=50, height=50)
nextButton.place(relx=0.55, rely=0.25, anchor="w", width=50, height=50)
# pauseButton.grid(row = 0, column = 1, padx = 7, pady = 10) This button will be replaced because when play button is pressed the image will change


def seek_song(value):
    if (player.playing):
        seek_pos = float(value) * player.audio.info.length  # turns the slider value to seconds
        player.seek_pos_offset = seek_pos    # update the point where the song plays to the song position of the slider
        pygame.mixer.music.play(start=player.seek_pos_offset)  #play the song where sldier is put to 


#function to update the progress bar as the song plays
def update_progressbar():
    if (player.playing):
        if progress_bar.cget("state") == "disabled":
            progress_bar.configure(state="normal")
        current_timesec = (pygame.mixer.music.get_pos() / 1000) + player.seek_pos_offset # returns the position of the current paused music in milliseconds, then converts to seconds, adds the offset to calc the actual position of the song
        current_time = current_timesec / player.audio.info.length # gets time and turns it into a value bwt 0.0 and 1.0 for the progress bar
        if (current_time > .9): # Check if the song is near the end
            groot.after(100, on_end)
        progress_bar.set(current_time)  #sets the progress of the bar to the current time of the song
        minutes, seconds = divmod(int(current_timesec), 60) #turns the current time value into an int and then divides it by 60 to get the elapsed time in minutes and seconds (stores them as a tuple)
        elapsed_time.configure(text="{:02d}:{:02d}".format(minutes, seconds)) #formats the minutes and seconds as 2-digit numbers with leading zeros
        # print(f"Elapsed Time: {minutes:02d}:{seconds:02d}") #debug test 
        groot.after(1000, update_progressbar) #schedules the function to run every second to show real-time progress
        
        # print("progress bar value:",progress_bar.get()) #debug test
    else:
        if progress_bar.cget("state") == "normal": # Makes the progress bar unclicable during no music
            progress_bar.configure(state="disabled")
#creating and placing the progress bar and elapsed time label
progress_bar = ctk.CTkSlider(bottomFrame, orientation="horizontal",
     width = 400, 
     height= 20,
     corner_radius=60,
     progress_color= "#BDA500",
     button_color="#b4a324",
     button_hover_color="#6f6518",
     command = seek_song,
     state="disabled" # Make it not draggable when not playing
     )  
progress_bar.place(relx=0.5, rely=.6, anchor="center")
progress_bar.set(0) # Intially at 0
elapsed_time = tk.Label(bottomFrame, text="00:00")
elapsed_time.place(relx=.84, rely=.6, anchor="w")

def set_volume(value): 
    player.volume = float(value)  #assign the slider value to volume variable
    if not player.isMuted:
        pygame.mixer.music.set_volume(player.volume)  #set the volume to volume
    print("volume: ", (player.volume) * 100) #debug test
    volume_indicator()

def toggle_mute():
    if player.isMuted:  #unmute function, set volume to the volume before it was muted
        player.volume = player.previous_vol   
        pygame.mixer.music.set_volume(player.volume)
        volume_butt.set(player.volume)
        player.isMuted = False
    else:  #mute function sets volume to 0
        player.previous_vol = player.volume
        pygame.mixer.music.set_volume(0)
        player.isMuted = True
    volume_indicator()

volume_butt = ctk.CTkSlider(bottomFrame, from_=0, to= 1, width=70,
    progress_color="#BDA500", 
    button_color="#b4a324",
    button_hover_color="#6f6518",
    command = set_volume)
volume_butt.place(relx=.71, rely=.25, anchor="w")

fullvolImage = tk.PhotoImage(file=f"{project_path}/assets/images/fullvol.png")
medvolImage = tk.PhotoImage(file=f"{project_path}/assets/images/medvol.png")
lowvolImage = tk.PhotoImage(file=f"{project_path}/assets/images/lowvol.png")
mutedImage = tk.PhotoImage(file=f"{project_path}/assets/images/muted.png")

def volume_indicator():
    if player.isMuted or player.volume <= 0:
        volume_icon.configure(image=mutedImage)
        volume_butt.set(0)
    elif player.volume > 0.7:
        volume_icon.configure(image=fullvolImage)
    elif 0.5 <= player.volume <= 0.7:
        volume_icon.configure(image=medvolImage)
    else:
        volume_icon.configure(image=lowvolImage)

volume_icon = tk.Button(bottomFrame, image=fullvolImage, borderwidth=0, command=toggle_mute)
volume_icon.place(relx=.65, rely=.25, anchor="w", height=50)
volume_butt.set(player.volume)

def on_end():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            player.seek_pos_offset = 0
            if (player.selected >= len(player.queue)-1):
                return
            print('music end event')
            original_index = player.originalQueue.index(player.queue[player.selected]) # Gets the original index in the Listbox to adapt for shuffles
            songList.selection_clear(original_index) # Clears the previous selection
            player.selected += 1
            songList.selection_set(player.originalQueue.index(player.queue[player.selected])) # Selects the currently playing song
            groot.after(100,playMusic(player.selected, True))
            return


groot.mainloop()
