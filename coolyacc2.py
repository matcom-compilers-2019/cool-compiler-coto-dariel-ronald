import ply.yacc as yacc
from coolex import lexer, tokens
from NodosAST import *

from cool_errors import SyntacticError, throw_exception
ERROR = None


def p_program(p):
    '''program : class SEMICOLON program
               | class SEMICOLON'''

    if len(p) == 4:
        p[3].classes.insert(0,p[1])
        p[0] = p[3]
    else:
        p[0] = ProgramNode([p[1]])


def p_class(p):
    'class : CLASS TYPE inheritence LBRACE features RBRACE'

    class_declaration = ClassNode(p[2],p[3],p[5])
    p[0] = class_declaration


def p_inheritence(p):
    '''inheritence : INHERITS TYPE
                    | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = 'Object'


def p_features(p):
    '''features : feature SEMICOLON features
                | empty'''

    if len(p) == 4:
        p[3].insert(0, p[1])
        p[0] = p[3]
    else:
        p[0] = []


def p_feature_method_declaration(p):
    '''feature : method_declaration
               '''
    p[0] = p[1]


def p_feature_attribute(p):
    '''feature : attribute'''
    p[0] = AttributeNode(p[1][0][0],p[1][0][1],p[1][1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

def p_attribute(p):
    '''attribute : id_type
                | id_type ASSIGN expression'''
    #  esto devuelve una tupla((id,type),value)
    new_attr = (p[1], None)
    if len(p) == 4:
        new_attr = (p[1], p[3])
    p[0] = new_attr


def p_id_type(p):
    'id_type : ID TDOTS TYPE'
    # esto lo que devuelve es(id,type)
    p[0] = (p[1],p[3])


def p_method_declaration(p):
    'method_declaration : ID LBRACKET formals RBRACKET TDOTS TYPE LBRACE expression RBRACE'

    new_method = MethodNode(p[1],p[3],p[6],p[8])
    p[0] = new_method
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_formals(p):
    '''formals : id_type COMMA formals
                | id_type'''

    if len(p) == 4:
        # aqui devolvemos una lista de id_type, que es una tupla (id,type)
        p[3].insert(0, p[1])
        p[0] = p[3]
    else:
        p[0] = [p[1]]


def p_formals_empty(p):
    '''formals : empty'''
    p[0] = []


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    if len(p) == 4:
        p[3].insert(0, p[1])
        p[0] = p[3]
    else:
        p[0] = [p[1]]


def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = NotNode(p[2])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)






def p_expression_plus_minus(p):
    '''expression : expression PLUS expression
            | expression MINUS expression
            '''

    if p[2] == '+':
        p[0] = PlusNode(p[1], p[3])
    elif p[2] == '-':
        p[0] = MinusNode(p[1], p[3])

    p[0].line = p.lineno(2)
    p[0].index = p.lexpos(2)


def p_expression_mult_div(p):
    '''expression : expression TIMES expression
            | expression DIVIDE expression
            '''
    if p[2] == '*':
        p[0] = StarNode(p[1], p[3])
    elif p[2] == '/':
        p[0] = DivNode(p[1], p[3])

    p[0].line = p.lineno(2)
    p[0].index = p.lexpos(2)


def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS
                '''
    p[0] = NegationNode(p[2])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_g(p):
    '''expression : LBRACKET expression RBRACKET
            | ISVOID expression
            | block
            | conditional
            | loop
            | case
            | dispatch
            | BCOMPLEMENT expression
            '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        if p[1] == 'isvoid':
            p[0] = IsVoidNode(p[2])
        else:
            p[0] = IntegerComplementNode(p[2])
        p[0].line = p.lineno(1)
        p[0].index = p.lexpos(1)
    else:
        p[0] = p[1]


def p_block(p):
    'block : LBRACE expression_list RBRACE'
    p[0] = BlockNode(p[2])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_variable(p):
    '''expression : ID'''
    p[0] = ObjectNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_type_int(p):
    '''expression : INTEGER '''
    p[0] = IntNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_type_str(p):
    '''expression : STRING'''
    p[0] = StrNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_type_bool(p):
    '''expression : TRUE
            | FALSE'''
    p[0] = BoolNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

# def p_atom_types_error(p):
#     'atom : error'
#     print("Error con el atom types")


def p_expression_newtype(p):
    '''expression : NEW TYPE'''
    p[0] = NewTypeNode(p[2])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_l(p):
    '''expression : MINUS let_expression %prec UMINUS
                | let_expression '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NegationNode(p[2])
        p[0].line = p.lineno(1)
        p[0].index = p.lexpos(1)


def p_dispatch(p):
    '''dispatch : expression especific DOT dispatch_call
                | dispatch_call'''
    if len(p) == 5:
        if p[2] is None:
            p[0] = DispatchNode(p[4][0],p[4][1],p[1])
        else:
            p[0] = StaticDispatchNode(p[4][0], p[4][1], p[1], p[2])
        p[0].line = p.lineno(3)
        p[0].index = p.lexpos(3)
    else:
        p[0] = DispatchNode(p[1][0],p[1][1], None)
        p[0].line = p.lineno(1)
        p[0].index = p.lexpos(1)


def p_especific(p):
    '''especific : DISP TYPE
                 | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_dispatch_call(p):
    'dispatch_call : ID LBRACKET params_expression RBRACKET'
    p[0] = (p[1],p[3])


def p_params_expression(p):
    '''params_expression : expression
                            | expression COMMA params_expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]


def p_params_expression_empty(p):
    '''params_expression : empty'''
    p[0] = []


def p_empty(p):
    'empty :'


def p_let_expression(p):
    'let_expression : LET declaration_list IN expression'
    p[0] = LetVarNode(p[2],p[4])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_declaration_list(p):
    '''declaration_list : attribute COMMA declaration_list
                        | attribute'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[3].insert(0,p[1])
        p[0] = p[3]


# def p_declaration(p):
#     '''declaration : id_type ASSIGN expression
#                     | id_type'''

def p_conditional(p):
    'conditional : IF expression THEN expression ELSE expression FI'
    p[0] = ConditionalNode(p[2], p[4], p[6])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_loop(p):
    'loop : WHILE expression LOOP expression POOL'
    p[0] = LoopNode(p[2],p[4])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_case(p):
    'case : CASE expression OF implications ESAC'
    p[0] = CaseNode(p[2],p[4])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_implications(p):
    '''implications : implication SEMICOLON implications
                    | implication SEMICOLON'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[3].insert(0,p[1])
        p[0] = p[3]


def p_implication(p):
    '''implication : id_type IMPLY expression'''
    # new_implication = Implication()
    # new_implication.id, new_implication.type = p[1]
    # new_implication.expression = p[3]
    # p[0] = new_implication
    p[0] = (p[1],p[3])


def p_expression_cmp(p):
    '''expression : expression LTHAN expression
                    | expression LETHAN expression
                    | expression EQUALS expression'''
    if p[2] == '<':
        p[0] = LowerThanNode(p[1], p[3])
    elif p[2] == '<=':
        p[0] = LowerEqualThanNode(p[1], p[3])
    elif p[2] == '=':
        p[0] = EqualThanNode(p[1], p[3])

    p[0].line = p.lineno(2)
    p[0].index = p.lexpos(2)

def p_expression_assign(p):
    'expression : ID ASSIGN expression'
    p[0] = AssignNode(ObjectNode(p[1]), p[3])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_error(p):
    if p is None:
        throw_exception(SyntacticError, -1, -1, 'Last file \';\' not founded')
    throw_exception(SyntacticError,p.lineno, p.lexpos,str(p))



precedence = (
    ('right','ASSIGN'),
    ('left','NOT'),
    ('nonassoc','LTHAN','LETHAN','EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'), #Unary minus operator
    ('right','ISVOID'),
    ('right','BCOMPLEMENT'),
    ('left','DISP'),
    ('left','DOT')
)

# from coolex import data, lexer

parser = yacc.yacc()
# parser.parse(data,lexer,True)
