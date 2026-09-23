import os
from pathlib import Path

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
desktop_size = (tela.current_w, tela.current_h)
resolution_options = [
    size for size in [(800, 600), (980, 720), (1280, 720), (1366, 768),
                      (1600, 900), (1920, 1080)]
    if size[0] <= desktop_size[0] and size[1] <= desktop_size[1]
]
if (980, 720) not in resolution_options:
    resolution_options.append((980, 720))
resolution_options.sort(key=lambda size: size[0] * size[1])
display_size = (980, 720)
window = pygame.display.set_mode(display_size)
# Toda a interface e o jogo usam esta superficie logica. Somente a apresentacao
# final e escalada, preservando coordenadas, proporcao e colisoes.
screen = pygame.Surface((WIDTH, HEIGHT)).convert()

screenfull = 1

def present():
    window_width, window_height = window.get_size()
    scale = min(window_width / WIDTH, window_height / HEIGHT)
    draw_size = (max(1, round(WIDTH * scale)), max(1, round(HEIGHT * scale)))
    offset = ((window_width - draw_size[0]) // 2, (window_height - draw_size[1]) // 2)
    window.fill((5, 10, 12))
    window.blit(pygame.transform.smoothscale(screen, draw_size), offset)
    pygame.display.flip()


def logical_mouse(position=None):
    mouse_x, mouse_y = position if position is not None else pygame.mouse.get_pos()
    window_width, window_height = window.get_size()
    scale = min(window_width / WIDTH, window_height / HEIGHT)
    draw_width, draw_height = WIDTH * scale, HEIGHT * scale
    offset_x = (window_width - draw_width) / 2
    offset_y = (window_height - draw_height) / 2
    return (int((mouse_x - offset_x) / scale), int((mouse_y - offset_y) / scale))


def set_display_mode(fullscreen, resolution):
    global window, screenfull, display_size
    display_size = resolution
    flags = pygame.FULLSCREEN if fullscreen else 0
    window = pygame.display.set_mode(display_size, flags)
    screenfull = 2 if fullscreen else 1


def fullscreen_off():
    set_display_mode(False, display_size)
    return screen

def fullscreen_on():
    set_display_mode(True, display_size)
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

# Configuracoes persistentes da sessao. Os valores antigos eram recriados toda
# vez que a tela era aberta, fazendo os controles parecerem inoperantes.
music_volume = 0.5
sfx_volume = 0.5
difficulty = "medio"

#INSTRUÇÕES
pag1 = pygame.image.load('Imagens/instruçoes/pág1.png')
pag1 = pygame.transform.scale(pag1, [WIDTH, HEIGHT])

pag2 = pygame.image.load('Imagens/instruçoes/pág2.png')
pag2 = pygame.transform.scale(pag2, [WIDTH, HEIGHT])

pag3 = pygame.image.load('Imagens/instruçoes/pág3.png')
pag3 = pygame.transform.scale(pag3, [WIDTH, HEIGHT])

pag4 = pygame.image.load('Imagens/instruçoes/pág4.png')
pag4 = pygame.transform.scale(pag4, [WIDTH, HEIGHT])

pag5 = pygame.image.load('Imagens/instruçoes/pág5.png')
pag5 = pygame.transform.scale(pag5, [WIDTH, HEIGHT])

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

    present()

    menu_music.stop()
    jogo_music.stop()
    hard_music.stop()
    menu_music.play(-1)

    while pygame.event.wait() or pygame.event.get():

        # Reconstroi o menu a cada quadro; telas modais nao deixam residuos.
        screen.blit(fundo, (0, 0))
        screen.blit(titulo, (290, 0))
        mouse = logical_mouse()
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
                # O loop espera o proximo evento; restaure o menu imediatamente.
                screen.blit(fundo, (0, 0))
                screen.blit(titulo, (290, 0))
                present()
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
            
        present()

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
        

        mouse = logical_mouse()
        press = pygame.mouse.get_pressed()[0]
        comandos = pygame.key.get_pressed()

        

        if 530 + 20 > mouse[0] > 530 and 672 + 24 > mouse[1] > 672:
            screen.blit(proximo, (530, 672))
            if press:
                pags +=1
                present()

        if 435 + 20 > mouse[0] > 435 and 672 + 24 > mouse[1] > 672:
            screen.blit(anterior, (435, 672))
            if pygame.mouse.get_pressed()[0]:
                pags -=1
                present()

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if comandos[pygame.K_ESCAPE]:
            menu()
            

        if pags <= 0:
            pags = 5
        elif pags >= 6:
            pags = 1
            
        present()

def conf():
    """Painel de configuracoes com layout fixo, estado persistente e sliders."""
    global music_volume, sfx_volume, difficulty, n, b

    draft_music = music_volume
    draft_sfx = sfx_volume
    draft_difficulty = difficulty
    draft_fullscreen = screenfull == 2
    draft_resolution = display_size
    dragging = None
    notice_until = 0
    clock = pygame.time.Clock()
    settings_background = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

    colors = {
        "overlay": (8, 18, 22, 218), "panel": (20, 42, 46),
        "card": (25, 51, 55), "border": (56, 91, 91),
        "text": (242, 246, 238), "muted": (164, 183, 177),
        "accent": (238, 175, 81), "accent_dark": (126, 83, 34),
        "success": (102, 198, 142),
    }
    title_font = pygame.font.Font(font_name, 38)
    section_font = pygame.font.Font(font_name, 23)
    body_font = pygame.font.Font(font_name, 18)
    small_font = pygame.font.Font(font_name, 15)

    music_track = pygame.Rect(94, 244, 300, 10)
    sfx_track = pygame.Rect(94, 344, 300, 10)
    difficulty_buttons = {
        "facil": pygame.Rect(535, 205, 105, 46),
        "medio": pygame.Rect(650, 205, 105, 46),
        "dificil": pygame.Rect(765, 205, 105, 46),
    }
    window_button = pygame.Rect(535, 365, 160, 52)
    fullscreen_button = pygame.Rect(710, 365, 160, 52)
    resolution_down = pygame.Rect(535, 465, 46, 42)
    resolution_up = pygame.Rect(824, 465, 46, 42)
    apply_button = pygame.Rect(620, 605, 205, 54)
    close_button = pygame.Rect(837, 605, 80, 54)

    def label(value, font, color, position, centered=False):
        image = font.render(value, True, color)
        rect = image.get_rect(center=position) if centered else image.get_rect(topleft=position)
        screen.blit(image, rect)

    def button(rect, value, selected=False, primary=False):
        hovered = rect.collidepoint(logical_mouse())
        if primary:
            fill = (250, 193, 103) if hovered else colors["accent"]
            text_color = (35, 29, 21)
        elif selected:
            fill = (150, 99, 40) if hovered else colors["accent_dark"]
            text_color = colors["text"]
        else:
            fill = (49, 82, 82) if hovered else (38, 67, 69)
            text_color = colors["text"]
        pygame.draw.rect(screen, fill, rect, border_radius=10)
        border = colors["accent"] if selected else colors["border"]
        pygame.draw.rect(screen, border, rect, 2, border_radius=10)
        label(value, body_font, text_color, rect.center, True)

    def slider(track, value):
        pygame.draw.rect(screen, (47, 69, 69), track, border_radius=5)
        fill = track.copy()
        fill.width = round(track.width * value)
        if fill.width:
            pygame.draw.rect(screen, colors["accent"], fill, border_radius=5)
        knob_x = track.left + round(track.width * value)
        pygame.draw.circle(screen, colors["text"], (knob_x, track.centery), 12)
        pygame.draw.circle(screen, colors["accent"], (knob_x, track.centery), 12, 3)
        label(f"{round(value * 100)}%", body_font, colors["text"],
              (track.right + 34, track.centery), True)

    def value_from_mouse(track, mouse_x):
        return max(0.0, min(1.0, (mouse_x - track.left) / track.width))

    def set_preview_volumes():
        menu_music.set_volume(draft_music)
        jogo_music.set_volume(draft_music)
        hard_music.set_volume(draft_music)
        jogar_saco.set_volume(draft_sfx)
        click_music.set_volume(draft_sfx)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                draft_music, draft_sfx = music_volume, sfx_volume
                set_preview_volumes()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                event_pos = logical_mouse(event.pos)
                if music_track.inflate(24, 34).collidepoint(event_pos):
                    dragging = "music"
                    draft_music = value_from_mouse(music_track, event_pos[0])
                    set_preview_volumes()
                elif sfx_track.inflate(24, 34).collidepoint(event_pos):
                    dragging = "sfx"
                    draft_sfx = value_from_mouse(sfx_track, event_pos[0])
                    set_preview_volumes()
                elif window_button.collidepoint(event_pos):
                    draft_fullscreen = False
                elif fullscreen_button.collidepoint(event_pos):
                    draft_fullscreen = True
                elif resolution_down.collidepoint(event_pos):
                    index = resolution_options.index(draft_resolution)
                    draft_resolution = resolution_options[(index - 1) % len(resolution_options)]
                    click_music.play()
                elif resolution_up.collidepoint(event_pos):
                    index = resolution_options.index(draft_resolution)
                    draft_resolution = resolution_options[(index + 1) % len(resolution_options)]
                    click_music.play()
                elif close_button.collidepoint(event_pos):
                    draft_music, draft_sfx = music_volume, sfx_volume
                    set_preview_volumes()
                    running = False
                elif apply_button.collidepoint(event_pos):
                    music_volume, sfx_volume = draft_music, draft_sfx
                    difficulty = draft_difficulty
                    speed, level = {
                        "facil": (10, 0), "medio": (16, 1), "dificil": (22, 2)
                    }[difficulty]
                    lixos.LIXOVELOCIDADE = buraco.LIXOVELOCIDADE = n = speed
                    b = level
                    set_preview_volumes()
                    if (draft_fullscreen != (screenfull == 2)
                            or draft_resolution != display_size):
                        set_display_mode(draft_fullscreen, draft_resolution)
                    click_music.play()
                    notice_until = pygame.time.get_ticks() + 1800
                else:
                    for option, rect in difficulty_buttons.items():
                        if rect.collidepoint(event_pos):
                            draft_difficulty = option
                            click_music.play()
                            break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                event_pos = logical_mouse(event.pos)
                if dragging == "music":
                    draft_music = value_from_mouse(music_track, event_pos[0])
                else:
                    draft_sfx = value_from_mouse(sfx_track, event_pos[0])
                set_preview_volumes()

        screen.blit(settings_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(colors["overlay"])
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(48, 38, WIDTH - 96, HEIGHT - 76)
        pygame.draw.rect(screen, colors["panel"], panel, border_radius=20)
        pygame.draw.rect(screen, colors["border"], panel, 2, border_radius=20)

        label("CONFIGURACOES", title_font, colors["text"], (82, 66))
        label("Ajuste sua experiencia de jogo", small_font, colors["muted"], (84, 111))
        pygame.draw.line(screen, colors["border"], (84, 143), (896, 143), 1)

        pygame.draw.rect(screen, colors["card"], (75, 166, 385, 365), border_radius=14)
        label("AUDIO", section_font, colors["accent"], (94, 183))
        label("Musica", body_font, colors["text"], (94, 211))
        slider(music_track, draft_music)
        label("Efeitos sonoros", body_font, colors["text"], (94, 311))
        slider(sfx_track, draft_sfx)
        label("Clique ou arraste para ajustar", small_font, colors["muted"], (94, 385))

        pygame.draw.rect(screen, colors["card"], (495, 166, 400, 365), border_radius=14)
        label("DIFICULDADE", section_font, colors["accent"], (520, 183))
        for option, rect in difficulty_buttons.items():
            button(rect, option.capitalize(), option == draft_difficulty)
        descriptions = {
            "facil": "Ritmo tranquilo, sem buracos.",
            "medio": "Ritmo equilibrado e obstaculos.",
            "dificil": "Mais velocidade e obstaculos.",
        }
        label(descriptions[draft_difficulty], small_font, colors["muted"], (535, 269))
        pygame.draw.line(screen, colors["border"], (520, 318), (870, 318), 1)
        label("MODO DE EXIBICAO", section_font, colors["accent"], (520, 336))
        button(window_button, "Janela", not draft_fullscreen)
        button(fullscreen_button, "Tela cheia", draft_fullscreen)
        label("RESOLUCAO", small_font, colors["muted"], (535, 442))
        button(resolution_down, "<")
        button(resolution_up, ">")
        resolution_text = f"{draft_resolution[0]} x {draft_resolution[1]}"
        label(resolution_text, body_font, colors["text"], (702, 486), True)
        label("Exibicao e resolucao mudam ao aplicar.", small_font,
              colors["muted"], (535, 512))

        if pygame.time.get_ticks() < notice_until:
            label("Configuracoes aplicadas", small_font, colors["success"], (84, 623))
        button(apply_button, "Aplicar alteracoes", primary=True)
        button(close_button, "Voltar")
        label("ESC para voltar", small_font, colors["muted"], (84, 652))
        present()

    pygame.event.clear([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])


def game_over():
    screen.blit(gameover,(WIDTH/4.5, 200))
    screen.blit(gameover_novamente, (150,580))
    screen.blit(gameover_sair, (550,580))

    present()

    while pygame.event.wait() or pygame.event.get():

        mouse = logical_mouse()
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
            
        present()

def faci():
    global b, n, difficulty
    lixos.LIXOVELOCIDADE = 10
    buraco.LIXOVELOCIDADE = 10
    b = 0
    n = 10
    difficulty = "facil"

def medi():   
    global b, n, difficulty
    lixos.LIXOVELOCIDADE = 16
    buraco.LIXOVELOCIDADE = 16
    b = 1
    n = 16
    difficulty = "medio"

def difi():
    global b, n, difficulty
    lixos.LIXOVELOCIDADE = 22
    buraco.LIXOVELOCIDADE = 22
    b = 2
    n = 22
    difficulty = "dificil"

def jogo(n, b):
    
    # objetos
    pontos = 0
    lixo_mochila = 0
    capacidade = 8
    timer = 0
    buraco_time = 0
    contagem = 60
    collide = 0
    fps = 30
    bu = b
    charge_start = None
    combo = 0
    last_hit = 0
    feedback = "Colete lixo e segure ESPACO para arremessar"
    feedback_until = pygame.time.get_ticks() + 3500
    dash_until = 0
    dash_ready = 0
    end_time = pygame.time.get_ticks() + 60000

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
        jogo_music.play(-1)
    else:
        hard_music.play(-1)

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
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tela = False
                elif event.key == pygame.K_SPACE and lixo_mochila > 0 and charge_start is None:
                    charge_start = pygame.time.get_ticks()
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    now = pygame.time.get_ticks()
                    if now >= dash_ready:
                        dash_until = now + 280
                        dash_ready = now + 2200
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE and charge_start is not None:
                charge = min(1.0, (pygame.time.get_ticks() - charge_start) / 1000)
                atirar = tiro(objectGroup, tiro_group,
                              speed=18 + round(charge * 18), charge=charge)
                atirar.rect.center = player.rect.center
                lixo_mochila -= 1
                charge_start = None
                player.current_image = 0
                jogar_saco.stop()
                jogar_saco.play()

        now = pygame.time.get_ticks()
        contagem = max(0, math.ceil((end_time - now) / 1000))
        player.move_speed = 24 if now < dash_until else 13
        if combo and now - last_hit > 2500:
            combo = 0
        timer += 1
        buraco_time += 1
        collide += 1

        if buraco_time >= {0: 90, 1: 65, 2: 48}[bu]:
            buraco_time = 0
            if bu == 1:
                buraco = buracos(objectGroup, buraco_group)
            if bu == 2:
                for y in range(0, 2):
                    buraco = buracos(objectGroup, buraco_group)
        if timer >= {0: 30, 1: 24, 2: 18}[bu]:
            timer = 0
            novo_lixo = LixoL(objectGroup, Lixo_group) if randint(0, 1) else LixoR(objectGroup, Lixo_group)
            novo_lixo.rect.x = randint(150, 810)
            if bu == 2 and randint(0, 2) == 0:
                extra = LixoL(objectGroup, Lixo_group)
                extra.rect.x = randint(150, 810)

        if contagem == 0:
            game_over()
            tela = False

        # Update
        objectGroup.update()

        # Coleta exige gerenciamento de capacidade: lixo excedente continua na pista.
        coletados = pygame.sprite.spritecollide(player, Lixo_group, False)
        if coletados and lixo_mochila < capacidade:
            coletados[0].kill()
            lixo_mochila += 1
            feedback = f"Mochila {lixo_mochila}/{capacidade}"
            feedback_until = now + 700

        # Pontuacao combina sequencia, precisao horizontal e carga ideal.
        acertos = pygame.sprite.spritecollide(carro, tiro_group, True)
        for acerto in acertos:
            combo = min(combo + 1, 9)
            last_hit = now
            distancia = abs(acerto.rect.centerx - carro.rect.centerx)
            bonus_precisao = 2 if distancia < 24 else 0
            bonus_carga = 2 if 0.55 <= acerto.charge <= 0.80 else 0
            ganho = 2 + combo + bonus_precisao + bonus_carga
            pontos += ganho
            if bonus_precisao and bonus_carga:
                feedback = f"PERFEITO! +{ganho}"
            elif bonus_precisao:
                feedback = f"PRECISAO! +{ganho}"
            else:
                feedback = f"ACERTO +{ganho}"
            feedback_until = now + 900
        
        if collide > 3:
            if pygame.sprite.spritecollide(player, buraco_group, True):
                collide = 0
                if lixo_mochila > 0:
                    lixo_mochila = max(0, lixo_mochila - 2)
                combo = 0
                feedback = "TROPECOU! Combo perdido"
                feedback_until = now + 1200

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
        text(screen, f"{lixo_mochila}/{capacidade}", 30, 270, 80, (238, 175, 81, 0))
        text(screen, f"{contagem}", 30, 799, 22, (238, 175, 81, 0))

        if combo > 1:
            text(screen, f"COMBO x{combo}", 25, 490, 24, (255, 213, 116))

        # Barra de carga: a faixa verde e o ponto ideal de forca.
        if charge_start is not None:
            charge = min(1.0, (now - charge_start) / 1000)
            bar = pygame.Rect(365, 665, 250, 18)
            pygame.draw.rect(screen, (24, 42, 44), bar, border_radius=8)
            ideal = pygame.Rect(bar.x + round(bar.width * .55), bar.y,
                                round(bar.width * .25), bar.height)
            pygame.draw.rect(screen, (65, 122, 78), ideal, border_radius=8)
            fill = bar.copy()
            fill.width = round(bar.width * charge)
            pygame.draw.rect(screen, (238, 175, 81), fill, border_radius=8)
            pygame.draw.rect(screen, (242, 246, 238), bar, 2, border_radius=8)
            text(screen, "FORCA", 16, 490, 640, (242, 246, 238))

        dash_left = max(0, dash_ready - now)
        dash_status = "SHIFT: DASH" if dash_left == 0 else f"DASH {dash_left / 1000:.1f}s"
        text(screen, dash_status, 16, 865, 675, (242, 246, 238))
        if now < feedback_until:
            text(screen, feedback, 19, 490, 105, (255, 224, 156))

        present()

menu()
pygame.quit()
