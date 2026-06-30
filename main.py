from tkinter import *
from tkinter import ttk, colorchooser
from figuras import (
    Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
)

# ---------- Variáveis globais ----------
figuras = []          # lista de figuras já finalizadas (instâncias de Figura)
figura_nova = None    # figura em construção (instância de Figura) ou None
cor_borda_atual = "black"
cor_preenchimento_atual = None   # None significa transparente

# ---------- Funções (a serem implementadas) ----------
def escolher_cor(tipo):
    pass

def limpar_preenchimento():
    pass

def desenhar_todas():
    pass

def is_figura_degenerada(fig):
    pass

def iniciar_figura_nova(event):
    pass

def atualizar_figura_nova(event):
    pass

def incluir_figura_nova(event):
    pass

def desfazer(event=None):
    pass

# ---------- Configuração da janela ----------
root = Tk()
root.title("Paint Orientado a Objetos")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
paddings = {"padx": 5, "pady": 5}
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(7, weight=1)

# ---------- Widgets ----------
label_forma = ttk.Label(frame, text="Escolha a forma:")
label_forma.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root)
tipo_figura_var.set("Linha")
opcoes = ["Linha", "Rabisco", "Retangulo", "Oval", "Circulo", "Poligono"]
option_menu = ttk.OptionMenu(frame, tipo_figura_var, *opcoes)
option_menu.grid(column=1, row=0, sticky=W, **paddings)

label_lados = ttk.Label(frame, text="Lados:")
label_lados.grid(column=2, row=0, sticky=W, **paddings)
num_lados_var = IntVar(root)
num_lados_var.set(5)
spin_lados = Spinbox(frame, from_=3, to=20, textvariable=num_lados_var, width=5)
spin_lados.grid(column=3, row=0, sticky=W, **paddings)

label_preench = ttk.Label(frame, text="Preenchimento:")
label_preench.grid(column=4, row=0, sticky=W, **paddings)

botao_cor_preench = Button(frame, text="", command=lambda: escolher_cor("preenchimento"),
                           bg="SystemButtonFace", width=8)
botao_cor_preench.grid(column=5, row=0, sticky=W, **paddings)

botao_limpar_preench = Button(frame, text="Limpar", command=limpar_preenchimento)
botao_limpar_preench.grid(column=6, row=0, sticky=W, **paddings)

label_borda = ttk.Label(frame, text="Borda:")
label_borda.grid(column=7, row=0, sticky=W, **paddings)

botao_cor_borda = Button(frame, text="", command=lambda: escolher_cor("borda"),
                         bg=cor_borda_atual, width=8)
botao_cor_borda.grid(column=8, row=0, sticky=W, **paddings)

canvas = Canvas(frame, bg="white", width=800, height=600)
canvas.grid(column=0, row=1, columnspan=10, sticky="nsew", **paddings)

# ---------- Bindings ----------
canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
canvas.bind("<B1-Motion>", atualizar_figura_nova)
canvas.bind("<ButtonRelease-1>", incluir_figura_nova)
root.bind("<Control-z>", desfazer)

# ---------- Inicialização ----------
desenhar_todas()
root.mainloop()