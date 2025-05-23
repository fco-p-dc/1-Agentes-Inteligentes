#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Francisco Del Castillo'

import entornos_f
import entornos_o
from random import choice
import random


class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, A, B, ..., I)
    donde robot puede tener los valores "A", "B", ..., "I"
    A, B, ..., I son los estados de los cuartos
    donde cada cuarto puede tener los valores "limpio", "sucio".

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    "subir" solo es válida en los primeros dos pisos.
    "bajar" solo es válida en los últimos dos pisos.
    Las acciones de subir y baja son mas costosas que las de mover a la izquierda o derecha.
    Limpiar es menor que cualquier accion
    
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=None):
        """
        Por default inicialmente el robot está en A y los nueve cuartos
        están sucios

        """

        if x0 is None:
            self.x0 = ["A", "sucio", "sucio", "sucio", "sucio",
                        "sucio", "sucio", "sucio", "sucio", "sucio"]
        else:
            self.x = x0[:]
        self.costo = 0

        self.adyacencias = {
            "A": {"ir_Derecha": "B", "bajar": "D"},
            "B": {"ir_Izquierda": "A", "ir_Derecha": "C", "bajar": "E"},
            "C": {"ir_Izquierda": "B", "bajar": "F"},
            "D": {"subir": "A", "ir_Derecha": "E", "bajar": "G"},
            "E": {"subir": "B", "ir_Derecha": "F", "ir_Izquierda": "D", "bajar": "H"},
            "F": {"subir": "C", "ir_Izquierda": "E", "bajar": "I"},
            "G": {"subir": "D", "ir_Derecha": "H"},
            "H": {"subir": "E", "ir_Derecha": "I", "ir_Izquierda": "G"},
            "I": {"subir": "F", "ir_Izquierda": "H"}
        }

    def accion_legal(self, accion):
        if accion == "limpiar" or accion == "nada":
            return True
        
        robot_actual = self.x[0]
        return accion in self.adyacencias[robot_actual]


    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        # Incrementa el costo si hace algo útil o si algún cuarto está sucio
        robot = self.x[0]
        algo_sucio = "sucio" in self.x[1:]
        
        if accion != "nada" or algo_sucio:
            self.costo += 1
            
        # Aplica la acción
        if accion == "limpiar":
            # Limpia el cuarto actual
            indice = self._indice_cuarto(robot)
            self.x[indice] = "limpio"
        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            # Mueve el robot según la dirección
            self.x[0] = self.adyacencias[robot][accion]

    def percepcion(self):
        robot = self.x[0]
        indice = self._indice_cuarto(robot)
        estado_limpieza = self.x[indice]
        return robot, estado_limpieza
    
    def _indice_cuarto(self, cuarto):
        """
        Auxliar para convertir una letra de cuarto en su índice 
        correspondiente en el array
        """
        
        return ord(cuarto) - ord('A') + 1

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones
        self.entorno = None  # Referencia al entorno para verificar acciones legales

    def programa(self, percepcion):
        if not percepcion:
            return choice(self.acciones)
        
        # Si tenemos percepcion, podemos filtrar acciones legales
        robot = percepcion[0]
        acciones_legales = []
        
        # Las acciones "limpiar" y "nada" siempre son legales
        acciones_legales.extend(["limpiar", "nada"])
        
        # Movimientos basados en la posicion actual
        movimientos = {
            "A": ["ir_Derecha", "bajar"],
            "B": ["ir_Izquierda", "ir_Derecha", "bajar"],
            "C": ["ir_Izquierda", "bajar"],
            "D": ["subir", "ir_Derecha", "bajar"],
            "E": ["subir", "ir_Derecha", "ir_Izquierda", "bajar"],
            "F": ["subir", "ir_Izquierda", "bajar"],
            "G": ["subir", "ir_Derecha"],
            "H": ["subir", "ir_Derecha", "ir_Izquierda"],
            "I": ["subir", "ir_Izquierda"]
        }
        
        if robot in movimientos:
            acciones_legales.extend(movimientos[robot])
        
        acciones_legales = [a for a in acciones_legales if a in self.acciones]
        
        if not acciones_legales:
            return "nada"  # Si no hay acciones legales, nada
            
        return choice(acciones_legales)


class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepcion):
        if not percepcion:  # Si no hay percepción, actua aleatoriamente
            return choice(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"])
        
        robot, situacion = percepcion
        
        # Si el cuarto está sucio, lo limpia
        if situacion == "sucio":
            return "limpiar"
        
        # Si no, se mueve a un cuarto adyacente aleatoriamente
        movimientos_posibles = {
            "A": ["ir_Derecha", "bajar"],
            "B": ["ir_Izquierda", "ir_Derecha", "bajar"],
            "C": ["ir_Izquierda", "bajar"],
            "D": ["subir", "ir_Derecha", "bajar"],
            "E": ["subir", "ir_Derecha", "ir_Izquierda", "bajar"],
            "F": ["subir", "ir_Izquierda", "bajar"],
            "G": ["subir", "ir_Derecha"],
            "H": ["subir", "ir_Derecha", "ir_Izquierda"],
            "I": ["subir", "ir_Izquierda"]
        }
        
        return choice(movimientos_posibles[robot])


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        
        self.modelo = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
        
        
        self.no_visitados = ["B", "C", "D", "E", "F", "G", "H", "I"]
        
        self.adyacencias = {
            "A": {"ir_Derecha": "B", "bajar": "D"},
            "B": {"ir_Izquierda": "A", "ir_Derecha": "C", "bajar": "E"},
            "C": {"ir_Izquierda": "B", "bajar": "F"},
            "D": {"subir": "A", "ir_Derecha": "E", "bajar": "G"},
            "E": {"subir": "B", "ir_Derecha": "F", "ir_Izquierda": "D", "bajar": "H"},
            "F": {"subir": "C", "ir_Izquierda": "E", "bajar": "I"},
            "G": {"subir": "D", "ir_Derecha": "H"},
            "H": {"subir": "E", "ir_Derecha": "I", "ir_Izquierda": "G"},
            "I": {"subir": "F", "ir_Izquierda": "H"}
        }
        
        # Invertimos la estructura para facilitar la busqueda de caminos
        self.ady_inverso = {}
        for origen, destinos in self.adyacencias.items():
            for accion, destino in destinos.items():
                if destino not in self.ady_inverso:
                    self.ady_inverso[destino] = {}
                self.ady_inverso[destino][self._accion_inversa(accion)] = origen

    def _accion_inversa(self, accion):
        inversas = {
            "ir_Derecha": "ir_Izquierda",
            "ir_Izquierda": "ir_Derecha",
            "subir": "bajar",
            "bajar": "subir"
        }
        return inversas.get(accion, accion)

    def programa(self, percepcion):
        # Actualiza el modelo interno con la percepcion actual
        if percepcion:
            robot, situacion = percepcion
            self.modelo[0] = robot
            indice = ord(robot) - ord('A') + 1
            self.modelo[indice] = situacion
            
            # Elimina el cuarto actual de la lista de no visitados
            if robot in self.no_visitados:
                self.no_visitados.remove(robot)
        
        # Decide
        robot = self.modelo[0]
        indice_actual = ord(robot) - ord('A') + 1
        estado_actual = self.modelo[indice_actual]
        
        if estado_actual == "sucio":
            return "limpiar"
        
        # Si hay cuartos no visitados, busca el mas cercano
        if self.no_visitados:
            proximo_paso = self._encontrar_paso_hacia_no_visitado(robot)
            return proximo_paso
        
        if all(estado == "limpio" for estado in self.modelo[1:]):
            return "nada"
        
        # Si queda sucio, va a el
        for i, estado in enumerate(self.modelo[1:], 1):
            if estado == "sucio":
                cuarto_sucio = chr(ord('A') + i - 1)
                # Encuentra el camino al cuarto sucio
                proximo_paso = self._encontrar_paso_hacia(robot, cuarto_sucio)
                return proximo_paso
        
        # Por defecto, moverse aleatoriamente
        return choice(list(self.adyacencias[robot].keys()))
    
    def _encontrar_paso_hacia_no_visitado(self, origen):
        """
        Encuentra el siguiente paso hacia el cuarto no visitado más cercano
        """
        if not self.no_visitados:
            return "nada"
        
        # BFS para encontrar el camino más corto a cualquier no visitado
        visitados = {origen}
        cola = [(origen, [])]
        
        while cola:
            nodo, camino = cola.pop(0)
            
            # Si este nodo es un cuarto no visitado, devuelve el primer paso del camino
            if nodo in self.no_visitados and nodo != origen:
                return camino[0]
                
            # Explora los vecinos
            for accion, vecino in self.adyacencias.get(nodo, {}).items():
                if vecino not in visitados:
                    nuevo_camino = camino + [accion] if camino else [accion]
                    cola.append((vecino, nuevo_camino))
                    visitados.add(vecino)
        
        # Por defecto, moverse aleatoriamente
        return choice(list(self.adyacencias[origen].keys()))
    
    def _encontrar_paso_hacia(self, origen, destino):
        """
        Encuentra el siguiente paso hacia el destino especificado
        """
        if origen == destino:
            return "nada"
        
        visitados = {origen}
        cola = [(origen, [])]
        
        while cola:
            nodo, camino = cola.pop(0)
            
            for accion, vecino in self.adyacencias.get(nodo, {}).items():
                if vecino not in visitados:
                    nuevo_camino = camino + [accion] if camino else [accion]
                    if vecino == destino:
                        return nuevo_camino[0]
                    cola.append((vecino, nuevo_camino))
                    visitados.add(vecino)
        
        # Por defecto, moverse aleatoriamente
        return choice(list(self.adyacencias[origen].keys()))

class NueveCuartosCompletamenteCiego(NueveCuartos):
    """
    Igual que NueveCuartos, pero no se puede ver nada

    """
    def percepcion(self):
        return []

class NueveCuartosCiego(NueveCuartos):
    """
    Igual que NueveCuartos, pero solo se puede ver el cuarto actual

    """
    def percepcion(self):
        return self.x[0] # Solo devuelve la posición del robot
    
class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo  ciego

    """
    def __init__(self):
        self.ubicacion_actual = "A"  # Asumimos que empezamos en A
        self.estados_limpieza = {cuarto: "desconocido" for cuarto in "ABCDEFGHI"}
        self.cuartos_limpiados = set()
        
        self.adyacencias = {
            "A": {"ir_Derecha": "B", "bajar": "D"},
            "B": {"ir_Izquierda": "A", "ir_Derecha": "C", "bajar": "E"},
            "C": {"ir_Izquierda": "B", "bajar": "F"},
            "D": {"subir": "A", "ir_Derecha": "E", "bajar": "G"},
            "E": {"subir": "B", "ir_Derecha": "F", "ir_Izquierda": "D", "bajar": "H"},
            "F": {"subir": "C", "ir_Izquierda": "E", "bajar": "I"},
            "G": {"subir": "D", "ir_Derecha": "H"},
            "H": {"subir": "E", "ir_Derecha": "I", "ir_Izquierda": "G"},
            "I": {"subir": "F", "ir_Izquierda": "H"}
        }
        
        # Plan de recorrido sistemático
        self.cuartos_objetivo = ["A", "B", "C", "F", "I", "H", "G", "D", "E"]
        self.objetivo_actual = 0

    def programa(self, percepcion):
        """
        Si percepcion contiene la ubicación actual, la usamos
        Si no, mantenemos nuestro modelo interno
        """
        # Intentar extraer ubicación de la percepción si está disponible
        if percepcion and len(percepcion) > 0:
            self.ubicacion_actual = percepcion[0]
        
        # Si no hemos limpiado el cuarto actual, limpiarlo
        if self.ubicacion_actual not in self.cuartos_limpiados:
            self.cuartos_limpiados.add(self.ubicacion_actual)
            return "limpiar"
        
        # Si todos los cuartos han sido visitados, terminar
        if len(self.cuartos_limpiados) >= 9:
            return "nada"
        
        # Moverse al siguiente cuarto objetivo
        if self.objetivo_actual < len(self.cuartos_objetivo):
            cuarto_objetivo = self.cuartos_objetivo[self.objetivo_actual]
            
            if self.ubicacion_actual == cuarto_objetivo:
                self.objetivo_actual += 1
                if self.objetivo_actual < len(self.cuartos_objetivo):
                    cuarto_objetivo = self.cuartos_objetivo[self.objetivo_actual]
                else:
                    return "nada"
            
            # Calcular ruta al cuarto objetivo
            accion = self._calcular_siguiente_movimiento(cuarto_objetivo)
            
            # Actualizar ubicación basada en la acción
            if accion in self.adyacencias[self.ubicacion_actual]:
                self.ubicacion_actual = self.adyacencias[self.ubicacion_actual][accion]
            
            return accion
        
        return "nada"
    
    def _calcular_siguiente_movimiento(self, destino):
        """
        Calcula el siguiente movimiento para llegar al destino
        usando BFS simple
        """
        if self.ubicacion_actual == destino:
            return "nada"
        
        # BFS para encontrar ruta más corta
        from collections import deque
        
        cola = deque([(self.ubicacion_actual, [])])
        visitados = {self.ubicacion_actual}
        
        while cola:
            cuarto_actual, ruta = cola.popleft()
            
            for accion, siguiente_cuarto in self.adyacencias[cuarto_actual].items():
                if siguiente_cuarto == destino:
                    return ruta[0] if ruta else accion
                
                if siguiente_cuarto not in visitados:
                    visitados.add(siguiente_cuarto)
                    cola.append((siguiente_cuarto, ruta + [accion]))
        
        return "nada"  # No se encontro ruta

class NueveCuartosEstocastico(NueveCuartos):
    """
    Igual que NueveCuartos, pero con probabilidades de 80% para limpiar 
    y 20% para no limpiar. Con 80% de probabilidad de moverse de cuarto
    y 10% de no moverse o 10% de realizar una accion legal aleatoria.

    """
    def __init__(self, x0=None):
        super().__init__(x0)
        
    def transicion(self, accion):
        
        if not self.accion_legal(accion):
            raise ValueError(f"La acción {accion} no es legal para este estado")
        
        # Incrementa el costo si hace algo util o si algun cuarto esta sucio
        robot = self.x[0]
        algo_sucio = "sucio" in self.x[1:]
        
        if accion != "nada" or algo_sucio:
            self.costo += 1
            
        # Estocastico numero
        probabilidad = random.random()
        
        if accion == "limpiar":
            # 80% de probabilidad de limpiar correctamente
            if probabilidad <= 0.8:
                indice = self._indice_cuarto(robot)
                self.x[indice] = "limpio"
            # 20% de probabilidad de no hacer nada
            # No se hace nada adicional
        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            if probabilidad <= 0.8:
                # 80% de probabilidad de moverse como se espera
                self.x[0] = self.adyacencias[robot][accion]
            elif probabilidad <= 0.9:
                # 10% de probabilidad de no hacer nada
                pass
            else:
                # 10% de probabilidad de hacer una accion legal aleatoria
                acciones_legales = list(self.adyacencias[robot].keys()) + ["limpiar", "nada"]
                accion_aleatoria = random.choice(acciones_legales)
                if accion_aleatoria == "limpiar":
                    indice = self._indice_cuarto(robot)
                    self.x[indice] = "limpio"
                elif accion_aleatoria != "nada":
                    self.x[0] = self.adyacencias[robot][accion_aleatoria]

class AgenteReactivoModeloNueveCuartosEstocastico(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo estocastico

    """
    def __init__(self):
        self.adyacencias = {
            "A": {"ir_Derecha": "B", "bajar": "D"},
            "B": {"ir_Izquierda": "A", "ir_Derecha": "C", "bajar": "E"},
            "C": {"ir_Izquierda": "B", "bajar": "F"},
            "D": {"subir": "A", "ir_Derecha": "E", "bajar": "G"},
            "E": {"subir": "B", "ir_Derecha": "F", "ir_Izquierda": "D", "bajar": "H"},
            "F": {"subir": "C", "ir_Izquierda": "E", "bajar": "I"},
            "G": {"subir": "D", "ir_Derecha": "H"},
            "H": {"subir": "E", "ir_Derecha": "I", "ir_Izquierda": "G"},
            "I": {"subir": "F", "ir_Izquierda": "H"}
        }
        
        # Estado interno del agente
        self.cuartos_verificados_limpios = set()  # Se guardan los cuartos limpios
        self.objetivo_actual = None
        self.accion_anterior = None
        self.ubicacion_anterior = None
        self.intentos_limpieza = {}  # Intentos por cuarto
        self.intentos_movimiento = 0  # Contador de intentos fallidos
        
    def programa(self, percepcion):
        """
        Programa reactivo que se adapta a las percepciones del ambiente estocastico
        """
        ubicacion_actual, estado_limpieza = percepcion
        
        # Verificar si la accion anterior tuvo exito
        self._verificar_accion_anterior(ubicacion_actual)
        
        if estado_limpieza == "limpio":
            self.cuartos_verificados_limpios.add(ubicacion_actual)
            if ubicacion_actual in self.intentos_limpieza:
                del self.intentos_limpieza[ubicacion_actual]
        
        accion = self._decidir_accion(ubicacion_actual, estado_limpieza)
        
        # Guardar informacion para la proxima iteracion
        self.accion_anterior = accion
        self.ubicacion_anterior = ubicacion_actual
        
        return accion
    
    def _verificar_accion_anterior(self, ubicacion_actual):
        """
        Verifica si la accion anterior tuvo el efecto esperado
        """
        if self.accion_anterior is None:
            return
            
        if self.accion_anterior in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            if self.ubicacion_anterior in self.adyacencias:
                ubicacion_esperada = self.adyacencias[self.ubicacion_anterior].get(self.accion_anterior)
                if ubicacion_actual == ubicacion_esperada:
                    # Movimiento exitoso
                    self.intentos_movimiento = 0
                else:
                    # Movimiento fallidoa
                    self.intentos_movimiento += 1
    
    def _decidir_accion(self, ubicacion_actual, estado_limpieza):
        """
        Decide la prxima accion basada en la percepcion actual
        """
        if estado_limpieza == "sucio":
            # Contar intentos de limpieza en este cuarto
            if ubicacion_actual not in self.intentos_limpieza:
                self.intentos_limpieza[ubicacion_actual] = 0
            
            self.intentos_limpieza[ubicacion_actual] += 1
            
            # Si hemos intentado muchas veces, tal vez mejor movernos y volver
            if self.intentos_limpieza[ubicacion_actual] > 5:
                self.intentos_limpieza[ubicacion_actual] = 0
                return self._mover_aleatoriamente(ubicacion_actual)
            
            return "limpiar"
        
        # Si todos los cuartos estan limpios, terminar
        if len(self.cuartos_verificados_limpios) >= 9:
            return "nada"
        
        # Buscar el proximo cuarto que necesita ser limpiado
        return self._buscar_siguiente_objetivo(ubicacion_actual)
    
    def _buscar_siguiente_objetivo(self, ubicacion_actual):
        """
        Busca el siguiente cuarto que necesita ser visitado
        """
        cuartos_no_verificados = []
        for cuarto in "ABCDEFGHI":
            if cuarto not in self.cuartos_verificados_limpios:
                cuartos_no_verificados.append(cuarto)
        
        if not cuartos_no_verificados:
            return "nada"
        
        # Cuarto mas cercano
        objetivo = self._cuarto_mas_cercano(ubicacion_actual, cuartos_no_verificados)
        
        if objetivo == ubicacion_actual:
            return "limpiar"
        
        # Calcular el siguiente movimiento hacia el objetivo
        return self._siguiente_movimiento_hacia(ubicacion_actual, objetivo)
    
    def _cuarto_mas_cercano(self, origen, candidatos):
        """
        Encuentra el cuarto mas cercano usando distancia Manhattan
        """
        def posicion(cuarto):
            # Convertir A-I a coordenadas (fila, columna)
            return divmod(ord(cuarto) - ord('A'), 3)
        
        pos_origen = posicion(origen)
        distancia_minima = float('inf')
        mas_cercano = candidatos[0]
        
        for candidato in candidatos:
            pos_candidato = posicion(candidato)
            distancia = abs(pos_origen[0] - pos_candidato[0]) + abs(pos_origen[1] - pos_candidato[1])
            if distancia < distancia_minima:
                distancia_minima = distancia
                mas_cercano = candidato
        
        return mas_cercano
    
    def _siguiente_movimiento_hacia(self, origen, destino):
        """
        Calcula el siguiente movimiento hacia el destino
        """
        if origen == destino:
            return "limpiar"
        
        # BFS con preferencia por movimientos que han fallado menos
        from collections import deque
        
        cola = deque([(origen, [])])
        visitados = {origen}
        
        while cola:
            cuarto_actual, ruta = cola.popleft()
            
            acciones_disponibles = list(self.adyacencias[cuarto_actual].items())
            
            # Si hemos tenido muchos fallos de movimiento, ser ma conservador
            if self.intentos_movimiento > 3:
                if self.accion_anterior in self.adyacencias[cuarto_actual]:
                    return self.accion_anterior
            
            for accion, siguiente_cuarto in acciones_disponibles:
                if siguiente_cuarto == destino:
                    return ruta[0] if ruta else accion
                
                if siguiente_cuarto not in visitados:
                    visitados.add(siguiente_cuarto)
                    cola.append((siguiente_cuarto, ruta + [accion]))
        
        # Si no encontramos ruta, movernos aleatoriamente
        return self._mover_aleatoriamente(origen)
    
    def _mover_aleatoriamente(self, ubicacion_actual):
        """
        Realiza un movimiento aleatorio cuando no hay una estrategia clara
        """
        acciones_movimiento = list(self.adyacencias[ubicacion_actual].keys())
        if acciones_movimiento:
            return random.choice(acciones_movimiento)
        return "nada"

class AgenteReactivoModeloNueveCuartosCompletamenteCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo completamente ciego

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ["?", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
        self.adyacencias = {
            "A": {"ir_Derecha": "B", "bajar": "D"},
            "B": {"ir_Izquierda": "A", "ir_Derecha": "C", "bajar": "E"},
            "C": {"ir_Izquierda": "B", "bajar": "F"},
            "D": {"subir": "A", "ir_Derecha": "E", "bajar": "G"},
            "E": {"subir": "B", "ir_Derecha": "F", "ir_Izquierda": "D", "bajar": "H"},
            "F": {"subir": "C", "ir_Izquierda": "E", "bajar": "I"},
            "G": {"subir": "D", "ir_Derecha": "H"},
            "H": {"subir": "E", "ir_Derecha": "I", "ir_Izquierda": "G"},
            "I": {"subir": "F", "ir_Izquierda": "H"}
        }
        
        # La estrategia será recorrer sistemáticamente todos los cuartos
        self.plan = self._generar_plan_recorrido()
        self.paso_actual = 0

    def programa(self, _):
        robot = self.modelo[0]
        
        # Si no sabemos dónde está el robot, suponemos que está en A
        if robot == "?":
            self.modelo[0] = "A"
            robot = "A"
        
        # Encuentra el índice del cuarto actual
        indice_actual = ord(robot) - ord('A') + 1
        estado_actual = self.modelo[indice_actual]
        
        # Si el cuarto actual está sucio, lo limpia
        if estado_actual == "sucio":
            accion = "limpiar"
            self.modelo[indice_actual] = "limpio"
            return accion
        
        # Sigue el plan de recorrido
        if self.paso_actual < len(self.plan):
            accion = self.plan[self.paso_actual]
            self.paso_actual += 1
            
            # Actualiza el modelo según la acción
            if accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
                destino = self.adyacencias[robot][accion]
                self.modelo[0] = destino
            elif accion == "limpiar":
                indice = ord(self.modelo[0]) - ord('A') + 1
                self.modelo[indice] = "limpio"
            
            return accion
        
        # Si hemos terminado el plan, verifica si todos los cuartos están limpios
        if all(estado == "limpio" for estado in self.modelo[1:]):
            return "nada"
        
        # Si aún hay cuartos sucios, regenera el plan
        self.plan = self._generar_plan_recorrido()
        self.paso_actual = 0
        return self.programa(_)
    
    def _generar_plan_recorrido(self):
        """
        Genera un plan para recorrer todos los cuartos sistemáticamente
        """
        # Este es un plan predefinido para recorrer todos los cuartos desde A
        # siguiendo un patrón en espiral o serpiente
        plan = [
            "limpiar" if self.modelo[1] == "sucio" else "nada",
            
            "ir_Derecha",
            "limpiar" if self.modelo[2] == "sucio" else "nada",
            
            "ir_Derecha",
            "limpiar" if self.modelo[3] == "sucio" else "nada",
            
            "bajar",
            "limpiar" if self.modelo[6] == "sucio" else "nada",
            
            "ir_Izquierda",
            "limpiar" if self.modelo[5] == "sucio" else "nada",
            
            "ir_Izquierda",
            "limpiar" if self.modelo[4] == "sucio" else "nada",
            
            "bajar",
            "limpiar" if self.modelo[7] == "sucio" else "nada",
            
            "ir_Derecha",
            "limpiar" if self.modelo[8] == "sucio" else "nada",
            
            "ir_Derecha",
            "limpiar" if self.modelo[9] == "sucio" else "nada"
        ]
        
        # Filtra los nada innecesarios
        return [accion for accion in plan if accion != "nada"]
        

def test():
    """
    Prueba del entorno y los agentes

    """
    x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoNuevecuartos(), 
                         200)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(x0), 
                         AgenteReactivoModeloNueveCuartosCiego(), 
                         200)
    
    #print("Prueba del entorno completamente ciego con un agente reactivo con modelo")
    #entornos_o.simulador(NueveCuartosCompletamenteCiego(x0), 
    #                     AgenteReactivoModeloNueveCuartosCompletamenteCiego(), 
    #                     200)
    
    print("\n--- Prueba del entorno estocástico con un agente reactivo con modelo ---")
    entornos_o.simulador(NueveCuartosEstocastico(x0), 
              AgenteReactivoModeloNueveCuartosEstocastico(), 
              200)


if __name__ == "__main__":
    test()