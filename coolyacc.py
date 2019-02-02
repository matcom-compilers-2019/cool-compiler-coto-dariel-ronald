import ply.yacc as yacc
from coolex import *
from NodosAST import *


def p_program(p):
    '''program : class SEMICOLON program
               | class SEMICOLON'''

    if len(p) == 4:
        p[3].insert(0,p[1])
        p[0] = p[3]
    else:
        p[0] = [p[1]]


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


def p_expression(p):
    '''expression : assign
                    | upper_non'''
    p[0] = p[1]


def p_upper_non(p):
    '''upper_non : NOT upper_non
                | operator_non'''
    if len(p) == 3:
        p[0] = NotNode(p[2])
    else:
        p[0] = p[1]


def p_operator_non(p):
    '''operator_non : k_arith LTHAN k_arith
                    | k_arith LETHAN k_arith
                    | k_arith EQUALS k_arith
                    | k_arith'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '<':
            p[0] = LowerThanNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LowerEqualThanNode(p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualThanNode(p[1], p[3])


def p_k_arith(p):
    '''k_arith : arith
                | e_arith'''
    p[0] = p[1]


def p_assign(p):
    'assign : ID ASSIGN expression'
    p[0] = AssignNode(VariableNode(p[1]), p[3])


def p_arith(p):
    '''arith : arith PLUS term
            | arith MINUS term
            | term'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])


def p_factor(p):
    '''factor : MINUS factor %prec UMINUS
                | atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NegationNode(p[2])


def p_atom(p):
    '''atom : LBRACKET expression RBRACKET
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
            p[0] = BComplementNode(p[2])
    else:
        p[0] = p[1]


def p_block(p):
    'block : LBRACE expression_list RBRACE'
    p[0] = BlockNode(p[2])


def p_atom_variable(p):
    '''atom : ID'''
    p[0] = VariableNode(p[1])


def p_atom_type_int(p):
    '''atom : INTEGER '''
    p[0] = IntNode(p[1])

def p_atom_type_str(p):
    '''atom : STRING'''
    p[0] = StrNode(p[1])

def p_atom_type_bool(p):
    '''atom : TRUE
            | FALSE'''
    p[0] = BoolNode(p[1])

# def p_atom_types_error(p):
#     'atom : error'
#     print("Error con el atom types")

def p_atom_newtype(p):
    '''atom : NEW TYPE'''
    p[0] = NewTypeNode(p[2])


def p_e_arith(p):
    '''e_arith : arith PLUS e_term
                | arith MINUS e_term
                | e_term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])


def p_e_term(p):
    '''e_term : e_term TIMES e_factor
                | e_term DIVIDE e_factor
                | e_factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])


def p_e_factor(p):
    '''e_factor : MINUS e_factor %prec UMINUS
                | let_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NegationNode(p[2])


def p_let_expression(p):
    'let_expression : LET declaration_list IN expression'
    p[0] = LetVarNode(p[2],p[4])


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


def p_loop(p):
    'loop : WHILE expression LOOP expression POOL'
    p[0] = LoopNode(p[2],p[4])


def p_case(p):
    'case : CASE expression OF implications ESAC'
    p[0] = CaseNode(p[2],p[4])


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


def p_dispatch(p):
    '''dispatch : expression especific DOT dispatch_call
                | dispatch_call'''
    if len(p) == 5:
        p[0] = DispatchNode(p[4][0],p[4][1],p[1],p[2])
    else:
        p[0] = StaticDispatchNode(p[4][0],p[4][1])


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
        p[3].insert(0,p[1])
        p[0] = p[3]


def p_params_expression_empty(p):
    '''params_expression : empty'''
    p[0] = []


def p_empty(p):
    'empty :'


def p_error(p):
    print("Syntax error in input")

# precedence = (
#     ('right','ASSIGN'),
#     ('left','NOT'),
#     ('right','BCOMPLEMENT'),
#     ('right','ISVOID'),
#     ('nonassoc','LTHAN','LETHAN','EQUALS'),
#     ('left','PLUS','MINUS'),
#     ('left','TIMES','DIVIDE'),
#     ('left','DISP'),
#     ('left','DOT')
# )

precedence = (
    ('right','ASSIGN'),
    ('left','NOT'),
    ('nonassoc','LTHAN','LETHAN','EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),#Unary minus operator
    ('right','ISVOID'),
    ('right','BCOMPLEMENT'),
    ('left','DISP'),
    ('left','DOT')
)


parser = yacc.yacc()
parser.parse(data,lexer,True)
