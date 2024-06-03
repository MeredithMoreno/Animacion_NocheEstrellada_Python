from .Escena import Escena
from .Efectos import Efectos
from .Utilidades import Utilidades
from .Render import Render


class Fuentes:
    def __init__(self):
        imagen_original = Utilidades.leer_imagen('../img/assets/lanoche.png')
        imagen_sin_astros = Utilidades.leer_imagen('../img/assets/sinastros.png')
        imagen_espiral = Utilidades.leer_imagen('../img/assets/espiral.png')
        self.efectos = Efectos(imagen_original, imagen_sin_astros, imagen_espiral)
        self.datos_astros = Utilidades.obtener_datos_astros()

    def ejecutar(self):
        porcentaje = 0.35  # porcentaje inicial
        numero_escena = 1  # primer escenaDVV

        result = self.efectos.zoom_out(porcentaje)  # se hace el primer zoom out
        columna_inicial = result['columna_inicial']

        datos_raiz = {
            'nombre': 'Escena' + str(numero_escena),
            'imagen': result['imagen'],
            'pos_inicial': None,
            'porcentaje': porcentaje,
            'info': None
        }

        escena = Escena(datos_raiz)  # Nodo raiz, tiene el fondo de la escena

        for astro, data in self.datos_astros.items():  # construir el arbol de la primer escena
            escena.agregar_elemento(escena.obtener_raiz(), data)

        escena.recorrer_escena(porcentaje, numero_escena, columna_inicial, self.efectos)  # primer recorrido, se arma la primer escena

        # se hace el efecto zoom out a toda la imagen
        while columna_inicial > 0 and porcentaje <= 1:
            porcentaje = round(porcentaje + 0.01, 2)
            numero_escena += 1

            result_escena = self.efectos.zoom_out(porcentaje)
            columna_inicial = result_escena['columna_inicial']

            porcentajes_astros = Utilidades.obtener_porcentajes_astros()
            nombre_escena = Utilidades.obtener_nombre_escena(numero_escena)

            if porcentaje in porcentajes_astros:
                # cambiar la imagen del nodo raiz, este sería la nueva escena
                nodo_raiz = escena.obtener_raiz()
                nodo_raiz.actualizar_imagen(result_escena['imagen'])
                nodo_raiz.actualizar_nombre(nombre_escena)
                nodo_raiz.actualizar_porcentaje(porcentaje)

                escena.recorrer_escena(porcentaje, numero_escena, columna_inicial, self.efectos)
            else:
                # print("Se imprimira una escena de acuerdo al porcentaje de avance")
                Utilidades.escribir_imagen(nombre_escena, self.efectos.escalar_a_imagen_original(result_escena['imagen']))

        # se hace el efecto de la espiral cuando ya se acabó el zoom out

        numero_imagenes_espiral = 72
        numero_escena += 1

        for i in range(numero_imagenes_espiral):
            espiral_random = self.efectos.efecto_espiral()
            fondo_combinado = self.efectos.combinar_con_fondo_original(espiral_random)
            nombre_escena_espiral = Utilidades.obtener_nombre_escena(numero_escena)
            Utilidades.escribir_imagen(nombre_escena_espiral, fondo_combinado)
            numero_escena += 1

        # ultimo paso se renderiza
        Render.renderizar()

