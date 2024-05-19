import pygame.sprite
from random import randint  #Debug


class Card(pygame.sprite.Sprite):
    '''
    Cada carta é um objeto "Sprite" do pygame que pode carregar uma imagem e um
    retangulo. A imagem é a "cara" da carta e o retangulo servira para fazer a
    colizão entre as colunas, guarda outros atributos como valor, naiper e se a
    carta está aberta ou não.
    '''
    # Usado para saber qual é a ordem das cartas.
    order = 'a234567891jqk'

    def __init__(self, value, suit):
        # Incicializa.
        super().__init__()

        self.value = value
        self.suit = suit

        self.up = False
        self.color = 'black' if self.suit in ['c', 's'] else 'red'

        self.image = pygame.image.load('imgs/back.png')
        self.rect = self.image.get_rect()

        self.rect_color = [randint(0, 255), randint(0, 255), randint(0, 255)]  # DEBUG

    def set_rect_coord(self, rect):
        '''
        O "pygame.Rectangle" é um objeto transparente que servira verificar
        colizão entre os montes e de cartas, assim devemos atualizar a sua
        posição de acordo onde representa pela imagem.
        '''
        self.rect.x = rect.x
        self.rect.y = rect.y

    def flip(self):
        # Serve para tanto para abre ou fechar as cartas.
        if self.up:
            self.up = False
            self.image = pygame.image.load('imgs/back.png')
        else:
            self.up = True
            self.image = pygame.image.load(f'imgs/{self.value}{self.suit}.png')

    def follows(self, other):
        '''
        Verifica se o valor da carta 'self' é o proximo da carta 'other' na
        ordem das cartas.
        '''
        return True if Card.order.index(self.value[0]) == Card.order.index(other.value[0]) - 1 else False

    def same_suit(self, other):
        # Verifica se o valor da carta de 'self' e 'other' tem o mesmo naipe.
        return self.suit == other.suit

    def same_color(self, other):
        # Verifica se a carta 'self' e 'other' tem o mesmo naipe.
        return self.color == other.color

    def __repr__(self):
        # Representação da classe.
        return f'{self.value}{self.suit}'
