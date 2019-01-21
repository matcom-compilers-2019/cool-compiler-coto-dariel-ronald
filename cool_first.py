import ply.yacc as yacc
from coolex import tokens
from test import test

def p_program(p):
    '''program : class SEMICOLON program
               | class SEMICOLON'''
    if len(p)>3:
        p[0] = ("Programs declaration",p[1],p[2],p[3])
    else:
        p[0] = ("Program declaration",p[1],p[2])

    print(p[:])

def p_class(p):
    'class : CLASS TYPE inheritence LBRACE features RBRACE'
    p[0] = ("Class declaration",p[1],p[2],p[3],p[4],p[5],p[6])
    print(p[:])


def p_inheritence(p):
    '''inheritence : INHERITS TYPE
                    | empty'''
    if len(p)==3:
        p[0]=("inherits",p[1],p[2])
    else:
        p[0]=("empty")

    print(p[:])

def p_features(p):
    '''features : feature SEMICOLON features
                | empty'''
    if len(p)==4:
        p[0] = ("features",p[1],p[2],p[3])
    else:
        p[0]=("empty")
    print(p[:])

def p_feature(p):
    '''feature : method_declaration
               | attribute'''
    p[0] = ("feature",p[1])        
    print(p[:])

def p_attribute(p):
    '''attribute : id_type
                | id_type ASSIGN expression'''
    if len(p) == 2:
        p[0]= ("attribute", p[1])
    else:
        p[0] = ("atribute", p[1],p[2],p[3])
    print(p[:])


def p_id_type(p):
    'id_type : ID TDOTS TYPE'
    p[0] = ("id_type",p[1],p[2],p[3])
    print(p[:])

def p_method_declaration(p):
    'method_declaration : ID LBRACKET formals RBRACKET TDOTS TYPE block'
    p[0] = ("method_declaration",p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    print(p[:])

def p_block(p):
    'block : LBRACE expression_list RBRACE'
    p[0] = ("block",p[1],p[2],p[3])
    print(p[:])

def p_formals(p):
    '''formals : id_type COMMA formals
                | id_type
                | empty'''
    if len(p) > 2:
        p[0] = ("formals",p[1],p[2],p[3])
    elif len(p) == 2:
        p[0] = ("formal",p[1])
    else:
        p[0] = ("empty")
    print(p[:])

def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    if len(p) == 4:
        p[0] = ("expression_list", p[1],p[2],p[3])
    else:
        p[0] = ("expression_list", p[1],p[2])
    print(p[:])

def p_expression(p):
    '''expression : assign
                    | dispatch
                    | conditional
                    | loop
                    | block
                    | let_expression
                    | case
                    | NEW TYPE
                    | ISVOID expression
                    | expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | BCOMPLEMENT expression
                    | expression LTHAN expression
                    | expression LETHAN expression
                    | expression EQUALS expression
                    | NOT expression
                    | LBRACKET expression RBRACKET
                    | ID
                    | INTEGER
                    | STRING
                    | TRUE
                    | FALSE'''
    if len(p) == 4:
        p[0] = ("expressions",p[1],p[2],p[3])
    elif len(p) == 3:
        p[0] = ("expression",p[1],p[2])
    else:
        p[0] = ("expression",p[1])
    print(p[:])

def p_assign(p):
    'assign : ID ASSIGN expression'
    p[0] = ("assign",p[1],p[2],p[3])
    print(p[:])

def p_let_expression(p):
    'let_expression : LET declaration_list IN expression'
    p[0] = ("let_expression",p[1],p[2],p[3],p[4])
    print(p[:])

def p_declaration_list(p):
    '''declaration_list : declaration COMMA declaration_list
                        | declaration'''
    if len(p) == 4:
        p[0] = ("declaration_lists",p[1],p[2],p[3])
    else:
        p[0] = ("declaration_list",p[1])
    print(p[:])

def p_declaration(p):
    '''declaration : id_type ASSIGN expression 
                    | id_type'''
    if len(p) == 4:
        p[0] = ("declaration",p[1],p[2],p[3])
    else:
        p[0] = ("declaration",p[1])
    print(p[:])
    
def p_conditional(p):
    'conditional : IF expression THEN expression ELSE expression FI'
    p[0] = ("conditional",p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    print(p[:])

def p_loop(p):
    'loop : WHILE expression LOOP expression POOL'
    p[0] = ("loop",p[1],p[2],p[3],p[4],p[5])
    print(p[:])

def p_case(p):
    'case : CASE expression OF implications ESAC'
    p[0] = ("case",p[1],p[2],p[3],p[4],p[5])
    print(p[:])

def p_implications(p):
    '''implications : implication COMMA implications
                    | implication '''
    if len(p) == 4:
        p[0] = ("implications",p[1],p[2],p[3])
    else:
        p[0] = ("implications",p[1])
    print(p[:])

def p_implication(p):
    '''implication : id_type IMPLY expression'''
    p[0] = ("implication",p[1],p[2],p[3])
    print(p[:])


def p_dispatch(p):
    '''dispatch : expression especific DOT dispatch_call
                | dispatch_call'''
    if len(p)==5:
        p[0] = ("dispatch",p[1],p[2],p[3],p[4])
    else:
        p[0] = ("dispatch",p[1])
    print(p[:])

def p_especific(p):
    '''especific : DISP TYPE
                 | empty'''
    if len(p) == 3:
        p[0] = ("especific",p[1],p[2])
    else:
        p[0] = ("empty")
    print(p[:])

def p_dispatch_call(p):
    'dispatch_call : ID LBRACKET params_expression RBRACKET'
    p[0] = ("dispatch_call",p[1],p[2],p[3],p[4])
    print(p[:])

def p_params_expression(p):
    '''params_expression : expression
                            | expression COMMA params_expression
                            | empty'''
    if len(p) == 4:
        p[0] = ("params_expressions",p[1],p[2],p[3])
    elif len(p) == 2:
        p[0] = ("params_expressions",p[1])
    else:
        p[0] = ("empty")

    print(p[:])

def p_empty(p):
    'empty :'
    p[0]=("empty")
    print(p[:])
    

def p_error(p):
    print("Syntax error in input {}".fo rmat(p))
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

for t in test:
    parser.parse(t)

