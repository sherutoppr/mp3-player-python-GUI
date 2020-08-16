from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("MP3 Player")
root.geometry("500x450")  # 500px X 400px


# initialise pygame
pygame.mixer.init()

# create function to deal with time
def play_time():

    # check if the song is stopped
    if stopped:
        return

    # grab current song time
    current_time = pygame.mixer.music.get_pos() / 1000

    # convert song time to time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # get the current song
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/Sheru Khan/Documents/toppr_tech/songs/{song}.mp3'


    # find current song length
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    # convert to time format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    if int(song_slider.get()) == int(song_length):
        stop()
    elif paused:
        pass
    else:
        # move slider along 1 sec at a time
        next_time = int(song_slider.get()) + 1
        # set new output value to slider
        song_slider.config(to=song_length, value=next_time)

        # convert slider position to time format
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(song_slider.get())))



    # add current time to status bar
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} / {converted_song_length} ')

    # create loop to check time every second
    status_bar.after(1000, play_time)


# function to add one song to playlist
def add_song():
    song = filedialog.askopenfilename(initialdir='../songs/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    # my_label.config(text=song)
    #strip out directory structure
    song = song.replace("C:/Users/Sheru Khan/Documents/toppr_tech/songs/", "")
    song = song.replace(".mp3", "")
    playlist_box.insert(END, song)

# function to add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='../songs/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    
    for song in songs:
        song = song.replace("C:/Users/Sheru Khan/Documents/toppr_tech/songs/", "")
        song = song.replace(".mp3", "")
        playlist_box.insert(END, song)


# function to delete a song
def delete_song():
    # delete highlighted song from playlist
    playlist_box.delete(ANCHOR)


# function to delete all songs
def delete_all_songs():
    playlist_box.delete(0, END)


# function to play song
def play():

    # set stopped to false when song is now playing
    global stopped
    stopped = FALSE

    song = playlist_box.get(ACTIVE)
    my_label.config(text=song)
    song = f'C:/Users/Sheru Khan/Documents/toppr_tech/songs/{song}.mp3'

    # load song with pygame mixer
    pygame.mixer.music.load(song)

    # play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    # get song time
    play_time()


global stopped 
stopped = False
# function to stop the song
def stop():
    # stop the song
    pygame.mixer.music.stop()  

    # clear playlist bar
    playlist_box.selection_clear(ACTIVE) 

    # clear the status bar
    status_bar.config(text='Time Elapsed: 00:00:00 / 00:00:00 ')

    # set our slider to zero
    song_slider.config(value=0)

    # set stop variable to true
    global stopped
    stopped = True

    # remove song name
    my_label.config(text="")

# create paused variable
global paused
paused = False


# function to pause the song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # make unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # make pause
        pygame.mixer.music.pause()
        paused = True


# create function to play the next song
def next_song(is_next):

    # reset the slider position
    song_slider.config(value=0)

    # get the current song number 
    next_one = playlist_box.curselection()

    if is_next:
        next_one = next_one[0]+1
    else:
        next_one = next_one[0]-1

    # get the song title from playlist box
    song = playlist_box.get(next_one)

    my_label.config(text=song)
    song = f'C:/Users/Sheru Khan/Documents/toppr_tech/songs/{song}.mp3'

    # load song with pygame mixer
    pygame.mixer.music.load(song)

    # play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    # clear active bar in playlist
    playlist_box.selection_clear(0, END)

    # move active bar to next song
    playlist_box.activate(next_one)

    # set active bar to next song
    playlist_box.selection_set(next_one, last=None) 


# create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# create song slider function
def slide(x):
    song = playlist_box.get(ACTIVE)
    my_label.config(text=song)
    song = f'C:/Users/Sheru Khan/Documents/toppr_tech/songs/{song}.mp3'

    # load song with pygame mixer
    pygame.mixer.music.load(song)

    # play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())

# create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)


# create volume slider frame
volume_frame = LabelFrame(main_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

# create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=130, value=1, command=volume)
volume_slider.pack(pady=10)


# create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)


# create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="white", width=60, selectbackground='green', selectforeground='white')
playlist_box.grid(row=0, column=0)

# create button image
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')


# create button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# create play/stop button
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=lambda: next_song(False))
forword_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=lambda: next_song(True))
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forword_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# create add song Menu DROPDOWN
add_song_menu = Menu(my_menu, tearoff=0)   # tearoff=0 to remove dotted line 
my_menu.add_cascade(label="Songs", menu=add_song_menu)

# add one song 
add_song_menu.add_command(label="Add one song", command=add_song)

# add many song 
add_song_menu.add_command(label="Add many song", command=add_many_songs)

# create delete song menu dropdown
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a Song", command=delete_song)
remove_song_menu.add_command(label="Delete all Songs", command=delete_all_songs)


# create status bar
status_bar = Label(root, text='Time Elapsed: 00:00:00 / 00:00:00 ', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# temporary label
my_label = Label(root, text='')
my_label.pack(pady=20)


root.mainloop()
