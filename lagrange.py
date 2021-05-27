def lagrange(x0, x):
    """
    Compute the Lagrange basis at the nodes `x` and evaluate each basis function
    at `x0`. The lagrange basis satsifies the property: 
    L_i(x_j) = 0 if i != j and L_i(x_j) = 1 if i = j.
    
    Args:
        x0 : Point to evalute basis functions at.
        x : Nodes to construct basis functions at.
    
    Returns:
        L : Lagrange basis (array of the same length as `x`). 
    """
    import numpy as np

    if len(x) == 1:
        return [1.0]

    n = len(x)
    L = np.zeros((n,))
    l = node_polynomial(x0, x)
    for j in range(n):
            L[j] = lagrange_basis(x0, j, x, l)
    
    return L

def node_polynomial(x0, x):
    # Compute node polynomial
    l = 1.0;
    n = len(x)
    for i in range(n):
            l = l*(x[i] - x0)
    return l

def lagrange_basis(x0, j, x, l):
     # Compute a lagrange basis function L_j at node `x_j` and evaluate it at 
     # `x0`
     import numpy as np
     n = len(x)
     lj = 1.0
     denom = 1.0

     if abs(x[j] - x0) < 1e-12:
        return lj;

     for k in range(n):
         if j == k:
            continue
         denom = denom*(x[j] - x[k])
     

     lam = 1.0/denom
     lj = l*lam/(x0 - x[j])

     return lj
