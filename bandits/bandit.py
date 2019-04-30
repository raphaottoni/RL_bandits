import argparse
import numpy as np
from collections import defaultdict

class Bandit:
    """
    This class implement a multi-armed bandit object

    """

    def __init__(self, means, STDs, non_stationary = False, uses_mean_before_change = 30, standard_deviation_of_change = 5.0, seed = 42):
        '''
        Class constructor

        Args:

            means (list of floats): list of all arms reward means (gaussian modeling)

            STDs (list of floats): list of all arms standard deviations (Gaussian modeling)

            non-stationary (Boolean): if True the mean of the gaussian reward modeling will change, it will remain stationary otherwise

            uses_before_change (integer): The mean of how many times the arm will be used before its gaussian reward modeling change.

            standard_deviation_of_change (float): The standard deviation that will be used when the mean of the arm gaussian reward need to be changed.

            seed (integer):  seed used for random processes.
        '''

        if len(means) != len(STDs):
            raise Exception("the number of arms indicated by the list of reward means is not the same as indicated as the list of standard-deviation of those means")
    
        # Set the tracking variables
        self.means = means
        self.STDs  = STDs
        self.stationary = False if non_stationary else True
        self.uses_mean_before_change = uses_mean_before_change
        self.arm_uses = len(means) * [0]
        self.total_arms_uses = 0
        self.arms_rewards = defaultdict(list)
        self.acumulative_reward = 0
        self.acumulative_optimal_reward = 0
        self.standard_deviation_of_change = standard_deviation_of_change

        #set the seed
        np.random.seed(seed)
        
    def __str__ (self):
        '''
        Class wrapper for print

        '''
        number_of_arms = len(self.means)
        arms_type = "STATIONARY" if self.stationary else "NON-STATIONARY"

        return "Mult-armed bandit with " + str(number_of_arms) + " "  + arms_type  +  " arms.\n" +\
               "Reward_means = " + str(self.means) +  "\n" +\
               "Rewards_stds = " + str(self.STDs) + "\n" +\
               "Arm mean uses before change reward mean = " + str(self.uses_mean_before_change) + "\n" +\
               "Uses of each arm " + str(self.arm_uses) + "\n" +\
               "Accumalated reward with " + str(self.total_arms_uses) + " now:" + str(self.acumulative_reward) + "\n" +\
               "The simulated optimal reward with " + str(self.total_arms_uses) + " now:" + str(self.acumulative_optimal_reward) + "\n"

    def pretend_pull_optimal_arm(self):
        '''
        This function always pull the arm with the highest mean. It serves as a optimal threshold
        '''

        # Finds the id of the best arm
        best_arm_id = self.means.index(max(self.means))

        # calculate the optimal reward 
        reward = np.random.normal(self.means[best_arm_id], self.STDs[best_arm_id], 1)[0]

        
        # Acumulate the pretend reward
        self.acumulative_optimal_reward += reward

    def pull_arm(self, arm_id):
        '''
        Perform an pull action of <arm_id>

        Args:
            arm_id (integer): The id of the arm that will be activated

        Return:
            (float): Reward given when pulling this arm
        '''

        if arm_id >= len(self.means) or arm_id < 0:
            raise Exception("[" + self.__name__ + "] Invalid <arm_id> to pull. The ID was " + str(arm_id) +\
                            " which is outside the accepted range of 0-" + str(len(self.means) - 1)) 

        # Saves the seed state before pull (to not interfer with other random processess )
        random_state = np.random.get_state()

        # calculate the reward 
        reward = np.random.normal(self.means[arm_id], self.STDs[arm_id], 1)[0]

        # count the use of this arm
        self.arm_uses[arm_id] += 1
        self.total_arms_uses += 1
        self.acumulative_reward += reward

        # Save history
        self.arms_rewards[arm_id].append(reward)

        # Return to the previous random state
        np.random.set_state(random_state)

        # Pretend what it would do if the best arm was selected
        self.pretend_pull_optimal_arm()

        # check if the mean should change
        if not self.stationary and self.arm_uses[arm_id] % self.uses_mean_before_change == 0:
            # changes the mean 
            self.means[arm_id] = np.random.normal(self.means[arm_id], self.standard_deviation_of_change, 1)[0]

        return reward

def main():
    '''
    Main
    '''

    # Argument Parser
    parser = argparse.ArgumentParser(description='Mult-armed Bandit.')

    parser.add_argument('-ms', '--means', type=float, nargs='+', required=True,
                        help="list of all arms reward means")
    parser.add_argument('-stds', '--stand_deviations', type=float, nargs='+', required=True,
                        help="list of all arms standard deviations")
    parser.add_argument('-ns', '--non-stationary', action='store_true',
                        help="if set true, the mean rewards of each arm will change over usage.")
    parser.add_argument('-cstd', '--standard_deviation_of_change', default=5.0, type=float,
                        help="The stand deviation of the gaussian distribution when changing the initial distribution regarding <means> when <non-stationary> was set to True")
    parser.add_argument('-umbc', '--uses_mean_before_change', type=int,
                        help="The mean number of times a arm will be used before change its reward function", default = 30)

    # initialize parser
    args = parser.parse_args()

    bandit = Bandit(args.means, args.stand_deviations, args.non_stationary, args.uses_mean_before_change, args.standard_deviation_of_change)
    print(bandit)
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(1))
    print(bandit)


if __name__ == '__main__':
    main()
