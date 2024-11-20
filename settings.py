import os
#Arquivo de configurções gerais do jogo, como cores, imagens, sons, etc.
class General:
    WIDTH = 800
    HEIGHT = 600

class Colors:
    PINK = (255, 105, 180)
    CIANO = (139, 219, 220)
    DARK_PINK = (255, 20, 147)
    WHITE = (255, 255, 255)
    GREEN = (194, 255, 114)
    RED = (255, 0, 0)


#Caminho das imagens e sons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class Images:
    rocket = os.path.join(BASE_DIR, 'sources/rocket.png')
    background_home = os.path.join(BASE_DIR, 'sources/background-home.png')
    background_game = os.path.join(BASE_DIR, 'sources/background-game.png')
    enemy = os.path.join(BASE_DIR, 'sources/enemy.png')
    background_loss = os.path.join(BASE_DIR, 'sources/background-loss.png')
    background_win = os.path.join(BASE_DIR, 'sources/background-win.png')

class Sounds:
    click = os.path.join(BASE_DIR, 'sources/click-sound.mp3')
    background = os.path.join(BASE_DIR, 'sources/background-sound.mp3')
    laser = os.path.join(BASE_DIR, 'sources/laser-sound.mp3')
    enemy_laser = os.path.join(BASE_DIR, 'sources/enemy-laser-sound.mp3')