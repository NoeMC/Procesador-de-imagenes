from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
from imutils import imutils


class principal:
    def __init__(self):

        self.imaOriginal = None
        self.imaProcesada = None
        self.toGuardar = None
        self.VentanaRoot = Tk()
        it = imutils(self.VentanaRoot)
        self.menuBar = Menu(self.VentanaRoot)
        self.VentanaRoot.title("PDI-imagenes")
        self.VentanaRoot.geometry('1020x480')
        self.VentanaRoot.config(menu = self.menuBar)
        
        self.left_frame = Frame(self.VentanaRoot, width=450, height=400, bg='black')
        self.left_frame.grid(row=0, column=0,sticky=W+E, padx=10, pady=5)

        self.right_frame = Frame(self.VentanaRoot, width=450, height=400, bg='#5C5C5C')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)
        
        self.panelA = None
        self.panelB = None
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Abrir",command = self.colocarImagenOriginal)
        self.filemenu.add_command(label="Guardar", command = self.Guardar)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.VentanaRoot.quit)

        self.imagenMenu = Menu(self.menuBar, tearoff=0)
        self.subMenu = Menu(self.menuBar, tearoff=0)
        self.subMenu.add_command(label="Potencia", command = lambda : self.aplicaFiltro(it.exponencial(self.imaOriginal)))
        self.subMenu.add_command(label="Gamma", command = lambda : self.aplicaFiltro(it.gamma(self.imaOriginal)))
        self.imagenMenu.add_command(label = "GrayScale", command = lambda : self.aplicaFiltro(it.blancoNegro(self.imaOriginal)))
        self.imagenMenu.add_command(label = "Histograma", command = lambda : it.muestraHisto(self.imaOriginal))
        self.imagenMenu.add_command(label = "Histograma equalizado", command = lambda : self.aplicaFiltro(it.equalizaHisto(self.imaOriginal)))
        self.imagenMenu.add_command(label = "Segmentos lineales", command = lambda : self.aplicaFiltro(it.segmentosLineales(self.imaOriginal)))
        self.imagenMenu.add_cascade(label="Contraste", menu = self.subMenu)
        
        self.subFiltro = Menu(self.menuBar, tearoff=0)
        self.subFiltro.add_command(label = "Promedio", command = lambda : self.aplicaFiltro(it.promedio(self.imaOriginal)))
        self.subFiltro.add_command(label = "Mediana", command = lambda : self.aplicaFiltro(it.mediana(self.imaOriginal)))
        #self.subFiltro.add_command(label = "Media")

        self.menuOpera = Menu(self.menuBar, tearoff=0)
        #self.menuOpera.add_command(label = "Suma")
        #self.menuOpera.add_command(label = "Resta")
        self.menuOpera.add_command(label = "Rotacion", command = lambda : self.aplicaFiltro(it.rotar(self.imaOriginal)))
        self.menuOpera.add_command(label = "Traslacion", command = lambda : self.aplicaFiltro(it.traslacion(self.imaOriginal)))
        
        self.lineales =  Menu(self.menuBar, tearoff=0)
        self.lineales.add_command(label="Sobel", command = lambda : self.aplicaFiltro(it.sobel(self.imaOriginal)))
        self.lineales.add_command(label="Prewitt", command = lambda : self.aplicaFiltro(it.prewitt(self.imaOriginal)))
        self.lineales.add_command(label="Fre-Chen", command = lambda : self.aplicaFiltro(it.getFreiChenImage(self.imaOriginal)))

        self.altas = Menu(self.menuBar, tearoff=0)
        self.altas.add_command(label = "Laplaciano", command = lambda : self.aplicaFiltro(it.laplacian(self.imaOriginal)))
        self.altas.add_command(label = "High Boost", command = lambda : self.aplicaFiltro(it.realce(self.imaOriginal)))
        self.altas.add_command(label = "Unsharp", command = lambda : self.aplicaFiltro(it.realce(self.imaOriginal)))
        self.altas.add_cascade(label = "Gradiente",menu = self.lineales)
        self.altas.add_command(label = "Canny", command = lambda : self.aplicaFiltro(it.canny(self.imaOriginal)))

        self.filtroMenu = Menu(self.menuBar, tearoff=0)
        self.filtroMenu.add_cascade(label="Pasa bajas", menu = self.subFiltro)
        self.filtroMenu.add_cascade(label="Pasa Altas", menu = self.altas)

        self.ruido = Menu(self.menuBar, tearoff=0)
        #self.ruido.add_command(label = "Aditivo")
        self.ruido.add_command(label = "Impulsivo", command = lambda : self.aplicaFiltro(it.ruidoimp(self.imaOriginal)))
        self.ruido.add_command(label = "Gaussiano", command = lambda : self.aplicaFiltro(it.ruidoGauss(self.imaOriginal)))
        self.ruido.add_command(label = "Sal y pimienta", command = lambda : self.aplicaFiltro(it.salYPi(self.imaOriginal)))

        self.menuBar.add_cascade(label="Archivo", menu=self.filemenu)
        self.menuBar.add_cascade(label="Contraste", menu=self.imagenMenu)
        self.menuBar.add_cascade(label="Operaciones", menu=self.menuOpera)
        self.menuBar.add_cascade(label = "Ruido", menu = self.ruido)
        self.menuBar.add_cascade(label="Filtros", menu=self.filtroMenu)
        self.VentanaRoot.mainloop()
        
    
    def colocarImagenOriginal(self):
        ruta = filedialog.askopenfilename()
        if len(ruta) > 0:
            image = cv2.imread(ruta)
            self.imaOriginal = image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = self.formatoTK(image)
            if self.panelA is None: #or self.panelB is None
                self.panelA = Label(image=image)
                self.panelA.image = image
                self.panelA.pack(in_=self.left_frame,side="left", padx=10, pady=10)

            else:
                self.panelA.configure(image=image)
                self.panelA.image = image


    def colocarImagenProcesada(self):
        if self.panelB is None:
            self.panelB = Label(image=self.imaProcesada)
            self.panelB.image = self.imaProcesada
            self.panelB.pack(in_=self.right_frame, side="right", padx=10, pady=10)
        else:
            self.panelB.configure(image=self.imaProcesada)
            self.panelB.image = self.imaProcesada
        self.VentanaRoot.update()

    def formatoTK(self, image):
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image)
    
    def aplicaFiltro(self,image):
        self.toGuardar = image
        self.imaProcesada = self.formatoTK(image)
        self.colocarImagenProcesada()

    def Guardar(self):
        cv2.imwrite('imagen0.png',self.toGuardar)



a = principal()
