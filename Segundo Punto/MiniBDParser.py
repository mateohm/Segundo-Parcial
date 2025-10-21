from MiniBDLexer import MiniBDLexer

class MiniBDParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, tipo=None):
        tok = self.actual()
        if tok is None:
            raise SyntaxError("Fin inesperado del código.")
        if tipo and tok.tipo != tipo and tok.valor != tipo:
            raise SyntaxError(f"Se esperaba '{tipo}' pero se encontró '{tok.valor}'.")
        self.pos += 1
        return tok

    def programa(self):
        while self.actual():
            self.sentencia()

    def sentencia(self):
        t = self.actual()
        if t is None:
            return
        val = t.valor.upper()
        if val == "CREAR":
            self.crear()
        elif val == "MODIFICAR":
            self.modificar()
        elif val == "ELIMINAR":
            self.eliminar()
        elif val == "INSERTAR":
            self.insertar()
        elif val == "CONSULTAR":
            self.consultar()
        elif val == "ACTUALIZAR":
            self.actualizar()
        else:
            raise SyntaxError(f"Sentencia desconocida: {val}")

    def crear(self):
        self.consumir("CREAR")
        siguiente = self.actual().valor.upper()
        if siguiente == "BASE":
            self.consumir("BASE")
            self.consumir("IDENTIFICADOR")
            self.consumir(";")
        elif siguiente == "TABLA":
            self.consumir("TABLA")
            self.consumir("IDENTIFICADOR")
            self.consumir("(")
            self.columna_def()
            while self.actual().valor == ",":
                self.consumir(",")
                self.columna_def()
            self.consumir(")")
            self.consumir(";")
        else:
            raise SyntaxError("Se esperaba 'BASE' o 'TABLA' después de CREAR.")

    def modificar(self):
        self.consumir("MODIFICAR")
        siguiente = self.actual().valor.upper()
        if siguiente == "BASE":
            self.consumir("BASE")
            self.consumir("IDENTIFICADOR")
            self.consumir("AJUSTAR")
            self.consumir("IDENTIFICADOR")
            self.consumir(";")
        elif siguiente == "TABLA":
            self.consumir("TABLA")
            self.consumir("IDENTIFICADOR")
            self.consumir("AGREGAR")
            self.consumir("COLUMNA")
            self.columna_def()
            self.consumir(";")
        else:
            raise SyntaxError("Se esperaba 'BASE' o 'TABLA' después de MODIFICAR.")

    def eliminar(self):
        self.consumir("ELIMINAR")
        siguiente = self.actual().valor.upper()
        if siguiente == "TABLA":
            self.consumir("TABLA")
            self.consumir("IDENTIFICADOR")
            self.consumir(";")
        elif siguiente == "DE":
            self.consumir("DE")
            self.consumir("IDENTIFICADOR")
            if self.actual().valor.upper() == "DONDE":
                self.consumir("DONDE")
                self.expresion()
            self.consumir(";")
        else:
            raise SyntaxError("Se esperaba 'TABLA' o 'DE' después de ELIMINAR.")

    def insertar(self):
        self.consumir("INSERTAR")
        self.consumir("EN")
        self.consumir("IDENTIFICADOR")
        self.consumir("(")
        self.consumir("IDENTIFICADOR")
        while self.actual().valor == ",":
            self.consumir(",")
            self.consumir("IDENTIFICADOR")
        self.consumir(")")
        self.consumir("VALORES")
        self.consumir("(")
        self.literal()
        while self.actual().valor == ",":
            self.consumir(",")
            self.literal()
        self.consumir(")")
        self.consumir(";")

    def consultar(self):
        self.consumir("CONSULTAR")
        if self.actual().valor == "*":
            self.consumir("*")
        else:
            self.consumir("IDENTIFICADOR")
            while self.actual().valor == ",":
                self.consumir(",")
                self.consumir("IDENTIFICADOR")
        self.consumir("DE")
        self.consumir("IDENTIFICADOR")
        if self.actual() and self.actual().valor.upper() == "DONDE":
            self.consumir("DONDE")
            self.expresion()
        self.consumir(";")

    def actualizar(self):
        self.consumir("ACTUALIZAR")
        self.consumir("IDENTIFICADOR")
        self.consumir("ESTABLECER")
        self.consumir("IDENTIFICADOR")
        self.consumir("=")
        self.expresion()
        while self.actual().valor == ",":
            self.consumir(",")
            self.consumir("IDENTIFICADOR")
            self.consumir("=")
            self.expresion()
        if self.actual() and self.actual().valor.upper() == "DONDE":
            self.consumir("DONDE")
            self.expresion()
        self.consumir(";")

    def columna_def(self):
        self.consumir("IDENTIFICADOR")
        self.consumir("IDENTIFICADOR")  
        if self.actual() and self.actual().valor.upper() == "NO":
            self.consumir("NO")
            self.consumir("NULO")

    def literal(self):
        tok = self.actual()
        if tok.tipo in ("ENTERO_LITERAL", "DECIMAL_LITERAL", "CADENA_LITERAL") or tok.valor.upper() in ("VERDADERO", "FALSO"):
            self.consumir(tok.tipo if tok.tipo != "IDENTIFICADOR" else tok.valor.upper())
        else:
            raise SyntaxError("Se esperaba un valor literal.")

    def expresion(self):
        if self.actual().tipo == "IDENTIFICADOR":
            self.consumir("IDENTIFICADOR")
            if self.actual().valor in ("=", ">", "<", "+", "-", "*", "/"):
                self.consumir(self.actual().valor)
                if self.actual().tipo in ("IDENTIFICADOR", "ENTERO_LITERAL", "DECIMAL_LITERAL", "CADENA_LITERAL"):
                    self.consumir(self.actual().tipo)
                else:
                    raise SyntaxError("Expresión mal formada.")
            else:
                raise SyntaxError("Operador no válido en expresión.")
        else:
            raise SyntaxError("Se esperaba una expresión válida.")
