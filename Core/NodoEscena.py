from .Utilidades import Utilidades


class NodoEscena:
    """
    Clase para representar un nodo en el árbol de la escena.
    """

    def __init__(self, datos):
        # print(datos)
        self.nombre = datos['nombre']
        self.imagen = Utilidades.validar_imagen(datos['imagen'])
        self.pos_inicial = datos['pos_inicial']
        self.porcentaje = datos['porcentaje']
        self.info = datos['info']
        self.is_activo = True
        self.hijos = []  # Lista de nodos hijos

    def agregar_hijo(self, hijo):
        # Agrega un hijo a este nodo.
        self.hijos.append(hijo)

    def obtener_hijos(self):
        # Devuelve la lista de nodos hijos.
        return self.hijos

    def obtener_porcentaje(self):
        return self.porcentaje

    def obtener_imagen(self):
        return self.imagen

    def obtener_info(self):
        return self.info

    def obtener_nombre(self):
        return self.nombre

    def activa(self):
        self.is_activo = True

    def desactiva(self):
        self.is_activo = False

    def actualizar_imagen(self, imagen):
        # Asigna una nueva matriz bidimensional al nodo.
        self.imagen = Utilidades.validar_imagen(imagen)

    def actualizar_nombre(self, nombre):
        self.nombre = nombre

    def actualizar_porcentaje(self, porcentaje):
        self.porcentaje = porcentaje

