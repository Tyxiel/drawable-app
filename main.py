from tkinter import *
from tkinter import ttk, colorchooser
from figuras import (
    Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Orientado a Objetos")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ---------- Variáveis de estado ----------
        self.figuras = []          # lista de figuras finalizadas
        self.figura_nova = None    # figura em construção
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = ""   # "" significa transparente

        # ---------- Configuração da interface ----------
        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        paddings = {"padx": 5, "pady": 5}
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(8, weight=1)

        # ---------- Widgets ----------
        label_forma = ttk.Label(self.frame, text="Escolha a forma:")
        label_forma.grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(root)
        self.tipo_figura_var.set("Linha")
        opcoes = ["Linha", "Rabisco", "Retangulo", "Oval", "Circulo", "Poligono"]
        option_menu = ttk.OptionMenu(self.frame, self.tipo_figura_var, *opcoes)
        option_menu.grid(column=1, row=0, sticky=W, **paddings)

        label_lados = ttk.Label(self.frame, text="Lados:")
        label_lados.grid(column=2, row=0, sticky=W, **paddings)
        self.num_lados_var = IntVar(root)
        self.num_lados_var.set(5)
        spin_lados = Spinbox(self.frame, from_=3, to=20, textvariable=self.num_lados_var, width=5)
        spin_lados.grid(column=3, row=0, sticky=W, **paddings)

        label_preench = ttk.Label(self.frame, text="Preenchimento:")
        label_preench.grid(column=4, row=0, sticky=W, **paddings)

        self.botao_cor_preench = Button(self.frame, text="", 
                                        command=lambda: self.escolher_cor("preenchimento"),
                                        bg="SystemButtonFace", width=8)
        self.botao_cor_preench.grid(column=5, row=0, sticky=W, **paddings)

        botao_limpar_preench = Button(self.frame, text="Limpar", 
                                      command=self.limpar_preenchimento)
        botao_limpar_preench.grid(column=6, row=0, sticky=W, **paddings)

        label_borda = ttk.Label(self.frame, text="Borda:")
        label_borda.grid(column=7, row=0, sticky=W, **paddings)

        self.botao_cor_borda = Button(self.frame, text="", 
                                      command=lambda: self.escolher_cor("borda"),
                                      bg=self.cor_borda_atual, width=8)
        self.botao_cor_borda.grid(column=8, row=0, sticky=W, **paddings)

        self.canvas = Canvas(self.frame, bg="white", width=800, height=600)
        self.canvas.grid(column=0, row=1, columnspan=10, sticky="nsew", **paddings)

        # ---------- Bindings ----------
        self.canvas.bind("<ButtonPress-1>", self.iniciar_figura_nova)
        self.canvas.bind("<B1-Motion>", self.atualizar_figura_nova)
        self.canvas.bind("<ButtonRelease-1>", self.incluir_figura_nova)
        self.root.bind("<Control-z>", self.desfazer)

        # ---------- Inicialização ----------
        self.desenhar_todas()

    # ---------- Métodos ----------
    def escolher_cor(self, tipo):
        """Abre o seletor de cores e atualiza a cor de borda ou preenchimento."""
        cor = colorchooser.askcolor(title=f"Escolha a cor de {tipo}")
        if cor and cor[1]:
            if tipo == "borda":
                self.cor_borda_atual = cor[1]
                try:
                    self.botao_cor_borda.config(background=self.cor_borda_atual)
                except Exception:
                    pass
            else:
                self.cor_preenchimento_atual = cor[1]
                try:
                    self.botao_cor_preench.config(background=self.cor_preenchimento_atual)
                except Exception:
                    pass

    def limpar_preenchimento(self):
        """Remove o preenchimento e reseta o botão."""
        self.cor_preenchimento_atual = ""
        try:
            self.botao_cor_preench.config(background="SystemButtonFace")
        except Exception:
            pass

    def desenhar_todas(self):
        """Limpa o canvas e redesenha todas as figuras e a pré-visualização."""
        self.canvas.delete("all")
        for f in self.figuras:
            try:
                f.desenhar(self.canvas, dash=False)
            except Exception:
                pass
        if self.figura_nova is not None:
            try:
                self.figura_nova.desenhar(self.canvas, dash=True)
            except Exception:
                pass

    def is_figura_degenerada(self, fig):
        """Retorna True se a figura for degenerada (sem área ou pontos suficientes)."""
        if isinstance(fig, Rabisco):
            return len(fig.pontos) < 4
        if isinstance(fig, Linha):
            return (fig.x1, fig.y1) == (fig.x2, fig.y2)
        if isinstance(fig, (Retangulo, Oval, Circulo, PoligonoRegular)):
            return (fig.x1, fig.y1) == (fig.x2, fig.y2)
        return False

    def iniciar_figura_nova(self, event):
        """Cria uma nova figura no início do clique."""
        tipo = self.tipo_figura_var.get()
        x, y = event.x, event.y

        if tipo == "Linha":
            self.figura_nova = Linha(self.cor_borda_atual, x, y, x, y)
        elif tipo == "Rabisco":
            r = Rabisco(self.cor_borda_atual)
            r.adicionar_ponto(x, y)
            self.figura_nova = r
        elif tipo == "Retangulo":
            self.figura_nova = Retangulo(self.cor_borda_atual, self.cor_preenchimento_atual, x, y, x, y)
        elif tipo == "Oval":
            self.figura_nova = Oval(self.cor_borda_atual, self.cor_preenchimento_atual, x, y, x, y)
        elif tipo == "Circulo":
            self.figura_nova = Circulo(self.cor_borda_atual, self.cor_preenchimento_atual, x, y, x, y)
        elif tipo == "Poligono":
            lados = self.num_lados_var.get()
            self.figura_nova = PoligonoRegular(self.cor_borda_atual, self.cor_preenchimento_atual, lados, x, y, x, y)
        else:
            self.figura_nova = None

        self.desenhar_todas()

    def atualizar_figura_nova(self, event):
        """Atualiza a figura em construção durante o movimento do mouse."""
        if self.figura_nova is None:
            return
        x, y = event.x, event.y
        try:
            self.figura_nova.atualizar(x, y)
        except Exception:
            if isinstance(self.figura_nova, Rabisco):
                self.figura_nova.adicionar_ponto(x, y)
        self.desenhar_todas()

    def incluir_figura_nova(self, event):
        """Finaliza a figura em construção e a adiciona à lista, se não for degenerada."""
        if self.figura_nova is None:
            return
        if not self.is_figura_degenerada(self.figura_nova):
            try:
                self.figura_nova.cor_borda = self.cor_borda_atual
                if hasattr(self.figura_nova, "cor_preenchimento"):
                    self.figura_nova.cor_preenchimento = self.cor_preenchimento_atual
            except Exception:
                pass
            self.figuras.append(self.figura_nova)
        self.figura_nova = None
        self.desenhar_todas()

    def desfazer(self, event=None):
        """Remove a última figura finalizada e redesenha."""
        if self.figuras:
            self.figuras.pop()
            self.desenhar_todas()


# ---------- Ponto de entrada ----------
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()