from opciones import opciones
import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import math

class imutils:
    def __init__(self,padre):
        self.padre = padre

    def blancoNegro(self,imagen):
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    def metodoUnSharp(self,imagenOrigi, imagenBlur, k):
        """
        implementa el metodo Unsharp
        donde recibe como parametros, la imagen orignal,
        la imagen opcada, y el valor de k
        """
        n = float(k + 1) * imagenOrigi - float(k) * imagenBlur
        n = np.maximum(n, np.zeros(n.shape))
        n = np.minimum(n, 255 * np.ones(n.shape))
        n = n.round().astype(np.uint8)
        return n

    def opacar(self,original):
        return cv2.GaussianBlur(original,(5,5),0)

    
    def realce(self,imagen):
        campos = ('K')
        ventana = opciones(campos,self.padre,nombre = "unsharp")
        valores = ventana.getValores()
        ima = self.opacar(imagen)
        b = self.metodoUnSharp(imagen, ima, valores[0])
        return cv2.cvtColor(b,cv2.COLOR_BGR2RGB)
    
    def promedio(self, imagen):
        campos = ("tamaño",)
        ventana = opciones(campos,self.padre,nombre = "tamaño de la ventana")
        valores = ventana.getValores()
        ima = cv2.blur(imagen,(int(valores[0]),int(valores[0])))
        return cv2.cvtColor(ima,cv2.COLOR_BGR2RGB)

    def mediana(self,imagen):
        campos = ("tamaño",)
        ventana = opciones(campos,self.padre,nombre = "tamaño de la ventana")
        valores = ventana.getValores()
        ima = cv2.medianBlur(imagen,int(valores[0]))
        return cv2.cvtColor(ima,cv2.COLOR_BGR2RGB)

    def adjust_gamma(self,imagen, gamma):
    	invGamma = 1.0 / gamma
    	table = np.array([((i / 255.0) ** invGamma) * 255
    		for i in np.arange(0, 256)]).astype("uint8")
    	return cv2.LUT(imagen, table)
    
    def gamma(self,imagen):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        campos = ("gamma",)
        ventana = opciones(campos,self.padre,nombre = "unsharp")
        valores = ventana.getValores()
        adjusted = self.adjust_gamma(imagen, valores[0])
        return cv2.cvtColor(adjusted,cv2.COLOR_BGR2RGB)
    
    def ruidoimp(self,imagen):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        porcentaje=10
        dato_minimo=0
        dato_maximo=255
        height= imagen.shape[0]
        width =imagen.shape[1]
        tamaño=height*width
        auxiliar=(tamaño*porcentaje)//800
        #pixeles blancos
        for x in range(auxiliar):
     
            coordenada_x=random.randrange(2, width-2)
            coordenada_y=random.randrange(2, height-2)
            
            imagen[coordenada_y, coordenada_x]=dato_maximo 
            imagen[coordenada_y+1, coordenada_x]=dato_maximo 
            imagen[coordenada_y, coordenada_x+1]=dato_maximo 
            imagen[coordenada_y+1, coordenada_x+1]=dato_maximo 
     
        #pixeles negros
        for x in range(auxiliar):
     
            coordenada_x=random.randrange(2, width-2)
            coordenada_y=random.randrange(2, height-2)
            
            imagen[coordenada_y, coordenada_x]=dato_minimo
            imagen[coordenada_y+1, coordenada_x]=dato_minimo
            imagen[coordenada_y, coordenada_x+1]=dato_minimo 
            imagen[coordenada_y+1, coordenada_x+1]=dato_minimo
            
        return cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

    def imprime(self, nombre):
        plt.figure()
        plt.title("Histograma B&N")
        plt.xlabel("Bins")
        plt.ylabel("# de pixeles")
        plt.plot(nombre)
        plt.xlim([0, 256])
        plt.show()
    
    def muestraHisto(self, imagen):
        ima = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        ima = cv2.calcHist([ima], [0], None, [256], [0, 256])
        self.imprime(ima)
    
    def equalizaHisto(self, imagen):
        ima = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(ima)

    def sobel(self,imagen):
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        #sobel Blanco y negro
        sobel_x = np.array ([[1, 0, -1],[2, 0, -2],[1, 0, -1]]) 
        sobel_y = np.array ([[1, 2,  1],[0, 0, 0],[-1, -2, -1]])
        filter_imagey = cv2.filter2D (gray, -1, sobel_y)
        filter_imagex = cv2.filter2D (gray, -1, sobel_x)
        img_sobel = filter_imagey + filter_imagex

        return cv2.cvtColor(img_sobel,cv2.COLOR_BGR2RGB)
    
    def prewitt(self,imagen):
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
        kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        img_prewittx = cv2.filter2D(gray, -1, kernelx)
        img_prewitty = cv2.filter2D(gray, -1, kernely)
        img_prewitt = img_prewittx + img_prewitty
    
        return cv2.cvtColor(img_prewitt,cv2.COLOR_BGR2RGB)

    def ruidoGauss(self,image):
        campos = ("porcentaje","desviacion")
        ventana = opciones(campos,self.padre,nombre = "unsharp")
        valores = ventana.getValores()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean = valores[0]
        var = valores[1]
        sigma = var**0.5
        gaussian = np.random.normal(mean,sigma,(image.shape[0],image.shape[1]))
        noisy_image = np.zeros(image.shape, np.float32)
        if len(image.shape) == 2:
            noisy_image = image + gaussian
        else:
            noisy_image[:, :, 0] = image[:, :, 0] + gaussian
            noisy_image[:, :, 1] = image[:, :, 1] + gaussian
            noisy_image[:, :, 2] = image[:, :, 2] + gaussian
        cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
        noisy_image = noisy_image.astype(np.uint8)
        return cv2.cvtColor(noisy_image,cv2.COLOR_BGR2RGB)

    def laplacian(self,imagen):
        campos = ("Kernel",)
        ventana = opciones(campos,self.padre,nombre = "Tamaño de kernel")
        valores = ventana.getValores()
        imagen = cv2.GaussianBlur(imagen, (3, 3), 0)
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        dst = cv2.Laplacian(gray, cv2.CV_16S, ksize=int(valores[0]))
        abs_dst = cv2.convertScaleAbs(dst)
        return cv2.cvtColor(abs_dst,cv2.COLOR_BGR2RGB)
    
    def salYPi(self, imagen):
        campos = ("Sal y pimienta","cantidad")
        ventana = opciones(campos,self.padre,nombre = "Sal y Pimienta")
        valores = ventana.getValores()
        row, col, _ = imagen.shape
        print(row,col)
        salt_vs_pepper = valores[0]
        amount = valores[1]
        num_salt = np.ceil(amount * imagen[0].size * salt_vs_pepper)
        num_pepper = np.ceil(amount * imagen[0].size * (1.0 - salt_vs_pepper))
    
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in imagen.shape]
        imagen[coords[0], coords[1], :] = 1


        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in imagen.shape]
        imagen[coords[0], coords[1], :] = 0
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    def rotar(self, image):
        campos = ("Angulo",)
        ventana = opciones(campos,self.padre,nombre = "Rotar")
        valores = ventana.getValores()
        center = None
        (h, w) = image.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, valores[0], 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        return cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
    
    def traslacion(self, image):
        campos = ("valor X","valor Y")
        ventana = opciones(campos,self.padre,nombre = "trasladar")
        valores = ventana.getValores()
        M = np.float32([[1, 0, valores[0]], [0, 1, valores[1]]])
        shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return cv2.cvtColor(shifted, cv2.COLOR_BGR2RGB)

    def exponencial(self,img):
        campos = ("gamma (.5)",)
        ventana = opciones(campos,self.padre,nombre = "contraste Expo")
        valores = ventana.getValores()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rows = img.shape[0]
        columns = img.shape[1]
        
        img2 = np.zeros( (rows, columns), dtype = np.uint8)
        
        gamma = valores[0]
        c = 255/255**gamma
        
        for x in range(0,rows):
            for y in range(0,columns):
                n=img[x, y]
                dato=n*c*gamma
                img2[x, y] = dato      

        return cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    def segmentosLineales(self,img):
        campos = ("Intervalo A","Intervalo B")
        ventana = opciones(campos,self.padre,nombre = "Seleccionar segmentos")
        valores = ventana.getValores()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rows = img.shape[0]
        columns = img.shape[1]
        img2 = np.zeros( (rows, columns), dtype = np.uint8)
        
        #intervalos
        a = valores[0]
        b = valores[1]
    
        for x in range(0,rows):
            for y in range(0,columns):
                r = img[x][y]
                if a <=r and r<=b:
                    img2[x][y] = 255
                else:
                    img2[x][y] = 0
        
        return cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    def canny(self,img):
        campos = ("min val","max val")
        ventana = opciones(campos,self.padre,nombre = "valores")
        valores = ventana.getValores()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(img,valores[0],valores[1])
