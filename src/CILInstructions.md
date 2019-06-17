# Instrucciones de CIL

En CIL todo son enteros de 32 bits.

| Instruction                            | Description                            |
| -------------------------------------- | -------------------------------------- |
| GETATTR y b                            | x = y.b                                |
| SETATTR y b x                          | y.b = x                                |
| GETINDEX a i                           | x = a[i]                               |
| SETINDEX a i x                         | a[i] = x                               |
| x = ALLOCATE T                         | Devolver una instancia de tipo T       |
| x = ARRAY y                            | crear un array de longitud y           |
| t = TYPEOF x                           | devuelve el tipo del objeto x          |
| LABEL label                            | crear el label                         |
| GOTO label                             | saltar al label                        |
| IF x GOTO label                        | si x>0 saltar a label                  |
| x = CALL f                             | ejecutar la funcion f                  |
| x = VCALL T f                          | ejecutar la funcion f que del tipo T   |
| PARAM a                                | paso de parámetros                     |
| RETURN x ;<br/>RETURN 0 ;<br/>RETURN ; | Retorno de funcion                     |
| x = LOAD msg                           | cargar direccion                       |
| y= LENGTH x                            | devolver la longitud de l array x      |
| y = CONCAT z w                         | concatenar                             |
| y = PREFIX x n                         |                                        |
| y = SUBSTRING x n                      |                                        |
| z = STR y                              | convertir a string                     |
| x = READ ;<br/>PRINT x ;               | leer y escribir de la entrada estandar |
| t = GETPARENT T                        | devolver el puntero de  la clase padre |
| ARG x                                  | cargar argumento x                     |
| LOCAL a                                | variables locales                      |

