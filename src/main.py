from coolex import lexer
from coolyacc2 import parser
from semantic import TypeCheckerVisitor
from cool_utils import Scope
import fileinput
from cool_errors import CoolErrorLogger
from tqdm import tqdm
from cool_to_cil import *
from cil_to_mips import *
import logging
from hashlib import sha256
from cil_utils import CILScope
logging.basicConfig()


def main():
    print(CoolErrorLogger([]))
    logging.info('Loading data...')
    data = ''
    for line in tqdm(fileinput.input()):
        data += line

    compile_cool(data)


def check_semantic(ast):
    scope = Scope()

    tchecv = TypeCheckerVisitor()
    tchecv.visit(ast, scope)


def compile_cool(data):
    cool_ast = parser.parse(data, lexer,debug=True)

    logging.info('Checking semantic...')
    check_semantic(cool_ast)

    logging.info('Generating IL code')

    ctcv = COOLToCILVisitor()
    cilScope = CILScope()
    cil_ast = ctcv.visit(cool_ast,cilScope)

    logging.info('Generating to mips')
    mips_visitor = CILtoMIPSVisitor()

    mips_visitor.visit(cil_ast)

    program = mips_visitor.get_mips_program_code()
    program_name = sha256(program.encode()).hexdigest()
    with open(f'{program_name}.s', 'w') as file:
        file.writelines(program)

if __name__ == '__main__':
    main()



















