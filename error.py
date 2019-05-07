from comp_version_info import VERSION, COPYRIGHT, NAME
import sys


def throw_exception(error_type,*args):
    print(CoolError([error_type(*args)]))
    sys.exit(-1)


class CoolError():
    def __init__(self, body_errors: list):
        self.body_errors = [str(i) for i in body_errors]

    def __str__(self):

        header = '''{} Version: {}\n{}\n'''.format(NAME,VERSION,COPYRIGHT)
        body = ''.join(self.body_errors)
        return header+body


class Error():
    error_type = 'Error'

    def __init__(self, line, index, error_message):
        self.error_message = error_message
        self.line = line
        self.index = index

    def __str__(self):
        return '(line: {}, index: {}) - {}: {}\n'.format(self.line,
                                                         self.index,
                                                         self.error_type,
                                                         self.error_message)


class CompilerError(Error):
    '''
    Se reporta al detectar alguna anomalía con la entrada del compilador.
    Por ejemplo, si el fichero a compilar no existe
    '''
    error_type = "CompilerError"


class LexicographicError(Error):
    '''
    Errores detectados por el Lexer
    '''
    error_type = "LexicographicError"


class SyntacticError(Error):
    '''
    Errores detectados por el parser
    '''
    error_type = "SyntacticError"


class NameError(Error):
    '''
    Se reporta al referenciar in identificador en un ámbito que no es visible
    '''
    error_type = "NameError"


class TypeError(Error):
    '''
    Se reporta al  detectar un problema de tipos. Incluye:
    - incompatibilidad de tipos entre rvalue y lvalue
    - operación no definida entre objetos de ciertos tipos, y
    - tipo referenciado no definido
    '''
    error_type = "TypeError"


class AttributeError(Error):
    '''
    Se reporta cuando un atributo o método se referencia pero no está definido
    '''

    error_type = "AttributeError"

class SemanticError(Error):
    '''
        Cualquier otro error semántico
    '''
    error_type = "SemanticError"


