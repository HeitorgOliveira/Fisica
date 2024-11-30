import pygame as pg
import pygame_gui as pg_gui
import math
import random

### PARÂMETROS DA SIMULAÇÃO ###
G = 6.67430 # Constante gravitacional com magnitude menor

# Estrelas
RAIO_ESTRELA = 50
COR_ESTRELA = (255, 165, 0) #Laranja
QUANT_ESTRELAS = 500 # Quantidade inicial padrão de estrelas
# Range da velocidade das estrelas
LIM_INF_VEL_ESTRELA = 0
LIM_SUP_VEL_ESTRELA = 0
# Range da massa da estrela
LIM_INF_MASSA_ESTRELA = 100000000
LIM_SUP_MASSA_ESTRELA = 100000000


# Planetas
RAIO_PLANETA = 25
COR_PLANETA = (144, 238, 144) # Verde
QUANT_PLANETAS = 500 # Quantidade inicial padrão de planetas
# Range da velocidade dos planetas
LIM_INF_VEL_PLANETA = -1000
LIM_SUP_VEL_PLANETA = 1000
# Range da massa da estrela
LIM_INF_MASSA_PLANETA = 10
LIM_SUP_MASSA_PLANETA = 100
### CONSTANTES DA SIMULAÇÃO ###

pg.init() # Inicializando o pygame

### CONFIGURAÇÕES DA JANELA/GUI ###
LARGURA, ALTURA = 1250, 700 # Dimensões da janela
# Configurações do espaço virtual
ESCALA = 7
ESPACO_VIRT_LARG = LARGURA * ESCALA
ESPACO_VIRT_ALT = ALTURA * ESCALA

tela = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Simulação Espaço") # Título da janela
clock = pg.time.Clock() # Inicializando o clock para controlar o FPS

gui = pg_gui.UIManager((LARGURA, ALTURA)) # Inicializando a GUI

# Configuração dos "rótulos" (onde vão os sliders)
rot_estrelas = pg_gui.elements.UILabel(
  relative_rect = pg.Rect((10, 10), (250, 50)), # Posição e tamanho do rótulo
  text = "Quantidade de Estrelas", # Exibe a quantidade de estrelas atualmente selecionada
  manager = gui, 
)

rot_planetas = pg_gui.elements.UILabel(
  relative_rect = pg.Rect((10, 110), (250, 30)), # Posição e tamanho do rótulo
  text = "Quantidade de Planetas", # Exibe a quantidade de planetas atualmente selecionada
  manager = gui, 
)

rot_slider_estrelas = pg_gui.elements.UILabel(
  relative_rect = pg.Rect((220, 10), (100, 50)), # Posição e tamanho do rótulo
  text = str(QUANT_ESTRELAS), # Exibe a quantidade de estrelas atualmente selecionada
  manager = gui, 
)

rot_slider_planetas = pg_gui.elements.UILabel(
  relative_rect = pg.Rect((220, 110), (100, 50)), # Posição e tamanho do rótulo
  text = str(QUANT_PLANETAS), # Exibe a quantidade de planetas atualmente selecionada
  manager = gui, 
)

# Sliders
slider_estrelas = pg_gui.elements.UIHorizontalSlider(
  relative_rect = pg.Rect((10, 50), (200, 50)), # Posição e tamanho do rótulo
  start_value = QUANT_ESTRELAS, # Quantidade inicial padrão de estrelas
  value_range = (0, 1000), # Limites do slider
  manager = gui,
)

slider_planetas = pg_gui.elements.UIHorizontalSlider(
  relative_rect = pg.Rect((10, 150), (200, 50)), # Posição e tamanho do rótulo
  start_value = QUANT_PLANETAS, # Quantidade inicial padrão de planetas
  value_range = (0, 1000), # Limites do slider
  manager = gui,
)

# Botão de inicar
botao_iniciar = pg_gui.elements.UIButton(
  relative_rect = pg.Rect((10, 220), (100, 50)), # Posição e tamanho do botão
  text = "Iniciar", # Texto dentro do botão
  manager = gui,
)
### CONFIGURAÇÕES DA JANELA/GUI ###

### CLASSE DAS ESTRELAS E DOS PLANETAS ###
class CorpoCeleste:
  """
  Classe base para representar corpos celestes genéricos
    
  Atributos:
    x (float): Coordenada x no espaço
    y (float): Coordenada y no espaço
    vx (float): Velocidade no eixo x
    vy (float): Velocidade no eixo y
    massa (float): Massa do corpo celeste
    raio (float): Raio do corpo celeste
    ativo (bool): Estado do corpo (True se ativo, False se desativado)
    cor (tuple): Cor do corpo no formato RGB
    """

  def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.massa = massa
    self.raio = raio
    self.ativo = True
    self.cor = cor


class Estrela(CorpoCeleste):
  """
  Classe que representa uma estrela, herdando de CorpoCeleste.
    
  Utiliza os mesmos atributos e comportamento de CorpoCeleste.
  """

  def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
    super().__init__(x, y, vx, vy, massa, raio, cor)


class Planeta(CorpoCeleste):
  """
  Classe que representa um planeta, herdando de CorpoCeleste.
    
  Utiliza os mesmos atributos e comportamento de CorpoCeleste.
  """

  def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
    super().__init__(x, y, vx, vy, massa, raio, cor)
### CLASSE DAS ESTRELAS E DOS PLANETAS ###


### FUNÇÕES ###
def atualizar_informacoes():
  """
  Atualiza a quantidade de estrelas e planetas (globalmente) com base no valor inserido no slider
  """
  global QUANT_ESTRELAS, QUANT_PLANETAS
  QUANT_ESTRELAS = int(slider_estrelas.get_current_value())
  QUANT_PLANETAS = int(slider_planetas.get_current_value())

def modulo(x: float) -> float:
  """
  Retorna o módulo de um número

  Parâmetros:
    x (float): Número

  Retorno
    modulo (float): Módulo de x
  """
  modulo = x
  if x < 0:
    modulo = -x
  
  return modulo

def gerar_posicao_aleatoria() -> tuple:
  """
  Gera coordenadas (x, y) aleatórias dentro do espaço virtual definido

  Parâmetros:
  
  Retorno:
    x, y (tuple): Coordendas (x, y)
  """

  x = random.uniform(0, ESPACO_VIRT_LARG)
  y = random.uniform(0, ESPACO_VIRT_ALT)

  return x, y

def criar_estrelas(quant_estrelas: int) -> list:
  """
  Cria uma lista de objetos da classe Estrela com atributos gerados aleatoriamente

  Parâmetros:
    quant_estrelas (int): Quantidade de estrelas a serem geradas

  Rertorno:
    listaEstrelas: Lista de objetos Estrela
  """

  # Lista de objetos Estrela
  listaEstrelas = []

  # Criando uma estrela com os parâmetros definidos, e adicionando ela à lista
  for _ in range(quant_estrelas):
    x, y = gerar_posicao_aleatoria()

    listaEstrelas.append(Estrela(
      x, y, # Coordendas iniciais x e y
      random.uniform(LIM_INF_VEL_ESTRELA, LIM_SUP_VEL_ESTRELA), # Vx
      random.uniform(LIM_INF_VEL_ESTRELA, LIM_SUP_VEL_ESTRELA), # Vy
      random.uniform(LIM_INF_MASSA_ESTRELA, LIM_SUP_MASSA_ESTRELA), # Massa
      RAIO_ESTRELA, COR_ESTRELA
    ))

  return listaEstrelas

def criar_planetas(quant_planetas: int) -> list:
  """
  Cria uma lista de objetos da classe Estrela com atributos gerados aleatoriamente

  Parâmetros:
    quant_planetas (int): Quantidade de planetas a serem gerados

  Rertorno:
    listaPlanetas: Lista de objetos Planeta
  """

  # Lista de objetos Planeta
  listaPlanetas = []

  # Criando um planeta com os parâmetros definidos, e adicionando ela à lista
  for _ in range(quant_planetas):
    x, y = gerar_posicao_aleatoria()

    listaPlanetas.append(Planeta(
      x, y, # Coordendas iniciais x e y
      random.uniform(LIM_INF_VEL_PLANETA, LIM_SUP_VEL_PLANETA), # Vx
      random.uniform(LIM_INF_VEL_PLANETA, LIM_SUP_VEL_PLANETA), # Vy
      random.uniform(LIM_INF_MASSA_PLANETA, LIM_SUP_MASSA_PLANETA), # Massa
      RAIO_PLANETA, COR_PLANETA
    ))

  return listaPlanetas

def interacao_corpos(corpoA, corpoB : CorpoCeleste):
  """
  Calcula a interação gravitacional entre dois corpos e altera as velocidades dos corpos de acordo

  Parâmetros:
  corpoA (CorpoCeleste): Primeiro corpo envolvido
  corpoB (CorpoCeleste): Segundo corpo envolvido

  Retorno:

  """

  # Calculando a distância entre os dois corpos
  distX = corpoB.x - corpoA.x
  distY = corpoB.y - corpoA.y
  distanciaAB = math.sqrt(distX ** 2 + distY ** 2)

  # Para evitar uma divisão por zero, verificamos se a distância é maior que um limite mínimo
  if distanciaAB > 0.01:
    # Calculando o valor da força gravitacional entre esses dois corpos
    forcaGrav = G * corpoA.massa * corpoB.massa / (distanciaAB ** 2)

    # Calculando as acelerações de cada corpo, em cada eixo
    ax_corpoA = forcaGrav * distX / (distanciaAB * corpoA.massa)
    ay_corpoA = forcaGrav * distY / (distanciaAB * corpoA.massa)

    ax_corpoB = -forcaGrav * distX / (distanciaAB * corpoB.massa)
    ay_corpoB = -forcaGrav * distY / (distanciaAB * corpoB.massa)

    # Atualizando as velocidades dos corpos
    corpoA.vx += ax_corpoA
    corpoA.vy += ay_corpoA

    corpoB.vx += ax_corpoB
    corpoB.vy += ay_corpoB

def atualizar_corpos():
  """
  Atualiza as posições de todas as estrelas e planetas ativos no momento

  Parâmetros:

  Retorno: 

  """

  # Estrelas
  for i in range(QUANT_ESTRELAS):
    # Pulando estrelas inativas
    if not estrelas[i].ativo:
      continue

    # Calculando interações entre estrelas
    for j in range(i + 1, QUANT_ESTRELAS):
      if estrelas[j].ativo:
        interacao_corpos(estrelas[i], estrelas[j])

    # Calculando interações entre estrelas e planetas
    for j in range(QUANT_PLANETAS):
      if planetas[j].ativo:
        interacao_corpos(estrelas[i], planetas[j])

    # Atualizando as posições das estrelas
    estrelas[i].x += estrelas[i].vx
    estrelas[i].y += estrelas[i].vy


  # Planetas
  for i in range(QUANT_PLANETAS):
    # Pulando planetas inativos
    if not planetas[i].ativo:
      continue

    # Calculando interações entre planetas
    for j in range(i + 1, QUANT_PLANETAS):
      if planetas[j].ativo:
        interacao_corpos(planetas[i], planetas[j])

    # Atualizando as posições dos planetas
    planetas[i].x += planetas[i].vx
    planetas[i].y += planetas[i].vy

def desenhar_objeto(x_virtual: float, y_virtual: float, raio: float, cor):
  # Converte as coordenadas do espaço virtual para o espaço da tela (com escala)
  x_tela = x_virtual / ESCALA
  y_tela = y_virtual / ESCALA
  raio_tela = raio / ESCALA

  # Desenha o círculo na tela
  pg.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))

def desenhar_corpos():
  """
  Desenha todos os corpos ativos na tela.
    
  Parâmetros:

  Retorno:

  """
  for estrela in estrelas:
    if estrela.ativo:
      # Desenha a estrela na tela com sua cor original
      desenhar_objeto(estrela.x, estrela.y, estrela.raio, estrela.cor)

  for planeta in planetas:
    if planeta.ativo:
      # Desenha o planeta na tela com sua cor original
      desenhar_objeto(planeta.x, planeta.y, planeta.raio, planeta.cor)

### FUNÇÕES ###

### SIMULAÇÃO ###
rodando = True # Flag para controlar o loop principal
sim_ativa = False # Flag para controlar a simulação

while rodando:
  # Configuração de FPS
  tempo_delta = clock.tick(60) / 1000.0 # Limitando a 60 o FPS

  # Processando eventos do pygame
  for evento in pg.event.get():
    # Fechar a janela
    if evento.type == pg.QUIT:
      rodando = False

    # Atualizando os valores de acordo com os slider
    if evento.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
      if evento.ui_element == slider_estrelas:
        rot_slider_estrelas.set_text(str(int(slider_estrelas.get_current_value())))
      elif evento.ui_element == slider_planetas:
        rot_slider_planetas.set_text(str(int(slider_planetas.get_current_value())))

    # Processando o botão de iniciar
    if evento.type == pg.USEREVENT:
      if evento.user_type == pg_gui.UI_BUTTON_PRESSED:
        if evento.ui_element == botao_iniciar:
          # Iniciando simulação
          atualizar_informacoes()
          estrelas = criar_estrelas(QUANT_ESTRELAS)
          planetas = criar_planetas(QUANT_PLANETAS)
          sim_ativa = True

    # Processando eventos da GUI
    gui.process_events(evento)
  
  # Atualizando GUI
  gui.update(tempo_delta)

  # Fundo preto
  tela.fill((0, 0, 0))

  if sim_ativa:
    atualizar_corpos()
    desenhar_corpos()

  # Fazendo a GUI aparecer
  gui.draw_ui(tela)

  # Atualizando a tela
  pg.display.flip()

pg.quit()
### SIMULAÇÃO ###