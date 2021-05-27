import pyawp
import sympy as sp

def test_str_eqs():
    x, y = sp.symbols('x y')

    l = [y]
    r = [x]

    out = pyawp.str_eqs(l, r)
    assert out == 'y =&  x '
    r = [x + x**2]
    out = pyawp.str_eqs(l, r, terms_per_line=1)
    assert r'y =&  x  \\' in out

def test_str_tensor_eqs():
    mat = lambda sym : sp.Matrix([[sp.symbols('%s%d%d'%(sym,i,j))  \
                                   for i in range(2)] for j in range(2)])

    A = mat('a')
    B = mat('b')
    sp.pprint(A)
    out = pyawp.str_tensor_eqs(A, B)
    assert r'a_{00} =&  b_{00} \\a_{10} =&  b_{10}' in out

    B = B + B**2
    out = pyawp.str_tensor_eqs(A, B, terms_per_line=2)
    assert r'a_{00} =&  b_{00}  + b_{00}^{2}' in out

    B = mat('b')
    out = pyawp.str_tensor_eqs(A, B, terms_per_line=2, symmetric=True)
    assert r'b_{01}' not in out
