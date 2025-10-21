import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    def __repr__(self):
        return f"<{self.tipo}:{self.valor}>"

class MiniBDLexer:
    PALABRAS_CLAVE = {
        "CREAR", "BASE", "MODIFICAR", "AJUSTAR", "TABLA", "AGREGAR", "COLUMNA",
        "ELIMINAR", "INDICE", "EN", "INSERTAR", "VALORES", "CONSULTAR", "DE",
        "DONDE", "ACTUALIZAR", "ESTABLECER", "NO", "NULO", "ENTERO", "DECIMAL",
        "TEXTO", "BOOLEANO", "VERDADERO", "FALSO"
    }

    TOKENS_REGEX = [
        ("DECIMAL_LITERAL", r"\d+\.\d+"),
        ("ENTERO_LITERAL", r"\d+"),
        ("CADENA_LITERAL", r"'[^']*'"),
        ("IDENTIFICADOR", r"[A-Za-zÁÉÍÓÚáéíóú_][A-Za-zÁÉÍÓÚáéíóú0-9_]*"),
        ("SIMBOLO", r"[(),;=+\-*/]"),
        ("ESPACIO", r"[ \t\r\n]+"),
    ]

    def __init__(self, texto):
        self.texto = texto

    def tokenizar(self):
        tokens = []
        pos = 0
        while pos < len(self.texto):
            match = None
            for tipo, patron in self.TOKENS_REGEX:
                regex = re.compile(patron)
                match = regex.match(self.texto, pos)
                if match:
                    valor = match.group(0)
                    if tipo == "ESPACIO":
                        break
                    elif tipo == "IDENTIFICADOR" and valor.upper() in self.PALABRAS_CLAVE:
                        tokens.append(Token(valor.upper(), valor.upper()))
                    else:
                        tokens.append(Token(tipo, valor))
                    break
            if not match:
                raise SyntaxError(f"Carácter no reconocido: '{self.texto[pos]}' en posición {pos}")
            pos = match.end(0)
        return tokens
