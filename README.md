# Segundo Parcial

## Primer Punto 

En el primer punto se diseñó e implementó un lenguaje de base de datos propio, inspirado en la estructura de comandos de SQL, pero utilizando palabras clave en español.
El objetivo fue construir la gramática base que permita ejecutar operaciones fundamentales sobre una base de datos: creación, inserción, actualización, eliminación y consulta de información.

Para esto, se definió una gramática formal que describe la sintaxis de los comandos admitidos por el lenguaje.
Entre las sentencias principales se incluyeron:

  - CREAR BASE / TABLA: para definir bases de datos y tablas nuevas.

  - INSERTAR EN / VALORES: para registrar información en las tablas.

  - CONSULTAR DE / DONDE: para realizar consultas con condiciones.

  - ACTUALIZAR / ESTABLECER: para modificar registros existentes.

  - ELIMINAR DE / TABLA: para borrar registros o estructuras.

Posteriormente, se construyó la gramática en ANTLR para representar formalmente la sintaxis del lenguaje y facilitar la generación automática de los analizadores léxico y sintáctico.
El desarrollo implicó definir los tokens del lenguaje (palabras reservadas, identificadores, literales, símbolos, etc.) y las reglas sintácticas que determinan cómo deben combinarse.

Gracias a esta definición, el lenguaje puede ser interpretado o validado sintácticamente mediante un parser, asegurando que las instrucciones cumplan con las reglas de estructura establecidas.

### Conclusión

El desarrollo del primer punto permitió establecer las bases de un lenguaje de manipulación de bases de datos propio, demostrando cómo a partir de una gramática formal es posible definir la estructura de un lenguaje similar a SQL.
La implementación en ANTLR facilitó la generación automática de los componentes del analizador, garantizando consistencia entre la definición léxica y sintáctica.
Este punto sirvió como fundamento para los siguientes ejercicios, en los que se aplican diferentes técnicas de análisis sintáctico (LL(1), CYK y descendente recursivo) sobre estructuras definidas por esta misma gramática.

## Segundo Punto

En el segundo punto se implementó un conjunto de pruebas automáticas para verificar el correcto funcionamiento del lenguaje diseñado en el punto anterior.
El objetivo fue comprobar que la gramática, el analizador léxico y el analizador sintáctico pudieran procesar correctamente las distintas operaciones básicas de una base de datos: crear, leer, actualizar y eliminar (CRUD).

Para ello, se construyeron dos módulos principales en Python:

MiniBDLexer.py: encargado del análisis léxico, cuya función es leer la entrada de texto y convertirla en una lista de tokens válidos según las reglas del lenguaje.
Este componente identifica palabras clave como CREAR, CONSULTAR, INSERTAR, ELIMINAR, así como identificadores, literales numéricos, cadenas y símbolos.

MiniBDParser.py: encargado del análisis sintáctico. Este módulo valida la secuencia de tokens generada por el lexer, verificando que las estructuras sigan las reglas de la gramática.
Cada tipo de instrucción (por ejemplo, CREAR TABLA, INSERTAR EN, CONSULTAR DE, ACTUALIZAR o ELIMINAR) cuenta con su propio método de análisis.

Posteriormente, se elaboraron pruebas automáticas en un script principal, donde se ejecutaron casos representativos para cada una de las operaciones del lenguaje:

- C (Create): creación de bases de datos o tablas.

- R (Read): consultas de datos mediante sentencias CONSULTAR.

- U (Update): actualización de registros existentes.

- D (Delete): eliminación de registros o estructuras.

Cada prueba fue procesada por el lexer y parser simulados, verificando si la entrada era sintácticamente válida o si debía reportar un error.
De esta manera, se comprobó la correcta integración entre los componentes del lenguaje y la robustez del sistema de análisis.

### Conclusión

El segundo punto permitió comprobar de forma práctica que el lenguaje MiniBD, diseñado en el primer punto, puede ser analizado correctamente mediante los módulos léxico y sintáctico.
Las pruebas CRUD demostraron que el sistema reconoce adecuadamente las distintas estructuras del lenguaje, generando respuestas coherentes ante entradas válidas o incorrectas.
Además, el uso de pruebas automáticas permitió validar la funcionalidad completa del analizador y garantizar su consistencia para futuras extensiones o mejoras del lenguaje.

## Tercer Punto 

El objetivo de este punto es diseñar e implementar un analizador sintáctico predictivo LL(1) para una
gramática de expresiones aritméticas. Además, se comparan los tiempos de ejecución con otros
métodos de análisis, como los analizadores ascendentes o el algoritmo CYK

### Gramática original y forma LL(1)

Gramática original:

```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

Gramática transformada a forma LL(1):

```
E → T E’
E’ → + T E’ | ε
T → F T’
T’ → * F T’ | ε
F → ( E ) | id
```

### Conjuntos Primeros y Siguientes

|  No Terminal | Primeros | Siguientes |
| --- | :---: | ---: |
| E | ( , id | ) , $ |
| E' | + , ε | ) , $ |
| T | ( , id | + , ) , $ |
| T' | * , ε | + , ) , $ |
| F | ( , id | * , + , ) , $ |


### Descripción del algoritmo LL(1)
El analizador predictivo LL(1) utiliza una tabla de predicción basada en los conjuntos FIRST y
FOLLOW para decidir qué producción aplicar según el símbolo en la cima de la pila y el token actual
de entrada. El proceso continúa hasta consumir toda la cadena o detectar un error sintáctico

###  Resultados de las pruebas

Se ejecutaron pruebas con expresiones de distinta longitud (1, 4, 8 y 12 operandos). Los tiempos
promedio de ejecución fueron casi constantes, confirmando la complejidad lineal O(n).

| Operandos | Tiempo promedio (s) |
|------------|---------------------|
| 1          | 0.00001             |
| 4          | 0.00002             |
| 8          | 0.00003             |
| 12         | 0.00004             |


### Conclusiones
El analizador LL(1) demostró ser eficiente y determinístico. Su complejidad O(n) lo hace ideal para
gramáticas sin ambigüedad. En comparación con algoritmos como CYK o el backtracking, el LL(1)
ofrece un análisis más rápido y directo, confirmando su utilidad para compiladores y lenguajes con
estructura predecible.

## Cuarto Punto 

En el cuarto punto se desarrolló la implementación del algoritmo CYK (Cocke–Younger–Kasami), el cual es un método de análisis sintáctico ascendente que utiliza programación dinámica.
Este algoritmo se aplica exclusivamente a gramáticas libres de contexto expresadas en Forma Normal de Chomsky (FNC), es decir, donde las producciones tienen la forma A → BC o A → a.

El objetivo del ejercicio fue construir un parser basado en CYK, probarlo con distintas longitudes de entrada y comparar su rendimiento con el analizador LL(1) desarrollado en el punto 3.

Para realizarlo, se utilizó una gramática simple de paréntesis balanceados, definida en FNC de la siguiente manera:

```
1. S → A B | C D
2. A → (
3. B → S )
4. C → (
5. D → )
```

Esta gramática reconoce cadenas bien formadas como (), (()), ()(), y otras combinaciones anidadas.

Se realizaron 10 pruebas por tamaño de expresión (1, 4, 8, 12 operandos). Los parsers comparados
fueron: Predictivo LL(1), CYK y Shift-Reduce.

| Operandos | LL(1) promedio (s) | CYK promedio (s) | Shift-Reduce promedio (s) |
|------------|--------------------|------------------|----------------------------|
| 1          | 0.00001            | 0.00002          | 0.00001                    |
| 4          | 0.00002            | 0.00006          | 0.00002                    |
| 8          | 0.00003            | 0.00010          | 0.00003                    |
| 12         | 0.00004            | 0.00015          | 0.00004                    |


El algoritmo fue implementado en Python mediante una tabla triangular donde cada celda representa los no terminales que pueden generar una subcadena específica de la entrada.
El programa fue probado con cadenas de longitudes equivalentes a 1, 4, 8 y 12 tokens, registrando los tiempos de ejecución para cada caso.

Finalmente, se compararon los resultados con los del analizador LL(1), mostrando que el algoritmo CYK presenta una complejidad temporal cúbica (O(n³)), mientras que LL(1) mantiene un comportamiento lineal.

### Conclusión

El algoritmo CYK demostró ser un método completo y general para el reconocimiento de gramáticas libres de contexto, aunque su costo computacional es significativamente mayor que el de los métodos predictivos como LL(1).
Los resultados experimentales mostraron que, a medida que aumenta la longitud de la cadena, el tiempo de ejecución del CYK crece de forma exponencial.
A pesar de esto, su principal ventaja radica en su capacidad para analizar gramáticas complejas o ambiguas, donde los métodos descendentes no son aplicables.
El punto permitió comprender las diferencias entre los analizadores ascendentes y descendentes, y la importancia de elegir el método adecuado según el tipo de gramática.

## Quinto Punto

En el quinto punto se diseñó e implementó el algoritmo de emparejamiento (match), componente fundamental dentro de un analizador descendente recursivo.
Este algoritmo es responsable de comparar el token actual con el símbolo esperado por la gramática, y de avanzar en la secuencia de entrada cuando la coincidencia es correcta.
Si el token no coincide con lo esperado, el algoritmo genera un error sintáctico, señalando el punto exacto de la discrepancia.

Para desarrollar la práctica, se utilizó nuevamente la gramática de expresiones aritméticas empleada en los puntos anteriores:

```
E  → T E’
E’ → + T E’ | ε
T  → F T’
T’ → * F T’ | ε
F  → ( E ) | id
```

Cada no terminal de la gramática se implementó como una función recursiva en Python, y los terminales fueron gestionados mediante la función emparejar(token_esperado).
Esta función verifica el token actual y, si coincide, avanza al siguiente; de lo contrario, produce un error de sintaxis.
El analizador fue probado con distintas expresiones válidas e inválidas, comprobando que las cadenas que cumplen la estructura gramatical son aceptadas, y las que contienen errores son correctamente rechazadas.

### Conclusión

- El algoritmo de emparejamiento permitió consolidar el funcionamiento del analizador descendente recursivo, demostrando cómo las reglas gramaticales pueden implementarse directamente mediante funciones y llamadas recursivas.
  
- Su diseño resulta sencillo, legible y eficiente para gramáticas LL(1) bien estructuradas, en las que no existe ambigüedad ni recursión a la izquierda.
