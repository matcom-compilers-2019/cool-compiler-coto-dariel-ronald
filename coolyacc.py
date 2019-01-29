import ply.yacc as yacc
from coolex import *
from NodosAST import *


def p_program(p):
    '''program : class SEMICOLON program
               | class SEMICOLON'''

    if len(p) == 4:
        p[3].classes.append(p[1])
        p[0] = p[3]
    else:
        new_program = Program()
        new_program.classes.append(p[1])
        p[0] = new_program

def p_class(p):
    'class : CLASS TYPE inheritence LBRACE features RBRACE'

    class_declaration = Class()
    class_declaration.type = p[2]
    class_declaration.inherit = p[3]
    class_declaration.features = p[5]
    p[0] = class_declaration

def p_inheritence(p):
    '''inheritence : INHERITS TYPE
                    | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None



def p_features(p):
    '''features : feature SEMICOLON features
                | empty'''

    if len(p) == 4:
        p[3].append(p[1])
        p[0] = p[3]
    else:
        p[0] = []


def p_feature(p):
    '''feature : method_declaration
               | attribute'''
    p[0] = p[1]


def p_attribute(p):
    '''attribute : id_type
                | id_type ASSIGN expression'''
    new_attr = Attribute()

    if len(p) == 4:
        new_attr.value = p[3]
    new_attr.id, new_attr.type = p[1]
    p[0] = new_attr


def p_id_type(p):
    'id_type : ID TDOTS TYPE'
    p[0] = (p[1],p[3])


def p_method_declaration(p):
    'method_declaration : ID LBRACKET formals RBRACKET TDOTS TYPE LBRACE expression RBRACE'

    new_method = Method()
    new_method.id = p[1]
    new_method.parameters = p[3]
    new_method.return_type = p[6]
    new_method.expressions = p[7]
    p[0] = new_method


def p_block(p):
    'block : LBRACE expression_list RBRACE'
    p[0] = p[2]



def p_formals(p):
    '''formals : id_type COMMA formals
                | id_type'''
    new_formal = Formal()
    new_formal.id,new_formal.type = p[1]

    if len(p) == 4:
        p[3].append(new_formal)
        p[0] = p[3]
    else:
        p[0] = [new_formal]


def p_formals_empty(p):
    '''formals : empty'''
    p[0] = []


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    if len(p) == 4:
        p[3].append(p[1])
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
        p[0] = UnaryExpression()
        p[0].operator = p[1]
        p[0].expression = p[2]
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
        p[0] = BinaryExpression()
        p[0].operator = p[2]
        p[0].left_expression = p[1]
        p[0].right_expression = p[3]


def p_k_arith(p):
    '''k_arith : arith
                | e_arith'''
    p[0] = p[1]


def p_assign(p):
    'assign : ID ASSIGN expression'
    new_assing = Assign()
    new_assing.id, new_assing.expression = p[1],p[3]
    p[0] = new_assing

def p_arith(p):
    '''arith : arith PLUS term
            | arith MINUS term
            | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_bexpression = BinaryExpression()
        new_bexpression.operator = p[2]
        new_bexpression.left_expression,new_bexpression.right_expression = p[1],p[3]
        p[0] = new_bexpression


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_bexpression = BinaryExpression()
        new_bexpression.operator = p[2]
        new_bexpression.left_expression,new_bexpression.right_expression = p[1],p[3]
        p[0] = new_bexpression


def p_factor(p):
    '''factor : MINUS factor %prec UMINUS
                | atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_uexpression = UnaryExpression()
        new_uexpression.operator,new_uexpression.expression = p[1],p[2]
        p[0] = new_uexpression


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
        new_uexpression = UnaryExpression()
        new_uexpression.operator = p[1]
        new_uexpression.expression = p[2]
        p[0] = new_uexpression
    else:
        p[0] = p[1]


def p_atom_variable(p):
    '''atom : ID'''
    p[0] = Variable()
    p[0].id = p[1]


def p_atom_types(p):
    '''atom : INTEGER
            | STRING
            | TRUE
            | FALSE'''
    new_atom = Atom()
    new_atom.value = p[1]
    p[0] = new_atom

# def p_atom_types_error(p):
#     'atom : error'
#     print("Error con el atom types")

def p_atom_newtype(p):
    '''atom : NEW TYPE'''
    p[0] = NewType()
    p[0].type = p[2]


def p_e_arith(p):
    '''e_arith : arith PLUS e_term
                | arith MINUS e_term
                | e_term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_bexpression = BinaryExpression()
        new_bexpression.operator = p[2]
        new_bexpression.left_expression,new_bexpression.right_expression = p[1],p[3]
        p[0] = new_bexpression


def p_e_term(p):
    '''e_term : e_term TIMES e_factor
                | e_term DIVIDE e_factor
                | e_factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_bexpression = BinaryExpression()
        new_bexpression.operator = p[2]
        new_bexpression.left_expression,new_bexpression.right_expression = p[1],p[3]
        p[0] = new_bexpression

def p_e_factor(p):
    '''e_factor : MINUS e_factor %prec UMINUS
                | let_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        new_uexpression = UnaryExpression()
        new_uexpression.operator,new_uexpression.expression = p[1],p[2]
        p[0] = new_uexpression

def p_let_expression(p):
    'let_expression : LET declaration_list IN expression'
    new_let = LetVar()
    new_let.declarations = p[2]
    new_let.in_expression = p[4]
    p[0] = new_let


def p_declaration_list(p):
    '''declaration_list : attribute COMMA declaration_list
                        | attribute'''
    if len(p) == 1:
        p[0] = [p[1]]
    else:
        p[3].append(p[1])
        p[0] = p[3]


# def p_declaration(p):
#     '''declaration : id_type ASSIGN expression
#                     | id_type'''

def p_conditional(p):
    'conditional : IF expression THEN expression ELSE expression FI'
    new_conditional = Conditional()
    new_conditional.if_expression = p[2]
    new_conditional.then_expression = p[4]
    new_conditional.else_expression = p[6]
    p[0] = new_conditional


def p_loop(p):
    'loop : WHILE expression LOOP expression POOL'
    new_loop = Loop()
    new_loop.while_expression = p[2]
    new_loop.loop_expression = p[4]
    p[0] = new_loop


def p_case(p):
    'case : CASE expression OF implications ESAC'
    new_case = Case()
    new_case.case_expression = p[2]
    new_case.implications = p[4]
    p[0] = new_case


def p_implications(p):
    '''implications : implication COMMA implications
                    | implication '''
    if len(p) == 1:
        p[0] = [p[1]]
    else:
        p[0] = p[3].append(p[1])


def p_implication(p):
    '''implication : id_type IMPLY expression'''
    new_implication = Implication()
    new_implication.id, new_implication.type = p[1]
    new_implication.expression = p[3]
    p[0] = new_implication


def p_dispatch(p):
    '''dispatch : expression especific DOT dispatch_call
                | dispatch_call'''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[4].left_expression = p[1]
        p[4].dispatch_type = p[3]
        p[0] = p[4]


def p_especific(p):
    '''especific : DISP TYPE
                 | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_dispatch_call(p):
    'dispatch_call : ID LBRACKET params_expression RBRACKET'
    new_dispatch = Dispatch()
    new_dispatch.func_id = p[1]
    new_dispatch.parameters = p[3]
    p[0] = new_dispatch


def p_params_expression(p):
    '''params_expression : expression
                            | expression COMMA params_expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[3].append(p[1])


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
parser.parse(data,lexer=lexer,debug=True,tracking=True)
