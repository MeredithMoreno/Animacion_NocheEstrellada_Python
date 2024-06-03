import cv2
import numpy as np
import random
from .Area import Area


class Efectos:
    def __init__(self, imagen_original, imagen_sin_astros, imagen_espiral):
        self.imagen_original = imagen_original
        self.imagen_sin_astros = imagen_sin_astros
        self.imagen_espiral = imagen_espiral
        self.alto_imagen_original = imagen_original.shape[0]
        self.ancho_imagen_original = imagen_original.shape[1]

    @staticmethod
    def fade_circular(imagen_astro, radio_circunferencia, centro_x, centro_y):
        # Obtener dimensiones de la imagen
        alto, ancho, _ = imagen_astro.shape

        # Crear una imagen con canal alfa (fondo transparente) del mismo tamaño que la original
        imagen_con_alpha = np.zeros((alto, ancho, 4), dtype=np.uint8)

        # Copiar la imagen original a la nueva imagen con canal alfa
        imagen_con_alpha[:, :, :3] = imagen_astro[:, :, :3]  # Copiar los primeros 3 canales (RGB)

        # Crear una máscara circular blanca con el centro transparente
        mascara = np.zeros((alto, ancho), dtype=np.uint8)
        cv2.circle(mascara, (centro_x, centro_y), radio_circunferencia, (255, 255, 255), -1)

        # Aplicar la máscara al canal alfa para hacer transparente el área fuera del círculo
        imagen_con_alpha[:, :, 3] = mascara

        return imagen_con_alpha

    def efecto_espiral(self):

        imagen_modificada = self.imagen_espiral.copy()
        # Obtener dimensiones de la imagen
        alto, ancho, canales = imagen_modificada.shape

        # Iterar sobre grupos circulares de 10 píxeles de radio de forma aleatoria
        for _ in range(10):  # Modificar 10 grupos de píxeles por iteración
            # Seleccionar aleatoriamente el centro del círculo
            centro_x = random.randint(10, ancho - 10)
            centro_y = random.randint(10, alto - 10)

            # Crear una máscara circular
            mascara = np.zeros((alto, ancho), dtype=np.uint8)
            rr, cc = np.meshgrid(np.arange(alto), np.arange(ancho), indexing='ij')
            distancia = np.sqrt((rr - centro_y) ** 2 + (cc - centro_x) ** 2)
            mascara[distancia <= 10] = 255

            # Aplicar la intensificación del color solo dentro del círculo, considerando el canal alfa
            intensidad = random.uniform(1.0, 5.0)
            for canal in range(canales):  # Iterar sobre todos los canales
                # Aplicar la intensificación si el píxel está dentro del círculo y el canal no es el canal alfa
                if canal != 3:
                    imagen_modificada[:, :, canal][mascara == 255] = np.clip(
                        imagen_modificada[:, :, canal][mascara == 255] * intensidad, 0, 255).astype(np.uint8)

        # Añadir el canal alfa de la imagen original a la imagen modificada
        imagen_modificada = cv2.cvtColor(imagen_modificada, cv2.COLOR_RGB2RGBA)
        imagen_modificada[:, :, 3] = self.imagen_espiral[:, :, 3]

        return imagen_modificada

    def combinar_con_fondo_original(self, seccion):
        fondo_actual = self.imagen_original

        for i in range(seccion.shape[0]):
            for j in range(seccion.shape[1]):
                if seccion[i, j][3] != 0:
                    fondo_actual[i, j] = seccion[i, j]

        return fondo_actual

    def asignar_con_fondo_sin_astros(self, seccion):
        # asigna la seccion de la actual escena a la imagen sin astros
        fondo_modificado = self.imagen_sin_astros.copy()

        # calcular inicial y y inicial x
        posicion_x = self.ancho_imagen_original - seccion.shape[1]
        posicion_y = 0

        fondo_modificado[posicion_y:posicion_y + seccion.shape[0], posicion_x:posicion_x + seccion.shape[1], :] = seccion

        self.imagen_sin_astros = fondo_modificado

    @staticmethod
    def combinar_con_fondo(fondo, seccion):

        fondo_actual = fondo

        for i in range(seccion.shape[0]):
            for j in range(seccion.shape[1]):
                if seccion[i, j][3] != 0:
                    fondo_actual[i, j] = seccion[i, j]

        return fondo_actual

    def escalar_a_imagen_original(self, imagen):
        return cv2.resize(imagen, (self.ancho_imagen_original, self.alto_imagen_original), interpolation=cv2.INTER_AREA)

    @staticmethod
    def seleccionar_area(area, imagen):
        seccion = imagen[area.yInicial:area.yInicial + area.alto, area.xInicial:area.xInicial + area.ancho]
        return seccion

    @staticmethod
    def combinar_astro_con_escena(info_astro, imagen_astro, imagen_escena):
        posicion_x = info_astro['inicial_x']
        posicion_y = info_astro['inicial_y']

        imagen_escena_modificada = imagen_escena.copy()

        area_a_recortar = Area(posicion_x, posicion_y, imagen_astro.shape[1], imagen_astro.shape[0])
        fondo_seleccionado = Efectos.seleccionar_area(area_a_recortar, imagen_escena)

        combinado = Efectos.combinar_con_fondo(fondo_seleccionado, imagen_astro)
        # Insertar la sección en la imagen modificada
        imagen_escena_modificada[posicion_y:posicion_y + combinado.shape[0], posicion_x:posicion_x + combinado.shape[1], :] = combinado

        return imagen_escena_modificada

    def zoom_out(self, percent):
        # se calcula el ancho y alto de acuerdo a porcentaje, y respetando la relación de aspecto
        alto_cropped_percent = round(self.alto_imagen_original * percent)
        ancho_cropped_percent = round(self.ancho_imagen_original * percent)

        # se resta para obtener las coordenadas de la columna inicial, es la que se va recorriendo
        columna_inicial = self.ancho_imagen_original - ancho_cropped_percent

        lanoche_cropped = self.imagen_sin_astros[0:alto_cropped_percent, columna_inicial:self.ancho_imagen_original]

        return {
            'imagen': lanoche_cropped,
            'columna_inicial': columna_inicial
        }

    