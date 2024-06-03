import cv2
import numpy as np
import os


class Utilidades:
    @staticmethod
    def leer_imagen(ruta_img):
        """
        Lee una imagen desde una ruta especificada.

        Parámetros:
            ruta_img (str): La ruta de la imagen a leer.

        Retorna:
            numpy.ndarray: La imagen leída en formato BGR o BGRA.
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        imagen = cv2.imread(ruta_img, cv2.IMREAD_UNCHANGED)
        if imagen is None:
            print("La imagen no existe")
            return None
        else:
            if imagen.shape[2] == 3:  # como es bgr -> bgra
                imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2BGRA)
        return imagen

    @staticmethod
    def escribir_imagen(nombre, imagen):
        """
        Escribe una imagen en el directorio de salida.

        Parámetros:
            nombre (str): El nombre del archivo de imagen.
            imagen (numpy.ndarray): La imagen a escribir.

        Retorna:
            bool: True si la escritura fue exitosa, False de lo contrario.
        """
        result = cv2.imwrite(f'../img/escenas/{nombre}.png', imagen)
        print(result)

    @staticmethod
    def validar_imagen(imagen):
        """
        Valida si la entrada es una matriz bidimensional (ndarray).

        Parámetros:
            imagen (numpy.ndarray): La imagen a validar.

        Retorna:
            numpy.ndarray: La imagen validada si es una matriz bidimensional.

        Lanza:
            ValueError: Si la entrada no es una matriz bidimensional.
        """
        if isinstance(imagen, np.ndarray):
            return imagen
        else:
            raise ValueError("Los datos deben ser una matriz bidimensional (ndarray).")

    @staticmethod
    def obtener_porcentajes_astros():
        """
        Obtiene una lista de porcentajes para el tamaño de los astros.

        Retorna:
            list: Una lista de porcentajes para el tamaño de los astros.
        """
        return [0.35, 0.37, 0.49, 0.8, 0.84, 0.92, 1]

    @staticmethod
    def obtener_nombre_escena(numero, i=None):
        """
        Genera el nombre de la escena.

        Parámetros:
            numero (int): El número de la escena.
            i (int, opcional): El índice de la escena (default: None).

        Retorna:
            str: El nombre de la escena generado.
        """
        id_escena = '00'
        if i is not None:
            id_escena = '0' + str(i) if i < 10 else str(i)

        numero_escena = str(numero)
        if numero < 10:
            numero_escena = '00' + str(numero)
        elif numero < 100:
            numero_escena = '0' + str(numero)

        return f'Escena{str(numero_escena)}.{id_escena}'

    @staticmethod
    def obtener_datos_astros():
        """
        Obtiene los datos de los astros.

        Retorna:
            dict: Un diccionario que contiene los datos de los astros.
        """
        path = '../img/assets/astros/'
        astro1 = Utilidades.leer_imagen(path + 'astro1.png')
        astro2 = Utilidades.leer_imagen(path + 'astro2.png')
        astro3 = Utilidades.leer_imagen(path + 'astro3.png')
        astro4 = Utilidades.leer_imagen(path + 'astro4.png')
        astro5 = Utilidades.leer_imagen(path + 'astro5.png')
        astro6 = Utilidades.leer_imagen(path + 'astro6.png')
        astro7 = Utilidades.leer_imagen(path + 'astro7.png')

        porcentajes_astros = Utilidades.obtener_porcentajes_astros()

        datos_astros = {
            '1': {
                'nombre': 'astro1',
                'pos_inicial': 475,
                'imagen': astro1,
                'porcentaje': porcentajes_astros[0],
                'info': {
                    'centro_x': 90,
                    'centro_y': 43,
                    'radio_maximo': 123,
                    'inicial_x': 80,
                    'inicial_y': 0,
                }
            },
            '2': {
                'nombre': 'astro2',
                'pos_inicial': 388,
                'imagen': astro2,
                'porcentaje': porcentajes_astros[1],
                'info': {
                    'centro_x': 30,
                    'centro_y': 30,
                    'radio_maximo': 44,
                    'inicial_x': 5,
                    'inicial_y': 40,
                }
            },
            '3': {
                'nombre': 'astro3',
                'pos_inicial': 313,
                'imagen': astro3,
                'porcentaje': porcentajes_astros[2],
                'info': {
                    'centro_x': 37,
                    'centro_y': 0,
                    'radio_maximo': 42,
                    'inicial_x': 3,
                    'inicial_y': 0,
                }
            },
            '4': {
                'nombre': 'astro4',
                'pos_inicial': 124,
                'imagen': astro4,
                'porcentaje': porcentajes_astros[3],
                'info': {
                    'centro_x': 23,
                    'centro_y': 18,
                    'radio_maximo': 31,
                    'inicial_x': 2,
                    'inicial_y': 105,
                }
            },
            '5': {
                'nombre': 'astro5',
                'pos_inicial': 115,
                'imagen': astro5,
                'porcentaje': porcentajes_astros[4],
                'info': {
                    'centro_x': 50,
                    'centro_y': 50,
                    'radio_maximo': 71,
                    'inicial_x': 18,
                    'inicial_y': 190,
                }
            },
            '6': {
                'nombre': 'astro6',
                'pos_inicial': 53,
                'imagen': astro6,
                'porcentaje': porcentajes_astros[5],
                'info': {
                    'centro_x': 28,
                    'centro_y': 26,
                    'radio_maximo': 39,
                    'inicial_x': 4,
                    'inicial_y': 10,
                }
            },
            '7': {
                'nombre': 'astro7',
                'pos_inicial': 0,
                'imagen': astro7,
                'porcentaje': porcentajes_astros[6],
                'info': {
                    'centro_x': 6,
                    'centro_y': 24,
                    'radio_maximo': 30,
                    'inicial_x': 0,
                    'inicial_y': 185,
                }
            },
        }
        return datos_astros
