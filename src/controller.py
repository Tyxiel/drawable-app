# controller.py
from tkinter import colorchooser
from src.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
from tkinter import *
import pickle
from tkinter import filedialog

class DrawingController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # ----- Gerenciamento de cores -----
    def escolher_cor(self, tipo):
        cor = colorchooser.askcolor(title=f"Escolha a cor de {tipo}")
        if cor and cor[1]:
            if tipo == "borda":
                self.model.cor_borda_atual = cor[1]
            else:
                self.model.cor_preenchimento_atual = cor[1]
            self.view.atualizar_botao_cor(tipo, cor[1])

    def limpar_preenchimento(self):
        self.model.cor_preenchimento_atual = ""
        self.view.resetar_botao_preenchimento()

    # ----- Eventos de mouse -----
    def iniciar_figura_nova(self, event):
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
        if self.model.figuras:
            self.model.figuras.pop()
            self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)
    
    #----- Persistencia ----
    def salvar(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension= "*.pkl",
            filetypes=[("Arquivos do Aplicativo de desenho", "*.pkl")],
            title="Escolha onde salvar seu desenho"
        )
        if caminho:
            with open(caminho, "wb") as arquivo:
                pickle.dump(self.model.figuras, arquivo)
        
    #def abrir_arquivo(self):