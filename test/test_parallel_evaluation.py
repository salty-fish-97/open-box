import os
import sys
import time
import numpy as np

from ConfigSpace.hyperparameters import UniformFloatHyperparameter
sys.path.append(os.getcwd())
from litebo.optimizer.parallel_smbo import pSMBO
from litebo.config_space import ConfigurationSpace


def branin(x):
    # time_cost = np.random.randint(6)
    # time.sleep(time_cost)
    xs = x.get_dictionary()
    x1 = xs['x1']
    x2 = xs['x2']
    a = 1.
    b = 5.1 / (4.*np.pi**2)
    c = 5. / np.pi
    r = 6.
    s = 10.
    t = 1. / (8.*np.pi)
    ret = a*(x2-b*x1**2+c*x1-r)**2+s*(1-t)*np.cos(x1)+s
    print('call obj', ret)
    return ret


cs = ConfigurationSpace()
x1 = UniformFloatHyperparameter("x1", -5, 10, default_value=0)
x2 = UniformFloatHyperparameter("x2", 0, 15, default_value=0)
cs.add_hyperparameters([x1, x2])

bo = pSMBO(branin, cs, max_runs=10, time_limit_per_trial=3, logging_dir='logs', parallel_strategy='async')
bo.run()
inc_value = bo.get_incumbent()
print('BO', '='*30)
print(inc_value)

# # Evaluate the random search.
# bo = BayesianOptimization(branin, cs, max_runs=50, time_limit_per_trial=3, sample_strategy='random', logging_dir='logs')
# bo.run()
# inc_value = bo.get_incumbent()
# print('RANDOM', '='*30)
# print(inc_value)