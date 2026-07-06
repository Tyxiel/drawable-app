# view.py
from tkinter import *
from tkinter import ttk

class DrawingView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.canvas = None

        self._criar_widgets()
        self._configurar_bindings()

    def _criar_widgets(self):
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(8, weight=1)

        paddings = {"padx": 5, "pady": 5}

        ttk.Label(self.frame, text="Escolha a forma:").grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(value="Linha")
        opcoes = ["Linha", "Rabisco", "Retangulo", "Oval", "Circulo", "Poligono"]
        ttk.OptionMenu(self.frame, self.tipo_figura_var, *opcoes).grid(column=1, row=0, sticky=W, **paddings)

        ttk.Label(self.frame, text="Lados:").grid(column=2, row=0, sticky=W, **paddings)
        self.num_lados_var = IntVar(value=5)
        Spinbox(self.frame, from_=3, to=20, textvariable=self.num_lados_var, width=5).grid(column=3, row=0, sticky=W, **paddings)

        ttk.Label(self.frame, text="Preenchimento:").grid(column=4, row=0, sticky=W, **paddings)
        self.botao_cor_preench = Button(self.frame, text="", bg="SystemButtonFace", width=8,
                                        command=lambda: self.controller.escolher_cor("preenchimento"))
        self.botao_cor_preench.grid(column=5, row=0, sticky=W, **paddings)
        Button(self.frame, text="Limpar", command=lambda: self.controller.limpar_preenchimento()).grid(column=6, row=0, sticky=W, **paddings)

        ttk.Label(self.frame, text="Borda:").grid(column=7, row=0, sticky=W, **paddings)
        self.botao_cor_borda = Button(self.frame, text="", bg="black", width=8,
                                      command=lambda: self.controller.escolher_cor("borda"))
        self.botao_cor_borda.grid(column=8, row=0, sticky=W, **paddings)

        self.canvas = Canvas(self.frame, bg="white", width=800, height=600)
        self.canvas.grid(column=0, row=1, columnspan=10, sticky="nsew", **paddings)

    def _configurar_bindings(self):
        self.canvas.bind("<ButtonPress-1>", lambda event: self.controller.iniciar_figura_nova(event))
        self.canvas.bind("<B1-Motion>", lambda event: self.controller.atualizar_figura_nova(event))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.controller.incluir_figura_nova(event))
        self.root.bind("<Control-z>", lambda event: self.controller.desfazer(event))

    def desenhar_todas(self, figuras, figura_nova):
        """Limpa o canvas e redesenha todas as figuras e a pré-visualização tracejada."""
        self.canvas.delete("all")
        for f in figuras:
            f.desenhar(self.canvas, dash=False)
        if figura_nova is not None:
            figura_nova.desenhar(self.canvas, dash=True)

    def atualizar_botao_cor(self, tipo, cor):
        """Atualiza a cor de fundo do botão correspondente."""
        if tipo == "borda":
            self.botao_cor_borda.config(bg=cor)
        else:
            self.botao_cor_preench.config(bg=cor)

    def resetar_botao_preenchimento(self):
        self.botao_cor_preench.config(bg="SystemButtonFace")