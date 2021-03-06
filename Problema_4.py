#!/usr/bin/env python3.7
from functools import reduce
from typing import Callable, Dict, Set, Tuple, Any


def compose_functions(f: Callable, g: Callable) -> Callable:
    def fog(x:Any) -> Any:
        return g(f(x))
    return fog


def or_function(v1: bool, v2: bool)-> bool:
    return v1 or v2


def turing_machine(sigma: Set[chr],
                   gamma: Set[chr],
                   b: chr,
                   delta: Dict[Tuple[chr, str], Tuple[chr, str, int]],
                   f: Set[str],
                   s: str,
                   max_iter: int = 10000):

    def delta_fn(char: chr, state: str) -> str:
        print(f'{char} , {state} : {delta.get((char,state), "_")}')
        return delta.get((char,state), (char, "q_i", 0))

    def evaluate_word(word: str):
        return evaluate(b+word+b, 1, s, 1)

    def evaluate(word: str, head_position: int, state: chr, iter_num:int) -> str:
        if word[0] != b or head_position < 0:
            evaluate(b + word, head_position + 1, state, iter_num)
        if word[-1] != b or head_position >= len(word):
            evaluate(word + b, head_position, state, iter_num)
        print(f'w: {word[:head_position]}|{word[head_position]}|{word[head_position+1:]}')
        (new_char, new_state, direction) = delta_fn(word[head_position], state)
        if new_state == "q_i" or iter_num > max_iter:
            return "Rejected"
        if new_state in f:
            return "Accepted"
        return evaluate(word[:head_position] + new_char + word[head_position+1:],
                        head_position + direction,
                        new_state,
                        iter_num + 1)


    if reduce(or_function, (k not in gamma for k, v in delta.keys())):
        raise Exception('char in delta is not in sigma')
    return evaluate_word

if __name__ == "__main__":

# Lenguaje = {w | w = bbbb aaa bbb ab ab ab a}
# M = {Sigma, Gamma, Q, F, s, b}
# Sigma = {a, b}
# Gamma = {a, b, @}
# Q = {s, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17}
# s = s
# F = {s, q17}
# b = @

# Estructura
#(Caracter, Estado) : (CaracterReemplazado, TransicionEstado, Direccion)
    MT = {('a', 's') : ('a', 'No', 0),
          ('b', 's') : ('@', 'q1', 1), #B
          ('@', 's') : ('@', 'No', 0),

          ('a', 'q1') : ('a', 'No', 0),
          ('b', 'q1') : ('@', 'q2', 1), #B
          ('@', 'q1') : ('@', 'No', 0),

          ('a', 'q2') : ('a', 'No', 0),
          ('b', 'q2') : ('@', 'q3', 1), #B
          ('@', 'q2') : ('@', 'No', 0),

          ('a', 'q3') : ('a', 'No', 0),
          ('b', 'q3') : ('@', 'q4', 1), #B
          ('@', 'q3') : ('@', 'No', 0),

          # AAA
          ('a', 'q4') : ('@', 'q5', 1), #A
          ('b', 'q4') : ('b', 'No', 0),
          ('@', 'q4') : ('@', 'No', 0),

          ('a', 'q5') : ('@', 'q6', 1), #A
          ('b', 'q5') : ('b', 'No', 0),
          ('@', 'q5') : ('@', 'No', 0),

          ('a', 'q6') : ('@', 'q7', 1), #A
          ('b', 'q6') : ('b', 'No', 0),
          ('@', 'q6') : ('@', 'No', 0),

          # BBB
          ('a', 'q7') : ('a', 'No', 0),
          ('b', 'q7') : ('@', 'q8', 1), #B
          ('@', 'q7') : ('@', 'No', 0),

          ('a', 'q8') : ('a', 'No', 0),
          ('b', 'q8') : ('@', 'q9', 1), #B
          ('@', 'q8') : ('@', 'No', 0),

          ('a', 'q9') : ('a', 'No', 0),
          ('b', 'q9') : ('@', 'q10', 1), #B
          ('@', 'q9') : ('@', 'No', 0),

          # AB
          ('a', 'q10') : ('a', 'q11', 1), #A
          ('b', 'q10') : ('b', 'No', 0),
          ('@', 'q10') : ('@', 'No', 0),

          ('a', 'q11') : ('a', 'No', 0),
          ('b', 'q11') : ('@', 'q12', 1), #B
          ('@', 'q11') : ('@', 'No', 0),

          # AB
          ('a', 'q12') : ('a', 'q13', 1), #A
          ('b', 'q12') : ('b', 'No', 0),
          ('@', 'q12') : ('@', 'No', 0),

          ('a', 'q13') : ('a', 'No', 0),
          ('b', 'q13') : ('@', 'q14', 1), #B
          ('@', 'q13') : ('@', 'No', 0),

          # AB
          ('a', 'q14') : ('a', 'q15', 1), #A
          ('b', 'q14') : ('b', 'No', 0),
          ('@', 'q14') : ('@', 'No', 0),

          ('a', 'q15') : ('a', 'No', 0),
          ('b', 'q15') : ('@', 'q16', 1), #B
          ('@', 'q15') : ('@', 'No', 0),

          # A
          ('a', 'q16') : ('a', 'Si', 1), #A
          ('b', 'q16') : ('b', 'No', 0),
          ('@', 'q16') : ('@', 'No', 0)
          }

    stri = 'bbbbaaabbbabababa' #CADENA A PROBAR
    sigma = {'a','b'}
    b = '@'
    gamma = {b} | sigma
    f = {'Si'}
    s = 's'

    tm = turing_machine(sigma,gamma,b,MT,f,s)
    result = tm(stri)
    print(result)
