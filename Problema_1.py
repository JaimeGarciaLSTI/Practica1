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

# Lenguaje = {a^n b^m c^n-m | n,m>=0 y n>=m}
# M = {Sigma, Gamma, Q, F, s, B}
# Sigma = {a, b, c}
# Gamma = {a, b, c, @}
# Q = {s, q1, q2, q3, q4, q5}
# s = s
# F = {s}
# Beta = @

# Estructura
#(Caracter, Estado) : (CaracterReemplazado, TransicionEstado, Direccion)
    MT = {('a', 's') : ('@', 'q1', 1),
          ('b', 's') : ('b', 'No', 0),
          ('c', 's') : ('c', 'No', 0),
          ('@', 's') : ('@', 'Si', 0),
          
          ('a', 'q1') : ('a', 'q1', 1),
          ('b', 'q1') : ('a', 'q2', -1),
          ('c', 'q1') : ('a', 'q4', 1),
          ('@', 'q1') : ('@', 'No', 0),
          
          ('a', 'q2') : ('a', 'q2', -1),
          ('b', 'q2') : ('b', 'No', 0), 
          ('c', 'q2') : ('b', 'No', 0), 
          ('@', 'q2') : ('@', 'q3', 1),
          
          ('a', 'q3') : ('@', 's', 1),
          ('b', 'q3') : ('b', 'No', 0), 
          ('c', 'q3') : ('c', 'No', 0), 
          ('@', 'q3') : ('@', 'No', 0),

          ('a', 'q4') : ('a', 'No', 0),
          ('b', 'q4') : ('b', 'No', 0), 
          ('c', 'q4') : ('c', 'q4', 1), 
          ('@', 'q4') : ('@', 'q5', -1),

          ('a', 'q5') : ('a', 'q5', -1),
          ('b', 'q5') : ('b', 'No', 0), 
          ('c', 'q5') : ('c', 'q5', -1), 
          ('@', 'q5') : ('@', 'q3', 1),
          }

    stri = 'aabb' #CADENA A PROBAR
    sigma = {'a','b','c'}
    b = '@'
    gamma = {b} | sigma
    f = {'Si'}
    s = 's'

    tm = turing_machine(sigma,gamma,b,MT,f,s)
    result = tm(stri)
    print(result)
