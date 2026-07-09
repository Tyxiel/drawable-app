from abc import ABC, abstractmethod
import math

class Figura(ABC):
    """
    Classe abstrata que serve de base e define a interface comum para todas as figuras geométricas do sistema.
    
    Responsabilidade: Definir propriedades básicas de cores e os métodos obrigatórios de desenho e atualização.
    
    @author JPChaves 
    @version 1.0
    """
    def __init__(self, cor_borda, cor_preenchimento):
        """
        Construtor da classe abstrata Figura.
        
        @param cor_borda: str contendo a cor da linha externa da figura.
        @param cor_preenchimento: str contendo a cor interna da figura (vazio para transparente).
        """
        self.cor_preenchimento = cor_preenchimento
        self.cor_borda = cor_borda

    @abstractmethod
    def desenhar(self, canvas, dash=False):
        """
        Desenha a figura geométrica no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        pass

    @abstractmethod
    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """
        pass


class Linha(Figura):
    """
    Classe que representa uma linha no sistema de desenho.
    Responsabilidade: receber os pontos iniciais e finais a partir do clique do mouse e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda, x1, y1, x2, y2):
        """
        Construtor da classe Linha.
        
        @param cor_borda: str contendo a cor da figura Linha.
        @param x1: int coordenada X inical do clique.
        @param y1: int coordenada Y inical do clique.
        @param x2: int coordenada X final do arrasto.
        @param y2: int coordenada Y final do arrasto.
        """
        super().__init__(cor_borda, cor_preenchimento=None)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        """
        Desenha a Linha no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
    
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """ 
        self.x2, self.y2 = x, y


class Rabisco(Figura):
    """
    Classe que representa um desenho livre no sistema de desenho.
    Responsabilidade: receber todos os pontos que o mouse passar pressionado e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda):
        """
        Construtor da classe Rabisco.
        
        @param cor_borda: str contendo a cor da figura Rabisco.
        
        """
        super().__init__(cor_borda, cor_preenchimento=None)
        self.pontos = []  # lista de coordenadas (x1,y1,x2,y2,...)

    def adicionar_ponto(self, x, y):
        """
        Adiciona linearmente as coordenadas X e Y na lista de pontos

        @param x: int coordenada X capturada pelo mouse.
        @param y: int coordenada Y capturada pelo mouse.
        """
        self.pontos.append(x)
        self.pontos.append(y)

    def desenhar(self, canvas, dash=False):
        """
        Desenha o Rabisco no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        if len(self.pontos) >= 4:

            canvas.create_line(self.pontos, fill=self.cor_borda, width=3,
                               dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza o desenho livre capturando os novos pontos durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """ 
        self.adicionar_ponto(x, y)


class Retangulo(Figura):
    """
    Classe que representa um retangulo no sistema de desenho.
    Responsabilidade: receber os pontos iniciais e finais a partir do clique do mouse e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        """
        Construtor da classe Retangulo.
        
        @param cor_borda: str contendo a cor da borda da figura Retangulo.
        @param cor_preenchimento: str contendo a cor interna da figura Retangulo.
        @param x1: int coordenada X inical do clique.
        @param y1: int coordenada Y inical do clique.
        @param x2: int coordenada X final do arrasto.
        @param y2: int coordenada Y final do arrasto.
        """
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        """
        Desenha o Retangulo no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                fill=self.cor_preenchimento, outline=self.cor_borda,
                                width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """ 
        self.x2, self.y2 = x, y


class Oval(Figura):
    """
    Classe que representa um Oval no sistema de desenho.
    Responsabilidade: receber os pontos iniciais e finais a partir do clique do mouse e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        """
        Construtor da classe Oval.
        
        @param cor_borda: str contendo a cor da borda da figura Oval.
        @param cor_preenchimento: str contendo a cor interna da figura Oval.
        @param x1: int coordenada X inical do clique.
        @param y1: int coordenada Y inical do clique.
        @param x2: int coordenada X final do arrasto.
        @param y2: int coordenada Y final do arrasto.
        """
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        """
        Desenha o Oval no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_preenchimento, outline=self.cor_borda,
                           width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """ 
        self.x2, self.y2 = x, y


class Circulo(Figura):
    """
    Classe que representa um Circulo no sistema de desenho.
    Responsabilidade: receber os pontos iniciais e finais a partir do clique do mouse e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        """
        Construtor da classe Circulo.
        
        @param cor_borda: str contendo a cor da borda da figura Circulo.
        @param cor_preenchimento: str contendo a cor interna da figura Circulo.
        @param x1: int coordenada X inical do clique.
        @param y1: int coordenada Y inical do clique.
        @param x2: int coordenada X final do arrasto.
        @param y2: int coordenada Y final do arrasto.
        """
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1 = x1, y1
        self._ajustar_circulo(x2, y2)

    def _ajustar_circulo(self, x2, y2):
        """
        Ajusta o retangulo diretor do Oval para que seja sempre equilatero

        @param x2: int coordenada X final do clique
        @param y2: int coordenada Y final do clique
        """
        dx = x2 - self.x1
        dy = y2 - self.y1
        size = max(abs(dx), abs(dy))
        self.x2 = self.x1 + size if dx >= 0 else self.x1 - size
        self.y2 = self.y1 + size if dy >= 0 else self.y1 - size

    def desenhar(self, canvas, dash=False):
        """
        Desenha o Circulo no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_preenchimento, outline=self.cor_borda,
                           width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """ 
        self._ajustar_circulo(x, y)


class PoligonoRegular(Figura):
    """
    Classe que representa um poligono regular de N lados no sistema de desenho.
    Responsabilidade: Calcular as coordenadas dos vertices com base no raio e renderizar a forma.
    
    @author JPChaves
    @version 1.0
    """
    def __init__(self, cor_borda, cor_preenchimento, num_lados, x1, y1, x2, y2):
        """
        Construtor da classe PoligonoRegular.
        
        @param cor: str com a cor da borda do poligono.
        @param preenchimento: str com a cor interna (vazio para transparente).
        @param lados: int com o numero de lados (minimo 3).
        @param x1: int coordenada X inicial do clique.
        @param y1: int coordenada Y inicial do clique.
        @param x2: int coordenada X final do arrasto.
        @param y2: int coordenada Y final do arrasto.
        """
        super().__init__(cor_borda, cor_preenchimento)
        self.num_lados = num_lados
        self.x1, self.y1 = x1, y1
        self._atualizar_pontos(x2, y2)

    def _atualizar_pontos(self, x2, y2):
        """
        Calcula os pontos da caixa delimitadora quadrada, o centro e o raio diretor do polígono.
        
        @param x2: int coordenada X atual do mouse.
        @param y2: int coordenada Y atual do mouse.
        """
        dx = x2 - self.x1
        dy = y2 - self.y1
        size = max(abs(dx), abs(dy))
        self.x2 = self.x1 + size if dx >= 0 else self.x1 - size
        self.y2 = self.y1 + size if dy >= 0 else self.y1 - size
        self.centro_x = (self.x1 + self.x2) / 2
        self.centro_y = (self.y1 + self.y2) / 2
        self.raio = size / 2
        self._calcular_vertices()

    def _calcular_vertices(self):
        """
        Calcula as coordenadas (x, y) de cada vértice utilizando trigonometria a partir de um ângulo inicial.
        """
        self.vertices = []
        angulo_inicial = -math.pi / 2
        incremento = 2 * math.pi / self.num_lados
        for i in range(self.num_lados):
            ang = angulo_inicial + i * incremento
            x = self.centro_x + self.raio * math.cos(ang)
            y = self.centro_y + self.raio * math.sin(ang)
            self.vertices.append((x, y))

    def desenhar(self, canvas, dash=False):
        """
        Desenha o Poligono Regular no Canvas do Tkinter.
        
        @param canvas: Objeto Canvas onde a figura será renderizada.
        @param dash: bool indicando se a borda deve ser desenhada com traço tracejado (para pré-visualização).
        """
        print(self.cor_preenchimento)
        pontos_planos = []
        for x, y in self.vertices:
            pontos_planos.extend([x, y])
        canvas.create_polygon(pontos_planos,
                              fill=self.cor_preenchimento, outline=self.cor_borda,
                              width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais da figura de forma dinâmica durante o arrasto do mouse.
        
        @param x: int nova coordenada X do mouse.
        @param y: int nova coordenada Y do mouse.
        """
        self._atualizar_pontos(x, y)