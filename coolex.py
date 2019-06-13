import ply.lex as lex
from ply.lex import TOKEN
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
# t_STRING = r'\"[a-zA-Z_][a-zA-Z_0-9]*\"'
# t_STRING = r'\"(.)*\"'
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


# LEXER STATES
def states():
    return (
        ("STRING", "exclusive"),
        ("COMMENT", "exclusive")
    )
states = states()

###
# THE STRING STATE
@TOKEN(r"\"")
def t_start_string(token):
    token.lexer.push_state("STRING")
    token.lexer.string_backslashed = False
    token.lexer.stringbuf = ""


@TOKEN(r"\n")
def t_STRING_newline(token):
    token.lexer.lineno += 1
    if not token.lexer.string_backslashed:
        print("String newline not escaped")
        token.lexer.skip(1)
    else:
        token.lexer.string_backslashed = False


@TOKEN(r"\"")
def t_STRING_end(token):
    if not token.lexer.string_backslashed:
        token.lexer.pop_state()
        token.value = token.lexer.stringbuf
        token.type = "STRING"
        return token
    else:
        token.lexer.stringbuf += '"'
        token.lexer.string_backslashed = False


@TOKEN(r"[^\n]")
def t_STRING_anything(token):
    if token.lexer.string_backslashed:
        if token.value == 'b':
            token.lexer.stringbuf += '\b'
        elif token.value == 't':
            token.lexer.stringbuf += '\t'
        elif token.value == 'n':
            token.lexer.stringbuf += '\n'
        elif token.value == 'f':
            token.lexer.stringbuf += '\f'
        elif token.value == '\\':
            token.lexer.stringbuf += '\\'
        else:
            token.lexer.stringbuf += token.value
        token.lexer.string_backslashed = False
    else:
        if token.value != '\\':
            token.lexer.stringbuf += token.value
        else:
            token.lexer.string_backslashed = True


# STRING ignored characters
t_STRING_ignore = ''


# STRING error handler
def t_STRING_error(token):
    print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
    token.lexer.skip(1)


###
# THE COMMENT STATE
@TOKEN(r"\(\*")
def t_start_comment(token):
    token.lexer.push_state("COMMENT")
    token.lexer.comment_count = 0


@TOKEN(r"\(\*")
def t_COMMENT_startanother(t):
    t.lexer.comment_count += 1


@TOKEN(r"\*\)")
def t_COMMENT_end(token):
    if token.lexer.comment_count == 0:
        token.lexer.pop_state()
    else:
        token.lexer.comment_count -= 1


# COMMENT ignored characters
t_COMMENT_ignore = ''


# COMMENT error handler
def t_COMMENT_error(token):
    token.lexer.skip(1)

# def t_COMMENT(t):
#     r'(--(.)*--)'
#     return ''


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

from cool_errors import throw_exception, LexicographicError

def t_error(t):
    throw_exception(LexicographicError,0,0,"Illegal character '%s'" % t.value[0])

tokens = tokens + list(reserved.values())

lexer = lex.lex()
