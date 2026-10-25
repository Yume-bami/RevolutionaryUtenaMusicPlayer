import sys, os, random, pygame
from mutagen.mp3 import MP3 
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QPushButton, QLabel, QFrame, QButtonGroup, QSlider
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import Qt, QTimer



class Utena_Player(QWidget):
    pygame.mixer.init()
    def __init__(self):
        super().__init__()
        self.all_songs = []
        self.all_gifs = []
        self.btn_id = 0
        self.playing_song_duration = 0 #starting timestamp

        self.setGeometry(700,300,700,600)

        self.scroll_area = QScrollArea(self)
        self.widget_with_da_songs = QWidget(self)
        self.song_btngroup = QButtonGroup(self)
        self.gif_label = QLabel(self)
        self.gif = QMovie(self)
        self.title_label = QLabel(self)
        self.current_song_playing = QLabel("Won't you play a song?",self)
        self.music_frame = QFrame(self)
        self.playnpause_btn = QPushButton(" ►",self, clicked = lambda:self.pause_or_unpause())
        self.prev_btn = QPushButton(self, clicked = lambda:self.prev_song())
        self.next_btn = QPushButton(self, clicked = lambda:self.next_song())
        self.player = QMediaPlayer(self)
        self.shuffle_btn = QPushButton(self, clicked = lambda: self.shuffle())
        self.slider = QSlider(self, orientation= Qt.Orientation.Horizontal)
        self.time_label1 = QLabel("00:00",self)
        self.time_label2 = QLabel("00:00",self)
        self.timer = QTimer(self)
        self.my_msg = QLabel(random.choice(["Hello dear", "Hi babe", "Miss me?"]),self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Revolutionary Girl Utena Music Player")
        self.setWindowIcon(QIcon(".../revolutionary girl utena rose.png"))

        #scroll area
        self.scroll_area.setFixedSize(200, 600)
        
        #layout for the widgets in the scroll area
        self.vbox = QVBoxLayout(self.widget_with_da_songs)

        #setting up gif
        self.gif_label.setGeometry(250, 150, 400, 250)
        self.gif_label.setScaledContents(True)

        #title label
        self.title_label.setGeometry(240, 5, 400, 140)
        self.title_label.setPixmap(QPixmap(".../decoration_label.png"))
        self.title_label.setScaledContents(True)

        #music frame
        self.music_frame.setGeometry(200, 400, 500, 200)
        self.music_frame.lower()

        #current_song_playing
        self.current_song_playing.setGeometry(210,410,480,40)

        #play, prev, next buttons
        self.playnpause_btn.setGeometry(410,510,80,70)
        self.prev_btn.setGeometry(320,520,70,60)
        self.next_btn.setGeometry(510,520,70,60)
        self.shuffle_btn.setGeometry(585,525,50,50)

        #slider and time
        self.slider.setGeometry(250, 480, 400, 20)
        self.time_label1.setGeometry(220, 500, 40, 25)
        self.time_label2.setGeometry(640, 500, 40, 25)

        self.my_msg.setGeometry(220,520,100,60)

        #new font 
        font_id = QFontDatabase.addApplicationFont(".../FontsFree-Net-Didot-HTF-M42-Medium.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        utena_font = QFont(font_family, 100)
        self.setFont(utena_font)


        #style sheet

        self.setStyleSheet(
                            """
                            QWidget{
                              font-size: 50px; color: #FCF7FB; border: 2px solid #562C87;
                                }
                            QPushButton{
                                font-size: 20px; color: purple; background-color: black; text-align: left; font: bold
                                }
                            QFrame{
                                border-width: 10px; border-style: outset; border-color: #888888;
                                }
                            QSlider::handle:horizontal {
                                background: white
                                }
                            QSlider{
                                border: transparent;
                                }       
                                ;background: black  """)

        self.gif_label.setStyleSheet("border: 2px transparent;")
        self.title_label.setStyleSheet("border: 2px transparent;")
        self.current_song_playing.setStyleSheet("border: 2px solid #EC96BD; font-size: 28px; color: #EC96BD")
        self.time_label1.setStyleSheet("border: transparent; font-size: 16px")
        self.time_label2.setStyleSheet("border: transparent; font-size: 16px")
        self.my_msg.setStyleSheet("border: transparent; font-size: 15px; text-align: left")
        
        self.playnpause_btn.setStyleSheet("border-image: url(.../revolutionary girl utena rose.png) 3 10 3 10; border-top: 3px transparent;"
                                          "border-bottom: 3px transparent; border-right: 10px transparent; border-left: 10px transparent;" \
                                          "font-size: 30px; color: black; text-align: center")
        self.prev_btn.setStyleSheet("border-image: url(.../purple_rose.png) 3 10 3 10; border-top: 3px transparent;"
                                    "border-bottom: 3px transparent; border-right: 10px transparent; border-left: 10px transparent;" \
                                    "font-size: 30px; color: black;") 
        self.next_btn.setStyleSheet("border-image: url(.../purple_rose.png) 3 10 3 10; border-top: 3px transparent;"
                                    "border-bottom: 3px transparent; border-right: 10px transparent; border-left: 10px transparent;" \
                                    "font-size: 30px; color: black;")                               
        self.shuffle_btn.setStyleSheet("border-image: url(.../shuffle.png) 3 10 3 10; border-top: 3px transparent;"
                                    "border-bottom: 3px transparent; border-right: 10px transparent; border-left: 10px transparent;")
        
        
        
                                                                         
    
        
        

        #(colors= utena pink: #EC96BD, anthy purple: #562C87)
        

        self.load_songs()
        self.change_gif()
        self.song_btngroup.idClicked.connect(lambda btn_id: self.update_current_song_name(btn_id))
        self.song_btngroup.idClicked.connect(lambda btn_id: self.take_id(btn_id))
        self.timer.timeout.connect(self.song_playing_duration)
        self.slider.valueChanged.connect(self.update_slider)
        

        

    def load_songs(self):
        self.all_songs = []
        for file in os.listdir(".../Music"):
            if file.endswith(".mp3"):
                self.all_songs.append(file)

        self.add_songnames_to_scrollarea()


    def add_songnames_to_scrollarea(self):
        for i in range(len(self.all_songs)):
            self.songinsidewidget = QPushButton(QIcon(".../revolutionary girl utena rose.png"),f"{self.all_songs[i]}".removesuffix(".mp3"), self, clicked=lambda: self.change_gif())
            self.song_btngroup.addButton(self.songinsidewidget)
            self.vbox.addWidget(self.songinsidewidget)
            
        self.scroll_area.setWidget(self.widget_with_da_songs)


    def change_gif(self):

        self.all_gifs = []
        for file in os.listdir(".../Utena_gifs"):
            if file.endswith(".gif"):
                self.all_gifs.append(file)
        self.gif = QMovie(f".../Utena_gifs/{random.choice(self.all_gifs)}")
        self.gif_label.setMovie(self.gif)
        self.gif.start()

    def update_current_song_name(self, id):
        self.current_song_playing.setText(self.song_btngroup.button(id).text())
        self.play_music(current_song = self.current_song_playing)
        
    def play_music(self, current_song):
        file = f"C:/Users/Riz/Desktop/Yo_python/tung/Music/{current_song.text()}.mp3"
        self.duration_of_file(file)

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        self.playnpause_btn.setText("⬤")
        
        self.slider.setSliderPosition(0)
        self.slider.setRange(0,int(self.song_length))

        self.playing_song_duration = 0
        self.timer.start(1000)

        

        
       

    def pause_or_unpause(self):
        if self.current_song_playing.text() != "Won't you play a song?":
            self.my_msg.setText("")
            if self.playnpause_btn.text() == " ►":
                self.playnpause_btn.setText("⬤")
                pygame.mixer.music.unpause()
                self.timer.start()
            else:
                self.playnpause_btn.setText(" ►")
                pygame.mixer.music.pause()
                self.timer.stop()
        else:
            self.my_msg.setText(random.choice(["Choose a song..", "Bruh", "I'm sensitive"]))

    def take_id(self,id):
        self.btn_id = id
    
    def prev_song(self):
        if self.current_song_playing.text() != "Won't you play a song?":
            if self.btn_id != -2:
                self.btn_id = self.btn_id+1
                self.update_current_song_name(self.btn_id)
                self.take_id(self.btn_id)
                self.change_gif()
            else:
                self.my_msg.setText("No prev songs") #someplace to print that no more previous songs
        else:
            self.my_msg.setText(random.choice(["Choose a song..", "Idiot", "This isn't funny"]))

    def next_song(self):
        if self.current_song_playing.text() != "Won't you play a song?":
            if self.btn_id != -len(self.all_songs)-1:
                    self.btn_id = self.btn_id-1
                    self.update_current_song_name(self.btn_id)
                    self.take_id(self.btn_id)
                    self.change_gif()
            else:
                self.my_msg.setText("No more songs") #someplace to print that last song has been reached
        else:
            self.my_msg.setText(random.choice(["Choose a song..", "Don't...", "This is sad"]))
        


    def shuffle(self):
        self.btn_id = random.randrange(-len(self.all_songs), -2)
        self.update_current_song_name(self.btn_id)
        self.take_id(self.btn_id)
        self.my_msg.setText("That tickles..")
        self.change_gif()
        
        
        #this doesn't make a shuffle playlist, only shuffles the song once

    def duration_of_file(self, file):
        self.song_length = MP3(file).info.length
        self.interval2 = divmod(self.song_length, 60)

        self.min2 = int(self.interval2[0])
        self.sec2 = int(self.interval2[1])

        self.time_label2.setText(f"{self.min2:02}:{self.sec2:02}")

    def song_playing_duration(self):
        if self.playing_song_duration == int(self.song_length):
            self.next_song() 
        else:
            self.playing_song_duration += 1
            self.interval = divmod(self.playing_song_duration, 60)
            self.min = int(self.interval[0])
            self.sec = int(self.interval[1])
            self.time_label1.setText(f"{self.min:02}:{self.sec:02}")
            self.slider.setSliderPosition(self.playing_song_duration)

    def update_slider(self, new_position):
        self.my_msg.setText("Love this one")
        self.playing_song_duration = new_position

        self.interval = divmod(self.playing_song_duration, 60)
        self.min = int(self.interval[0])
        self.sec = int(self.interval[1])
        self.time_label1.setText(f"{self.min:02}:{self.sec:02}")

        self.slider.setSliderPosition(self.playing_song_duration)

        pygame.mixer.music.set_pos(self.playing_song_duration)    


def main():
    app = QApplication(sys.argv)
    utena_player = Utena_Player()
    utena_player.show()
    sys.exit(app.exec_())
        

if __name__ == "__main__":
    main()
