from collections import Counter
from typing import List

from azure.quantum.optimization import Term

def tSimplify ( terms0 : List [ Term ] ) -> List [ Term ] :
    terms = []
    
    for term in terms0 :
        combined = False
        term.ids.sort()

        for t in terms :
            if t.ids == term.ids :
                t.c += term.c
                combined = True
                break

        if not combined :
            terms.append ( term )

    for t in terms :
        if t.c == 0 :
            terms.remove ( t )

    return ( terms )

def tAdd ( terms0 : List [ Term ] , terms1 : List [ Term ] ) -> List [ Term ] :
    return tSimplify ( terms0 + terms1 )
  
def tSubtract ( terms0 : List [ Term ] , terms1 : List [ Term ] ) -> List [ Term ] :
    terms = []
    for term0 in terms0 :
        terms.append( Term ( c = term0.c , indices = term0.ids ) )

    for term1 in terms1 :
        terms.append ( Term ( c = -1 * term1.c , indices = term1.ids ) )

    return tSimplify ( terms )

def tMultiply ( terms0 : List [ Term ] , terms1 : List [ Term ] ) -> List [ Term ] :
    terms = []
    for term0 in terms0 :
        for term1 in terms1 :
            terms.append ( Term ( c =  term0.c * term1.c , indices = term0.ids + term1.ids ) )
    return tSimplify ( terms )

def tSquare ( terms0 : List [ Term ] ) -> List [ Term ] :
    return ( tMultiply ( terms0 , terms0 ) )

def tFixPre ( terms0 : List  [ Term ] , fix : dict ) -> List [ Term ] :
    terms = []
    for term in terms0 :
        for index , value in fix.items () :
            if index in term.ids :
                if value > 0 :
                    while index in term.ids : 
                        term.ids.remove ( index )
                    terms.append ( term )
            else :
                terms.append ( term )
    return terms 

def tFixPost ( result : dict , fix : dict ) -> dict :
    r = result
    for index , value in fix.items () :
        r [ str ( index ) ] = value
    return r

def tFindIndex ( terms0 : List  [ Term ] , fix : dict ) :
    for term in terms0 :
        for index , value in fix.items () :
            if index in term.ids :
                print ( term , end ='' )
    print ( '*' )