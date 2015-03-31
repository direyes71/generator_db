__author__ = 'diego'

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


def calculate_minimium_coating(request):
    dependencies = request.POST['dependencies']
    dependencies = eval(dependencies)
    functional_set = SetDF()
    for item in dependencies:
        for key in item.iterkeys():
            functional_set.dfs.append(DF(key, item[key]))

    f_m = functional_set.minimal_coating()
    fm_list = []
    for i in f_m.dfs:
        fm_list.append(str(i))
        print i
    return HttpResponse(
        json.dumps({'data': fm_list}),
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
        # Step 0
        F0 = SetDF(self)

        # Step 1
        F1 = SetDF()
        for i in F0.dfs:
            if len(i.Y) > 1:
                for j in i.Y:
                    F1.dfs.append(DF(i.X, j))
            else:
                F1.dfs.append(i)

        # Step 2
        F2 = SetDF(F1)
        for i in F1.dfs:
            Z = i.X
            for B in i.X:
                c1 = F1.calculate_closing(Z.replace(B, ""))
                if i.Y in c1:
                    Ft = SetDF(F2)
                    Ft.delete_fd(DF(Z, i.Y))
                    Ft.delete_fd(DF(Z.replace(B, ""), i.Y))
                    c2 = Ft.calculate_closing(Z.replace(B, ""))
                    if i.Y in c2:
                        Z = Z.replace(B, "")

            i.X = Z

        # Step 3
        Fm = SetDF(F2)
        for i in F2.dfs:
            G = SetDF(Fm)
            G.delete_fd(i)
            c = G.calculate_closing(i.X)
            if AttrIsIn(c, i.Y):
                Fm = G

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
