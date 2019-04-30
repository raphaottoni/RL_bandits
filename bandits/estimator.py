import argparse
import numpy as np
from collections import defaultdict
from bandits.bandit import Bandit

class Estimator:
    """
    This class implement a estimator to track the distribution of each bandit arm used

    """

    def __init__(self, n_arms = 10, non_stationary_arms = False, initial_values = 0.0, step_size = 0.1):
        '''
        Class constructor

        Args:

            n_arms (integer): How many arms it will track

            non_stationary_arms (Boolean): if False the estimator will consider that all arms have a fixed gaussian distribution of reward.

            initial_values (float): the initial mean value of each arm. Default: 0.0

            step_size (Boolean): the ratio wich the new rewards will be pondered higher than the old ones. It is only used when <stationary_arms> is False.

        '''

        if n_arms <= 0:
            raise Exception("[Estimator] The number of arms cannot be negative or zero. The <n_arms> passed to constructor was {}".format(n_arms))
    
        # Set the tracking variables
        self.n_arms  = n_arms
        self.stationary = False if non_stationary_arms else True
        self.step_size = step_size
        self.arms_uses = n_arms * [0]
        self.current_estimations_each_arm =  n_arms * [initial_values]
        
    def __str__ (self):
        '''
        Class wrapper for print

        '''
        arms_type = "STATIONARY" if self.stationary else "NON-STATIONARY"

        return "Estimator tracking " + str(self.n_arms) + " "  + arms_type  +  " arms.\n" +\
               "Current mean estimation for each arm = " + str(self.current_estimations_each_arm) +  "\n" +\
               "Current uses of each arm = " + str(self.arms_uses) +  "\n"

    def arm_pull(self, arm_id, reward):
        '''
        This function recieves the data from one bandit arm pull and updates the current estimation of that arm
        '''
    
        # Verify if nature of the arm, if it is stationary or not
        if self.stationary:

            # save the information that the arm was pulled
            self.arms_uses[arm_id] += 1

            # Estimate the new mean of the arm
            self.current_estimations_each_arm[arm_id] = self.current_estimations_each_arm[arm_id] + (reward - self.current_estimations_each_arm[arm_id])/self.arms_uses[arm_id]
        else:

            # save the information that the arm was pulled
            self.arms_uses[arm_id] += 1

            # estimate the new mean of the arm
            self.current_estimations_each_arm[arm_id] = self.current_estimations_each_arm[arm_id] + self.step_size * (reward - self.current_estimations_each_arm[arm_id])


def main():
    '''
    Main 
    '''

    # Argument Parser
    parser = argparse.ArgumentParser(description='Tracking estimator for each bandit arm\' mean.')

    parser.add_argument('-n', '--n_arms', type=int, required=True,
                        help="the number of arms the estimator will track")
    parser.add_argument('-ns', '--non-stationary', action='store_true',
                        help="if set true, the mean rewards of each arm will change over usage.")

    # initialize parser
    args = parser.parse_args()

    bandit = Bandit([10,8], [4,2], args.non_stationary)
    estimator = Estimator(args.n_arms, args.non_stationary)

    print(bandit)
    print(estimator)

    for i in range(100000):
        estimator.arm_pull(0,bandit.pull_arm(0))
    print(bandit)
    print(estimator)


if __name__ == '__main__':
    main()
