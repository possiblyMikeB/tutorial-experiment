import sys, hashlib, os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# initial mass for each of the three bodies
M0 = np.array([
    0.8, 
    1.1, 
    1.0
])

# initial momenta ...
P0 = np.array([
   [0.0, 0.0],
   [0.0, 0.0],
   [0.0, 0.0]
])

# initial positions ...
R0 = None

# rhs of autonomous ODE system
def three_body_ode(t, s):
    """
    Name: threebody_ode_sys
    Synop: 
        calculates the instantaneous values of the time-derivative
      of state variables for a system of three bodies only 
      under the influence of non-rel gravity in 2D. 
    Assumption: 
       s[0:6] code the position of the bodies 
       s[6:12] code the momenta ...
       s[12:15] code the masses ...
    """
    r12=np.sqrt((s[0]-s[2])**2 + (s[1]-s[3])**2)**3
    r13=np.sqrt((s[0]-s[4])**2 + (s[1]-s[5])**2)**3
    r23=np.sqrt((s[2]-s[4])**2 + (s[3]-s[5])**2)**3
    return [
        s[6+0]/s[12+0],
        s[6+1]/s[12+0],
        s[6+2]/s[12+1],
        s[6+3]/s[12+1],
        s[6+4]/s[12+2],
        s[6+5]/s[12+2],
        - s[12+1]*(s[0]-s[2])/r12 - s[12+2]*(s[0]-s[4])/r13,
        - s[12+1]*(s[1]-s[3])/r12 - s[12+2]*(s[1]-s[5])/r13,
        - s[12+0]*(s[2]-s[0])/r12 - s[12+2]*(s[2]-s[4])/r23,
        - s[12+0]*(s[3]-s[1])/r12 - s[12+2]*(s[3]-s[5])/r23,
        - s[12+0]*(s[4]-s[0])/r13 - s[12+1]*(s[4]-s[2])/r23,
        - s[12+0]*(s[5]-s[1])/r13 - s[12+1]*(s[5]-s[3])/r23,
        0.0,
        0.0,
        0.0
    ]


def solve(r0=R0, p0=P0, m0=M0, t_max=50.0, t_delta=0.001):
    """
    Name: solve
    Synop:
      assemble initial conditions and return approximate 
     solution to ODE system.
    """
    # holds initial ODE-system state
    s0 = np.zeros(15)
    
    # assign initial masses 
    s0[12:15] = m0
    # initial momenta ...
    s0[6:12] = p0.flatten()
    # initial positions ... 
    s0[0:6] = r0.flatten()
    
    # assemble simple t-mesh
    t_eval = np.arange(0, t_max+t_delta, t_delta)
    
    # compute & return apporximate solution to ODE sys on `t`-mesh
    sol = solve_ivp(
        three_body_ode, [0, t_max], s0, 
        t_eval=t_eval
    )
    
    return np.reshape(
        sol.y.T[:,:6],
        (sol.y.shape[-1], 3, 2)
    )


def main():
    # parse commandline arguments
    try: 
        R0 = np.array(list(map(float, sys.argv[1:])))
    except:
        print("ERROR: must provide exactly six floating point values"
              " as commandline arguments")
        return 1
    
    # solve three-body problem for given ICs
    sol = solve(R0)
    
    # generate plot showing evoluation of bodies
    plt.figure(figsize = (12, 8))
    plt.title(f'$R_0 = [{", ".join(sys.argv[1:])}]$')
    # trajectories
    for ii in range(3):
        plt.plot(sol[:, ii, 0], sol[:, ii, 1])
    
    # starting position
    plt.scatter(
        sol[0,:,0], sol[0,:,1], c='r', marker='+', s=30)
    
    plt.xlim([-2.5,2.5])
    plt.ylim([-2.5,2.5])
    plt.xlabel('x')
    plt.ylabel('y')
    
    # generate unique filename
    imgfile = hashlib.sha256(
        ','.join(sys.argv[1:]).encode('utf-8')
    ).hexdigest() + '.png'
    
    # save plot
    plt.savefig(os.path.join('imgs', imgfile))
    return 0

if __name__ == "__main__":
    sys.exit(main())
    pass
