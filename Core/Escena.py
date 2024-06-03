from .NodoEscena import NodoEscena
from .Efectos import Efectos
from .Utilidades import Utilidades


class Escena:
    def __init__(self, datos):
        self.raiz = None  # Nodo raíz del árbol
        self.crear_raiz(datos)

    def crear_raiz(self, datos):
        # Crea el nodo raíz con una imagen especificada.
        self.raiz = NodoEscena(datos)

    def obtener_raiz(self):
        # Devuelve el nodo raíz de la escena.
        return self.raiz

    def agregar_elemento(self, padre, datos=None):
        # Agrega un nuevo elemento a la escena bajo el nodo padre especificado.
        nuevo_nodo = NodoEscena(datos)
        padre.agregar_hijo(nuevo_nodo)
        return nuevo_nodo

    def construir_escena(self, numero_escena, imagen_escena_actual, nodo_astro, efectos):
        info_astro = nodo_astro.obtener_info()

        numero_imagenes = 72
        radio_maximo = info_astro['radio_maximo'] 

        incremento = radio_maximo / numero_imagenes

        imagen_construida = None

        for i in range(1, numero_imagenes + 1):
            imagen_astro_efecto = Efectos.fade_circular(nodo_astro.obtener_imagen(), int(i * incremento), info_astro['centro_x'], info_astro['centro_y'])
            # combinar con la escena actual
            imagen_construida = Efectos.combinar_astro_con_escena(info_astro, imagen_astro_efecto, imagen_escena_actual)

            nombre_escena = Utilidades.obtener_nombre_escena(numero_escena, i)

            Utilidades.escribir_imagen(nombre_escena, efectos.escalar_a_imagen_original(imagen_construida))
            print(nombre_escena)

        if imagen_construida is not None:
            # aqui se manda la ultima escena que generó y la combina con la imagen sin los astros para que se vea reflejado el avance
            efectos.asignar_con_fondo_sin_astros(imagen_construida)

        

    def recorrer_escena(self, porcentaje, numero_escena, columna_inicial, efectos, nodo=None, nivel=0, imagen_a_construir=None):
        # Recorre el árbol de la escena y muestra la estructura.

        if nodo is None:
            nodo = self.raiz

        nodo_nombre = nodo.obtener_nombre()
        nodo_porcentaje = nodo.obtener_porcentaje()

        # Imprimir el nombre del nodo con un sangrado para indicar el nivel en el árbol
        print(" " * nivel * 2 + f"- {nodo_nombre} - porcentaje {nodo_porcentaje}")

        if imagen_a_construir is None and nivel == 0:
            imagen_a_construir = nodo.obtener_imagen()
            print(f'columna_inicial: {columna_inicial}')
            print(imagen_a_construir.shape)
        else:
            # coincide el porcentaje que se lleva con el porcentaje de aparicion del nodo
            if nodo_porcentaje is not None and porcentaje == nodo_porcentaje:
                print(" " * nivel * 3 + f"- {nodo_nombre} - seleccionado")
                self.construir_escena(numero_escena, imagen_a_construir, nodo, efectos)

        # Recorrer los nodos hijos recursivamente
        for hijo in nodo.obtener_hijos():
            self.recorrer_escena(porcentaje, numero_escena, columna_inicial, efectos, hijo, nivel + 1, imagen_a_construir)
