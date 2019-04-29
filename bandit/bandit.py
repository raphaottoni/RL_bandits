import argparse
import numpy as np

class Bandit:
    """
    This class implement a multi-armed bandit object

    """

    def __init__(self, means, STDs, stationary = True, uses_before_change = 30, seed = 42):
        '''
        Class constructor

        Args:

            means (list of double): list of all arms rewards means (gaussian modeling)

            STDs (list of double): list of all arms standard deviations (Gaussian modeling)

            Statitionary (Boolean): Either or not the gaussian modelings will be stationary or the means will change

            uses_before_change (integer): The mean of how many times the arm will be used before its gaussian reward modeling change.

            seed (integer):  seed used for random processes.
        '''

        self.original_means = means
        self.STDs  = STDs
        self.stationary = stationary
        self.uses_before_change = uses_before_change
        



def main():
    '''
     Main function to run Data Preparation as a standalone script.
     '''

    # Argument Parser
    parser = argparse.ArgumentParser(description='Data spark.')

    parser.add_argument('-ms', '--means', type=int, nargs='+', required=True,
                        help="The path where the two datasets (elasticity and training) will be stored.")
    # initialize parser
    args = parser.parse_args()

    print(args)




if __name__ == '__main__':
    main()
