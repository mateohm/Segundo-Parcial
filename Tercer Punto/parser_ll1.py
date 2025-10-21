class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens + ['$']  # Agregar fin de cadena
        self.pos = 0
        self.pila = ['$', 'E']

    # Tabla LL(1) basada en la gramatica transformada
    TABLA = {
        ('E', 'id'): ['T', 'E\''],
        ('E', '('):  ['T', 'E\''],

        ('E\'', '+'): ['+', 'T', 'E\''],
        ('E\'', ')'): ['ε'],
        ('E\'', '$'): ['ε'],

        ('T', 'id'): ['F', 'T\''],
        ('T', '('):  ['F', 'T\''],

        ('T\'', '*'): ['*', 'F', 'T\''],
        ('T\'', '+'): ['ε'],
        ('T\'', ')'): ['ε'],
        ('T\'', '$'): ['ε'],

        ('F', 'id'): ['id'],
        ('F', '('): ['(', 'E', ')']
    }

    def analizar(self):
        print(f"\nTokens: {self.tokens}\n")
        while True:
            tope = self.pila[-1]
            actual = self.tokens[self.pos]
            print(f"Pila: {self.pila} | Token actual: {actual}")

            if tope == actual == '$':
                print("Cadena aceptada.")
                return True

            elif tope == actual:
                # Coincidencia terminal
                self.pila.pop()
                self.pos += 1

            elif tope in ('+', '*', '(', ')', 'id', '$'):
                # Error: terminal no coincide
                raise SyntaxError(f"Error sintáctico: se esperaba {tope}, se encontró {actual}")

            else:
                # No terminal: buscar producción
                produccion = self.TABLA.get((tope, actual))
                if not produccion:
                    raise SyntaxError(f"No hay regla para ({tope}, {actual})")

                # Aplicar producción
                self.pila.pop()
                if produccion != ['ε']:
                    for simbolo in reversed(produccion):
                        self.pila.append(simbolo)

    @staticmethod
    def tokenizar(cadena):
        # Tokenizacion simple (id, operadores, parentesis)
        tokens = []
        for c in cadena.split():
            if c in ('+', '*', '(', ')'):
                tokens.append(c)
            else:
                tokens.append('id')
        return tokens

# Prueba rapida 
if __name__ == "__main__":
    expresion = "id + id * id"
    tokens = ParserLL1.tokenizar(expresion)
    parser = ParserLL1(tokens)
    parser.analizar()
