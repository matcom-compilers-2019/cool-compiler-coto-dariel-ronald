import logging

logging.basicConfig()

def verify_asts(parser_result, expected, root_class):
    '''
    Recibe dos ast y realiza un dfs por ellos comparando campo por campo nodo por nodo, lanza una AssertionError
    en caso de que no sean iguales los ast.
    :param parser_result: ast1
    :param expected: ast2
    :param root_class: La clase raíz de la jerarquía del ast. Ejemplo: Node.
    :return:
    '''
    assert ast_checker(parser_result, expected, root_class)


def ast_checker(node1, node2, root_class):
    if type(node1) != type(node2):
        logging.error(f'Type {type(node1)} from {node1} is not equals to {type(node2)} from {node2}')
        return False
    is_a_Node = issubclass(type(node1), root_class)
    is_an_iterable = type(node1) == tuple or type(node1) == list
    if is_a_Node:
        properties1 = node1.__dict__
        properties2 = node2.__dict__

        for field, value1 in properties1.items():
            if field == 'index' or field == 'line':
                continue

            value2 = properties2[field]
            if not ast_checker(value1, value2,root_class):
                logging.error(f'Found error while checking field {field}')
                return False
        return True
    elif is_an_iterable:

        for i, value1 in enumerate(node1):

            value2 = node2[i]
            if not ast_checker(value1, value2,root_class):
                return False
        return True
    result = node1 == node2
    if not result:
        logging.error(f'{node1} is not equals to {node2}')
    return result

#
# class MyEncoder(json.JSONEncoder):
#     def default(self,obj):
#         if isinstance(obj,Node):
#             new_dict = obj.__dict__.copy()
#             for field in new_dict:
#                 field_value = new_dict[field]
#                 if isinstance(field_value,Node):
#                     field_value = self.default(field_value)
#                 elif isinstance(field_value,list) or isinstance(field_value,tuple):
#                     new_field = [self.default(item)for item in field_value]
#                     field_value = new_field if isinstance(field_value,list) else tuple(new_field)
#                 else:
#                     field_value = json.dumps(field_value)
#                 new_dict[field] = field_value
#             return json.dumps(new_dict)
#         elif isinstance(obj,list) or isinstance(obj,tuple):
#             new_field = [self.default(item)for item in obj]
#             new_obj = new_field if isinstance(obj,list) else tuple(new_field)
#             return json.dumps(new_obj)
#         return json.dumps(obj)
#
