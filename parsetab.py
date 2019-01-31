
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightASSIGNleftNOTnonassocLTHANLETHANEQUALSleftPLUSMINUSleftTIMESDIVIDErightUMINUSrightISVOIDrightBCOMPLEMENTleftDISPleftDOTASSIGN BCOMPLEMENT CASE CLASS COMMA DISP DIVIDE DOT ELSE EQUALS ESAC FALSE FI ID IF IMPLY IN INHERITS INTEGER ISVOID LBRACE LBRACKET LET LETHAN LOOP LTHAN MINUS NEW NOT OF PLUS POOL RBRACE RBRACKET SEMICOLON STRING TDOTS THEN TIMES TRUE TYPE WHILEprogram : class SEMICOLON program\n               | class SEMICOLONclass : CLASS TYPE inheritence LBRACE features RBRACEinheritence : INHERITS TYPE\n                    | emptyfeatures : feature SEMICOLON features\n                | emptyfeature : method_declaration\n               feature : attributeattribute : id_type\n                | id_type ASSIGN expressionid_type : ID TDOTS TYPEmethod_declaration : ID LBRACKET formals RBRACKET TDOTS TYPE LBRACE expression RBRACEformals : id_type COMMA formals\n                | id_typeformals : emptyexpression_list : expression SEMICOLON expression_list\n                        | expression SEMICOLONexpression : assign\n                    | upper_nonupper_non : NOT upper_non\n                | operator_nonoperator_non : k_arith LTHAN k_arith\n                    | k_arith LETHAN k_arith\n                    | k_arith EQUALS k_arith\n                    | k_arithk_arith : arith\n                | e_arithassign : ID ASSIGN expressionarith : arith PLUS term\n            | arith MINUS term\n            | termterm : term TIMES factor\n            | term DIVIDE factor\n            | factorfactor : MINUS factor %prec UMINUS\n                | atomatom : LBRACKET expression RBRACKET\n            | ISVOID expression\n            | block\n            | conditional\n            | loop\n            | case\n            | dispatch\n            | BCOMPLEMENT expression\n            block : LBRACE expression_list RBRACEatom : IDatom : INTEGER atom : STRINGatom : TRUE\n            | FALSEatom : NEW TYPEe_arith : arith PLUS e_term\n                | arith MINUS e_term\n                | e_terme_term : e_term TIMES e_factor\n                | e_term DIVIDE e_factor\n                | e_factore_factor : MINUS e_factor %prec UMINUS\n                | let_expressionlet_expression : LET declaration_list IN expressiondeclaration_list : attribute COMMA declaration_list\n                        | attributeconditional : IF expression THEN expression ELSE expression FIloop : WHILE expression LOOP expression POOLcase : CASE expression OF implications ESACimplications : implication COMMA implications\n                    | implication implication : id_type IMPLY expressiondispatch : expression especific DOT dispatch_call\n                | dispatch_callespecific : DISP TYPE\n                 | emptydispatch_call : ID LBRACKET params_expression RBRACKETparams_expression : expression\n                            | expression COMMA params_expression\n    params_expression : emptyempty :'
    
_lr_action_items = {'CLASS':([0,4,],[3,3,]),'$end':([1,4,6,],[0,-2,-1,]),'SEMICOLON':([2,13,15,16,18,19,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,93,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,150,151,],[4,20,-8,-9,-10,-3,-12,-11,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,121,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-13,-64,]),'TYPE':([3,8,22,58,68,97,],[5,11,29,89,100,125,]),'INHERITS':([5,],[8,]),'LBRACE':([5,7,9,11,23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,125,129,139,141,145,],[-78,10,-5,-4,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,139,60,60,60,60,]),'RBRACE':([10,12,14,20,24,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,92,101,105,106,107,108,109,110,111,112,113,114,116,117,120,121,126,128,130,131,133,142,143,146,151,],[-78,19,-7,-78,-6,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,120,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-18,-70,-74,-59,-61,-17,-65,-66,150,-64,]),'ID':([10,20,21,23,34,40,46,47,53,59,60,61,62,63,66,70,71,75,76,77,78,79,80,81,99,118,119,121,122,123,124,129,139,141,144,145,],[17,17,25,33,74,74,33,33,33,25,33,33,33,33,25,33,33,74,74,74,74,74,74,74,127,33,25,33,33,33,25,33,33,33,25,33,]),'LBRACKET':([17,23,33,34,40,46,47,53,60,61,62,63,70,71,74,75,76,77,78,79,80,81,118,121,122,123,127,129,139,141,145,],[21,46,71,46,46,46,46,46,46,46,46,46,46,46,71,46,46,46,46,46,46,46,46,46,46,46,71,46,46,46,46,]),'TDOTS':([17,25,65,],[22,22,97,]),'COMMA':([18,27,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,91,101,103,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,137,142,143,149,151,],[-10,66,-12,-11,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,119,-29,129,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,144,-65,-66,-69,-64,]),'IN':([18,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,90,91,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,132,142,143,151,],[-10,-12,-11,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,118,-63,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-62,-65,-66,-64,]),'ASSIGN':([18,29,33,74,],[23,-12,70,70,]),'RBRACKET':([21,26,27,28,29,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,66,71,72,74,82,83,86,87,88,89,98,101,102,103,104,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,129,130,131,140,142,143,151,],[-78,65,-15,-16,-12,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-78,-78,-21,-47,-36,-59,117,-39,-45,-52,-14,-29,128,-75,-77,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-78,-59,-61,-76,-65,-66,-64,]),'NOT':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'MINUS':([23,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,60,61,62,63,64,70,71,72,74,75,76,77,78,79,80,81,82,83,84,85,87,88,89,101,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,123,126,128,129,130,131,139,141,142,143,145,151,],[40,-19,-20,-47,40,-22,-26,79,-28,-32,40,-55,-35,-58,-37,-60,40,40,-40,-41,-42,-43,-44,40,-48,-49,-50,-51,40,40,40,40,-71,40,40,-21,-47,40,40,40,40,40,40,40,-35,-59,115,115,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,115,-57,-38,40,-46,40,40,40,-70,-74,40,-59,-61,40,40,-65,-66,40,-64,]),'ISVOID':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'BCOMPLEMENT':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'INTEGER':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'STRING':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'TRUE':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'FALSE':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'NEW':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,]),'LET':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,84,85,115,118,121,122,123,129,139,141,145,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'IF':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,]),'WHILE':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,]),'CASE':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,]),'IMPLY':([29,138,],[-12,145,]),'DISP':([30,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,73,74,82,83,86,87,88,89,93,94,95,96,101,103,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,134,135,142,143,146,147,149,151,],[68,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-20,68,-47,-35,-58,68,68,68,-52,68,68,68,68,68,68,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,68,68,68,-65,-66,68,68,68,-64,]),'DOT':([30,31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,67,69,72,73,74,82,83,86,87,88,89,93,94,95,96,100,101,103,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,134,135,142,143,146,147,149,151,],[-78,-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,99,-73,-20,-78,-47,-35,-58,-78,-39,-45,-52,-78,-78,-78,-78,-72,-29,-78,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-78,-78,-65,-66,-78,-78,-78,-64,]),'TIMES':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,80,84,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-58,-39,-45,-52,-29,-23,-24,-25,80,84,80,84,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'DIVIDE':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,81,85,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-58,-39,-45,-52,-29,-23,-24,-25,81,85,81,85,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'PLUS':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,78,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-59,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'LTHAN':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,75,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-58,-39,-45,-52,-29,None,None,None,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'LETHAN':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,76,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-58,-39,-45,-52,-29,None,None,None,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'EQUALS':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,77,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-35,-58,-39,-45,-52,-29,None,None,None,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'THEN':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,94,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,122,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'LOOP':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,95,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,123,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'OF':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,96,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,124,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,-64,]),'ELSE':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,134,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,141,-65,-66,-64,]),'POOL':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,135,142,143,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,142,-65,-66,-64,]),'FI':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,142,143,147,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,-65,-66,151,-64,]),'ESAC':([31,32,33,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,54,55,56,57,64,72,74,82,83,87,88,89,101,105,106,107,108,109,110,111,112,113,114,116,117,120,126,128,130,131,136,137,142,143,148,149,151,],[-19,-20,-47,-22,-26,-27,-28,-32,-55,-35,-58,-37,-60,-40,-41,-42,-43,-44,-48,-49,-50,-51,-71,-21,-47,-36,-59,-39,-45,-52,-29,-23,-24,-25,-30,-53,-31,-54,-33,-34,-56,-57,-38,-46,-70,-74,-59,-61,143,-68,-65,-66,-67,-69,-64,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,4,],[1,6,]),'class':([0,4,],[2,2,]),'inheritence':([5,],[7,]),'empty':([5,10,20,21,30,66,71,73,86,87,88,93,94,95,96,101,103,129,131,134,135,146,147,149,],[9,14,14,28,69,28,104,69,69,69,69,69,69,69,69,69,69,104,69,69,69,69,69,69,]),'features':([10,20,],[12,24,]),'feature':([10,20,],[13,13,]),'method_declaration':([10,20,],[15,15,]),'attribute':([10,20,59,119,],[16,16,91,91,]),'id_type':([10,20,21,59,66,119,124,144,],[18,18,27,18,27,18,138,138,]),'formals':([21,66,],[26,98,]),'expression':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[30,73,73,86,87,88,93,94,95,96,101,103,73,73,73,73,73,73,73,131,93,134,135,103,146,147,149,]),'assign':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'upper_non':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[32,72,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'operator_non':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'k_arith':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[36,36,36,36,36,36,36,36,36,36,36,36,105,106,107,36,36,36,36,36,36,36,36,36,36,36,36,]),'arith':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'e_arith':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'term':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,108,110,39,39,39,39,39,39,39,39,39,39,]),'e_term':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,109,111,41,41,41,41,41,41,41,41,41,41,]),'factor':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[42,42,82,42,42,42,42,42,42,42,42,42,42,42,42,42,42,112,113,42,42,42,42,42,42,42,42,]),'e_factor':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,84,85,115,118,121,122,123,129,139,141,145,],[43,43,83,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,114,116,130,43,43,43,43,43,43,43,43,]),'atom':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'let_expression':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,84,85,115,118,121,122,123,129,139,141,145,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'block':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'conditional':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'loop':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'case':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'dispatch':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,118,121,122,123,129,139,141,145,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'dispatch_call':([23,34,40,46,47,53,60,61,62,63,70,71,75,76,77,78,79,80,81,99,118,121,122,123,129,139,141,145,],[64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,126,64,64,64,64,64,64,64,64,]),'especific':([30,73,86,87,88,93,94,95,96,101,103,131,134,135,146,147,149,],[67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,]),'declaration_list':([59,119,],[90,132,]),'expression_list':([60,121,],[92,133,]),'params_expression':([71,129,],[102,140,]),'implications':([124,144,],[136,148,]),'implication':([124,144,],[137,137,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class SEMICOLON program','program',3,'p_program','coolyacc.py',7),
  ('program -> class SEMICOLON','program',2,'p_program','coolyacc.py',8),
  ('class -> CLASS TYPE inheritence LBRACE features RBRACE','class',6,'p_class','coolyacc.py',19),
  ('inheritence -> INHERITS TYPE','inheritence',2,'p_inheritence','coolyacc.py',25),
  ('inheritence -> empty','inheritence',1,'p_inheritence','coolyacc.py',26),
  ('features -> feature SEMICOLON features','features',3,'p_features','coolyacc.py',35),
  ('features -> empty','features',1,'p_features','coolyacc.py',36),
  ('feature -> method_declaration','feature',1,'p_feature_method_declaration','coolyacc.py',46),
  ('feature -> attribute','feature',1,'p_feature_attribute','coolyacc.py',52),
  ('attribute -> id_type','attribute',1,'p_attribute','coolyacc.py',57),
  ('attribute -> id_type ASSIGN expression','attribute',3,'p_attribute','coolyacc.py',58),
  ('id_type -> ID TDOTS TYPE','id_type',3,'p_id_type','coolyacc.py',67),
  ('method_declaration -> ID LBRACKET formals RBRACKET TDOTS TYPE LBRACE expression RBRACE','method_declaration',9,'p_method_declaration','coolyacc.py',73),
  ('formals -> id_type COMMA formals','formals',3,'p_formals','coolyacc.py',80),
  ('formals -> id_type','formals',1,'p_formals','coolyacc.py',81),
  ('formals -> empty','formals',1,'p_formals_empty','coolyacc.py',91),
  ('expression_list -> expression SEMICOLON expression_list','expression_list',3,'p_expression_list','coolyacc.py',96),
  ('expression_list -> expression SEMICOLON','expression_list',2,'p_expression_list','coolyacc.py',97),
  ('expression -> assign','expression',1,'p_expression','coolyacc.py',105),
  ('expression -> upper_non','expression',1,'p_expression','coolyacc.py',106),
  ('upper_non -> NOT upper_non','upper_non',2,'p_upper_non','coolyacc.py',111),
  ('upper_non -> operator_non','upper_non',1,'p_upper_non','coolyacc.py',112),
  ('operator_non -> k_arith LTHAN k_arith','operator_non',3,'p_operator_non','coolyacc.py',120),
  ('operator_non -> k_arith LETHAN k_arith','operator_non',3,'p_operator_non','coolyacc.py',121),
  ('operator_non -> k_arith EQUALS k_arith','operator_non',3,'p_operator_non','coolyacc.py',122),
  ('operator_non -> k_arith','operator_non',1,'p_operator_non','coolyacc.py',123),
  ('k_arith -> arith','k_arith',1,'p_k_arith','coolyacc.py',136),
  ('k_arith -> e_arith','k_arith',1,'p_k_arith','coolyacc.py',137),
  ('assign -> ID ASSIGN expression','assign',3,'p_assign','coolyacc.py',142),
  ('arith -> arith PLUS term','arith',3,'p_arith','coolyacc.py',147),
  ('arith -> arith MINUS term','arith',3,'p_arith','coolyacc.py',148),
  ('arith -> term','arith',1,'p_arith','coolyacc.py',149),
  ('term -> term TIMES factor','term',3,'p_term','coolyacc.py',161),
  ('term -> term DIVIDE factor','term',3,'p_term','coolyacc.py',162),
  ('term -> factor','term',1,'p_term','coolyacc.py',163),
  ('factor -> MINUS factor','factor',2,'p_factor','coolyacc.py',174),
  ('factor -> atom','factor',1,'p_factor','coolyacc.py',175),
  ('atom -> LBRACKET expression RBRACKET','atom',3,'p_atom','coolyacc.py',183),
  ('atom -> ISVOID expression','atom',2,'p_atom','coolyacc.py',184),
  ('atom -> block','atom',1,'p_atom','coolyacc.py',185),
  ('atom -> conditional','atom',1,'p_atom','coolyacc.py',186),
  ('atom -> loop','atom',1,'p_atom','coolyacc.py',187),
  ('atom -> case','atom',1,'p_atom','coolyacc.py',188),
  ('atom -> dispatch','atom',1,'p_atom','coolyacc.py',189),
  ('atom -> BCOMPLEMENT expression','atom',2,'p_atom','coolyacc.py',190),
  ('block -> LBRACE expression_list RBRACE','block',3,'p_block','coolyacc.py',204),
  ('atom -> ID','atom',1,'p_atom_variable','coolyacc.py',209),
  ('atom -> INTEGER','atom',1,'p_atom_type_int','coolyacc.py',214),
  ('atom -> STRING','atom',1,'p_atom_type_str','coolyacc.py',218),
  ('atom -> TRUE','atom',1,'p_atom_type_bool','coolyacc.py',222),
  ('atom -> FALSE','atom',1,'p_atom_type_bool','coolyacc.py',223),
  ('atom -> NEW TYPE','atom',2,'p_atom_newtype','coolyacc.py',231),
  ('e_arith -> arith PLUS e_term','e_arith',3,'p_e_arith','coolyacc.py',236),
  ('e_arith -> arith MINUS e_term','e_arith',3,'p_e_arith','coolyacc.py',237),
  ('e_arith -> e_term','e_arith',1,'p_e_arith','coolyacc.py',238),
  ('e_term -> e_term TIMES e_factor','e_term',3,'p_e_term','coolyacc.py',249),
  ('e_term -> e_term DIVIDE e_factor','e_term',3,'p_e_term','coolyacc.py',250),
  ('e_term -> e_factor','e_term',1,'p_e_term','coolyacc.py',251),
  ('e_factor -> MINUS e_factor','e_factor',2,'p_e_factor','coolyacc.py',262),
  ('e_factor -> let_expression','e_factor',1,'p_e_factor','coolyacc.py',263),
  ('let_expression -> LET declaration_list IN expression','let_expression',4,'p_let_expression','coolyacc.py',271),
  ('declaration_list -> attribute COMMA declaration_list','declaration_list',3,'p_declaration_list','coolyacc.py',276),
  ('declaration_list -> attribute','declaration_list',1,'p_declaration_list','coolyacc.py',277),
  ('conditional -> IF expression THEN expression ELSE expression FI','conditional',7,'p_conditional','coolyacc.py',290),
  ('loop -> WHILE expression LOOP expression POOL','loop',5,'p_loop','coolyacc.py',295),
  ('case -> CASE expression OF implications ESAC','case',5,'p_case','coolyacc.py',300),
  ('implications -> implication COMMA implications','implications',3,'p_implications','coolyacc.py',305),
  ('implications -> implication','implications',1,'p_implications','coolyacc.py',306),
  ('implication -> id_type IMPLY expression','implication',3,'p_implication','coolyacc.py',314),
  ('dispatch -> expression especific DOT dispatch_call','dispatch',4,'p_dispatch','coolyacc.py',323),
  ('dispatch -> dispatch_call','dispatch',1,'p_dispatch','coolyacc.py',324),
  ('especific -> DISP TYPE','especific',2,'p_especific','coolyacc.py',332),
  ('especific -> empty','especific',1,'p_especific','coolyacc.py',333),
  ('dispatch_call -> ID LBRACKET params_expression RBRACKET','dispatch_call',4,'p_dispatch_call','coolyacc.py',341),
  ('params_expression -> expression','params_expression',1,'p_params_expression','coolyacc.py',346),
  ('params_expression -> expression COMMA params_expression','params_expression',3,'p_params_expression','coolyacc.py',347),
  ('params_expression -> empty','params_expression',1,'p_params_expression_empty','coolyacc.py',356),
  ('empty -> <empty>','empty',0,'p_empty','coolyacc.py',361),
]
