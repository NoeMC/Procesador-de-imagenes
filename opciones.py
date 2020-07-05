from tkinter import *

class opciones:

    def __init__(self,campos,padre,nombre = 'procesado'):
        self.raizV = Toplevel(padre)
        self.raizV.title(nombre)
        self.raizV.geometry('300x200')
        self.entradas = {}
        self.campos = campos
        self.valores = []
        for campo in campos:
            row = Frame(self.raizV)
            lab = Label(row, width=8, text=campo+" :", anchor='nw')
            ent = Entry(row)
            ent.insert(0, "0")
            row.pack(side="top", 
                    fill="y", 
                    padx=20, 
                    pady=5)
            lab.pack(side="left")
            ent.pack(side="right", 
                    expand="yes", 
                    fill="y")
            self.entradas[campo] = ent
        b1 = Button(self.raizV, text='Aplicar',command = lambda: self.quitaVentana(self.raizV))
        b1.pack(side = 'right',padx = 5, pady = 5 )
        padre.wait_window(self.raizV) #el gran hallazgo

    def quitaVentana(self,v):
        for campo in self.campos:
            self.valores.append(float(self.entradas[campo].get()))
        self.raizV.destroy()
    
    def getValores(self):
        return self.valores
