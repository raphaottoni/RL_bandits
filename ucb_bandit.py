import argparse
import numpy as np
from collections import defaultdict
from bandits.bandit import Bandit
from bandits.estimator import Estimator
import math
import random

class UCB1Bandit:
    """
    This class implements the UCB1 solution for multi-armed Bandits

    """

    def __init__(self, n_arms = 10, non_stationary_arms = False, step_size = 0.1, degree_of_exploration  = 1.0):
        '''
        Class constructor

        Args:

            n_arms (integer): How many arms it will track

            non_stationary_arms (Boolean): if False the estimator will consider that all arms have a fixed gaussian distribution of reward.

            step_size (Boolean): the ratio wich the new rewards will be pondered higher than the old ones. It is only used when <stationary_arms> is False.

            degree_of_exploration (float): The number that will multiple the upper bound of the UCB1 uncertaintie part of the formula (the higher, the more exploration)

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
        self.degree_of_exploration = degree_of_exploration
        

    def apply_strategy(self, n_pulls = 1000):
        '''
        This function applies the UCB1 strategy for the mult-armed bandit
        '''
    
        
        for n_pull in range(n_pulls):

            # We need to pull at least once each arm
            zero_uses_arms = [i for i, mean in enumerate(self.estimator.arms_uses) if mean == 0]

            if len(zero_uses_arms) >= 1:
                # pull the first of the unused arms
                self.estimator.arm_pull(zero_uses_arms[0], self.bandit.pull_arm(zero_uses_arms[0]))
            else:
                
                # Choose one of the arms accordingly with the UCB1 strategy
                # An optimistic view of the upper bound of the reward distribution
                reward_atractiviness = self.calculate_UCB1_atractiviness()

                best_arm_value  = max(reward_atractiviness)

                arms_indexes = [i for i, mean in enumerate(reward_atractiviness) if mean == best_arm_value]

                # Check for draw
                if len(arms_indexes) == 1:
                    # pull the most atractive arm
                    self.estimator.arm_pull(arms_indexes[0], self.bandit.pull_arm(arms_indexes[0]))
                else:
                    #randomly choose one of them
                    choice = random.choice(arms_indexes)
                    self.estimator.arm_pull(choice, self.bandit.pull_arm(choice))


    def calculate_UCB1_atractiviness(self):
        '''
        This functions apply the UCB1 formula to calcualte the upper bound confidence and use it
        to calculate the atractiviness of the arm

        Args:
            (none)

        Return:
            (list of floats): The atractivness of each arm regarding UCB1 formula
        '''
        
        ucb1_atractiviness = []
        number_arm_activations_so_far = sum(self.estimator.arms_uses)

        #Calculate for each arm
        for arm_id in range(self.estimator.n_arms):
    
            number_arm_activiation_arm_id_so_far  = self.estimator.arms_uses[arm_id]

            # Calculate the Upper Confidence Bound
            upper_bound = self.degree_of_exploration * math.sqrt(math.log(number_arm_activations_so_far)/number_arm_activiation_arm_id_so_far)

            ucb1_atractiviness.append(self.estimator.current_estimations_each_arm[arm_id] + upper_bound)

        return ucb1_atractiviness


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
    parser.add_argument('-de', '--degree-exploration', type=float, default=1.0,
                        help="The number that will multiple the upper bound of the UCB1 uncertaintie part of the formula (the higher, the more exploration)")

    # initialize parser
    args = parser.parse_args()

    ucb1_bandit = UCB1Bandit(args.n_arms, args.non_stationary, 0.1, args.degree_exploration)

    print(ucb1_bandit.bandit)
    print(ucb1_bandit.estimator)

    ucb1_bandit.apply_strategy(args.n_pulls)

    print(ucb1_bandit.bandit)
    print(ucb1_bandit.estimator)


if __name__ == '__main__':
    main()
