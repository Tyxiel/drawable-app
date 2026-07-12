# main.py
from tkinter import Tk
from src.model import DrawingModel
from src.view import DrawingView
from src.controller import DrawingController

if __name__ == "__main__":
    root = Tk()
    root.title("Paint Orientado a Objetos (MVC)")

    model = DrawingModel()
    view = DrawingView(root, None)
    controller = DrawingController(model, view)
    view.configurar_controller(controller)

    root.mainloop()