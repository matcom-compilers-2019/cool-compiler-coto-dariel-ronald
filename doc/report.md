| Nombre                  | Grupo | GitHub         |
| ----------------------- | ----- | -------------- |
| Ronald Diaz Rosales     | C-412 | @iampetroleo   |
| Ariel Coto Santiesteban | C-412 | @Ariel96cs     |
| Daryel Cutie Guazman    | C-412 | @Gitpepedaryel |



# GCC (Greatest COOL compiler)

GCC es un compilador hecho en Python 3 que tiene como objetivo lograr una traducción correcta de código escrito en el lenguaje COOL (Classroom Object Oriented Language) a código en lenguaje ensamblador MIPS ejecutable usando SPIM.

COOL es un lenguaje de programación que aunque es “pequeño”  incluye características de lenguajes de programación moderno, como son tipado estático, objetos y manejo automático de la memoria. Los programas en COOL son un conjunto de clases, con herencia, polimorfismo, funciones, atributos, declaraciones de variables, entre otras cosas.

## Arquitectura:

GCC sigue la arquitectura clásica de un compilador, consiste principalmente de dos componentes lógicas: Frontend y Backend.

El proceso de compilación comienza en el Frontend y culmina en el Backend, pasando por etapas en cada componente.

El Frontend consiste en tres etapas:

1. Análisis léxico.

2. Análisis sintáctico. 

3. Análisis semántico.

El Backend consiste en dos etapas:

1. Generación de código intermedio (CIL).
2. Generación de código objetivo (MIPS 32-bits). 

Estas etapas se encuentran dsitribuidas en 20 Módulos.

### Proceso de compilación:

#### Fronted:

El proceso de compilación comienza cuando se ejecuta el compilador(ver como se hace) pasándole un archivo que contiene un programa escrito en COOL. Primeramente se hace un análisis Lexicógrafico(ver: [`coolex.py`](/src/coolex.py)), donde se realiza la conversión de la secuencia inicial de caracteres proveniente del código fuente a una secuencia de tokens. En esta fase se detectan errores relacionados con la escritura incorrecta de símbolos. Luego, se pasa a hacer un análisis sintáctico del código de COOL (ver: [`coolyacc2.py`](/src/coolyacc2.py)), donde se determina la estructura sintáctica del programa a partir de los tokens y se obtiene el arbol de sintaxis abstracta del programa. En esta fase se detectan errores relacionados con la semantica del lenguaje.

La herramienta utilizada para los análisis léxicos y semánticos es PLY la cual es una implementación de las herramientas lex y yacc de C. Esta hace uso de LALR-parsing.  La gramática que se propone posee varios conflictos shift/reduce y reduce/reduce, los cuales se resuelven al definir la presedencia de símbolos en PLY y definir un orden de definición de las producciones.

 Para finalizar la fase de Frontend se realiza un análisis semántico(ver: [`semantic.py`](/src/semantic.py)) donde se verifican las condiciones semánticas del programa y se valida el uso correcto de todos los símbolos definidos. En esta fase se determinan los errores relacionados con los símbolos y tipos.

#### Backend:

Al culminar la etapa de Frontend se obtiene una estructura que representa el programa fuente escrito en COOL(ver: [`NodosAST.py`](/src/.py)). A partir de esta estructura se procede a formar una representación de un código intermedio entre el lenguaje fuente y el lenguaje objetivo. Esta representación intermedia se denomina CIL(ver: [`cool_to_cil.py`](/src/cool_to_cil.py)). La forma intermedia permite una traducción más simple al lenguaje objetivo. Finalmente se genera el código de el programa dado en el lenguaje objetivo(ver: [`cil_to_mips.py`](/src/cil_to_mips.py)). 



## Problemas y aspectos técnicos:

#### Generación de código intermedio:

Para la generación de código intermedio de COOL a MIPS si hizo uso de un lenguaje nos permitió generar código de COOL de forma más sencilla, ya que el salto directamente desde COOL a MIPS es demasiado complejo. Este lenguaje se denomina CIL, un código intermedio de 3 direcciones.

En CIL:

- No hay ningún tipo de chequeo ni ayuda por el runtime. 
- El signiﬁcado de una variable depende completamente del uso que se le dé.
- Es imprescindible tener cuidado con el orden de las deﬁniciones.  	
- Toda la consistencia está garantizada debido a que el chequeo semántico fue realizado con anterioridad.

Este lenguaje consta de 3 secciones principales, .Types para la declaración de tipos, .Data donde se almacenan los strings y un .Code para el código de las funciones

#### Instrucciones de CIL:

En CIL todo son enteros de 32 bits.

| Instruction                            | Description                                        |
| -------------------------------------- | -------------------------------------------------- |
| GETATTR y b                            | x = y.b                                            |
| SETATTR y b x                          | y.b = x                                            |
| GETINDEX a i                           | x = a[i]                                           |
| SETINDEX a i x                         | a[i] = x                                           |
| x = ALLOCATE T                         | Devolver una instancia de tipo T                   |
| x = ARRAY y                            | Crear un array de longitud y                       |
| t = TYPEOF x                           | Devuelve el tipo del objeto x                      |
| LABEL label                            | Crear el label                                     |
| GOTO label                             | Saltar al label                                    |
| IF x GOTO label                        | Si x>0 saltar a label                              |
| x = CALL f                             | Ejecutar la funcion f                              |
| x = VCALL T f                          | Ejecutar la funcion f que del tipo T               |
| PARAM a                                | Paso de parámetros                                 |
| RETURN x ;<br/>RETURN 0 ;<br/>RETURN ; | Retorno de funcion                                 |
| x = LOAD msg                           | Cargar direccion                                   |
| y= LENGTH x                            | Devolver la longitud de l array x                  |
| y = CONCAT z w                         | Concatenar                                         |
| LOCAL a                                | Variables locales                                  |
| y = SUBSTRING x n                      | Devolver subcadena que comienza en x de longitud n |
| z = STR y                              | Convertir a string                                 |
| x = READ ;<br/>PRINT x ;               | Leer y escribir de la entrada estandar             |
| t = GETPARENT T                        | Devolver el puntero de  la clase padre             |
| ARG x                                  | Cargar argumento x                                 |

#### Boxing y Unboxing:

Este constituye el método mediante el cual se transforman objetos por valor en objetos por referencia y viceversa, es de vital utilidad específicamente en el trabajo con tipos built in, en casos como en la ejecución de una instrucción de tipo case donde la expresión del case es por ejemplo, un entero.

#### Herencia, Polimorfismo y su manejo en MIPS:

Para garantizar un correcto funcionamiento de la herencia en el lenguaje, se asegura que cada tipo contenga los atributos y métodos que hereda de su padre; la obtención por parte del hijo de los miembros del padre sin errores, se logra mediante la realización de un orden topológico sobre los tipos existentes en cuanto a sus relaciones padre-hijo; de esta forma se evita que al intentar incluir en un tipo los atributos de otro, que este otro no tenga los atributos que debería.

Al generar en MIPS una instancia de un tipo, entre otras cosas se guarda en memoria un puntero hacia la tabla de métodos virtuales asociada altipo de la instancia. En dicha tabla se encuentran punteros hacia los métodos que se deben ejecutar en caso de que esta instancia los utilice. Estos punteros se encontrarán dirigidos hacia la dirección de memoria donde se encuentra la implementación del método hecha por el tipo en caso de que este lo implemente, o a la implementación hecha por el primer ancestro en caso contrario. Para resolver en Runtime un método se itera la tabla de métodos virtuales en busca del procedimiento con igual nombre de definición.

La representación de un tipo X en mips que se propone es:

| Espacio de reserva | Descripción                                       |
| ------------------ | ------------------------------------------------- |
| .word              | tamaño de definición                              |
| .word              | puntero al padre                                  |
| .word              | puntero al nombre de la clase                     |
| .word              | tamaño a reservar por cada instancia de este tipo |
| .word              | puntero al mismo tipo                             |
| .word              | puntero a la tabla de métodos virtuales           |
| .word              | cantidad de atributos                             |
| ...                | ... si tiene atributos la clase                   |
| .word              | puntero al nombre del atributo                    |
| .space 4           | espacio del valor del atributo                    |



### Link del Proyecto:

El proyecto esta [aquí ](https://github.com/matcom-compilers-2019/cool-compiler-coto-dariel-ronald)

### Bibliografia:

Introducción a la Construcción de Compiladores, Alejandro Piad Morffis.

Compilers,Principles, Techniques, & Tools Second Edition, Alfrd V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman.

Stanford's Compiler Theory Course.