"""
Módulo que define as classes de estado para cada ferramenta de desenho.
Responsabilidade: Encapsular o comportamento de clique, arrasto e liberação
do mouse para cada figura geométrica específica, eliminando condicionais do controlador.

@author: Samuel Campos, João Pedro Chaves, João Victor
@version: 2.0
@since: 2026-07-19
"""

from abc import ABC, abstractmethod
from src.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular

class EstadoFerramenta(ABC):
    """
    Classe abstrata base que define a interface comum para todos os estados de ferramentas.
    
    Garante que qualquer ferramenta implemente obrigatoriamente as ações de mouse.
    """
    def __init__(self, controller):
        """
        Construtor da classe base de estado.

        @param controller: Instância do DrawingController para permitir a manipulação do Model e View.
        """
        self.controller = controller

    @abstractmethod
    def ao_clicar(self, event):
        """Define o comportamento quando o botão esquerdo do mouse é pressionado."""
        pass

    @abstractmethod
    def ao_arrastar(self, event):
        """Define o comportamento enquanto o mouse é movido com o botão pressionado."""
        pass

    @abstractmethod
    def ao_soltar(self, event):
        """Define o comportamento quando o botão esquerdo do mouse é liberado."""
        pass


class EstadoLinha(EstadoFerramenta):
    """
    Estado específico para a ferramenta de desenho de Linhas retas.
    """
    def ao_clicar(self, event):
        """Instancia uma nova Linha com coordenadas iniciais e finais idênticas no ponto do clique."""
        x, y = event.x, event.y
        cor_borda = self.controller.model.cor_borda_atual
        self.controller.model.figura_nova = Linha(cor_borda, x, y, x, y)

    def ao_arrastar(self, event):
        """Atualiza a coordenada final da linha dinamicamente conforme o mouse se move."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Finaliza a construção da linha invocando o fluxo padrão de salvamento do controlador."""
        self.controller.finalizar_figura_comum()


class EstadoRabisco(EstadoFerramenta):
    """
    Estado específico para a ferramenta de desenho livre (Rabisco).
    """
    def ao_clicar(self, event):
        """Cria um novo objeto Rabisco inserindo o primeiro ponto da sequência."""
        cor_borda = self.controller.model.cor_borda_atual
        fig = Rabisco(cor_borda)
        fig.adicionar_ponto(event.x, event.y)
        self.controller.model.figura_nova = fig

    def ao_arrastar(self, event):
        """Acumula e registra todos os novos pontos geométricos gerados pela trajetória do mouse."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Finaliza o desenho livre e envia o conjunto de pontos para validação no controlador."""
        self.controller.finalizar_figura_comum()


class EstadoRetangulo(EstadoFerramenta):
    """
    Estado específico para a ferramenta de desenho de Retângulos.
    """
    def ao_clicar(self, event):
        """Cria o rascunho de um Retângulo aplicando as cores de borda e preenchimento atuais."""
        x, y = event.x, event.y
        cor_borda = self.controller.model.cor_borda_atual
        cor_preench = self.controller.model.cor_preenchimento_atual
        self.controller.model.figura_nova = Retangulo(cor_borda, cor_preench, x, y, x, y)

    def ao_arrastar(self, event):
        """Redimensiona o vértice oposto do retângulo de acordo com o arrasto do mouse."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Valida as dimensões e insere o retângulo permanentemente no modelo de dados."""
        self.controller.finalizar_figura_comum()


class EstadoOval(EstadoFerramenta):
    """
    Estado específico para a ferramenta de desenho de formas Ovais/Elipses.
    """
    def ao_clicar(self, event):
        """Inicia um objeto Oval delimitado pelas coordenadas do clique."""
        x, y = event.x, event.y
        cor_borda = self.controller.model.cor_borda_atual
        cor_preench = self.controller.model.cor_preenchimento_atual
        self.controller.model.figura_nova = Oval(cor_borda, cor_preench, x, y, x, y)

    def ao_arrastar(self, event):
        """Modifica a caixa delimitadora da elipse simulando o esticamento da forma."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Conclui a inserção da forma elíptica na lista de renderização estável."""
        self.controller.finalizar_figura_comum()


class EstadoCirculo(EstadoFerramenta):
    """
    Estado específico para a ferramenta de desenho de Círculos perfeitos (equiláteros).
    """
    def ao_clicar(self, event):
        """Cria o rascunho de um Círculo restrito pelas regras de proporção de raio."""
        x, y = event.x, event.y
        cor_borda = self.controller.model.cor_borda_atual
        cor_preench = self.controller.model.cor_preenchimento_atual
        self.controller.model.figura_nova = Circulo(cor_borda, cor_preench, x, y, x, y)

    def ao_arrastar(self, event):
        """Recalcula o diâmetro proporcional do círculo usando a maior distância de deslocamento."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Armazena o círculo finalizado caso não seja um clique estático (degenerado)."""
        self.controller.finalizar_figura_comum()


class EstadoPoligono(EstadoFerramenta):
    """
    Estado específico para a ferramenta de Polígonos Regulares de N lados.
    """
    def ao_clicar(self, event):
        """Instancia um polígono recuperando dinamicamente a quantidade de lados definida no Spinbox."""
        x, y = event.x, event.y
        cor_borda = self.controller.model.cor_borda_atual
        cor_preench = self.controller.model.cor_preenchimento_atual
        lados = self.controller.view.num_lados_var.get()
        self.controller.model.figura_nova = PoligonoRegular(cor_borda, cor_preench, lados, x, y, x, y)

    def ao_arrastar(self, event):
        """Recalcula a posição trigonométrica de todos os vértices do polígono baseado no raio."""
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar(event.x, event.y)

    def ao_soltar(self, event):
        """Fixa o polígono regular na tela e limpa o ponteiro temporário."""
        self.controller.finalizar_figura_comum()
