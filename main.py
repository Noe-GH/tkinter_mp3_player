import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import os
import pygame

# Global variables:
files_dir = ""
rep_status = 0

# Colors and fonts:
window_bg_color = '#1c1c1c'
playlist_bg_color = '#ff3300'
playlist_font_color = '#fbff00'
playlist_font = '"Lucida Console" 10'
playlist_selected_bg = 'black'
playlist_selected_fg = '#fbff00'


class MusicPlayer():
    def __init__(self):

        pygame.mixer.init()

        self.w = ThemedTk(theme='black')
        self.w.title('Music Player')
        self.w.resizable(0, 0)
        self.w.geometry('300x400+800+300')
        self.w.config(bg=window_bg_color)

        # Images:
        self.img_add = tk.PhotoImage(file='assets/add.png')
        self.img_remove = tk.PhotoImage(file='assets/remove.png')
        self.img_prev = tk.PhotoImage(file='assets/previous.png')
        self.img_play = tk.PhotoImage(file='assets/play.png')
        self.img_pause = tk.PhotoImage(file='assets/pause.png')
        self.img_next = tk.PhotoImage(file='assets/next.png')

        # Widget creation starts:
        self.listb_playlist = tk.Listbox(self.w, bg=playlist_bg_color,
                                         fg=playlist_font_color,
                                         font=playlist_font,
                                         selectbackground=playlist_selected_bg,
                                         selectforeground=playlist_selected_fg,
                                         height=14)

        self.frame_modbtns = ttk.Frame(self.w)
        self.btn_remove = ttk.Button(self.frame_modbtns, image=self.img_remove,
                                     command=self.delete_track)
        self.btn_add = ttk.Button(self.frame_modbtns, image=self.img_add,
                                  command=self.select_dir)

        self.frame_navbtns = ttk.Frame(self.w)
        self.btn_prev = ttk.Button(self.frame_navbtns, image=self.img_prev,
                                   command=lambda: self.select_track('prev'))
        self.btn_play = ttk.Button(self.frame_navbtns, image=self.img_play,
                                   command=self.play_track)
        self.btn_next = ttk.Button(self.frame_navbtns, image=self.img_next,
                                   command=lambda: self.select_track('next'))

        self.scale_vol = ttk.Scale(self.w, from_=0, to=1, value=1,
                                   command=self.set_volume)

        # Widget creation ends.

        # Widget placing starts:
        self.listb_playlist.pack(fill='x', padx=10, pady=10)

        self.frame_modbtns.pack(pady=10)
        self.btn_remove.grid(row=0, column=1)
        self.btn_add.grid(row=0, column=0)

        self.frame_navbtns.pack(pady=10)
        self.btn_prev.grid(row=0, column=0)
        self.btn_play.grid(row=0, column=1)
        self.btn_next.grid(row=0, column=2)

        self.scale_vol.pack(fill='x', padx=10, pady=5)

        # Widget placing ends.

        self.w.mainloop()

    def select_dir(self):
        '''
        Establishes the directory where the mp3 files are stored and inserts
        the names of the files in the playlist.
        '''
        try:
            change_files_dir(filedialog.askdirectory())
            files = os.listdir(files_dir)
            self.listb_playlist.delete(0, tk.END)
            for f in files:
                if f.split('.')[-1] == 'mp3':
                    self.listb_playlist.insert(tk.END, str(f))
        except FileNotFoundError:
            pass

    def delete_track(self):
        '''
        Deletes the current selected item from the playlist.
        '''
        self.listb_playlist.delete(tk.ANCHOR)

    def select_track(self, direction):
        '''
        Selects the next or previous item of the playlist, based on the
        current selected item.
            -direction: Receives either "next" or "prev" to establish where is
            the selection anchor is going to move.
        '''
        try:
            if direction == "next":
                track_index = self.listb_playlist.curselection()[0] + 1
            elif direction == "prev":
                track_index = self.listb_playlist.curselection()[0] - 1

            if (track_index >= 0 and
               track_index < self.listb_playlist.size()):
                self.listb_playlist.select_clear(0, tk.END)
                self.listb_playlist.activate(track_index)
                self.listb_playlist.select_set(track_index)
                self.listb_playlist.selection_anchor(track_index)
                self.listb_playlist.yview(track_index)
        except IndexError:
            pass

    def play_track(self):
        '''
        Plays and stops the music file.
        '''
        try:
            if rep_status == 0:
                pygame.mixer.music.load(files_dir + '/' +
                                        self.listb_playlist.get(tk.ANCHOR))
                self.btn_play.config(image=self.img_pause)
                pygame.mixer.music.play()
                change_rep_status(1)
            elif rep_status == 1:
                pygame.mixer.music.pause()
                self.btn_play.config(image=self.img_play)
                change_rep_status(0)
        except pygame.error:
            pass

    def set_volume(self, var):
        '''
        Changes the volume of the music played.
            *It receives no arguments when called.
        '''
        pygame.mixer.music.set_volume(self.scale_vol.get())


def change_files_dir(new_value):
    '''
    Assigns a value to the global variable files_dir.
        -new_value: Value assigned to files_dir.
    '''
    global files_dir
    files_dir = new_value


def change_rep_status(new_value):
    '''
    Assigns a value to the global variable rep_status.
        -new_value: Value assigned to rep_status.
    '''
    global rep_status
    rep_status = new_value


app = MusicPlayer()
