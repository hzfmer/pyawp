import sympy as sp

def covariant_basis(x, r):
    """
    Compute covariant basis vectors. 

    Arguments:
        x : List of mappings of physical coordinates to parameter coordinates
        r : List of parameter coordinates.

    Returns:
        a : Covariant basis (list of vectors). For example, `a[0]` gives the
            first covariant basis vector.
    """
    a1 = [sp.diff(xi,r[0]) for xi in x]
    a2 = [sp.diff(xi,r[1]) for xi in x]
    a3 = [sp.diff(xi,r[2]) for xi in x]
    return a1, a2, a3

def jacobian_matrix(a1,a2,a3):
    """
    Return the Jacobian matrix.

    """
    J = sp.Matrix([a1,a2,a3])
    return J

def contravariant_basis(J, a):
    """
    Compute contravariant basis vectors
    
    Arguments:
        J : Determinant of Jacobian
        a : Covariant basis (list of basis vectors)

    Returns:
        b : Contravariant basis (list of vectors). For example, `b[0]` gives the
            first contravariant basis vector.

    """
    return [a[1].cross(a[2])/J, a[2].cross(a[0])/J, a[0].cross(a[1])/J]

def metric_tensor(a):
    """
    Compute the metric tensor. Whether it is covariant or contravariant metric
    tensor depends which basis vectors are passed into this function.

    Arguments:
        a : Either the covariant or contravariant basis vectors.

    Returns:
        G : A symmetric and positive definite matrix `G[i,j]`.
    """
    m = len(a)
    G = sp.zeros(m,m)
    for i in range(m):
        for j in range(m):
            G[i,j] = a[i].dot(a[j])
    return G

def metrics(x, r, eval_J=0):
    """
    Compute metric coefficients for a mapping given physical coordinates `x` and
    parameter coordinates `r`.  
    
    To use, specify x = [x1, x2, x3] for each xi, as a
    function of each ri, i.e., `x1 = f(r1,r2,r3)`, etc.


    Example:
    >> import sympy as sp
    >> f = sp.Function('f')(r1,r2)
    >> x1 = f

    Returns:
        a : Covariant basis vectors
        b : Contravariant basis vectors
        Jmat : Jacobian matrix
        J : Determinant of Jacobian matrix

    """
    a1, a2, a3 = covariant_basis(x, r)
    Jmat = jacobian_matrix(a1,a2,a3)
    J = Jmat.det()
    a = [sp.Matrix(ai) for ai in [a1, a2, a3]]
    if eval_J:
        b = contravariant_basis(J, a)
    else:
        b = contravariant_basis(sp.symbols('J'), a)
    Ga = metric_tensor(a)
    Gb = metric_tensor(b)
    return a, b, Ga, Gb, Jmat, J 

def christoffel(a, b, r):
    """
    Compute the Christoffel symbols:

    \Gamma^k_{ij} = a^k \cdot \frac{\partial a_i}{\partial r^j}

    Input arguments:
        a : Covariant basis vectors
        b : Contravariant basis vectors
        r : Coordinates

    Returns:
        Gam : Christoffel symbols as an array of matrices. Symbol is defined as
                `Gam[k][i,j]`.
        Gamsym : `Gam

    """
    m = len(a)

    Gam = [0]*m
    for k in range(m):
        Gam[k] = sp.zeros(m)
        for i in range(m):
            for j in range(m):
                Gam[k][i,j] = b[k].dot([sp.diff(a[i][l], r[j]) \
                                        for l in range(m)]) 
    return Gam

