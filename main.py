from coolex import lexer
from coolyacc import parser
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope
import fileinput
from cool_errors import CoolErrorLogger
from tqdm import tqdm
from cool_to_cil import *
from cil_to_mips import *
import logging
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
    tcv = TypeCollectorVisitor(scope)
    tcv.visit(ast)

    tbv = TypeBuilderVisitor(scope)
    tbv.visit(ast)

    tchecv = TypeCheckerVisitor()
    tchecv.check_class_hierarchy(scope)
    tchecv.look_for_Main_Class(scope)
    tchecv.visit(ast, scope)


def compile_cool(data):
    cool_ast = parser.parse(data, lexer)

    logging.info('Checking semantic...')
    check_semantic(cool_ast)

    logging.info('Generating IL code')
    ctcv = COOLToCILVisitor()
    cil_ast = ctcv.visit(cool_ast)

    logging.info('Generating to mips')
    mips_visitor = CILtoMIPSVisitor()
    mips_visitor.visit(cil_ast)

    program = mips_visitor.get_mips_program_code()
    program_name = hash(program)

    with open(str(program_name)+'.s', 'w') as file:
        file.writelines(program)

if __name__ == '__main__':
    main()



















