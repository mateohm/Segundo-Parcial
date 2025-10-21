from antlr4 import *
from MiniBDLexer import MiniBDLexer
from MiniBDParser import MiniBDParser
import sys

# ejecuta una sentencia y verifica si es válida
def probar_sentencia(codigo, descripcion):
    print(f"\n--- Prueba: {descripcion} ---")
    input_stream = InputStream(codigo)
    lexer = MiniBDLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = MiniBDParser(tokens)
    parser.removeErrorListeners()
    
    try:
        parser.programa()
        print("✅ Sintaxis válida")
    except Exception as e:
        print("❌ Error de sintaxis:", str(e))

# PRUEBAS CRUD 

# C - CREAR
crear = """
CREAR TABLA usuarios (
    id ENTERO NO NULO,
    nombre TEXTO,
    edad ENTERO
);
"""

# R - CONSULTAR
consultar = """
CONSULTAR nombre, edad DE usuarios DONDE edad > 18;
"""

# U - ACTUALIZAR
actualizar = """
ACTUALIZAR usuarios ESTABLECER edad = 30 DONDE id = 1;
"""

# D - ELIMINAR
eliminar = """
ELIMINAR DE usuarios DONDE id = 1;
"""

# EJECUCIÓN DE PRUEBAS 

if __name__ == "__main__":
    probar_sentencia(crear, "CREAR (C)")
    probar_sentencia(consultar, "CONSULTAR (R)")
    probar_sentencia(actualizar, "ACTUALIZAR (U)")
    probar_sentencia(eliminar, "ELIMINAR (D)")
