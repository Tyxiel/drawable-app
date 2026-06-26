from tkinter import *
from tkinter import ttk
from tkinter import colorchoose
from abc import ABC, abstractmethod

class Figura(ABC):
  def __init__(self, cor_borda: str, cor_preenchimento: str, incompleta: bool):
    self.cor_borda = cor_borda
    self.cor_preenchimento = cor_preenchimento
    self.incompleta = incompleta
  
  @abstractmethod
  def desenhar(self):
    pass

  @abstractmethod
  def desenhar_previa(self):
    pass

  @abstractmethod
  def atualizar(self):
    pass

  @abstractmethod
  def adicionar_ponto(self):
    pass
  
  @abstractmethod
  def esta_incompleta(self):
    pass

class Linha(Figura):
  def __init__(self, cor_borda: str, cor_preenchimento: str, incompleta: bool, pos_inicial, pos_final):
    super().__init__(cor_borda, cor_preenchimento, incompleta)
    self.pos_inicial = pos_inicial
    self.pos_final = pos_final

  def atualizar(self, pos_final):
    self.pos_final = pos_final

  def desenhar(self):
    canvas.create_line((self.pos_inicial, self.pos_final), fill=self.cor_borda, width=3)

  def desenhar_previa(self):
    canvas.create_line((self.pos_inicial, self.pos_final), fill=self.cor_borda, width=3, dash=(4,2))

  def adicionar_ponto(self):
    pass

  def esta_incompleta(self):
    if self.pos_inicial == self.pos_final:
      self.incompleta = True

class Linha(Figura):
  def __init__(self, cor_borda: str, cor_preenchimento: str, incompleta: bool, pos_inicial, pos_final):
    super().__init__(cor_borda, cor_preenchimento, incompleta)
    self.pos_inicial = pos_inicial
    self.pos_final = pos_final

  def atualizar(self, pos_final):
    self.pos_final = pos_final

  def desenhar(self):
    canvas.create_line((self.pos_inicial, self.pos_final), fill=self.cor_borda, width=3)

  def desenhar_previa(self):
    canvas.create_line((self.pos_inicial, self.pos_final), fill=self.cor_borda, width=3, dash=(4,2))

  def adicionar_ponto(self):
    pass

  def esta_incompleta(self):
    if self.pos_inicial == self.pos_final:
      self.incompleta = True


# ******* MAIN *******#

figuras: list = []  # Todas as figuras desenhadas
figura_nova = (
    None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
)

root = Tk()
root.title("Paint no Python")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame = Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Widgets arranjados com Layout grid dentro de frame
paddings: dict[str, int] = {"padx": 5, "pady": 5}
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(7, weight=1)

# option menu
label = ttk.Label(frame, text="Escolha a forma a ser desenhada:")
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(
    root
)  # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(
    frame, tipo_figura_var, "Linha", "Linha", "Rabisco", "Retangulo", "Oval", "Circulo"
)
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# cores preechimento
cor_preechimento_atual = "white"
label_cores_internas = ttk.Label(frame, text="Cor de preenchimento:")
label_cores_internas.grid(column=2, row=0, sticky=W, **paddings)
botao_cor_preenchimento = Button(
    frame,
    text="",
    command=cores_preechimento,
    background=cor_preechimento_atual,
    width=10,
    height=1,
)

# cores preechimento
cor_preechimento_atual = None
label_cores_internas = ttk.Label(frame, text="Cor de preenchimento:")
label_cores_internas.grid(column=2, row=0, sticky=W, **paddings)
botao_cor_preenchimento = Button(
    frame,
    text="",
    command=cores_preechimento,
    background=cor_preechimento_atual,
    width=10,
    height=1,
)
botao_cor_preenchimento.grid(column=3, row=0, sticky=W, **paddings)
botao_limpar_preenchimento = Button(
    frame, text="Limpar preenchimento", command=limpar_preenchimento
)
botao_limpar_preenchimento.grid(column=4, row=0, sticky=W, **paddings)

# cores bordas
cor_borda_atual = "black"
label_cores_bordas = ttk.Label(frame, text="Cor da borda:")
label_cores_bordas.grid(column=4, row=0, sticky=W, **paddings)
label_cores_bordas.grid(column=5, row=0, sticky=W, **paddings)
botao_cor_borda = Button(
    frame, text="", command=cores_bordas, background=cor_borda_atual, width=10, height=1
)
botao_cor_borda.grid(column=6, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg="white", width=800, height=600)
canvas.grid(column=0, row=1, columnspan=10, sticky="nsew", **paddings)

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
canvas.bind("<B1-Motion>", atualizar_figura_nova)
canvas.bind("<ButtonRelease-1>", incluir_figura_nova)

root.bind("<Control-z>", desfazer)

root.mainloop()

canvas.create_polygon()