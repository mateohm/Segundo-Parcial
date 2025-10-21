import time
from pprint import pprint

class CYKParser:
    def __init__(self, reglas, simbolo_inicial):
        self.reglas = self.invertir_reglas(reglas)
        self.simbolo_inicial = simbolo_inicial

    def invertir_reglas(self, reglas):
        """Convierte el formato A -> α en α -> [A1, A2, ...]"""
        invertidas = {}
        for izquierda, derechas in reglas.items():
            for derecha in derechas:
                if derecha not in invertidas:
                    invertidas[derecha] = []
                invertidas[derecha].append(izquierda)
        return invertidas

    def analizar(self, cadena):
        """Implementación del algoritmo CYK"""
        n = len(cadena)
        if n == 0:
            return False

        # Crear una tabla triangular (matriz n x n)
        tabla = [[set() for _ in range(n)] for _ in range(n)]

        # llenar la diagonal con las reglas que generan terminales
        for i in range(n):
            simbolo = cadena[i]
            if simbolo in self.reglas:
                tabla[i][i].update(self.reglas[simbolo])

        # combinar subcadenas
        for l in range(2, n + 1):  # longitud de subcadena
            for i in range(n - l + 1):
                j = i + l - 1
                for k in range(i, j):
                    for A in tabla[i][k]:
                        for B in tabla[k + 1][j]:
                            if (A, B) in self.reglas:
                                tabla[i][j].update(self.reglas[(A, B)])

        pprint(tabla)  # mostrar tabla

        # La cadena es válida si el símbolo inicial esta en la celda superior derecha
        return self.simbolo_inicial in tabla[0][n - 1]


# Prueba de rendimiento
if __name__ == "__main__":
    # Gramatica en FNC
    reglas = {
        'S': [('A', 'B'), ('C', 'D')],
        'A': ['('],
        'B': ['S', ')'],
        'C': ['('],
        'D': [')']
    }

    parser = CYKParser(reglas, 'S')

    # Cadenas de prueba con distintos numeros de tokens
    pruebas = {
        1: "()",
        4: "()()",
        8: "()()()()",
        12: "()()()()()()"
    }

    resultados = []
    print("\n=== Pruebas de rendimiento CYK ===")
    for n, cadena in pruebas.items():
        inicio = time.perf_counter()
        aceptado = parser.analizar(list(cadena))
        fin = time.perf_counter()
        resultados.append((n, aceptado, fin - inicio))
        print(f"{n} tokens -> {'Aceptado' if aceptado else 'Rechazado'} | Tiempo: {fin - inicio:.6f}s")

    print("\nResumen de tiempos:")
    for r in resultados:
        print(f"Tokens: {r[0]} | Tiempo: {r[2]:.6f}s")
