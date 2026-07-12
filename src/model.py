# model.py
"""
Módulo responsável pelo modelo de dados do aplicativo de desenho.
Armazena as figuras, cores atuais e fornece verificação de figuras degeneradas.

@author: Samuel Campos
@version: 1.0
@since: 2026-07-12
"""

class DrawingModel:
    """
    Classe que representa o estado central do aplicativo.
    Responsabilidade: gerenciar a lista de figuras finalizadas, a figura em construção
    e as cores atuais de borda e preenchimento.

    @author: Samuel Campos
    @version: 1.0
    @since: 2026-07-12
    """

    def __init__(self):
        """
        Construtor da classe DrawingModel.
        Inicializa as listas e variáveis de estado com valores padrão.
        """
        self.figuras = []      # Lista de figuras já finalizadas
        self.figura_nova = None               # Figura em construção
        self.cor_borda_atual = "black"        # Cor da borda atualmente selecionada
        self.cor_preenchimento_atual = ""     # Cor de preenchimento ("" = transparente)

    @staticmethod
    def is_figura_degenerada(fig):
        """
        Verifica se uma figura é degenerada (sem tamanho ou sem pontos suficientes).

        @param fig: instância de uma subclasse de Figura.
        @return: bool – True se for degenerada, False caso contrário.
        @throws: ImportError se as classes de figuras não estiverem disponíveis.
        """
        from src.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
        if isinstance(fig, Rabisco):
            return len(fig.pontos) < 4
        if isinstance(fig, Linha):
            return (fig.x1, fig.y1) == (fig.x2, fig.y2)
        if isinstance(fig, (Retangulo, Oval, Circulo, PoligonoRegular)):
            return (fig.x1, fig.y1) == (fig.x2, fig.y2)
        return False