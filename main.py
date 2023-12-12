#main.py
from controller import Controller
from view import View
from model import Model


if __name__ == "__main__":      
    # Model
    model = Model()

    # View
    view = View(model)

    # Controller
    controller = Controller(model, view)
    
    # Run root.mainloop
    view.mainloop()
