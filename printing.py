import sympy
from sympy import Symbol
from sympy.printing.latex import LatexPrinter
from sympy.core.function import UndefinedFunction

class LatexPrinter2(LatexPrinter):
    """
    Overload the standard LatexPrinter to suppress displaying function arguments
    """
    def _print_Derivative(self, expr):
        function, *vars = expr.args
        if not isinstance(type(function), UndefinedFunction) \
        or not all(isinstance(i, Symbol) for i in vars):
            return super()._print_Derivative(expr)
        if len(expr.args[0].args) == 1:
            symbol = 'd'
        else:
            symbol = '\partial'

        return r'\frac{%s %s}{%s %s}' % \
                (symbol, self._print(Symbol(function.func.__name__)), \
                symbol,
                ' '.join([self._print(i) for i in vars]))
    def _print_Function(self, expr, *args, **kwargs):
        func = expr.func.__name__
        if hasattr(self, '_print_' + func):
            return getattr(self, '_print_' + func)(expr, exp)
        else:
            name = self._hprint_Function(func)
            return name
         
def latex(expr, settings=None):
    return LatexPrinter2(settings).doprint(expr)
 
def terms(lhs, expr,terms_per_line=1):
    """
    This function is written to handle displaying long latex equations.
    Modified implementation of: https://github.com/sympy/sympy/issues/3001
    """
    tex = r''
    terms = expr.as_ordered_terms()
    terms = sympy.Add.make_args(sympy.expand(expr))
    
    n_terms = len(terms)
    term_count = 1
    for i in range(n_terms):
        term = terms[i]
        term_start = r''
        term_end = r''
        sign = r'+'
        if term_count > terms_per_line:
            term_start = '&'
            term_count = 1
        if term_count == terms_per_line:
            term_end = r' \\'  + '\n'
        if term.as_ordered_factors()[0]==-1:
            term = -1*term
            sign = r'-'
        if i == 0: # beginning
            if sign == r'+': sign = r""
            tex += r'{:s} =& {:s} {:s} {:s}'.format(latex(lhs),
                                                     term_start,
                                                     latex(term),term_end)
        elif i == n_terms-1: # end
            tex += r'{:s} {:s} {:s} {:s}'.format(term_start,sign,latex(term),
                                                 term_end)
        else: # middle
            tex += r'{:s} {:s} {:s} {:s}'.format(term_start,sign,latex(term),
                                                 term_end)
        term_count += 1
    return tex

def str_eqs(eq_l, eq_r, terms_per_line=2):
    """
    Return a string of Latex-formatted equations that only contains n terms per
    line
    """
    out = []

    # Init terms for each line 
    try:
        len(terms_per_line)
    except:
        terms_per_line = [terms_per_line]*len(eq_l)

    for l, r, t in zip(eq_l, eq_r, terms_per_line):
        out.append(terms(l, r, terms_per_line=t))
    return r'\\'.join(out)

def str_tensor_eqs(eq_l, eq_r, terms_per_line=3, symmetric=False):
    """
    Return a string of Latex formatted equations suited for outputting symmetric
    tensors. 

    Input arguments:
        eq_l : Sympy Matrix that contains the left-hand side expression.
        eq_r : Sympy Matrix that contains the right-hand side expression.

    Optional arguments:
        terms_per_line : Number of terms to display on each line. Can be
        configured so that the number is different for each equation.

    """
    out = []

    # Init terms for each line 
    try:
        len(terms_per_line)
    except:
        terms_per_line = sympy.ones(eq_l.rows,eq_l.cols)*terms_per_line

    for i in range(eq_l.rows):
        if symmetric:
            start = i
        else:
            start = 0
        for j in range(start, eq_l.rows):
            out.append(terms(eq_l[i,j], eq_r[i,j],
                    terms_per_line=terms_per_line[i,j]))
    return r'\\'.join(out)

def christoffel(Gam, num_per_line=6):
    """
    Prepare Christoffel symbols for output by packing them into two arrays, lhs
    and rhs. Can then call for example `terms` to generate the latex output.
    """
    out = ''
    m = len(Gam)
    l = 1
    for k in range(m):
        for i in range(m):
            for j in range(i,m):
                out += '\Gamma^{%d}_{%d%d} &= %s & '%(k+1,i+1,j+1,\
                        latex(Gam[k][i,j]))
                if l % num_per_line == 0:
                    out += r'\\' + '\n'
                l += 1
    return out

def print_align(string, star=1, printit=1):
    if star:
        sym = '*'
    else:
        sym = ''
    out = r'\begin{align%s}'%sym + '\n' + string + r'\end{align%s}'%sym  + '\n'
    if printit:
        print(out)
    else:
        return out

def basis(a, symbol='a', sub='_'):
    out = ''
    for i, ai in enumerate(a):
        out += "\mathbf{%s}%s%d = %s"%(symbol,sub,i+1,latex(ai))
    return out

def matrix(G, symbol='G', sub='_', mattype='pmatrix'):
    out = ''
    m = G.rows
    out = '%s = \n'%symbol
    out += r'\begin{%s}'%mattype
    print(G)
    for i in range(m):
        out += '\n    '
        for j in range(m):
            print(i,j,G[i,j])
            latex(G[i,j])
            out += '%s &' % str((G[i,j]))
        out += r'\\'
    out += '\n' + r'\end{%s}'%mattype
    return out
