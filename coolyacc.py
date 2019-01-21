import ply.yacc as yacc
from coolex import tokens

def p_program(p):
    '''program : class SEMICOLON program
               | class SEMICOLON'''

def p_class(p):
    'class : CLASS TYPE inheritence LBRACE features RBRACE'

def p_inheritence(p):
    '''inheritence : INHERITS TYPE
                    | empty'''

def p_features(p):
    '''features : feature SEMICOLON features
                | empty'''

def p_feature(p):
    '''feature : method_declaration
               | attribute'''

def p_attribute(p):
    '''attribute : id_type
                | id_type ASSIGN expression'''

def p_id_type(p):
    'id_type : ID TDOTS TYPE'

def p_method_declaration(p):
    'method_declaration : ID LBRACKET formals RBRACKET TDOTS TYPE block'

def p_block(p):
    'block : LBRACE expression_list RBRACE'

def p_formals(p):
    '''formals : id_type COMMA formals
                | id_type
                | empty'''

def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''

def p_expression(p):
    '''expression : assign
                    | upper_non'''

def p_upper_non(p):
    '''upper_non : NOT upper_non
                | operator_non'''

def p_operator_non(p):
    '''operator_non : k_arith LTHAN k_arith
                    | k_arith LETHAN k_arith
                    | k_arith EQUALS k_arith
                    | k_arith'''

def p_k_arith(p):
    '''k_arith : arith
                | e_arith'''


def p_assign(p):
    'assign : ID ASSIGN expression'


def p_arith(p):
    '''arith : arith PLUS term
            | arith MINUS term
            | term'''


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''

def p_factor(p):
    '''factor : MINUS factor
                | atom'''

def p_atom(p):
    '''atom : LBRACKET expression RBRACKET
            | INTEGER
            | STRING
            | ID
            | TRUE
            | FALSE
            | ISVOID expression
            | block
            | conditional
            | loop
            | case
            | dispatch
            | NEW TYPE
            | BCOMPLEMENT expression'''

def p_e_arith(p):
    '''e_arith : arith PLUS e_term
                | arith MINUS e_term
                | e_term'''

def p_e_term(p):
    '''e_term : e_term TIMES e_factor
                | e_term DIVIDE e_factor
                | e_factor'''

def p_e_factor(p):
    '''e_factor : MINUS e_factor
                | let_expression'''

def p_let_expression(p):
    'let_expression : LET declaration_list IN expression'

def p_declaration_list(p):
    '''declaration_list : declaration COMMA declaration_list
                        | declaration'''

def p_declaration(p):
    '''declaration : id_type ASSIGN expression 
                    | id_type'''

def p_conditional(p):
    'conditional : IF expression THEN expression ELSE expression FI'

def p_loop(p):
    'loop : WHILE expression LOOP expression POOL'

def p_case(p):
    'case : CASE expression OF implications ESAC'

def p_implications(p):
    '''implications : implication COMMA implications
                    | implication '''

def p_implication(p):
    '''implication : id_type IMPLY expression'''


def p_dispatch(p):
    '''dispatch : expression especific DOT dispatch_call
                | dispatch_call'''

def p_especific(p):
    '''especific : DISP TYPE
                 | empty'''

def p_dispatch_call(p):
    'dispatch_call : ID LBRACKET params_expression RBRACKET'

def p_params_expression(p):
    '''params_expression : expression
                            | expression COMMA params_expression
                            | empty'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error in input")

precedence = (
    ('right','ASSIGN'),
    ('left','NOT'),
    ('right','BCOMPLEMENT'),
    ('right','ISVOID'),
    ('nonassoc','LTHAN','LETHAN','EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','DISP'),
    ('left','DOT')
)

parser = yacc.yacc()
