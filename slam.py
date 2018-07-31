import numpy as np
from helpers import make_data

# your implementation of slam should work with the following inputs
# feel free to change these input values and see how it responds!

# world parameters
num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world (square)

# robot parameters
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation


# make_data instantiates a robot, AND generates random landmarks for a given world size and number of landmarks
data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)


def initialize_constraints(N, num_landmarks, world_size):
    ''' This function takes in a number of time steps N, number of landmarks, and a world_size,
        and returns initialized constraint matrices, omega and xi.'''

    ## Recommended: Define and store the size (rows/cols) of the constraint matrix in a variable
    xy_dim = 2 + 2 * (N + num_landmarks)
    omega = np.zeros((xy_dim, xy_dim))
    xi = np.zeros((xy_dim, 1))

    ## TODO: Define the constraint matrix, Omega, with two initial "strength" values
    ## for the initial x, y location of our robot

    omega[0, 0] = 1  # x0=world_size/2
    omega[N + num_landmarks, 0] = 1  # y0=world_size/2

    ## TODO: Define the constraint *vector*, xi
    ## you can assume that the robot starts out in the middle of the world with 100% confidence
    xi[0] = world_size / 2  # x0=world_size/2
    xi[N + num_landmarks] = world_size / 2  # y0=world_size/2

    return omega, xi


## TODO: Complete the code to implement SLAM

## slam takes in 6 arguments and returns mu,
## mu is the entire path traversed by a robot (all x,y poses) *and* all landmarks locations
def slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise):
    ## TODO: Use your initilization to create constraint matrices, omega and xi
    initial_omega, initial_xi = initialize_constraints(N_test, num_landmarks_test, small_world)

    ## TODO: Iterate through each time step in the data
    ## get all the motion and measurement data as you iterate
    for time_step in range(N - 1):
        print(time_step)
        print('measurements: \n', data[time_step][0])
        print('motion: \n', data[time_step][1])

        ## TODO: update the constraint matrix/vector to account for all *measurements*
        ## this should be a series of additions that take into account the measurement noise
        # account for the first motion, dx = move1

        # Px(t) -> Px(t+1)
        px_t = 2 * time_step
        px_t1 = 3 * time_step

        omega[px_t, px_t] += 1
        omega[px_t, px_t1] += 1
        omega[px_t1, px_t] += -1
        omega[px_t1, px_t1] += 1

        # Py(t) -> Py(t+1)
        py_t = 2 * time_step + 1
        py_t1 = 3 * time_step + 1

        omega[py_t, py_t] += 1
        omega[py_t, py_t1] += 1
        omega[py_t1, py_t] += -1
        omega[py_t1, py_t1] += 1

        xi[2 * time_step] = data[time_step][1][0]
        xi[2 * time_step + 1] = data[time_step][1][1]

        ## TODO: update the constraint matrix/vector to account for all *motion* and motion noise

    ## TODO: After iterating through all the data
    ## Compute the best estimate of poses and landmark positions
    ## using the formula, omega_inverse * Xi
    mu = None

    return mu  # return `mu`


mu = slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)
