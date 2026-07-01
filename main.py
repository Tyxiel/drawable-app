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

# ---------- Funçoes implementadas ----------

def escolher_cor(tipo):
    #abre as opçao de cor e atualiza a cor de borda ou preenchimento.
    global cor_borda_atual, cor_preenchimento_atual
    cor = colorchooser.askcolor(title=f"Escolha a cor de {tipo}")
    if cor and cor[1]:
        if tipo == "borda":
            cor_borda_atual = cor[1]
            try:
                botao_cor_borda.config(background=cor_borda_atual)
            except Exception:
                pass
        else:
            cor_preenchimento_atual = cor[1]
            try:
                botao_cor_preench.config(background=cor_preenchimento_atual)
            except Exception:
                pass


def limpar_preenchimento():
    #remove o preenchimento e reseta o botao.
    global cor_preenchimento_atual
    cor_preenchimento_atual = None
    try:
        botao_cor_preench.config(background="SystemButtonFace")
    except Exception:
        pass


def desenhar_todas():
    canvas.delete("all") #limpa o a folha de desenho e desenha todas as figuras prontas e a pre visualizaçao.
    for f in figuras:
        try:
            f.desenhar(canvas, dash=False)
        except Exception:
            pass
    if figura_nova is not None:
        try:
            figura_nova.desenhar(canvas, dash=True)
        except Exception:
            pass


def is_figura_degenerada(fig):
    #retorna True se a figura for degenerada sem área ou pontos suficientes.

    if isinstance(fig, Rabisco):#precisa ter no minimo 2 pontos
        return len(fig.pontos) < 4
    if isinstance(fig, Linha):
        return (fig.x1, fig.y1) == (fig.x2, fig.y2)
    if isinstance(fig, (Retangulo, Oval, Circulo, PoligonoRegular)):
        return (fig.x1, fig.y1) == (fig.x2, fig.y2)
    return False


def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()
    x, y = event.x, event.y

    if tipo == "Linha":
        figura_nova = Linha(cor_borda_atual, x, y, x, y)
    elif tipo == "Rabisco":
        r = Rabisco(cor_borda_atual)
        r.adicionar_ponto(x, y)
        figura_nova = r
    elif tipo == "Retangulo":
        figura_nova = Retangulo(cor_borda_atual, cor_preenchimento_atual, x, y, x, y)
    elif tipo == "Oval":
        figura_nova = Oval(cor_borda_atual, cor_preenchimento_atual, x, y, x, y)
    elif tipo == "Circulo":
        figura_nova = Circulo(cor_borda_atual, cor_preenchimento_atual, x, y, x, y)
    elif tipo == "Poligono":
        lados = num_lados_var.get()
        figura_nova = PoligonoRegular(cor_borda_atual, cor_preenchimento_atual, lados, x, y, x, y)
    else:
        figura_nova = None

    desenhar_todas()


def atualizar_figura_nova(event):
    #atualiza o desenho que esta sendo feito enquanto o mouse se mexe segurando o botao.
    global figura_nova
    if figura_nova is None:
        return
    x, y = event.x, event.y
    try:
        figura_nova.atualizar(x, y)
    except Exception:
        if isinstance(figura_nova, Rabisco):
            figura_nova.adicionar_ponto(x, y)
    desenhar_todas()


def incluir_figura_nova(event):
    #finaliza a figura em construção e adiciona na lista se nao for degenerada.
    global figura_nova
    if figura_nova is None:
        return
    if not is_figura_degenerada(figura_nova):
        try:
            figura_nova.cor_borda = cor_borda_atual
            if hasattr(figura_nova, "cor_preenchimento"):
                figura_nova.cor_preenchimento = cor_preenchimento_atual
        except Exception:
            pass
        figuras.append(figura_nova)
    figura_nova = None
    desenhar_todas()


def desfazer(event=None):
    #remove a ultima forma feita e redesenha.
    if figuras:
        figuras.pop()
        desenhar_todas()

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
