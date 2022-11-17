import sys
import itertools
from random import randint


operators = ['+', '-', '*', '/', '%', '**', '//', '&', '|', '^', '~', '<<', '>>']
operators = ['&', '|', '^', '& ~', '| ~', '^ ~']
operators = ['&', '|', '^']

def comb(vals, size):
    return list(itertools.product(vals, repeat=size))

# FIXME genera doppioni quanto le espressioni hanno 3 elementi
def evaluate(expr):

  if len(expr) == 3:
    return [' '.join(expr)]

  res = []
  i = 1
  while i < len(expr):
    expr2 = expr[:i-1] + [f'({expr[i-1]} {expr[i]} {expr[i+1]})'] + expr[i+2:]
    res += [' '.join(expr2)]
    res += evaluate(expr2)
    i += 2
  return res

def get_exprs(operators, operands, num_ops):
  res = []
  for ops in comb(operators, num_ops):
    for opers in comb(operands, num_ops+1):
      i = 0
      expr = [opers[i]]
      for op in ops:
        expr.append(op)
        i += 1
        expr.append(opers[i])
      # dato un insieme di operatori e di operandi evaluate restituisce tutte le combinazioni possibili incluse le parentesi
      res += evaluate(expr)
  return res

def gen_vals(size):
  return [str(randint(1,100)) for i in range(size)]

def replace_operands(expr, values, operands):
  for i in range(len(operands)):
    expr = expr.replace(operands[i], values[i])
  return expr

def check(input_expr, expr, values, operands):
  example_expr = replace_operands(input_expr, values, operands)
  target = eval(example_expr)
  #print(f'{example_expr} = {target}')
  expr = replace_operands(expr, values, operands)
  val = eval(expr)
  if val == target:
    return True
  else:
    return False

def verify(input_expr, expr, operands):
  for i in range(100):
      # TODO gli operandi che trova potrebbero essere più di quelli effettivamente presenti perché le variabiali x si possono ripetere
      values = gen_vals(len(operands))
      if not check(input_expr, expr, values, operands):
        return False
  return True

def search(input_expr, operators, operands):
  expr_size = len(input_expr.split(" "))
  num_ops_max = expr_size // 2
  print("num_ops_max", num_ops_max)
  for num_ops in range(1, num_ops_max+1):
    print("num_ops", num_ops)
    for expr in get_exprs(operators, operands, num_ops):
      if verify(input_expr, expr, operands):
        print(f'expr {expr}')
        return

def get_operands(expr, operators):
  for op in operators:
    expr = expr.replace(op, "")
  return list(dict.fromkeys([x for x in expr.split(" ") if x != '']))

input_expr = sys.argv[1]
print(f'input_expr {input_expr}')
input_expr = input_expr.replace('(','').replace(')','')
print(input_expr)
operands = get_operands(input_expr, operators)
search(input_expr, operators, operands)


