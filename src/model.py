class DrawingModel:
  def __init__(self):
    self.figuras = []
    self.figura_nova = None
    self.cor_borda_atual = "black"
    self.cor_preenchimento_atual = ""

  @staticmethod
  def is_figura_degenerada(fig):
    from src.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, PoligonoRegular
    if isinstance(fig, Rabisco):
        return len(fig.pontos) < 4
    if isinstance(fig, Linha):
        return (fig.x1, fig.y1) == (fig.x2, fig.y2)
    if isinstance(fig, (Retangulo, Oval, Circulo, PoligonoRegular)):
        return (fig.x1, fig.y1) == (fig.x2, fig.y2)
    return False