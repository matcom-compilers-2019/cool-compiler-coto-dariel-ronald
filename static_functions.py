from cil_hierarchy import *


def get_distance(cool_to_cil):
        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("__get_distance", ["t1", "t2"]))

        cool_to_cil.current_function_name = "__get_distance"
        #aqui se definen el contador y la variable que contiene al padre actual en el que se encuentra revisando
        cool_to_cil.define_internal_local()
        current_parent = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.define_internal_local()
        count = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]

        #Se inicializan las variables previamente creadas
        cool_to_cil.register_instruction(CILAssignNode, current_parent, "t1")
        cool_to_cil.register_instruction(CILAssignNode, count, 0)

        #Labels
        l_base = cool_to_cil.next_label()
        l_end = cool_to_cil.next_label()

        #Se analiza el caso base (si el current_parent es de tipo Object)
        cool_to_cil.register_instruction(CILLabelNode, l_base)
        cool_to_cil.define_internal_local()
        base_case = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, base_case, CILEqualThanNode(current_parent, "Object"))
        cool_to_cil.register_instruction(CILGotoIfNode, base_case, l_end)

        #Se analiza si encontramos al tipo t2
        cool_to_cil.define_internal_local()
        local_dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, local_dest, CILEqualThanNode(current_parent, "t2"))
        cool_to_cil.register_instruction(CILGotoIfNode, local_dest, l_end)

        #Se actualizan los valores de current_parent y del count dentro del ciclo
        cool_to_cil.register_instruction(CILAssignNode, current_parent, CILGetParentNode(current_parent))
        cool_to_cil.register_instruction(CILAssignNode, count, CILPlusNode(count, 1))

        cool_to_cil.register_instruction(CILGotoNode, l_base)
        cool_to_cil.register_instruction(CILLabelNode, l_end)

        cool_to_cil.register_instruction(CILReturnNode, count)

        #Aqui se se anade la funcion creada a la lista de funciones estaticas y se elimina de la lista del dotcode
        cool_to_cil.static_functions.append(cool_to_cil.dotcode[-1].functions[-1])
        cool_to_cil.dotcode[-1].functions.remove(cool_to_cil.dotcode[-1].functions[-1])


def get_closest_type(cool_to_cil):
    cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("__get_closest_type",
                                                             ["my_type","my_types_array"]))
    cool_to_cil.current_function_name = "___get_closest_type"

    #Aqui se definen las variables principales que seran usadas(el indice del array, 
    # la distancia actual calculada entre my_type y my_types_array[index], el min_value que es la menor distancia
    # calculada en cada momento, el current_value que representa el elemento de la posicion index del array
    #y el min_index que representa el indice del valor de menor distancia hasta el momento)
    cool_to_cil.define_internal_local()
    index = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.define_internal_local()
    min_index = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.define_internal_local()
    current_value = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.define_internal_local()
    min_value = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.define_internal_local()
    dist = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]

    #Labels
    l_base = cool_to_cil.next_label()
    l_min = cool_to_cil.next_label()
    l_end = cool_to_cil.next_label()

    #Inicializacion del current_value, index y min_index
    cool_to_cil.register_instruction(CILAssignNode, index, 0)
    cool_to_cil.register_instruction(CILAssignNode, min_index, 0)
    cool_to_cil.register_instruction(CILAssignNode, current_value, CILGetIndexNode("my_types_array", index))

    #Se inicializa el min_value con la 1ra distancia
    my_call = CILBuiltInCallNode("__get_distance")
    my_call.params.append("my_type")
    my_call.params.append(current_value)
    cool_to_cil.register_instruction(CILAssignNode, min_value, my_call)

    cool_to_cil.register_instruction(CILLabelNode, l_base)

    #Aqui se analiza si el indice no se ha pasado de length(my_types_array
    #En caso de haberse pasado se realiza un salto a la etiqueta l_end
    cool_to_cil.define_internal_local()
    aux1 = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.define_internal_local()
    aux2 = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.register_instruction(CILAssignNode, aux1, CILLengthNode("my_types_array"))
    cool_to_cil.register_instruction(CILAssignNode, aux2, CILLowerEqualThanNode(aux1, index))
    cool_to_cil.register_instruction(CILGotoIfNode, aux2, l_end)

    #Aqui se analiza si la distancia entre my_type y el tipo que se encuentra en el array[index] es menor
    #que la menor distancia encontrada hasta el momento
    #En caso de ser menor se salta al label l_min que se encarga de actualizar el minimo
    my_call = CILBuiltInCallNode("__get_distance")
    my_call.params.append("my_type")
    my_call.params.append(current_value)

    cool_to_cil.register_instruction(CILAssignNode, dist, my_call)
    cool_to_cil.define_internal_local()
    aux3 = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
    cool_to_cil.register_instruction(CILAssignNode, aux3, CILLowerThanNode(dist, min_value))
    cool_to_cil.register_instruction(CILGotoIfNode, aux3, l_min)

    #Se actualizan los valores del index y del current_value para la siguiente iteracion del ciclo
    cool_to_cil.register_instruction(CILAssignNode, index, CILPlusNode(index, 1))
    cool_to_cil.register_instruction(CILAssignNode, current_value, CILGetIndexNode("my_types_array", index))

    cool_to_cil.register_instruction(CILGotoNode, l_base)
    
    #Esta es la parte donde se actualiza el valor minimo de ser requerido
    cool_to_cil.register_instruction(CILLabelNode, l_min)
    cool_to_cil.register_instruction(CILAssignNode, min_value, dist)
    cool_to_cil.register_instruction(CILAssignNode, min_index, index)

    cool_to_cil.register_instruction(CILGotoNode, l_base)

    cool_to_cil.register_instruction(CILLabelNode, l_end)
    cool_to_cil.register_instruction(CILReturnNode, min_index)

    #Aqui se se anade la funcion creada a la lista de funciones estaticas y se elimina de la lista del dotcode
    cool_to_cil.static_functions.append(cool_to_cil.dotcode[-1].functions[-1])
    cool_to_cil.dotcode[-1].functions.remove(cool_to_cil.dotcode[-1].functions[-1])
