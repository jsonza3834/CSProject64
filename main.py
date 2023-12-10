import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from controller import Controller
from view import View
from model import Model


if __name__ == "__main__":
   
    output_file_path = "cleaned.wav"  

    root = tk.Tk()
    root.title('Interactive Data Acoustic Modeling')
    root.resizable(False, False)
    root.geometry('650x800')

    
    # Model
    model = Model()
    
    view = View(root, model)

    controller = Controller(root, model, view, output_file_path)
    
    # Process Audio
    
    
    



    
    root.mainloop()
