from abc import ABC, abstractmethod
import math

class Figura(ABC):
    """Classe abstrata base para todas as figuras."""
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_preenchimento = cor_preenchimento
        self.cor_borda = cor_borda

    @abstractmethod
    def desenhar(self, canvas, dash=False):
        """Desenha a figura no canvas. Se dash=True, usa traço tracejado."""
        pass

    @abstractmethod
    def atualizar(self, x, y):
        """Atualiza a figura durante o movimento do mouse (para figuras em construção)."""
        pass


class Linha(Figura):
    def __init__(self, cor_borda, x1, y1, x2, y2):
        super().__init__(cor_borda, cor_preenchimento=None)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y


class Rabisco(Figura):
    def __init__(self, cor_borda):
        super().__init__(cor_borda, cor_preenchimento=None)
        self.pontos = []  # lista de coordenadas (x1,y1,x2,y2,...)

    def adicionar_ponto(self, x, y):
        self.pontos.append(x)
        self.pontos.append(y)

    def desenhar(self, canvas, dash=False):
        if len(self.pontos) >= 4:
            canvas.create_line(self.pontos, fill=self.cor_borda, width=3,
                               dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self.adicionar_ponto(x, y)


class Retangulo(Figura):
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                fill=self.cor_preenchimento, outline=self.cor_borda,
                                width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y


class Oval(Figura):
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=False):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_preenchimento, outline=self.cor_borda,
                           width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y


class Circulo(Figura):
    def __init__(self, cor_borda, cor_preenchimento, x1, y1, x2, y2):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1, self.y1 = x1, y1
        self._ajustar_circulo(x2, y2)

    def _ajustar_circulo(self, x2, y2):
        dx = x2 - self.x1
        dy = y2 - self.y1
        size = max(abs(dx), abs(dy))
        self.x2 = self.x1 + size if dx >= 0 else self.x1 - size
        self.y2 = self.y1 + size if dy >= 0 else self.y1 - size

    def desenhar(self, canvas, dash=False):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_preenchimento, outline=self.cor_borda,
                           width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self._ajustar_circulo(x, y)


class PoligonoRegular(Figura):
    def __init__(self, cor_borda, cor_preenchimento, num_lados, x1, y1, x2, y2):
        super().__init__(cor_borda, cor_preenchimento)
        self.num_lados = num_lados
        self.x1, self.y1 = x1, y1
        self._atualizar_pontos(x2, y2)

    def _atualizar_pontos(self, x2, y2):
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
        self.vertices = []
        angulo_inicial = -math.pi / 2
        incremento = 2 * math.pi / self.num_lados
        for i in range(self.num_lados):
            ang = angulo_inicial + i * incremento
            x = self.centro_x + self.raio * math.cos(ang)
            y = self.centro_y + self.raio * math.sin(ang)
            self.vertices.append((x, y))

    def desenhar(self, canvas, dash=False):
        print(self.cor_preenchimento)
        pontos_planos = []
        for x, y in self.vertices:
            pontos_planos.extend([x, y])
        canvas.create_polygon(pontos_planos,
                              fill=self.cor_preenchimento, outline=self.cor_borda,
                              width=3, dash=(4,2) if dash else ())

    def atualizar(self, x, y):
        self._atualizar_pontos(x, y)