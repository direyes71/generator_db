#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'diego'


import itertools
import json
from django.http import HttpResponse
from django.template.response import TemplateResponse


def home(request):
    #initialize()
    return TemplateResponse(
        request,
        'minimium_coating/home.html',
        {}
    )


def _load_data(request):
    # Load attributes
    attributes = request.POST['attributes']
    attributes = set(attributes)

    dependencies = request.POST['dependencies']
    dependencies = eval(dependencies)
    # Create instances
    functional_set = SetDF()
    # Load dependencies into set
    for item in dependencies:
        for key in item.iterkeys():
            functional_set.dfs.append(DF(key, item[key]))
    functional_set.attributes = attributes
    return functional_set


def calculate_minimium_coating(request):
    # Load dependencies
    functional_set = _load_data(request)
    # execute minimal_coating
    f_m = functional_set.minimal_coating()
    fm_list = []
    for i in f_m.dfs:
        fm_list.append(str(i))

    return HttpResponse(
        json.dumps({'data': fm_list, 'steps': functional_set.steps}),
        content_type='application/json',
    )


def calculate_candidate_keys(request):
    # Load dependencies
    functional_set = _load_data(request)
    # execute function to calculate candidate keys
    determinants = set()
    f_m = functional_set.minimal_coating()
    fm_list = []
    for i in f_m.dfs:
        fm_list.append(str(i))
        determinants.update(list(i.X))
    cand_keys_set = []

    for idx in range(1, len(determinants)):
        for det in itertools.combinations(determinants, idx):
            det = "".join(det)
            if functional_set.attributes == set(f_m.calculate_closing(det)):
                append = True
                det = set(list(det))
                for key in cand_keys_set:
                    if det.intersection(key) == key:
                        append = False
                if append:
                    cand_keys_set.append(set(list(det)))

    cand_keys = []
    for key in cand_keys_set:
        cand_keys.append("".join(key))

    return HttpResponse(
        json.dumps({'data': cand_keys, 'steps': functional_set.steps}),
        content_type='application/json',
    )


# Help methods
def joinNoDup(str1, str2):
    for i in str2:
        if i not in str1:
            str1 += i
    return str1

def AttrIsIn(s, a):
    count = 0
    for j in a:
        if j in s:
            count += 1
    if count == len(a):
        return True
    return False



class DF:
    """Functional dependency

        X -> Y (X determines Y)
    """
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.used = False

    def __repr__(self):
        return "%s -> %s" % (self.X, self.Y)

class SetDF:
    """Dependency function Set"""

    attributes = []

    def __init__(self, copyFrom=None):
        self.dfs = []
        if copyFrom is not None:
            for i in copyFrom.dfs:
                self.dfs.append(DF(i.X, i.Y))

    def calculate_closing(self, X):
        """Calculate X+ on the current function dependency set
        """
        Cl = X
        Clp = None
        for i in self.dfs:
            i.used = False

        while Cl != Clp:
            Clp = Cl
            for i in self.dfs:
                if i.used:
                    continue
                V = i.X
                W = i.Y
                if AttrIsIn(Cl, V):
                    Cl = joinNoDup(Cl, W)
                    i.used = True
        return Cl

    def delete_fd(self, df):
        """Extract one functional dependency of set"""
        for i in self.dfs:
            if i.X == df.X and i.Y == df.Y:
                self.dfs.remove(i)

    def minimal_coating(self):
        """calculate of minimal coating"""
        self.steps = [u'<h3>Pasos desarrollados para el cálculo</h3>']
        self.steps.append('1 - Simplifica los implicados')
        self.steps.append('<br />')
        # Step 0
        F0 = SetDF(self)

        # Step 1
        F1 = SetDF()
        for i in F0.dfs:
            if len(i.Y) > 1:
                for j in i.Y:
                    F1.dfs.append(DF(i.X, j))
                    self.steps.append(str(DF(i.X, j)))
            else:
                F1.dfs.append(i)
                self.steps.append(str(i))

        self.steps.append('<br />')

        # Step 2
        F2 = SetDF(F1)
        for i in F1.dfs:
            Z = i.X
            for B in i.X:
                c1 = F1.calculate_closing(Z.replace(B, ""))
                if i.Y in c1:
                    Ft = SetDF(F2)
                    Ft.delete_fd(DF(Z, i.Y))
                    self.steps.append('Elimina ' + Z + ' ' + str(i.Y))
                    Ft.delete_fd(DF(Z.replace(B, ""), i.Y))
                    self.steps.append('Elimina ' + Z.replace(B, "") + ' ' + str(i.Y))
                    c2 = Ft.calculate_closing(Z.replace(B, ""))
                    # Add to step
                    if Z.replace(B, "") and not (Z.replace(B, "") + '+ = ' + c2) in self.steps:
                        self.steps.append('Calcula' + ' ' + Z.replace(B, "") + '+ = ' + c2)
                    if i.Y in c2:
                        Z = Z.replace(B, "")

            i.X = Z

        # Step 3
        Fm = SetDF(F2)
        for i in F2.dfs:
            G = SetDF(Fm)
            G.delete_fd(i)
            self.steps.append('Elimina ' + ' ' + str(i))
            c = G.calculate_closing(i.X)
            if AttrIsIn(c, i.Y):
                Fm = G
                # Add to step
                if not (str(i.X) + '+ = ' + c) in self.steps:
                    self.steps.append('Calcula' + ' ' + str(i.X) + '+ = ' + c)

        return Fm


def initialize(dependencies):
    dependencies = eval(dependencies)
    functional_set = SetDF()
    for item in dependencies:
        for key in item.iterkeys():
            functional_set.dfs.append(DF(key, item[key]))

    f_m = functional_set.minimal_coating()
    fm_list = []
    for i in f_m.dfs:
        fm_list.append(i)
        print type(i)

    '''
    # Teste de Calculo de Clausuras
    print "Inicializando ...."
    F = SetDF()
    F.dfs.append(DF("AB", "C"))
    F.dfs.append(DF("C", "A"))
    F.dfs.append(DF("BC", "D"))
    F.dfs.append(DF("ACD", "B"))
    F.dfs.append(DF("D", "EG"))
    F.dfs.append(DF("BE", "C"))
    F.dfs.append(DF("CG", "BD"))
    F.dfs.append(DF("CE", "AG"))

    print
    print "Calculando algunas clausuras de muestra"
    print "B+  =", F.calculate_closing("B")
    print "A+  =", F.calculate_closing("A")
    print "C+  =", F.calculate_closing("C")
    print "CD+ =", F.calculate_closing("CD")
    print "D+  =", F.calculate_closing("D")

    print
    print "Dependencias Funcionales"
    for i in F.dfs:
        print i

    print
    print "Cubrimiento Minimal"
    Fm = F.CubrimientoMinimal()
    for i in Fm.dfs:
        print i
    '''
