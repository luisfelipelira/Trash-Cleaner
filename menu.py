import os
from pathlib import Path
from tkinter import messagebox

PROJECT_DIR = Path(__file__).resolve().parent
os.chdir(PROJECT_DIR)

import pygame
from moviepy.editor import VideoFileClip

from catador import Carro
from player import Player
from player import Lançar
from lixos import LixoL
from lixos import LixoR
from lixos import tiro
from buraco import buracos
import lixos
import buraco

import math
from random import randint

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 980
HEIGHT = 720

pygame.init()
pygame.display.set_caption("Trash Cleaner")
tela = pygame.display.Info()
width = tela.current_w - 386
height = tela.current_h -48
print(width, height)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((width,height), pygame.SRCALPHA)

screenfull = 1

def fullscreen_off(screen):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    global screenfull
    screenfull = 1
    return screen

def fullscreen_on(screen):
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
    global screenfull
    screenfull = 2
    return screen

# Iniciando imagens, sons e fontes e arquivos
invissible = (0, 0, 0, 0)
cor = (0, 255, 0, 255)

LIXOVELOCIDADE = 100

titulo = pygame.image.load('Imagens/menu/titulo.png')
titulo = pygame.transform.scale(titulo, [410, 180])
fundo = pygame.image.load('Imagens/menu/fundo.png')

jogar = pygame.image.load('Imagens/menu/play.png')
jogar_alt = pygame.image.load('Imagens/menu/playalt.png')

sair = pygame.image.load('Imagens/menu/sair.png')
sair_alt = pygame.image.load('Imagens/menu/sairalt.png')

config = pygame.image.load('Imagens/menu/config.png')
config_alt = pygame.image.load('Imagens/menu/configalt.png')

guide = pygame.image.load('Imagens/menu/guide.png')
guide_alt = pygame.image.load('Imagens/menu/guidealt.png')

cred = instruc = pygame.image.load('Imagens/menu/cred.png')
cred_alt = pygame.image.load('Imagens/menu/credalt.png')

pts = pygame.image.load('Imagens/hud/pts2.png')
mochila = pygame.image.load('Imagens/hud/mochila2.png')
time = pygame.image.load('Imagens/hud/timer2.png')

botao = [jogar, jogar_alt, sair, sair_alt]

#MUSICAS
menu_music = pygame.mixer.Sound('Sons/menu.ogg')
jogo_music = pygame.mixer.Sound('Sons/jogo.ogg')
hard_music = pygame.mixer.Sound('Sons/hard.wav')
jogar_saco = pygame.mixer.Sound('Sons/jogar o saco.wav')
click_music = pygame.mixer.Sound('Sons/click.ogg')

menu_music.set_volume(0.5)
jogo_music.set_volume(0.5)
hard_music.set_volume(0.5)

jogar_saco.set_volume(0.5)
click_music.set_volume(0.5)

#CONFIGURAÇOES

seleçao = pygame.image.load('Imagens/opçoes/dificuldade/seleçao.png')

fundo_conf = pygame.image.load('Imagens/opçoes/ret5.png')
fundo_conf = pygame.transform.scale(fundo_conf, (width, height))

sfx_titulo = pygame.image.load('Imagens/opçoes/sfx/titulosfx.png')
sfx_musica = pygame.image.load('Imagens/opçoes/sfx/musica.png')
sfx_ef = pygame.image.load('Imagens/opçoes/sfx/efsonoros.png')
sfx_mais = pygame.image.load('Imagens/opçoes/sfx/+.png')
sfx_menos = pygame.image.load('Imagens/opçoes/sfx/-.png')

sfx_click = pygame.image.load('Imagens/opçoes/sfx/clique.png')
sfx_barra = pygame.image.load('Imagens/opçoes/sfx/separaçao.png')

sfx_botao = [sfx_menos, sfx_mais]

dificuldade_titulo = pygame.image.load('Imagens/opçoes/dificuldade/titulo.png')
facil = pygame.image.load('Imagens/opçoes/dificuldade/facil.png')
medio = pygame.image.load('Imagens/opçoes/dificuldade/medio.png')
dificil = pygame.image.load('Imagens/opçoes/dificuldade/dificil.png')

video_titulo = pygame.image.load('Imagens/opçoes/video/video.png')
full = pygame.image.load('Imagens/opçoes/video/fullscreen.png')
janela = pygame.image.load('Imagens/opçoes/video/janela.png')

aplicar = pygame.image.load('Imagens/opçoes/botao/aplicar.png')
aplicar_alt = pygame.image.load('Imagens/opçoes/botao/aplicaralt.png')
fechar = pygame.image.load('Imagens/opçoes/botao/fechar.png')
fechar_alt = pygame.image.load('Imagens/opçoes/botao/fecharalt.png')

#INSTRUÇÕES
pag1 = pygame.image.load('Imagens/instruçoes/pág1.png')
pag1 = pygame.transform.scale(pag1, [width, height])

pag2 = pygame.image.load('Imagens/instruçoes/pág2.png')
pag2 = pygame.transform.scale(pag2, [width, height])

pag3 = pygame.image.load('Imagens/instruçoes/pág3.png')
pag3 = pygame.transform.scale(pag3, [width, height])

pag4 = pygame.image.load('Imagens/instruçoes/pág4.png')
pag4 = pygame.transform.scale(pag4, [width, height])

pag5 = pygame.image.load('Imagens/instruçoes/pág5.png')
pag5 = pygame.transform.scale(pag5, [width, height])

proximo = pygame.image.load('Imagens/instruçoes/go.png')
proximo = pygame.transform.scale(proximo, (20, 24))

proximo_alt = pygame.image.load('Imagens/instruçoes/go_alt.png')
proximo_alt = pygame.transform.scale(proximo_alt, (20, 24))

anterior = pygame.image.load('Imagens/instruçoes/back.png')
anterior = pygame.transform.scale(anterior, (20, 24))

anterior_alt = pygame.image.load('Imagens/instruçoes/back_alt.png')
anterior_alt = pygame.transform.scale(anterior_alt, (20, 24))

#GAMEOVER
gameover = pygame.image.load('Imagens/game over/gameover.png')

gameover_novamente = pygame.image.load('Imagens/game over/jogar.png')
gameover_novamente_alt = pygame.image.load('Imagens/game over/jogaralt.png')

gameover_sair = pygame.image.load('Imagens/game over/sair.png')
gameover_sair_alt = pygame.image.load('Imagens/game over/sairalt.png')


#passos = pygame.mixer.Sound('Sons/passos.wav')

clip = VideoFileClip('Imagens/intro.mp4')
clip.preview()

creditos = VideoFileClip('Imagens/creditos.mp4')

n = 10
b = 0
def game(n=10, b=0):
    jogo(n, b)

font_name = pygame.font.match_font('berlin sans FB', True, True)
def text(surf, text, size, x, y, cor): 
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, cor)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def menu():

    # Coloca as imagens
    screen.blit(fundo, (0, 0))
    screen.blit(titulo, (290, 0))

    pygame.display.flip()

    menu_music.stop()
    jogo_music.stop()
    hard_music.stop()
    menu_music.play()

    while pygame.event.wait() or pygame.event.get():

        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]

        #JOGAR
        if math.sqrt(((mouse[0] - 500)**2) + ((mouse[1] - 460)**2)) < 110:
            screen.blit(jogar_alt, (390, 350))
            if press:
                click_music.play()
                game(n, b)
        else:
            screen.blit(jogar, (390, 350))

        #SAIR
        if math.sqrt(((mouse[0] - 764)**2) + ((mouse[1] - 454)**2)) < 84:
            screen.blit(sair_alt, (680, 370))
            if press:
                quit()
        else:
            screen.blit(sair, (680, 370))
            
        #CONFIG
        if math.sqrt(((mouse[0] - 234)**2) + ((mouse[1] - 454)**2)) < 84:
            screen.blit(config_alt, (150, 370))
            if press:
                click_music.play()
                conf()
        else:
            screen.blit(config, (150, 370))
            

        #INSTRUÇOES
        if 250 + 223 > mouse[0] > 250 and 630 + 65 > mouse[1] > 630:
            screen.blit(guide_alt, (250, 630))
            if press:
                instruçoes()
        else:
            screen.blit(guide, (250, 630))

        #CREDITOS
        if 550 + 223 > mouse[0] > 550 and 630 + 65 > mouse[1] > 630:
            screen.blit(cred_alt, (550,630))
            if press:
                if screenfull == 1:
                    print('1')
                    creditos.preview()
                else:
                    print('2')
                    creditos.preview(fullscreen=True)
                menu()

        else:
            screen.blit(cred, (550,630))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        pygame.display.flip()

def conf():
    
    ef_txt = 5
    music_txt = 5
    vol_ef = 0.5
    vol_music = 0.5

    #colocando na tela
    screen.blit(fundo_conf, (0, 0))
    pygame.draw.circle(surface, (0, 0, 0, 10), [100, 100], 7)

    #audio
    screen.blit(sfx_titulo, (200, 70))
    screen.blit(sfx_ef, (100, 154))
    screen.blit(sfx_musica, (205, 203))

    screen.blit(sfx_botao[0], (300, 150))
    screen.blit(sfx_botao[1], (382, 150))
    screen.blit(sfx_barra, (370, 145))

    screen.blit(sfx_botao[0], (300, 200))
    screen.blit(sfx_botao[1], (382, 200))
    screen.blit(sfx_barra, (370, 195))

    #video
    screen.blit(video_titulo, (670, 250))
    screen.blit(janela, (600, 355))
    screen.blit(full, (601, 390))

    #dificuldade
    screen.blit(dificuldade_titulo, (100, 350))
    screen.blit(facil, (100, 450))
    screen.blit(medio, (100, 485))
    screen.blit(dificil, (100, 520))

    screen.blit(aplicar, (width -320, height -90))
    screen.blit(fechar, (width -140, height -90))

    while pygame.event.wait() or pygame.event.get():
        
        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()

        #CONTROLE DE VOLUME
        if 300 + 62 > mouse[0] > 300 and 150 + 35 > mouse[1] > 150:
            if press[0]:
                screen.blit(sfx_click, (300, 150))
                vol_ef -= 0.1
                ef_txt -= 1               
                print (vol_ef)
            else:
                screen.blit(sfx_botao[0], (300, 150))

        if 382 + 62 > mouse[0] > 382 and 150 + 35 > mouse[1] > 150:
            if press[0]:
                screen.blit(sfx_click, (382, 150))
                vol_ef += 0.1
                ef_txt += 1

                print (vol_ef)
            else:
                screen.blit(sfx_botao[1], (382, 150))
        
        if 300 + 62 > mouse[0] > 300 and 200 + 35 > mouse[1] > 200:
            if press[0]:
                screen.blit(sfx_click, (300, 200))
                vol_music -= 0.1
                music_txt -= 1
                print (vol_music)
            else:
                screen.blit(sfx_botao[0], (300, 200))

        if 382 + 62 > mouse[0] > 382 and 200 + 35 > mouse[1] > 200:
            if press[0]:
                screen.blit(sfx_click, (382, 200))
                vol_music += 0.1
                music_txt += 1
                print (vol_music)
            else:
                screen.blit(sfx_botao[1], (382, 200))

        #DISPLAY
        #JANELA
        if 600 + 182 > mouse[0] > 600 and 355 + 25 > mouse[1] > 355:
            screen.blit(seleçao, (603, 358))
            if press[0]:
                fullscreen_off(screen)
                conf()
                for u in range(0, 10):
                    screen.blit(janela, (600, 355))
        else:
            screen.blit(surface, (603-91, 357-90))

        #FULLSCREEN
        if 601 + 164 > mouse[0] > 601 and 390 + 23 > mouse[1] > 390:
            screen.blit(seleçao, (603, 392))
            if press[0]:
                fullscreen_on(screen)
                conf()
                for u in range(0, 10):
                    screen.blit(full, (601, 390))
        else:
            screen.blit(surface, (603-91, 392-90))
        #DIFICULDADE
        #FACIL
        if 100 + 90 > mouse[0] > 100 and 450 + 25 > mouse[1] > 450:
            screen.blit(seleçao, (100, 454))
            if press[0]:
                faci()
                for u in range(0, 10):
                    screen.blit(facil, (100, 450))
        else:
            screen.blit(surface, (100-91, 454-90))
        
        #MEDIO
        if 100 + 100 > mouse[0] > 100 and 485 + 23 > mouse[1] > 485:
            screen.blit(seleçao, (100, 489))
            if press[0]:
                medi()
                for u in range(0, 10):
                    screen.blit(medio, (100, 485))
        else:
            screen.blit(surface, (100-91, 489-90))
            

        #DIFICIL
        if 100 + 100 > mouse[0] > 100 and 520 + 24 > mouse[1] > 520:
            screen.blit(seleçao, (100, 524))
            if press[0]:
                difi()
                for u in range(0, 10):
                    screen.blit(dificil, (100, 520))
        else:
            screen.blit(surface, (100-91, 524-90))
            

        #APLICAR E SAIR
        if (width-320) + 169 > mouse[0] > (width-320) and (height-90) + 58 > mouse[1] > (height-90):
            screen.blit(aplicar_alt, (width -318, height -87))
            if press[0]:
                vol()
                pygame.display.update()
        else:
            screen.blit(aplicar, (width -320, height -90))

        if (width-140) + 105 > mouse[0] > (width-140) and (height-90) + 55 > mouse[1] > (height-90):
            screen.blit(fechar_alt, (width -139, height -88))
            if press[0]:
                menu() 

        else:
            screen.blit(fechar, (width -140, height -90))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()

        def vol_min():
            Tk().wm_withdraw()
            messagebox.showwarning('ATENÇÃO', 'Volume Mínimo Alcançado')
        def vol_max():
            Tk().wm_withdraw()
            messagebox.showwarning('ATENÇÃO', 'Volume Máximo Alcançado')

        if vol_ef < 0:
            vol_ef = 0
            vol_min()

        if vol_music < 0:
            vol_music = 0
            vol_min()

        if vol_ef > 1:
            vol_ef = 1
            vol_max()

        if vol_music > 1:
            vol_music = 1
            vol_max()
        
        pygame.display.flip()

        def vol():
            menu_music.set_volume(vol_music)
            jogo_music.set_volume(vol_music)
            hard_music.set_volume(vol_music)
            jogar_saco.set_volume(vol_ef)
            click_music.set_volume(vol_ef)
    
def instruçoes():
    pags = 1
    screen.blit(pag1, (0, 0))

    while pygame.event.wait() or pygame.event.get():

        if pags == 1:
            screen.blit(pag1, (0, 0))
        elif pags == 2:
            screen.blit(pag2, (0, 0))
        elif pags == 3:
            screen.blit(pag3, (0, 0))
        elif pags == 4:
            screen.blit(pag4, (0, 0))
        elif pags == 5:
            screen.blit(pag5, (0, 0))
        

        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]
        comandos = pygame.key.get_pressed()

        

        if 530 + 20 > mouse[0] > 530 and 672 + 24 > mouse[1] > 672:
            screen.blit(proximo, (530, 672))
            if press:
                pags +=1
                pygame.display.flip()

        if 435 + 20 > mouse[0] > 435 and 672 + 24 > mouse[1] > 672:
            screen.blit(anterior, (435, 672))
            if pygame.mouse.get_pressed()[0]:
                pags -=1
                pygame.display.flip()

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if comandos[pygame.K_ESCAPE]:
            menu()
            

        if pags <= 0:
            pags = 5
        elif pags >= 6:
            pags = 1
            
        pygame.display.flip()

def game_over():
    screen.blit(gameover,(WIDTH/4.5, 200))
    screen.blit(gameover_novamente, (150,580))
    screen.blit(gameover_sair, (550,580))

    pygame.display.flip()

    while pygame.event.wait() or pygame.event.get():

        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]

        #JOGAR
        if 150 + 294 > mouse[0] > 150 and 580 + 95 > mouse[1] > 580:
            screen.blit(gameover_novamente_alt, (150, 580))
            if press:
                jogo_music.stop()
                jogo(n, b)
        else:
            screen.blit(gameover_novamente, (150, 580))

        #SAIR
        if 550 + 294 > mouse[0] > 550 and 580 + 95 > mouse[1] > 580:
            screen.blit(gameover_sair_alt, (550,580))
            if press:
                menu()
        else:
            screen.blit(gameover_sair, (550,580))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        pygame.display.flip()

def faci():
    lixos.LIXOVELOCIDADE = 10
    global b
    b = 0
    global n
    n = 10
    Tk().wm_withdraw()
    messagebox.showinfo('ATENÇÃO', 'DIFICULDADE DEFINIDA COMO FACIL')

def medi():   
    lixos.LIXOVELOCIDADE = 16
    buraco.LIXOVELOCIDADE = 16
    global b
    b = 1
    global n
    n = 16
    Tk().wm_withdraw()
    messagebox.showinfo('ATENÇÃO', 'DIFICULDADE DEFINIDA COMO MEDIO')

def difi():
    lixos.LIXOVELOCIDADE = 22
    buraco.LIXOVELOCIDADE = 22
    global b
    b = 2
    global n
    n = 22
    Tk().wm_withdraw()
    messagebox.showinfo('ATENÇÃO', 'DIFICULDADE DEFINIDA COMO DIFICIL')

def jogo(n, b):
    
    # objetos
    pontos = 0
    lixo_mochila = 50
    timer = 0
    buraco_time = 0
    contagem = 60
    collide = 0
    t = 2
    fps = 30
    j = 0
    x = 8
    bu = b

    objectGroup = pygame.sprite.Group()

    Lixo_group = pygame.sprite.Group()
    tiro_group = pygame.sprite.Group()

    buraco_group = pygame.sprite.Group()

    Player_group = pygame.sprite.Group()
    player = Player()
    Player_group.add(player)

    Carro_group = pygame.sprite.Group()
    carro = Carro()
    Carro_group.add(carro)

    all_group = pygame.sprite.Group()

    # Fundo
    bg = pygame.image.load('Imagens/jogo/fundosemobjetos.png').convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_y = 0

    # Sounds
    andar = pygame.mixer.Sound('Sons/passos.wav')

    # Música

    menu_music.stop()
    if bu == 0 or bu == 1:
        jogo_music.play()
    else:
        hard_music.play()

    val = n
    clock = pygame.time.Clock()
    tela = True
    while tela:
        clock.tick(fps)
        # Faz o Fundo continuar infinito
        bg_y1 = bg_y % bg.get_height()
        bg_y += val

        screen.blit(bg, (0, bg_y1 - bg.get_height()))

        if bg_y1 < HEIGHT:
            screen.blit(bg, (0, bg_y1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if t > 15:
                    if event.key == pygame.K_SPACE:
                        t = 0
                        atirar = tiro(objectGroup, tiro_group)

                        if lixo_mochila >= 1:
                            atirar.rect.center = player.rect.center
                            lixo_mochila -= 1
                            player.current_image = 0
                            jogar_saco.stop()
                            jogar_saco.play()

        t += 1
        timer += 1
        buraco_time += 1
        collide += 1

        if buraco_time == 60:
            buraco_time = 0
            if bu == 1:
                buraco = buracos(objectGroup, buraco_group)
            if bu == 2:
                for y in range(0, 2):
                    buraco = buracos(objectGroup, buraco_group)
        if timer == fps:
            #time.sleep(0.1)
            timer = 0
            lixol = LixoL(objectGroup, Lixo_group)
            lixor = LixoR(objectGroup, Lixo_group)
            contagem -= 1
        
        if contagem == 0:
            game_over()
            tela = False

        # Update
        objectGroup.update()

        #colisão
        if pygame.sprite.groupcollide(Lixo_group, Player_group, True, False):
            lixo_mochila += 1

        if pygame.sprite.groupcollide(tiro_group, Carro_group, True, False):
            pontos += 2
        
        if collide > 3:
            if pygame.sprite.groupcollide(Player_group, buraco_group, False, False):
                collide = 0
                if lixo_mochila > 0:
                    lixo_mochila -= 5
                if lixo_mochila < 0:
                    lixo_mochila = 0

        objectGroup.draw(screen)

        Player_group.update()
        Player_group.draw(screen)

        Carro_group.update()
        Carro_group.draw(screen)

        all_group.update()
        all_group.draw(screen)

        screen.blit(pts, (15, 20))
        screen.blit(mochila, (15, 80))
        screen.blit(time, (655, 20))

        text(screen, f"{pontos}", 50, 280, 15, (238, 175, 81, 0))
        text(screen, f"{lixo_mochila}", 30, 260, 80, (238, 175, 81, 0))
        text(screen, f"{contagem}", 30, 799, 22, (238, 175, 81, 0))

        pygame.display.update()

menu()
pygame.quit()
