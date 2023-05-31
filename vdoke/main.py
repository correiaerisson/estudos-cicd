import vlc
import pafy
#import yt_dlp as youtube_dl
import pygame
import json
#import array
import moviepy
from moviepy.editor import *
import os
#import cv2

queue = None
songnumber = None
songfile = None
songname = None
songartist = None
songurl = None
clip = None
clipresized = None
numMusicas = '0'
playlist = []

equalizer = vlc.AudioEqualizer()

def drawTitle(t):
    titleFont = pygame.font.Font(None, 40)
    titleFont.set_bold(False)
    title = titleFont.render(t, True, yellow, None)
    title_xpos = (screen_w * 0.2)
    title_ypos = 50
    titleRect = title.get_rect()
    titleRect.center = (title_xpos , title_ypos)
    screen.blit(title, titleRect)

def drawArtist(a):
    artistFont = pygame.font.Font(None, 40)
    artistFont.set_bold(False)
    artist = artistFont.render(a, True, yellow, None)
    artist_xpos = (screen_w * 0.5)
    artist_ypos = 50
    artistRect = artist.get_rect()
    artistRect.center = (artist_xpos , artist_ypos)
    screen.blit(artist, artistRect)

def drawQueue(s):
    queueFont = pygame.font.Font(None, 40)
    queueFont.set_bold(False)
    queue = queueFont.render("Fila: "+str(s), True, yellow, None)
    queue_xpos = (screen_w * 0.8)
    queue_ypos = 50
    queueRect = queue.get_rect()
    queueRect.center = (queue_xpos , queue_ypos)
    screen.blit(queue, queueRect)

def openMedia(s):
    catalog = open('songs.json', "r")
    songs = json.loads(catalog.read())
    l = []
    try:
        for i in songs[s]:
            songname = i['name']
            songfile = i['file']
            songartist = i['artist']
            songurl = i['url']
        if os.path.exists(songfile):
            l = [songname, songfile, songartist, songurl]    
    except:
        print("not found")        
    return l

def play(f):
    clip = VideoFileClip(f)
    clipresized = clip.resize(width=screen_w, height=screen_h)
    clipresized.preview()
    clip.close()
    
def playList(p):
    numMusicas = len(p)
    for i in p:
        songname, songfile, songartist, songurl = openMedia(i)
        print(songname,"", songfile,"", songartist,"", songurl)
        print(p)
        clip = VideoFileClip(songfile)
        clipresized = clip.resize(width=screen_w, height=screen_h)
        clipresized.preview()
        clip.close()
        p.pop(0)
        
# POSICIONAMENTO DE MARQUEE VLC
middleleft = 1
middleright = 2
bottomleft = 9
topleft = 5
topright = 6
center = 0
centertop = 4

# DEFINICAO DE CORES
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
yellow = (255, 128, 0)
black = (0, 0, 0)

pygame.init()

clock = pygame.time.Clock()

infoObject = pygame.display.Info()
screen_w = infoObject.current_w
screen_h = infoObject.current_h

media_player = vlc.MediaPlayer()
media_player.toggle_fullscreen()

media_player.video_set_marquee_int(0, 1)
media_player.video_set_marquee_int(2, 0xffff00)
media_player.video_set_marquee_int(6, 20)
media_player.video_set_marquee_int(4, topleft)


# Define the background colour
# using RGB color coding.
background_colour = (255, 255, 255)
  
# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)

# Set the caption of the screen
pygame.display.set_caption('VDOkê')

# Configurações do painel inicial - seletor de música
small_font = pygame.font.Font(None, 100)
base_font = pygame.font.Font(None, 200)
user_text = '00000'
input_rect = pygame.Rect(screen_w * 0.5, screen_h // 2, 100, 100)
input_rect.center = (screen_w * 0.4, screen_h // 2)
color_active = pygame.Color('white')
color_passive = pygame.Color('chartreuse4')
color = color_active
active = True

# Fill the background colour to the screen
screen.fill(white)

# Variable to keep our game loop running
running = True

# game loop
while running:
    pygame.display.update()   
# for loop through the event queue  
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:               
        # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]

            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode
                # Ignora outros caracteres que não sejam numericos
                getVals = list([val for val in user_text if val.isnumeric()])
                user_text = "".join(getVals)

                # Verifica se o numero digitado é maior que 5
                #  se for elimina o primeiro número da lista
                if len(user_text) > 5:
                    user_text = user_text[1:]           
                songnumber = user_text

            if event.key == pygame.K_RETURN:
                    #clipresized.preview()
                    try:
                        playlist.append(songnumber)
                        #playList(playlist)
                        play(songnumber)
                        #user_text = '00000'
                        
                    except:
                        playlist.pop(0)
            #pygame.quit()
            
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
    
    
    if active:
        color = color_active
    else:
        color = color_passive
    
    try:
        songname, songfile, songartist, songurl = openMedia(songnumber)
        drawQueue(numMusicas)
        drawTitle(songname)
        drawArtist(songartist)
        #pygame.display.update()
    except:
        print("Música não encontrada")

    # EXIBE O CODIGO SELETOR DE MUSICA
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, black)
    #text_surface.center = (0 , 0)
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width()+10)
    

    pygame.display.flip()

    clock.tick(60)