# controller.py
"""
Módulo controlador que orquestra a interação entre a View e o Model.
Aplica o padrão State para evitar condicionais nas ferramentas de desenho.

@author: Samuel Campos, João Pedro Chaves, João Victor
@version: 2.0
@since: 2026-07-19
"""

from tkinter import colorchooser, filedialog
import pickle
from src.estados import (
    EstadoLinha, EstadoRabisco, EstadoRetangulo,
    EstadoOval, EstadoCirculo, EstadoPoligono
)

class DrawingController:
    """
    Controlador central que delega ações de mouse ao estado ativo da ferramenta.

    @author: Samuel Campos, João Pedro Chaves, João Victor
    @version: 2.0
    @since: 2026-07-19
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Mapeamento entre o nome da ferramenta (exibido no menu) e a classe de estado
        self._estados = {
            "Linha":     EstadoLinha,
            "Rabisco":   EstadoRabisco,
            "Retangulo": EstadoRetangulo,
            "Oval":      EstadoOval,
            "Circulo":   EstadoCirculo,
            "Poligono":  EstadoPoligono,
        }

        # Estado inicial (mesma ferramenta padrão da view)
        self.estado_atual = self._estados["Linha"](self)
        self.view.tipo_figura_var.trace('w', self._on_ferramenta_changed)

    def _on_ferramenta_changed(self, *args):
        """Atualiza o estado da ferramenta sempre que o menu de opções muda."""
        nome = self.view.tipo_figura_var.get()
        if nome in self._estados:
            self.estado_atual = self._estados[nome](self)

    # ----- Gerenciamento de cores -----
    def escolher_cor(self, tipo):
        """Abre o seletor de cores e atualiza a cor correspondente no modelo e na view."""
        cor = colorchooser.askcolor(title=f"Escolha a cor de {tipo}")
        if cor and cor[1]:
            if tipo == "borda":
                self.model.cor_borda_atual = cor[1]
            else:
                self.model.cor_preenchimento_atual = cor[1]
            self.view.atualizar_botao_cor(tipo, cor[1])

    def limpar_preenchimento(self):
        """Remove a cor de preenchimento e reseta o botão correspondente."""
        self.model.cor_preenchimento_atual = ""
        self.view.resetar_botao_preenchimento()

    # ----- Eventos de mouse (delegação pura) -----
    def iniciar_figura_nova(self, event):
        """Encaminha o clique para o estado da ferramenta ativa."""
        self.estado_atual.ao_clicar(event)

    def atualizar_figura_nova(self, event):
        """Encaminha o arrasto para o estado da ferramenta ativa."""
        self.estado_atual.ao_arrastar(event)
        self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    def incluir_figura_nova(self, event):
        """Encaminha a liberação do mouse para o estado ativo."""
        self.estado_atual.ao_soltar(event)

    # ----- Método auxiliar usado por todos os estados -----
    def finalizar_figura_comum(self):
        """
        Valida a figura em construção, aplica as cores atuais e a adiciona à lista.
        Esse método é chamado por todos os estados concretos no momento de soltar.
        """
        if self.model.figura_nova is None:
            return
        if not self.model.is_figura_degenerada(self.model.figura_nova):
            # Aplica cores atuais (podem ter sido alteradas durante o desenho)
            self.model.figura_nova.cor_borda = self.model.cor_borda_atual
            if hasattr(self.model.figura_nova, 'cor_preenchimento'):
                self.model.figura_nova.cor_preenchimento = self.model.cor_preenchimento_atual
            self.model.figuras.append(self.model.figura_nova)
        self.model.figura_nova = None
        self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    # ----- Desfazer -----
    def desfazer(self, event=None):
        """Remove a última figura finalizada e redesenha."""
        if self.model.figuras:
            self.model.figuras.pop()
            self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)

    # ----- Persistência -----
    def salvar(self):
        """Salva a lista de figuras em um arquivo .pkl."""
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Arquivos do Aplicativo de Desenho", "*.pkl")],
            title="Salvar desenho"
        )
        if caminho:
            with open(caminho, "wb") as arquivo:
                pickle.dump(self.model.figuras, arquivo)

    def abrir_arquivo(self):
        """Carrega figuras de um arquivo .pkl e substitui o desenho atual."""
        caminho = filedialog.askopenfilename(
            defaultextension=".pkl",
            filetypes=[("Arquivos do Aplicativo de Desenho", "*.pkl")],
            title="Abrir desenho"
        )
        if caminho:
            with open(caminho, "rb") as arquivo:
                self.model.figuras = pickle.load(arquivo)
            self.view.desenhar_todas(self.model.figuras, self.model.figura_nova)