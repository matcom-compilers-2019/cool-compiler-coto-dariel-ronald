import ply.yacc as yacc
from coolex import tokens
from NodosAST import *

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
    p[0] = AttributeNode(p[1][0][0], p[1][0][1], p[1][1])
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

def p_expression_case(p):
    'expression : case'
    p[0] = CaseNode(p[2],p[4])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_dispatch(p):
    'expression : dispatch'

def p_expression_conditional(p):
    'expression : conditional'
    p[0] = ConditionalNode(p[2], p[4], p[6])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

def p_expression_loop(p):
    'expression : loop'
    p[0] = LoopNode(p[2],p[4])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

def p_expression_let(p):
    'expression: let_expression'

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

def p_expression_id(p):
    'expression : ID'
    p[0] = ObjectNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

def p_expression_integer(p):
    'expression : INTEGER'
    p[0] = IntNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)


def p_expression_string(p):
    'expression : STRING'
    p[0] = StrNode(p[1])
    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

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

    if p[1] == 'true' or p[1] == 'false':
        p[0] = BoolNode(p[1])
    elif p[1] == 'new':
        p[0] = NewTypeNode(p[2])
    elif p[1] == 'not':
        p[0] = NotNode(p[2])
    elif p[1] == '~':
        p[0] = IntegerComplementNode(p[2])
    elif p[1] == 'isvoid':
        p[0] = IsVoidNode(p[2])
    elif len(p) == 4:
        if p[2] == '<':
            p[0] = LowerThanNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LowerEqualThanNode(p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualThanNode(p[1], p[3])
        elif p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])
        elif p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])

        elif p[1] == '{':
            p[0] = BlockNode(p[2])

    elif len(p) == 3:
        p[0] = ("expression",p[1],p[2])
    else:
        p[0] = ("expression",p[1])

    p[0].line = p.lineno(1)
    p[0].index = p.lexpos(1)

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
    print("Syntax error in input ")
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


