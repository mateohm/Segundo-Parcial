grammar MiniBD;

// REGLAS PRINCIPALES 

programa
    : sentencia* EOF
    ;

// Cada instrucción termina en punto y coma
sentencia
    : crearBase ';'
    | modificarBase ';'
    | crearTabla ';'
    | modificarTabla ';'
    | eliminarTabla ';'
    | crearIndice ';'
    | eliminarIndice ';'
    | insertar ';'
    | consultar ';'
    | actualizar ';'
    | eliminar ';'
    ;

// SENTENCIAS CRUD Y DDL 

// CREAR BASE nombre;
crearBase
    : 'CREAR' 'BASE' IDENTIFICADOR
    ;

// MODIFICAR BASE nombre AJUSTAR opcion;
modificarBase
    : 'MODIFICAR' 'BASE' IDENTIFICADOR 'AJUSTAR' IDENTIFICADOR
    ;

// CREAR TABLA nombre (columna tipo, ...);
crearTabla
    : 'CREAR' 'TABLA' IDENTIFICADOR '(' definicionColumna (',' definicionColumna)* ')'
    ;

// MODIFICAR TABLA nombre AGREGAR COLUMNA definicionColumna;
modificarTabla
    : 'MODIFICAR' 'TABLA' IDENTIFICADOR 'AGREGAR' 'COLUMNA' definicionColumna
    ;

// ELIMINAR TABLA nombre;
eliminarTabla
    : 'ELIMINAR' 'TABLA' IDENTIFICADOR
    ;

// CREAR INDICE nombre EN tabla (columna, ...);
crearIndice
    : 'CREAR' 'INDICE' IDENTIFICADOR 'EN' IDENTIFICADOR '(' IDENTIFICADOR (',' IDENTIFICADOR)* ')'
    ;

// ELIMINAR INDICE nombre EN tabla;
eliminarIndice
    : 'ELIMINAR' 'INDICE' IDENTIFICADOR 'EN' IDENTIFICADOR
    ;

// SENTENCIAS CRUD 

// INSERTAR EN tabla (col1, col2) VALORES (val1, val2);
insertar
    : 'INSERTAR' 'EN' IDENTIFICADOR '(' IDENTIFICADOR (',' IDENTIFICADOR)* ')'
      'VALORES' '(' literal (',' literal)* ')'
    ;

// CONSULTAR columnas DE tabla [DONDE expresion];
consultar
    : 'CONSULTAR' listaSeleccion 'DE' IDENTIFICADOR ('DONDE' expresion)?
    ;

// ACTUALIZAR tabla ESTABLECER col=expr [, ...] [DONDE expr];
actualizar
    : 'ACTUALIZAR' IDENTIFICADOR 'ESTABLECER' asignacion (',' asignacion)* ('DONDE' expresion)?
    ;

// ELIMINAR DE tabla [DONDE expr];
eliminar
    : 'ELIMINAR' 'DE' IDENTIFICADOR ('DONDE' expresion)?
    ;

// COMPONENTES DE SENTENCIAS 

// Lista de columnas en CONSULTAR
listaSeleccion
    : '*'
    | IDENTIFICADOR (',' IDENTIFICADOR)*
    ;

// Definición de columna
definicionColumna
    : IDENTIFICADOR tipoDato ('NO' 'NULO')?
    ;

// Tipos de datos posibles
tipoDato
    : 'ENTERO'
    | 'DECIMAL'
    | 'TEXTO'
    | 'BOOLEANO'
    ;

// Asignaciones usadas en ACTUALIZAR
asignacion
    : IDENTIFICADOR '=' expresion
    ;

// EXPRESIONES 

expresion
    : expresion ('+' | '-') termino
    | termino
    ;

termino
    : termino ('*' | '/') factor
    | factor
    ;

factor
    : '(' expresion ')'
    | IDENTIFICADOR
    | literal
    ;

// Literales
literal
    : ENTERO_LITERAL
    | DECIMAL_LITERAL
    | CADENA_LITERAL
    | 'VERDADERO'
    | 'FALSO'
    ;

// TOKENS 

IDENTIFICADOR
    : [a-zA-ZÁÉÍÓÚáéíóú_] [a-zA-ZÁÉÍÓÚáéíóú0-9_]*
    ;

ENTERO_LITERAL
    : [0-9]+
    ;

DECIMAL_LITERAL
    : [0-9]+ '.' [0-9]+
    ;

CADENA_LITERAL
    : '\'' (~['\\])* '\''
    ;

// Ignorar espacios
ESPACIO
    : [ \t\r\n]+ -> skip
    ;
