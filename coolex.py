import ply.lex as lex

tokens = [
    'TYPE',
    'SEMICOLON',
    'COMMA',
    'LBRACE',
    'RBRACE',
    'DOT',
    'TDOTS',
    'ASSIGN',
    'ID',
    'LBRACKET',
    'RBRACKET',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'INTEGER',
    'BCOMPLEMENT',
    'LTHAN',
    'LETHAN',
    'EQUALS',
    'STRING',
    'DISP',
    'IMPLY'
]

t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_TDOTS = r'\:'
t_DOT = r'\.'
t_ASSIGN = r'<-'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_BCOMPLEMENT = r'~'
t_IMPLY = r'=>'
t_LETHAN = r'<='
t_LTHAN = r'<'
t_EQUALS = r'='
t_DISP = r'@'
# me faltan por agregar simbolos y otras cosas
t_STRING = r'\"[a-zA-Z_][a-zA-Z_0-9]*\"'
t_TYPE = r'[A-Z][a-zA-Z_0-9]*'

reserved = {
    'let':'LET',
    'in':'IN',
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'fi':'FI',
    'while':'WHILE',
    'loop':'LOOP',
    'pool':'POOL',
    'class':'CLASS',
    
    'inherits':'INHERITS',
    'not': 'NOT',
    'isvoid': 'ISVOID',
    'true': 'TRUE',
    'false': 'FALSE',
    'new':'NEW',
    'case' : 'CASE',
    'of': 'OF',
    'esac':'ESAC'
}

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore = ' \t'
from error import LexicographicError
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

tokens = tokens + list(reserved.values())

lexer = lex.lex()
#
# data = '''
# class Cons inherits List {
#     xcar : Int;
#     xcdr : List;
#     isNil() : Bool { false };
#     init(hd : Int, tl : List) : Cons {
#     {
#         xcar <- hd;
#         xcdr <- tl;
#         self;
#         }
#     }
# };
#     '''


# data = '''
#
# class B  {
#     xcar2 : Int;
# };
# class A inherits B{
#     xcar1 : Int;
# };
# class Cons inherits A{
#     xcar : Int;
#     xcdr : String;
#     isNil() : Bool { false };
#     init(hd : Int, tl : String) : Cons {
#         {
#             xcar <- hd;
#             xcdr <- tl;
#             self;
#         }
#     };
# };
# '''
data = '''
class B {
s : String <- "Hello";
g (y:String) : Int {
y.concat(s)
};
f (x:Int) : Int {
x+1
};
};
class A inherits B {
a : Int;
b : B <- new B;
f(x:Int) : Int {
x+a
};
};
'''
# data = '''
# class A {
#        funk(): Int {
#             case 1 of
#                 x:Int => 10;
#                 x:String => "s";
#                 x:Bool => true;
#             esac
#        };
#     };
# '''

# lexer.input(data)
# for tok in lexer:
#     print(tok)
