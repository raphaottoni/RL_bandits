import argparse
import numpy as np
from collections import defaultdict

class Bandit:
    """
    This class implement a multi-armed bandit object

    """

    def __init__(self, means, STDs, non_stationary = False, uses_mean_before_change = 30, seed = 42):
        '''
        Class constructor

        Args:

            means (list of floats): list of all arms reward means (gaussian modeling)

            STDs (list of floats): list of all arms standard deviations (Gaussian modeling)

            non-stationary (Boolean): if True the mean of the gaussian reward modeling will change, it will remain stationary otherwise

            uses_before_change (integer): The mean of how many times the arm will be used before its gaussian reward modeling change.

            seed (integer):  seed used for random processes.
        '''

        if len(means) != len(STDs):
            raise Exception("the number of arms indicated by the list of reward means is not the same as indicated as the list of standard-deviation of those means")
    
        self.means = means
        self.STDs  = STDs
        self.stationary = False if non_stationary else True
        self.uses_mean_before_change = uses_mean_before_change
        self.arm_uses = len(means) * [0]
        self.total_arms_uses = 0
        self.arms_rewards = defaultdict(list)
        self.acumulative_reward = 0
        
    def __str__ (self):
        '''
        Class wrapper for print

        '''
        number_of_arms = len(self.means)
        arms_type = "STATIONARY" if self.stationary else "DYNAMIC"

        return "Mult-armed bandit with " + str(number_of_arms) + " "  + arms_type  +  " arms.\n" +\
               "Reward_means = " + str(self.means) +  "\n" +\
               "Rewards_stds = " + str(self.STDs) + "\n" +\
               "Arm mean uses before change reward mean = " + str(self.uses_mean_before_change) + "\n" +\
               "Uses of each arm " + str(self.arm_uses) + "\n" +\
               "Accumalated reward with " + str(self.total_arms_uses) + " now:" + str(self.acumulative_reward) + "\n"

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

        # calculate the reward 
        reward = np.random.normal(self.means[arm_id], self.STDs[arm_id], 1)[0]

        # count the use of this arm
        self.arm_uses[arm_id] += 1
        self.total_arms_uses += 1
        self.acumulative_reward += reward

        # Save history
        self.arms_rewards[arm_id].append(reward)

        # check if the mean should change
        if not self.stationary and self.arm_uses[arm_id] % self.uses_mean_before_change == 0:
            # changes the mean and the standard deviation
            self.means[arm_id] = np.random.normal(self.means[arm_id], 0.3, 1)[0]
            self.STDs[arm_id] = np.random.normal(self.STDs[arm_id], 0.3, 1)[0]

        return reward

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
    parser.add_argument('-ns', '--non-stationary', action='store_true',
                        help="if set true, the mean rewards of each arm will change over usage.")
    parser.add_argument('-umbc', '--uses_mean_before_change', type=int,
                        help="The mean number of times a arm will be used before change its reward function", default = 30)

    # initialize parser
    args = parser.parse_args()

    bandit = Bandit(args.means, args.stand_deviations, args.non_stationary, args.uses_mean_before_change)
    print(bandit)
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(0))
    print(bandit.pull_arm(1))
    print(bandit)





if __name__ == '__main__':
    main()
