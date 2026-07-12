# controller.py
"""
Módulo controlador que orquestra a interação entre a View e o Model.

@author: Samuel Campos, João Pedro Chaves, João Victor
@version: 1.0
@since: 2026-07-12
"""

from tkinter import colorchooser, filedialog
from src.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
import pickle

class DrawingController:
    """
    Classe que coordena as ações do usuário, atualizando o modelo e a view.

    Responsabilidade: processar eventos de clique/arrasto, gerenciar cores,
    persistência (salvar/abrir) e comando desfazer.

    @author: Samuel Campos, João Pedro Chaves, João Victor
    @version: 1.0
    @since: 2026-07-12
    """

    def __init__(self, model, view):
        """
        Construtor do controlador.

        @param model: instância de DrawingModel.
        @param view: instância de DrawingView.
        """
        self.model = model
        self.view = view

    # ----- Gerenciamento de cores -----
    def escolher_cor(self, tipo):
        """
        Abre o seletor de cores e atualiza a cor correspondente no modelo e na view.

        @param tipo: "borda" ou "preenchimento".
        """
        cor = colorchooser.askcolor(title=f"Escolha a cor de {tipo}")
        if cor and cor[1]:
            if tipo == "borda":
                self.model.cor_borda_atual = cor[1]
            else:
                self.model.cor_preenchimento_atual = cor[1]
            self.view.atualizar_botao_cor(tipo, cor[1])

    def limpar_preenchimento(self):
        """Remove a cor de preenchimento (torna transparente) e atualiza a view."""
        self.model.cor_preenchimento_atual = ""
        self.view.resetar_botao_preenchimento()

    # ----- Eventos de mouse -----
    def iniciar_figura_nova(self, event):
        """
        Cria uma nova figura no ponto onde o mouse foi pressionado.

        @param event: evento do Tkinter contendo as coordenadas x, y.
        """
        tipo = self.view.tipo_figura_var.get()
        x, y = event.x, event.y
        cor_borda = self.model.cor_borda_atual
        cor_preench = self.model.cor_preenchimento_atual

        if tipo == "Linha":
            fig = Linha(cor_borda, x, y, x, y)
        elif tipo == "Rabisco":
            fig = Rabisco(cor_borda)
            fig.adicionar_ponto(x, y)
        elif tipo == "Retangulo":
            fig = Retangulo(cor_borda, cor_preench, x, y, x, y)
        elif tipo == "Oval":
            fig = Oval(cor_borda, cor_preench, x, y, x, y)
        elif tipo == "Circulo":
            fig = Circulo(cor_borda, cor_preench, x, y, x, y)
        elif tipo == "Poligono":
            lados = self.view.num_lados_var.get()
            fig = PoligonoRegular(cor_borda, cor_preench, lados, x, y, x, y)
        else:
            fig = None

        self.model.figura_nova = fig
        self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    def atualizar_figura_nova(self, event):
        """
        Atualiza a figura em construção durante o arrasto do mouse.

        @param event: evento do Tkinter com novas coordenadas.
        """
        if self.model.figura_nova is None:
            return
        x, y = event.x, event.y
        try:
            self.model.figura_nova.atualizar(x, y)
        except Exception:
            if isinstance(self.model.figura_nova, Rabisco):
                self.model.figura_nova.adicionar_ponto(x, y)
        self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    def incluir_figura_nova(self, event):
        """
        Finaliza a figura em construção e a adiciona à lista de figuras, se não for degenerada.

        @param event: evento de liberação do botão do mouse.
        """
        if self.model.figura_nova is None:
            return
        if not self.model.is_figura_degenerada(self.model.figura_nova):
            # Aplica as cores atuais (podem ter mudado durante a criação)
            self.model.figura_nova.cor_borda = self.model.cor_borda_atual
            if hasattr(self.model.figura_nova, 'cor_preenchimento'):
                self.model.figura_nova.cor_preenchimento = self.model.cor_preenchimento_atual
            self.model.figuras.append(self.model.figura_nova)
        self.model.figura_nova = None
        self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    # ----- Desfazer -----
    def desfazer(self, event=None):
        """
        Remove a última figura adicionada e redesenha o canvas.

        @param event: evento opcional (tecla Ctrl+Z).
        """
        if self.model.figuras:
            self.model.figuras.pop()
            self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    # ----- Persistência -----
    def salvar(self):
        """
        Salva a lista de figuras em um arquivo .pkl usando pickle.
        Abre uma caixa de diálogo para escolher o local e nome do arquivo.
        """
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Arquivos do Aplicativo de Desenho", "*.pkl")],
            title="Salvar desenho"
        )
        if caminho:
            with open(caminho, "wb") as arquivo:
                pickle.dump(self.model.figuras, arquivo)

    def abrir_arquivo(self):
        """
        Abre um arquivo .pkl contendo uma lista de figuras e as carrega no modelo.
        Substitui as figuras atuais e redesenha a tela.
        """
        caminho = filedialog.askopenfilename(
            defaultextension=".pkl",
            filetypes=[("Arquivos do Aplicativo de Desenho", "*.pkl")],
            title="Abrir desenho"
        )
        if caminho:
            with open(caminho, "rb") as arquivo:
                self.model.figuras = pickle.load(arquivo)
            self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)