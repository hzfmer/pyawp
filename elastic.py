import sympy as sp


def velocities(x, t, sub='_'):
    """
    Returns the velocity vector v(x, t) (a matrix is returned)
    """
    return sp.Matrix([sp.Function('v%s%d'%(sub,i))(*x, t) for i in range(1,
                      len(x) + 1)])

def stress(x, t, sub='_', sym=True):
    """
    Returns the stress tensor s(x, t) (a matrix is returned)

    Optional arguments:
        sym : If true, then the stress tensor is symmetric.  
    """
    m = len(x)
    S = sp.zeros(m, m)
    for i in range(m):
        for j in range(m):
            S[i,j] = sp.Function('sigma%s%d%d'%(sub,i+1,j+1))(*x, t)
            if sym:
                S[j,i] = S[i,j]
    return S

def material(x=None):
    """
    Return isotropic elastic material parameters: rho, mu, lam

    """
    if not x:
        return sp.symbols('rho mu lambda')
    rho = Field('rho')(*x)
    mu = Field('mu')(*x)
    lam = Field('lambda')(*x)
    return rho, mu, lam

def vel_cart(v, s, rho, x, t):
    """
    Return velocity update equations (momentum balance) for Cartesian
    coordinates
    """
    m = len(v)
    lhs = [0]*m
    rhs = [0]*m
    for i in range(m):
        lhs[i] = rho*sp.diff(v[i],t)
        rhs[i] = sum([sp.diff(s[i,j], x[j]) for j in range(m)])
    return lhs, rhs

def vel_curved(v, s, rho, J, b, r, t):
    """
    Return velocity update equations (momentum balance) for curvilinear
    coordinates.
    """
    m = len(v)
    lhs = [0]*m
    rhs = [0]*m
    for i in range(m):
        lhs[i] = rho*sp.Derivative(v[i],t)
        rhs[i] = 1/J*sum([sp.Derivative(
                          sum([J*b[j][k]*s[i,k] for k in range(m)])
                          , r[j]) for j in range(m)])
    return lhs, rhs

def vel_covariant(v, s, rho, J, b, Gam, r, t):
    """
    Return velocity update equations (momentum balance) in covariant form.
    """
    m = len(v)
    lhs = [0]*m
    rhs = [0]*m
    for i in range(m):
        lhs[i] = rho*sp.Derivative(v[i],t)
        rhs[i] = 1/J*sum([sp.Derivative(J*s[i,j], r[j]) for j in range(m)]) \
                + sum([Gam[i][k,l]*s[k,l] for k in range(m) for l in range(m)]) 
    return lhs, rhs



def stress_cart(v, s, lam, mu, x, t):
    """
    Return stress update equations (Hooke's law) in Cartesian coordinates.
    """
    m = len(v)
    lhs = sp.zeros(m,m)
    rhs = sp.zeros(m,m)
    delta = sp.eye(m)
    for i in range(m):
        for j in range(m):
            lhs[i,j] = sp.diff(s[i,j],t)
            rhs[i,j] = lam*sum([sp.diff(v[k],x[k]) for k in range(m)])*delta[i,j]\
                    + mu*(sp.diff(v[i],x[j]) + sp.diff(v[j],x[i]))
    return lhs, rhs

def stress_curved(v, s, lam, mu, b, r, t):
    """
    Return stress update equations (Hooke's law) in curvilinear coordinates.
    """
    m = len(v)
    lhs = sp.zeros(m,m)
    rhs = sp.zeros(m,m)
    delta = sp.eye(m)
    for i in range(m):
        for j in range(m):
            lhs[i,j] = sp.diff(s[i,j],t)
            rhs[i,j] = lam*sum([sp.diff(v[k],r[l])*b[l][k] for k in range(m)   \
                                                           for l in range(m)]) \
                          *delta[i,j]                                          \
                    + mu*(sum([sp.diff(v[i],r[n])*b[n][j] for n in range(m)])  \
                        + sum([sp.diff(v[j],r[n])*b[n][i] for n in range(m)]))
    return lhs, rhs

def stress_covariant(v, s, lam, mu, Gb, Gam, r, t):
    """
    Return stress update equations (Hooke's law) in covariant form.
    """
    m = len(v)
    lhs = sp.zeros(m,m)
    rhs = sp.zeros(m,m)
    delta = sp.eye(m)
    for i in range(m):
        for j in range(m):
            lhs[i,j] = sp.diff(s[i,j],t)
            cov_k = lambda a : sum([sp.diff(a[k], r[k]) for k in range(m)]\
                                      + [Gam[k][k,l]*a[l] for k in range(m)\
                                                          for l in range(m)])

            cov = lambda a, p, q : sp.diff(a[p], r[q]) + \
                                      sum([Gam[p][q,k]*a[k] for k in range(m)])
            con = lambda a, p, q : sum([Gb[q,k]*cov(a,p,k) for k in range(m)]) 
            rhs[i,j] = lam*cov_k(v)*delta[i,j] + mu*con(v,i,j) + \
                                                 mu*con(v,j,i)
    return lhs, rhs







