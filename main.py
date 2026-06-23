from tkinter import *
from tkinter import ttk
from tkinter import colorchooser


# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova
    if tipo_figura_var.get() == "Linha":
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == "Rabisco":
        figura_nova = ("rabisco", [(event.x, event.y)])
    elif tipo_figura_var.get() == "Retangulo":
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == "Oval":
        figura_nova = ("oval", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == "Circulo":
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y))


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "linha":
        figura_nova = (
            "linha",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y),
        )
    elif figura_nova[0] == "retangulo":
        figura_nova = (
            "retangulo",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y),
        )
    elif figura_nova[0] == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "circulo":
        x1, y1, _, _ = figura_nova[1]
        dx = event.x - x1
        dy = event.y - y1
        size = max(abs(dx), abs(dy))

        if dx >= 0:
            x2 = x1 + size
        else:
            x2 = x1 - size

        if dy >= 0:
            y2 = y1 + size
        else:
            y2 = y1 - size

        figura_nova = ("circulo", (x1, y1, x2, y2))
    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event):
    if not incompleta(
        figura_nova
    ):  # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        fig, valores = figura_nova
        figuras.append((fig, (valores, cor_borda_atual, cor_preechimento_atual)))
    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")
    for fig, dados in figuras:
        values, cor_borda, cor_preechimento = dados
        if fig == "rabisco":
            canvas.create_line(values, fill=cor_borda, width=3)
        elif fig == "linha":
            canvas.create_line(
                values[0], values[1], values[2], values[3], fill=cor_borda, width=3
            )
        elif fig == "retangulo":
            canvas.create_rectangle(
                values[0],
                values[1],
                values[2],
                values[3],
                fill=cor_preechimento,
                outline=cor_borda,
                width=3,
            )
        elif fig == "oval":
            canvas.create_oval(
                values[0],
                values[1],
                values[2],
                values[3],
                fill=cor_preechimento,
                outline=cor_borda,
                width=3,
            )
        elif fig == "circulo":
            canvas.create_oval(
                values[0],
                values[1],
                values[2],
                values[3],
                fill=cor_preechimento,
                outline=cor_borda,
                width=3,
            )


def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=cor_borda_atual,
            width=3,
        )
    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill=cor_borda_atual, width=3)
    elif fig == "retangulo":
        canvas.create_rectangle(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=cor_preechimento_atual,
            outline=cor_borda_atual,
            width=3,
        )
    elif fig == "oval":
        canvas.create_oval(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=cor_preechimento_atual,
            outline=cor_borda_atual,
            width=3,
        )
    elif fig == "circulo":
        canvas.create_oval(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=cor_preechimento_atual,
            outline=cor_borda_atual,
            width=3,
        )


def incompleta(figura):
    fig, values = figura
    if fig == "rabisco":
        return len(values) <= 1
    else:
        return (values[0], values[1]) == (values[2], values[3])


def cores_preechimento():
    global cor_preechimento_atual
    cor_selecionada = colorchooser.askcolor(title="Escolha a cor de preenchimento")
<<<<<<< Updated upstream
    if cor_selecionada[1]:
        cor_preechimento_atual = cor_selecionada[1]

=======
    if cor_selecionada[1]: 
        cor_preechimento_atual = cor_selecionada[1] 
        botao_cor_preenchimento.config(bg = cor_preechimento_atual)
>>>>>>> Stashed changes

def cores_bordas():
    global cor_borda_atual
    cor_borda_selecionada = colorchooser.askcolor(
        title="Escolha a cor de preenchimento"
    )
    if cor_borda_selecionada[1]:
        cor_borda_atual = cor_borda_selecionada[1]
<<<<<<< Updated upstream


=======
        botao_cor_borda.config(bg = cor_borda_atual)
        
>>>>>>> Stashed changes
def desfazer(event=None):
    if figuras:
        figuras.pop()
        canvas.delete("all")
        desenhar_figuras()


# ******* MAIN *******#

figuras = []  # Todas as figuras desenhadas
figura_nova = (
    None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
)

root = Tk()
root.title("Exemplo de aplicação")
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {"padx": 5, "pady": 5}

# option menu
label = ttk.Label(frame, text="Escolha a forma a ser desenhada:")
label.grid(column=0, row=0, sticky=W, **paddings)
label2 = ttk.Label(frame, text="Escolha a cor:")
label2.grid(column=2, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(
    root
)  # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(
    frame, tipo_figura_var, "Linha", "Linha", "Rabisco", "Retangulo", "Oval", "Circulo"
)
option_menu.grid(column=1, row=0, sticky=W, **paddings)


# cores preechimento
<<<<<<< Updated upstream
cor_preechimento_atual = ""
label_cores_internas = ttk.Label(frame, text="Escolha a cor de preenchimento:")
label_cores_internas.grid(column=2, row=0, sticky=W, **paddings)
botao_cor_preenchimento = Button(
    frame, text="cor preechimento", command=cores_preechimento
)
botao_cor_preenchimento.grid(column=3, row=0, sticky=W, **paddings)

# cores bordas
cor_borda_atual = "black"
label_cores_bordas = ttk.Label(frame, text="Escolha a cor da borda:")
label_cores_bordas.grid(column=4, row=0, sticky=W, **paddings)
botao_cor_borda = Button(frame, text="cor borda", command=cores_bordas)
=======
cor_preechimento_atual = "white"
label_cores_internas = ttk.Label(frame, text="Cor de preenchimento:" )
label_cores_internas.grid(column=2, row=0, sticky=W, **paddings )
botao_cor_preenchimento = Button(frame, text ="                 ", command= cores_preechimento, background= cor_preechimento_atual)
botao_cor_preenchimento.grid(column=3, row=0, sticky=W, **paddings )

# cores bordas
cor_borda_atual = "black"
label_cores_bordas = ttk.Label(frame, text="Cor da borda:")
label_cores_bordas.grid(column=4, row=0, sticky=W, **paddings )
botao_cor_borda = Button(frame, text ="                 ", command= cores_bordas, background= cor_borda_atual)
>>>>>>> Stashed changes
botao_cor_borda.grid(column=5, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg="white", width=1200, height=1200)
canvas.grid(column=0, row=1, columnspan=10, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
canvas.bind("<B1-Motion>", atualizar_figura_nova)
canvas.bind("<ButtonRelease-1>", incluir_figura_nova)

root.bind("<Control-z>", desfazer)

root.mainloop()
