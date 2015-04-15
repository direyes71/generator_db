#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'diego'


# Author: Hong Lu, programming.luhong.org
# Licience: GPL

# variable name: stands for, what it is
# S: schema, tuple(R,F)
# R: relation, set of attributes
# F/G: functional dependencies, list of f/g
# f: functional dependency, tuple (L,R)
# L/R: left/right hand side of f, set of attributes
# K: key, set of attributes

from copy import copy,deepcopy

def canonicalize(F):
    # it'd be interesting to compare the following nested list comprehension with value accumulation constructs in lisp's for loop
    return [(L,r) for L,R in F for r in R]

def decanonicalize(F):
    F = deepcopy(F)
    dict = {}
    # frozenset turns L into immutable object
    for L,r in F: dict[frozenset(L)] = set()
    for L,r in F: dict[frozenset(L)].add(r)
    return [(set(L),R) for L,R in dict.items()]

# closure of set A of attributes wrt canonicalized dependencies F
def closure(A,F):
    C = copy(A)
    while 1:
        size1 = len(C)
        for (L,r) in F:
            if L <= C and r not in C: # <=: is subset
                C.add(r)
        size2 = len(C)
        if size1==size2: break;
    return C

# decide if canonicalized F entails f
def entail(F, f):
    L,r = f
    if r in closure(L,F): return True
    else: return False

# python's set/list only supports destructive remove, sucks
def removed(A,a):
    A = copy(A)
    A.remove(a)
    return A

# decide if K is a candidate key of a given schema
def is_key(K,S):
    R,F = S
    C = closure(K,canonicalize(F))
    if R <= C: return True
    else: return False

# find a candidate key given schema S
def candidate_key(S):
    R,F = S
    K = copy(R)
    while 1:
        size1 = len(K)
        for a in copy(K):
            if is_key(removed(K,a),S):
                K.remove(a)
        size2 = len(K)
        if size1==size2: break
    return K

# rr1 and rr2 remove redundancies given canonicalized F
def rr1(F):
    F = deepcopy(F)
    while 1:
        size1 = sum([len(L) for L,r in F])
        for L,r in F:
            for l in copy(L):
                if entail(F,(removed(L,l),l)):
                    L.remove(l)
        size2 = sum([len(L) for L,r in F])
        if size1==size2: break
    return F

def rr2(F):
    F = deepcopy(F)
    while 1:
        size1 = len(F)
        for f in copy(F):
            if entail(removed(F,f),f):
                F.remove(f)
        size2 = len(F)
        if size1==size2: break
    return F

# minimal_cover of canonicalized F
def minimal_cover(F):
    F = canonicalize(F)
    F = rr1(F)
    F = rr2(F)
    F = decanonicalize(F)
    return F

# the third normal form of scheme S
def nf3(S):
    R, F = S
    F = minimal_cover(F)
    RR = [left|right for (left,right) in F]
    for A in RR:
        if is_key(A, S): break
    else: # else clause rocks here
        K = candidate_key(S)
        RR.append(K)
        F.append((K,set()))
    return RR,F

# parse, tostr, test are only for testing purposes
def parse(S):
    def parsef(f):
        L,R = f.split('->')
        L = set([ord(l) for l in L])
        R = set([ord(r) for r in R])
        return (L,R)
    R, F = S
    F = copy(F)
    F = F.strip()
    F = F.replace(' ','')
    F = F.split(',')
    return (set([ord(a) for a in R]), [parsef(f) for f in F])

def tostr(F, RR):
    def f2str(f):
        L,R = f
        L = ''.join([chr(l) for l in L])
        R = ''.join([chr(r) for r in R])
        return L + '->' + R
    def R2str(R):
        # the fact that join is a string method instead of function sucks
        return ''.join([chr(a) for a in R])

    lR = [R2str(R) for R in RR]
    lf = [f2str(f) for f in F]
    return str(zip(lR,lf))

def test(R,F):
    S = (R,F)
    print "schema:", S
    S = parse(S)
    RR,F = nf3(S)
    print "3nf decomposition:", tostr(F, RR), "\n"
    return tostr(F, RR)