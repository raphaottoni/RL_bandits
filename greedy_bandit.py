import argparse
import numpy as np
from collections import defaultdict
from bandits.bandit import Bandit
from bandits.estimator import Estimator
import math
import random

class GreedyBandit:
    """
    This class implements the greedy solution for multi-armed Bandits

    """

    def __init__(self, n_arms = 10, non_stationary_arms = False, step_size = 0.1):
        '''
        Class constructor

        Args:

            n_arms (integer): How many arms it will track

            non_stationary_arms (Boolean): if False the estimator will consider that all arms have a fixed gaussian distribution of reward.

            step_size (Boolean): the ratio wich the new rewards will be pondered higher than the old ones. It is only used when <stationary_arms> is False.

        '''

        if n_arms <= 0:
            raise Exception("[GreedyBandit] The number of arms cannot be negative or zero. The <n_arms> passed to constructor was {}".format(n_arms))
    
        # Create the testbed mult-armed bandit
        arms_means = []
        arms_stds = []

        for i in range(n_arms):
            arms_means.append(np.random.normal(0,math.sqrt(1)))
            arms_stds.append(math.sqrt(1))

        # Create its Bandit and estimator
        self.bandit = Bandit(arms_means, arms_stds, non_stationary_arms)
        self.estimator = Estimator(n_arms, non_stationary_arms, 5.0)
        

    def apply_strategy(self, n_pulls = 1000):
        '''
        This function applies the basic greedy strategy for the mult-armed bandit
        '''
    
        
        for n_pull in range(n_pulls):

            maximun_value = max(self.estimator.current_estimations_each_arm)
            maximun_indexes = [i for i, mean in enumerate(self.estimator.current_estimations_each_arm) if mean == maximun_value]

            if len(maximun_indexes) == 1:
                # pull the most atractive arm
                self.estimator.arm_pull(maximun_indexes[0], self.bandit.pull_arm(maximun_indexes[0]))
            else:
                #randomly choose one of them
                choice = random.choice(maximun_indexes)
                self.estimator.arm_pull(choice, self.bandit.pull_arm(choice))


def main():
    '''
    Main 
    '''

    # Argument Parser
    parser = argparse.ArgumentParser(description='Tracking estimator for each bandit arm\' mean.')

    parser.add_argument('-n', '--n_arms', type=int, required=True,
                        help="the number of arms the estimator will track")
    parser.add_argument('-np', '--n_pulls', type=int, required=True,
                        help="the number of arm pulls that will be made")
    parser.add_argument('-ns', '--non-stationary', action='store_true',
                        help="if set true, the mean rewards of each arm will change over usage.")

    # initialize parser
    args = parser.parse_args()

    greedy_bandit = GreedyBandit(args.n_arms, args.non_stationary)

    print(greedy_bandit.bandit)
    print(greedy_bandit.estimator)

    greedy_bandit.apply_strategy(args.n_pulls)

    print(greedy_bandit.bandit)
    print(greedy_bandit.estimator)


if __name__ == '__main__':
    main()
