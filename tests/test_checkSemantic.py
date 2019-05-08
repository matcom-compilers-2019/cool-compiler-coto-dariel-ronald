from NodosAST import *
from coolyacc import parser
from .tools_for_testing import MyEncoder
import json

def test_first():
    program_ast = ProgramNode([ClassNode('Main', features=[
        MethodNode('main', [], 'SELF_TYPE', DispatchNode('out_string', "Hello, World.\n", None))
    ])])
    program_code = '''
    
    class Main inherits IO {
         main(): SELF_TYPE {
	        out_string("Hello, World.\n")
    };
};
    '''
    parser_result = parser.parse(program_code)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(program_ast, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected, parser_result)

