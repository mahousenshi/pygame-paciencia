from card import Card
from random import shuffle
import pygame



def surface(color):  # DEBUG - Imprime retângulos semitransparentes
    s = pygame.Surface((114, 162))
    s.set_alpha(128)
    s.fill(tuple(color))

    return s


class Game:
    # Esta classe é mais um conteiner que tem todas as varieveis do jogo.

    def __init__(self, tick=0):
        # Incicializa o baralho e o jogo.
        values = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
        suits = ['h', 'c', 'd', 's']

        # Cria o baralho
        deck = [Card(value, suit) for suit in suits for value in values]

        # Embaralha
        shuffle(deck)
        shuffle(deck)

        '''
        Aqui vamos crias as colunas e o seus respectivos retângulos para
        facilitar na hora das colizões.
        '''
        # Fundação: É para aonde as cartas irão em ordem.
        self.foundations_r = [pygame.Rect(29 + 172 * (3 + i), 20, 114, 162) for i in range(4)]
        self.foundations = [[], [], [], []]

        # Tablueiro: É aonde as cartas ficarao no tabuleiro.
        self.tableaus_r = [pygame.Rect(29 + 172 * i, 212, 114, 800) for i in range(7)]
        self.tableaus = []
        for i in range(1, 8):
            stack = []

            for j in range(i):
                card = deck.pop()
                card.rect.x = 29 + 172 * (i - 1)
                card.rect.y = 212 + 46 * j
                stack.append(card)

            stack[-1].flip()
            self.tableaus.append(stack)

        # Pesca: É para onde as cartas que não foram ao tabuleiro vai.
        self.stock_r = pygame.Rect(29, 20, 114, 162)
        self.stock = []
        while deck:
            card = deck.pop()
            card.set_rect_coord(self.stock_r)
            self.stock.append(card)

        # Lixo: É para aonde as cartas da pesca vão abertas
        self.waste_r = pygame.Rect(29 + 172, 20, 114, 162)
        self.waste = []

        # Aqui fica o monte de cartas clicado.
        self.clicked = []
        '''
        Aqui fica ande qual monte a carta para o caso de um movimento ilegal
        saber para onde voltar.
        '''
        self.source = ''

        # Coisas do duplo clique
        self.last_click = tick

        # Só para ter a imagem de um espaço vazio em memória.
        self.empty = pygame.image.load('imgs/empty.png')

    def reset(self, tick):
        # Reseta o tabuleiro
        self.__init__(tick)

    '''
    Aqui fica como foi cuidado cada envento, decidi quebrar assim por partes
    para tentar diminuir a quantidade de ifs que acabam deixando o codigo
    bem inelegivel.
    '''

    def mousedown(self, event, now):
        # Eventos de quando se clica nas cartas ou retângulos.
        double_click = False

        if event.button == 1:
            # Detecta um clique duplo
            if now - self.last_click <= 200:
                double_click = True
            self.last_click = now

            # Monte de pesca:
            if self.stock_r.collidepoint(event.pos):
                if self.stock:
                    # Se tiver cartas então manda para o lixo.
                    card = self.stock.pop()
                    card.set_rect_coord(self.waste_r)
                    card.flip()
                    self.waste.append(card)
                else:
                    # Se não retiver cartas então refaz o monte.
                    while self.waste:
                        card = self.waste.pop()
                        card.set_rect_coord(self.stock_r)
                        card.flip()
                        self.stock.append(card)

            # Lixo:
            if self.waste_r.collidepoint(event.pos) and self.waste:
                # Se tiver alguma carta então colocar na lista de clicados.
                if double_click:
                    # Se for um clique duplo verifica se encaixa na fundação
                    for i, foundation in enumerate(self.foundations):
                        if foundation:
                            card = foundation[-1]

                            if card.follows(self.waste[-1]) and card.same_suit(self.waste[-1]):
                                self.waste[-1].set_rect_coord(self.foundations_r[i])
                                self.foundations[i].append(self.waste.pop())
                                break

                        elif self.waste[-1].value == 'a':
                            self.waste[-1].set_rect_coord(self.foundations_r[i])
                            self.foundations[i].append(self.waste.pop())
                            break
                else:
                    # Se for um clique simples só coloca no clicked
                    self.clicked.append(self.waste.pop())
                    self.source = 'waste'

            # Fundação:
            for i, foundation in enumerate(self.foundations_r):
                # Mesmo que o lixo só que aqui fundação é uma lista.
                if foundation.collidepoint(event.pos) and self.foundations[i]:
                    self.clicked.append(self.foundations[i].pop())
                    self.source = f'foundation{i}'
                    break

            # Tabuleiro:
            for i, tableau in enumerate(self.tableaus):
                for j, card in enumerate(reversed(tableau)):
                    '''
                    Como a checagem é por ponto então um mesmo retangulo pode
                    ser clicado, com a orderm tradicional o mais acima é
                    clicado primeiro então devemos checar a ordem inversa.
                    '''
                    if card.rect.collidepoint(event.pos) and card.up:
                        # Só faz sentido se carta estiver aberta.
                        if double_click and not j:
                            # Aqui o clique duplo só faz sentido para j == 0
                            for k, foundation in enumerate(self.foundations):
                                if foundation:
                                    card_f = foundation[-1]

                                    if card_f.follows(card) and card_f.same_suit(card):
                                        card.set_rect_coord(self.foundations_r[k])
                                        self.foundations[k].append(self.tableaus[i].pop())

                                        # Vira a carta se tiver
                                        if self.tableaus[i] and not self.tableaus[i][-1].up:
                                            self.tableaus[i][-1].flip()
                                        break

                                elif card.value == 'a':
                                    card.set_rect_coord(self.foundations_r[k])
                                    self.foundations[k].append(self.tableaus[i].pop())

                                    if self.tableaus[i] and not self.tableaus[i][-1].up:
                                        self.tableaus[i][-1].flip()
                                    break

                        if self.tableaus[i]:
                            '''
                            Podemos ter multiplas cartas indo para o clicked
                            aqui
                            '''
                            j += 1
                            while j:
                                self.clicked.append(self.tableaus[i].pop())
                                j -= 1

                            self.source = f'tableau{i}'
                            break

    def mousemotion(self, event):
        # Eventos de quando se move o mouse.
        if self.clicked:  # and self.clicked[-1].rect.collidepoint(event.pos):
            '''
            Aqui vamos manipular o retangulo da ultima carta do monte de cartas
            clicadas. Só é preciso atualizar esta carta.
            '''
            self.clicked[-1].rect.move_ip(event.rel)

    def mouseup(self, event):
        # Eventos de quando se solta o botão do "mouse".
        if event.button == 1 and self.clicked:
            # Fundação
            for i, foundation in enumerate(self.foundations_r):
                if foundation.collidepoint(event.pos) and len(self.clicked) == 1:
                    # Só pode colocar uma carta de cada vez na fundação.
                    if self.foundations[i]:
                        '''
                        Se ja tem cartas tem que verificar se a carta de fora
                        tem o mesmo naipe e é a proxima;
                        '''
                        card = self.foundations[i][-1]

                        if card.follows(self.clicked[-1]) and card.same_suit(self.clicked[-1]):
                            self.clicked[-1].set_rect_coord(foundation)
                            self.foundations[i].append(self.clicked.pop())

                            self.flip_tableau()

                    elif self.clicked[-1].value == 'a':
                        # Se estiver vazio aceita somente se for um Ás.
                        self.clicked[-1].set_rect_coord(foundation)
                        self.foundations[i].append(self.clicked.pop())

                        self.flip_tableau()

                    break

            # Tabuleiro
            for i, tableau in enumerate(self.tableaus_r):
                if tableau.collidepoint(event.pos):
                    j = len(self.tableaus[i])

                    if self.tableaus[i]:
                        '''
                        Se tem uma carta no tabuleiro devemos verificar se ela
                        e de outra cor e é a posterior
                        '''
                        card = self.tableaus[i][-1]

                        if self.clicked[-1].follows(card) and not card.same_color(self.clicked[-1]):
                            while self.clicked:
                                other = self.clicked.pop()
                                other.rect.x = self.tableaus_r[i].x
                                other.rect.y = self.tableaus_r[i].y + 46 * j
                                self.tableaus[i].append(other)
                                j += 1

                            self.flip_tableau()

                    # elif self.clicked[-1].value == 'k':
                    else:
                        '''
                        A versão oficial só aceita um reis, mas aqui estamos
                        aceitando todas as cartas.
                        '''
                        while self.clicked:
                            other = self.clicked.pop()
                            other.rect.x = self.tableaus_r[i].x
                            other.rect.y = self.tableaus_r[i].y + 46 * j
                            self.tableaus[i].append(other)
                            j += 1

                        self.flip_tableau()

            if self.clicked:
                '''
                Se foi solta e se ainda o monte clicked não esta vazio então é
                porque ou o movimento é ilegal ou o retangulo não colidiu com
                nada, então deve voltar para a lugar de origem.
                '''
                # Lixo
                if self.source == 'waste':
                    self.clicked[-1].set_rect_coord(self.waste_r)
                    self.waste.append(self.clicked.pop())

                # Fundação:
                elif self.source.startswith('foundation'):
                    i = int(self.source[-1])

                    self.clicked[-1].set_rect_coord(self.foundations_r[i])
                    self.foundations[i].append(self.clicked.pop())

                # Tabuleiro:
                elif self.source.startswith('tableau'):
                    i = int(self.source[-1])
                    j = len(self.tableaus[i])

                    while self.clicked:
                        other = self.clicked.pop()
                        other.rect.x = self.tableaus_r[i].x
                        other.rect.y = self.tableaus_r[i].y + 46 * j
                        self.tableaus[i].append(other)
                        j += 1

            # De qualquer modo é bom resetar o clicked
            self.clicked = []
            self.source = ''

    def flip_tableau(self):
        if self.source.startswith('tableau'):
            i = int(self.source[-1])

            if self.tableaus[i] and not self.tableaus[i][-1].up:
                self.tableaus[i][-1].flip()

    @staticmethod
    def draw_list_or_empty(window, lst, empty, rect):
        # Ajuda a imprimir um espaço vazio ou a última carta do monte.
        window.blit(lst[-1].image if lst else empty, (rect.x, rect.y))

    def draw(self, window):
        # Parte responsavel para desenhar as cartas.
        '''
        Desenha os montes de pescas e lixo. Se não tiver cartas desenha um
        espaço vazio.
        '''
        # Pesca
        self.draw_list_or_empty(window, self.stock, self.empty, self.stock_r)
        # Vazio
        self.draw_list_or_empty(window, self.waste, self.empty, self.waste_r)

        # Fundação:
        for i, foundation in enumerate(self.foundations):
            self.draw_list_or_empty(window, foundation, self.empty, self.foundations_r[i])

        # Tabuleiro:
        for i, tableau in enumerate(self.tableaus):  # DEBUG -> tirar o enumerate
            # pygame.draw.rect(window, [255, 0, 0], self.tableaus_r[i])  # DEBUG
            for card in tableau:
                window.blit(card.image, (card.rect.x, card.rect.y))
                # window.blit(surface(card.rect_color), (card.rect.x, card.rect.y))  # DEBUG
                # pygame.draw.rect(window, card.rect_color, card.rect)  # DEBUG

        # Clicked
        if self.clicked:
            x = self.clicked[-1].rect.x
            y = self.clicked[-1].rect.y

            for i, card in enumerate(reversed(self.clicked)):
                window.blit(card.image, (x, y + 46 * i))
