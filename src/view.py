# view.py
"""
Módulo responsável pela interface gráfica (View) do aplicativo de desenho.

@author: João Victor
@version: 1.0
@since: 2026-07-12
"""

from tkinter import *
from tkinter import ttk

class DrawingView:
    """
    Classe que constrói e gerencia todos os widgets da interface gráfica.
    Responsabilidade: exibir o canvas, botões, menus e delegar ações ao controller.

    @author: João Victor
    @version: 1.0
    @since: 2026-07-12
    """

    def __init__(self, root, controller):
        """
        Construtor da DrawingView.

        @param root: janela principal Tk.
        @param controller: instância do DrawingController (pode ser None inicialmente).
        """
        self.root = root
        self.controller = controller
        self.canvas = None
        self._criar_widgets()
        self._configurar_bindings()

    def _criar_widgets(self):
        """Cria e organiza todos os widgets da interface."""
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
        self.menu_forma = ttk.OptionMenu(self.frame, self.tipo_figura_var, *opcoes)
        self.menu_forma.grid(column=1, row=0, sticky=W, **paddings)

        self.label_lados = ttk.Label(self.frame, text="Lados:")
        self.label_lados.grid(column=2, row=0, sticky=W, **paddings)
        self.num_lados_var = IntVar(value=5)
        vcmd = (self.root.register(self._validar_lados), '%P')
        self.spin_lados = Spinbox(
            self.frame, from_=3, to=20, textvariable=self.num_lados_var,
            width=5, validate='focusout', validatecommand=vcmd
        )
        self.spin_lados.grid(column=3, row=0, sticky=W, **paddings)

        ttk.Label(self.frame, text="Preenchimento:").grid(column=4, row=0, sticky=W, **paddings)
        self.botao_cor_preench = Button(self.frame, text="", bg="SystemButtonFace", width=8,
                                        command=lambda: self.controller.escolher_cor("preenchimento"))
        self.botao_cor_preench.grid(column=5, row=0, sticky=W, **paddings)
        Button(self.frame, text="Limpar", command=lambda: self.controller.limpar_preenchimento()).grid(column=6, row=0, sticky=W, **paddings)

        ttk.Label(self.frame, text="Borda:").grid(column=7, row=0, sticky=W, **paddings)
        self.botao_cor_borda = Button(self.frame, text="", bg="black", width=8,
                                      command=lambda: self.controller.escolher_cor("borda"))
        self.botao_cor_borda.grid(column=8, row=0, sticky=W, **paddings)

        # Botões Salvar e Abrir
        self.botao_salvar = Button(self.frame, text="Salvar", command=None)
        self.botao_salvar.grid(column=9, row=0, sticky=W, **paddings)

        self.botao_abrir = Button(self.frame, text="Abrir", command=None)
        self.botao_abrir.grid(column=10, row=0, sticky=W, **paddings)

        self.canvas = Canvas(self.frame, bg="white", width=800, height=600)
        self.canvas.grid(column=0, row=1, columnspan=12, sticky="nsew", **paddings)

        self.tipo_figura_var.trace('w', self._atualizar_visibilidade_lados)
        self._atualizar_visibilidade_lados()

    def _atualizar_visibilidade_lados(self, *args):
        """Mostra ou oculta os widgets de número de lados conforme a forma selecionada."""
        if self.tipo_figura_var.get() == "Poligono":
            self.label_lados.grid()
            self.spin_lados.grid()
        else:
            self.label_lados.grid_remove()
            self.spin_lados.grid_remove()

    def _configurar_bindings(self):
        """Associa eventos do mouse e teclado aos métodos do controller."""
        self.canvas.bind("<ButtonPress-1>", lambda event: self.controller.iniciar_figura_nova(event))
        self.canvas.bind("<B1-Motion>", lambda event: self.controller.atualizar_figura_nova(event))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.controller.incluir_figura_nova(event))
        self.root.bind("<Control-z>", lambda event: self.controller.desfazer(event))

    def desenhar_todas(self, figuras, figura_nova):
        """
        Redesenha todas as figuras finalizadas e a figura em construção (tracejada).

        @param figuras: lista de figuras finalizadas.
        @param figura_nova: figura em construção (ou None).
        """
        self.canvas.delete("all")
        for f in figuras:
            f.desenhar(self.canvas, dash=False)
        if figura_nova is not None:
            figura_nova.desenhar(self.canvas, dash=True)

    def atualizar_botao_cor(self, tipo, cor):
        """
        Atualiza a cor de fundo do botão de cor correspondente.

        @param tipo: "borda" ou "preenchimento".
        @param cor: string com a cor (ex: "#ff0000").
        """
        if tipo == "borda":
            self.botao_cor_borda.config(bg=cor)
        else:
            self.botao_cor_preench.config(bg=cor)

    def resetar_botao_preenchimento(self):
        """Restaura a cor de fundo do botão de preenchimento para a cor padrão do sistema."""
        self.botao_cor_preench.config(bg="SystemButtonFace")

    def _validar_lados(self, P):
        """
        Valida o número de lados digitado no Spinbox (deve ser inteiro >= 3).

        @param P: string com o valor proposto.
        @return: True se for válido, False caso contrário.
        """
        if P.strip() == "":
            return False
        try:
            return int(P) >= 3
        except ValueError:
            return False

    def configurar_controller(self, controller):
        """
        Configura a referência ao controller e ativa os botões de persistência.

        @param controller: instância do DrawingController.
        """
        self.controller = controller
        self.botao_salvar.config(command=self.controller.salvar)
        self.botao_abrir.config(command=self.controller.abrir_arquivo)