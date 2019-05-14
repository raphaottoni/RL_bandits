import argparse
import numpy as np
from collections import defaultdict
from bandits.bandit import Bandit
from bandits.estimator import Estimator
import math
import random

class StochasticGradientBandit:
    """
    This class implements a Gradient Bandint algorithm based on Stochastic Gradient Ascend

    """

    def __init__(self, n_arms = 10, non_stationary_arms = False, step_size = 0.1):
        '''
        Class constructor

        Args:

            n_arms (integer): How many arms it will track

            non_stationary_arms (Boolean): if False the estimator will consider that all arms have a fixed gaussian distribution of reward.

            step_size (Float): the rate of update on the preference of each arm due the reward recieved.


        '''

        if n_arms <= 0:
            raise Exception("[Stochastic Gradient Ascend Bandit] The number of arms cannot be negative or zero. The <n_arms> passed to constructor was {}".format(n_arms))
    
        # Create the testbed mult-armed bandit
        arms_means = []
        arms_stds = []

        for i in range(n_arms):
            arms_means.append(np.random.normal(0,math.sqrt(1)))
            arms_stds.append(math.sqrt(1))

        # Create its Bandit and estimator
        self.bandit = Bandit(arms_means, arms_stds, non_stationary_arms)
        self.estimator = Estimator(n_arms, non_stationary_arms, 5.0)
        self.step_size = step_size 
        self.n_arms = n_arms

        # Create the array of probabilities of each arm to be select
        self.arm_probabilities = [0] * n_arms

    def probability_of_choosing_each_arm(self):
        '''
        This function  calcualtes the probability of each arm of being selected

        Args:
            (none)

        return:
            (list of floats)
        '''


        pi_arms = []
        sum_base = 0.0

        for arm_id in range(self.n_arms):
            sum_base +=  math.exp(self.arm_probabilities[arm_id])

        # calculate the normalized probability of each arm
        for arm_id in range(self.n_arms):
            pi_arms.append(math.exp(self.arm_probabilities[arm_id]) / sum_base)

        return pi_arms
            
        

    def apply_strategy(self, n_pulls = 1000):
        '''
        This function applies the Stochastic Gradient Ascent algorithm
        '''
    
        
        for n_pull in range(n_pulls):
            
            # Chooses the arm to pull accordenly probabilities
            pi_arms = self.probability_of_choosing_each_arm()

            # prepare the probablities vector into a simplier way to choose one accordingly the probabilities
            for i in range(self.n_arms):
                if i != 0:
                    pi_arms[i] = pi_arms[i -1] + pi_arms[i]

            # Choose one accordigly the probabilities
            random_float = random.random()
            from IPython import embed
            embed()

            ## We need to pull at least once each arm
            #zero_uses_arms = [i for i, mean in enumerate(self.estimator.arms_uses) if mean == 0]

            #if len(zero_uses_arms) >= 1:
            #    # pull the first of the unused arms
            #    self.estimator.arm_pull(zero_uses_arms[0], self.bandit.pull_arm(zero_uses_arms[0]))
            #else:
            #    
            #    # Choose one of the arms accordingly with the UCB1 strategy
            #    # An optimistic view of the upper bound of the reward distribution
            #    reward_atractiviness = self.calculate_UCB1_atractiviness()

            #    best_arm_value  = max(reward_atractiviness)

            #    arms_indexes = [i for i, mean in enumerate(reward_atractiviness) if mean == best_arm_value]

            #    # Check for draw
            #    if len(arms_indexes) == 1:
            #        # pull the most atractive arm
            #        self.estimator.arm_pull(arms_indexes[0], self.bandit.pull_arm(arms_indexes[0]))
            #    else:
            #        #randomly choose one of them
            #        choice = random.choice(arms_indexes)
            #        self.estimator.arm_pull(choice, self.bandit.pull_arm(choice))


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
    parser.add_argument('-ss', '--step-size', type=float, default=0.1,
                        help="The step size used that will be used to update the arms probabilities")

    # initialize parser
    args = parser.parse_args()

    gradientBandit = StochasticGradientBandit(args.n_arms, args.non_stationary, args.step_size )

    print(gradientBandit.bandit)
    print(gradientBandit.estimator)

    gradientBandit.apply_strategy(args.n_pulls)

    print(gradientBandit.bandit)
    print(gradientBandit.estimator)


if __name__ == '__main__':
    main()
