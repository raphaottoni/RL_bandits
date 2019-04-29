import argparse
import numpy as np

class Bandit:
    """
    This class implement a multi-armed bandit object

    """

    def __init__(self, means, STDs, stationary = True, uses_mean_before_change = 30, seed = 42):
        '''
        Class constructor

        Args:

            means (list of floats): list of all arms reward means (gaussian modeling)

            STDs (list of floats): list of all arms standard deviations (Gaussian modeling)

            Statitionary (Boolean): Either or not the gaussian modelings will be stationary or the means will change

            uses_before_change (integer): The mean of how many times the arm will be used before its gaussian reward modeling change.

            seed (integer):  seed used for random processes.
        '''

        self.means = means
        self.STDs  = STDs
        self.stationary = stationary
        self.uses_mean_before_change = uses_mean_before_change
        
    def __str__ (self):
        '''
        Class wrapper for print

        '''
        number_of_arms = len(self.means)
        arms_type = "statinary" if self.stationary else "static"

        return "Mult-armed bandit with " + str(number_of_arms) + " "  + arms_type  +  " arms.\n" +\
               "Reward_means = " + str(self.means) +  "\n" +\
               "Rewards_stds = " + str(self.STDs) + "\n" +\
               "Arm mean uses before change reward mean = " + str(self.uses_mean_before_change) + "\n"

def main():
    '''
     Main function to run Data Preparation as a standalone script.
     '''

    # Argument Parser
    parser = argparse.ArgumentParser(description='Data spark.')

    parser.add_argument('-ms', '--means', type=float, nargs='+', required=True,
                        help="list of all arms reward means")
    parser.add_argument('-stds', '--stand_deviations', type=float, nargs='+', required=True,
                        help="list of all arms standard deviations")
    parser.add_argument('-s', '--stationary', action='store_true',
                        help="if set true, the mean rewards of each arm will change over usage.")
    parser.add_argument('-umbc', '--uses_mean_before_change', type=int,
                        help="The mean number of times a arm will be used before change its reward function", default = 30)

    # initialize parser
    args = parser.parse_args()

    bandit = Bandit(args.means, args.stand_deviations, args.stationary, args.uses_mean_before_change)
    print(bandit)





if __name__ == '__main__':
    main()
