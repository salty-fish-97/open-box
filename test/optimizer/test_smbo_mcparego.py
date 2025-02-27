import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.getcwd())

from openbox.optimizer.generic_smbo import SMBO
from openbox.utils.config_space import ConfigurationSpace, UniformFloatHyperparameter


def branin_currin(config):
    dic = config.get_dictionary()
    x1 = dic.get('x1')
    x2 = dic.get('x2')
    px1 = 15 * x1 - 5
    px2 = 15 * x2
    res = dict()

    f1 = (px2 - 5.1 / (4 * np.pi ** 2) * px1 ** 2 + 5 / np.pi * px1 - 6) ** 2 + 10 * (1 - 1 / (8 * np.pi)) * np.cos(
        px1) + 10
    f2 = (1 - np.exp(-1 / (2 * x2))) * (2300 * x1 ** 3 + 1900 * x1 ** 2 + 2092 * x1 + 60) / (
                100 * x1 ** 3 + 500 * x1 ** 2 + 4 * x1 + 20)
    res['objectives'] = [f1, f2]
    res['constraints'] = []
    return res


bc_params = {
    'float': {
        'x1': (0, 1, 0.5),
        'x2': (0, 1, 0.5)
    }
}
bc_cs = ConfigurationSpace()
bc_cs.add_hyperparameters([UniformFloatHyperparameter(e, *bc_params['float'][e]) for e in bc_params['float']])
bc_max_hv = 59.36011874867746
bc_ref_point = [18., 6.]

bo = SMBO(branin_currin, bc_cs,
          advisor_type='mcadvisor',
          task_id='mcparego',
          num_objectives=2,
          acq_type='mcparego',
          ref_point=bc_ref_point,
          max_runs=100, random_state=2)
history = bo.run()

# plot pareto front
if history.num_objectives in [2, 3]:
    history.plot_pareto_front()
    plt.show()

# plot hypervolume
history.plot_hypervolumes()
plt.show()
