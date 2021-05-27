"""

Module for handling SGTs (strain Green tensor's) and reciprocity

"""

def stresses_to_strains(sxx, syy, szz, sxy, sxz, syz, lami, mui):
    """
    Convert stresses sij to strains eij 

    Args:
        sxx ... syz: Stress tensor components, np.array of size nt x nr (nt =
            number of timesteps, nr = number of outputs) 
        lami: 1 / Lame`s first parameter, np.array of size 1 x nr,
        mui: 1 / shear modulus, np.array of size 1 x nr,

    Returns:
        exx ... eyz: Strain tensor components, of same size as the stress
            components.

    """

    lam = 1.0 / lami

    trace = sxx + syy + szz

    alpha = 0.5 * mui * lam / (3 * lam + 2.0 / mui)

    exx = 0.5 * mui * sxx - alpha * trace
    eyy = 0.5 * mui * syy - alpha * trace
    ezz = 0.5 * mui * szz - alpha * trace
    exy = 0.5 * mui * sxy
    exz = 0.5 * mui * sxz
    eyz = 0.5 * mui * syz
  
    return exx, eyy, ezz, exy, exz, eyz

def strains_to_stresses(exx, eyy, ezz, exy, exz, eyz, lam, mu):
    """
    Convert strains eij to stresses sij

    Args:
        exx .. eyz : Strain tensor components
        lam: Lame`s first parameter
        mu: shear modulus

    """

    trace = exx + eyy + ezz

    sxx = lam * trace + 2 * mu * exx
    syy = lam * trace + 2 * mu * eyy
    szz = lam * trace + 2 * mu * ezz
    sxy = 2 * mu * exy
    sxz = 2 * mu * exz
    syz = 2 * mu * eyz

    return sxx, syy, szz, sxy, sxz, syz

def compute_velocity(mij, Gij):
    """

    Determine the velocity field from the moment tensor components mij and
    strain Green's tensor. The specific velocity component is tied to the
    direction of the point force is used initialize the simulation.

    Args:
        mij: List of Moment tensor components in Voigt notation (see Notes)
        Gij: List of Moment tensor components in Voigt notation (see Notes)


    Notes:
        In Voigt notation, the symmetric tensor components are stacked as:
            xx, yy, zz, xy, xz, yz.

    """

    return  (mij[0] * Gij[0] + mij[1] * Gij[1] + mij[2] * Gij[2]
          +  2 * mij[3] * Gij[3] + 2 * mij[4] * Gij[4] + 2 * mij[5] * Gij[5])
