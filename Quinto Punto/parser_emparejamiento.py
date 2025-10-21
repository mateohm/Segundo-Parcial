tokens = []
indice = 0
token_actual = ""

def inicializar(entrada):
    global tokens, indice, token_actual
    tokens = entrada.split() + ["$"]
    indice = 0
    token_actual = tokens[indice]

def emparejar(token_esperado):
    """Verifica que el token actual coincide con el esperado y avanza."""
    global indice, token_actual
    if token_actual == token_esperado:
        indice += 1
        token_actual = tokens[indice]
    else:
        raise SyntaxError(f"Error de sintaxis: se esperaba '{token_esperado}', pero se encontró '{token_actual}'.")

# Reglas gramaticales
def E():
    T()
    E_prima()

def E_prima():
    if token_actual == "+":
        emparejar("+")
        T()
        E_prima()

def T():
    F()
    T_prima()

def T_prima():
    if token_actual == "*":
        emparejar("*")
        F()
        T_prima()

def F():
    if token_actual == "(":
        emparejar("(")
        E()
        emparejar(")")
    elif token_actual == "id":
        emparejar("id")
    else:
        raise SyntaxError(f"Token inesperado: '{token_actual}'.")

def analizar(cadena):
    inicializar(cadena)
    E()
    if token_actual == "$":
        print("Cadena aceptada.")
    else:
        print(f"Cadena no aceptada. Tokens restantes: {token_actual}")

#  Pruebas 
if __name__ == "__main__":
    print("=== PRUEBAS DEL ALGORITMO DE EMPAREJAMIENTO ===")
    cadenas = [
        "id + id * id",
        "( id + id ) * id",
        "id * ( id + id )",
        "id + * id"  # Error
    ]
    for c in cadenas:
        print(f"\nProbando: {c}")
        try:
            analizar(c)
        except Exception as e:
            print("Error:", e)
