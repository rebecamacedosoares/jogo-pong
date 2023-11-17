import pygame
import sys
import random
import time
import mysql.connector

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = 1280
        self.altura = 720
        self.fonte = pygame.font.SysFont("Consolas", int(self.largura/20))
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.relogio = pygame.time.Clock()
        self.icone = pygame.image.load('heart.ico')

        pygame.display.set_icon(self.icone)
        pygame.display.set_caption("Jogo de Pong")

        self.jogador1 = pygame.Rect(0, 0, 10, 100)
        self.jogador1.center = (100, self.altura/2)
        self.jogador1_img = pygame.image.load("robot.png")

        self.jogador2 = pygame.Rect(0, 0, 10, 100)
        self.jogador2.center = (self.largura-100, self.altura/2)
        self.jogador2_img = pygame.image.load("hamster.png")

        self.pontuacao_jogador1 = 0
        self.pontuacao_jogador2 = 0

        self.bola = pygame.Rect(0, 0, 20, 20)
        self.bola.center = (self.largura/2, self.altura/2)

        self.velocidade_x = 1
        self.velocidade_y = 1

        self.tempo_inicio = time.time()

        # Conexão com o banco de dados
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='Pong'
        )
        self.cursor = self.conexao.cursor()


    def tratar_entrada(self):
        # Trata entrada de eventos de teclado, as teclas são w e s para o jogador 1 e as setas para cima e para baixo são para o jogador 2
        teclas_pressionadas = pygame.key.get_pressed()

        if teclas_pressionadas[pygame.K_w]:
            if self.jogador1.top > 0:
                self.jogador1.top -= 2
        if teclas_pressionadas[pygame.K_s]:
            if self.jogador1.bottom < self.altura:
                self.jogador1.bottom += 2

        if teclas_pressionadas[pygame.K_UP]:
            if self.jogador2.top > 0:
                self.jogador2.top -= 2
        if teclas_pressionadas[pygame.K_DOWN]:
            if self.jogador2.bottom < self.altura:
                self.jogador2.bottom += 2

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def tratar_colisoes(self):
        # Trata colisões e determina a pontuação dos jogadores
        if self.bola.y >= self.altura:
            self.velocidade_y = -1
        if self.bola.y <= 0:
            self.velocidade_y = 1
        if self.bola.x <= 0:
            self.pontuacao_jogador2 += 1
            self.verificar_vitoria(self.pontuacao_jogador2, "2")
            self.resetar_bola()

        if self.bola.x >= self.largura:
            self.pontuacao_jogador1 += 1
            self.verificar_vitoria(self.pontuacao_jogador1, "1")
            self.resetar_bola()

        if self.jogador1.colliderect(self.bola) and self.velocidade_x < 0:
            self.velocidade_x = 1
        if self.jogador2.colliderect(self.bola) and self.velocidade_x > 0:
            self.velocidade_x = -1


    def verificar_vitoria(self, pontuacao, jogador):
        # Verifica qual jogador venceu a partida
        if pontuacao >= 10:
            tempo_final = time.time()
            tempo_total = tempo_final - self.tempo_inicio
            mensagem_vitoria = f"Parabéns, o jogador {jogador} venceu!"
            mensagem_tempo = f"Tempo total: {tempo_total:.2f} segundos"

            # Salva os dados da partida no banco de dados
            self.cursor.execute('INSERT INTO jogo (tempo, vencedor) VALUES (%s, %s)', (tempo_total, jogador))
            self.conexao.commit()

            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                self.tela.fill("Black")
                vitoria_texto = self.fonte.render(mensagem_vitoria, True, "#6495ED")
                tempo_total_texto = self.fonte.render(mensagem_tempo, True, "#6495ED")
                vitoria_texto_posicao = (self.largura/2 - vitoria_texto.get_width()/2, self.altura/2 - vitoria_texto.get_height() - 20)
                tempo_total_texto_posicao = (self.largura/2 - tempo_total_texto.get_width()/2, self.altura/2 + 20)

                coroa_img = pygame.image.load("coroa.png")
                coroa_img_posicao = (self.largura/2 - coroa_img.get_width()/2, self.altura/2 - coroa_img.get_height() - 100)
                self.tela.blit(coroa_img, coroa_img_posicao)

                self.tela.blit(vitoria_texto, vitoria_texto_posicao)
                self.tela.blit(tempo_total_texto, tempo_total_texto_posicao)

                pygame.display.update()
                pygame.time.wait(3000)


    def resetar_bola(self):
        # Após um jogador marcar 1 ponto, as configurações da bola são resetadas
        self.bola.center = (self.largura/2, self.altura/2)
        self.velocidade_x = random.choice([-1, 1])
        self.velocidade_y = random.choice([-1, 1])


    def atualizar_tela(self):
        # Atualiza a tela com as pontuações dos jogadores, velocidade da bola, imagens e desenhos
        pontuacao_texto = self.fonte.render(f"{self.pontuacao_jogador1} : {self.pontuacao_jogador2}", True, "#6495ED")
        pontuacao_texto_posicao = (self.largura/2 - pontuacao_texto.get_width()/2, 50)

        self.bola.x += self.velocidade_x * 1.5
        self.bola.y += self.velocidade_y * 1.5

        self.tela.fill("Black")

        pygame.draw.rect(self.tela, "#6495ED", self.jogador2)
        pygame.draw.rect(self.tela, "#6495ED", self.jogador1)
        pygame.draw.circle(self.tela, "#6495ED", self.bola.center, 10)

        # Posição do jogador1_img à esquerda de jogador1
        jogador1_img_pos = (self.jogador1.left - self.jogador1_img.get_width(), self.jogador1.centery - self.jogador1_img.get_height() // 2)
        self.tela.blit(self.jogador1_img, jogador1_img_pos)

        self.tela.blit(self.jogador2_img, self.jogador2)
        self.tela.blit(pontuacao_texto, pontuacao_texto_posicao)

        pygame.display.update()


    def loop_jogo(self):
        # Executa o loop do jogo
        self.resetar_bola()
        while True:
            self.tratar_entrada()
            self.tratar_colisoes()
            self.atualizar_tela()
            self.relogio.tick(300)


jogo = Jogo()
jogo.loop_jogo()
