import os
import torch
import random
from time import time
from copy import deepcopy

from tqdm.auto import tqdm
import numpy as np

from utils import *

torch.manual_seed(0)
random.seed(0)
np.random.seed(0)

    

def evaluate_pair_models(eval_type, models, config, csv_file):
    train_loader = config['data']['train']['full']
    models = [reset_bn_stats(base_model, train_loader) for base_model in config['models']['bases']]
    models = config['models']['bases']
    
    for idx, model in enumerate(models):
        results = evaluate_model(eval_type, model, config)
        results['Model'] = CONCEPT_TASKS[idx]
        write_to_csv(results, csv_file=csv_file)
        print(results)
    
    ensembler = SpoofModel(models)
    results = evaluate_model(eval_type, ensembler, config)
    results['Model'] = 'Ensemble'
    write_to_csv(results, csv_file=csv_file)
    print(results)


if __name__ == "__main__":
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    config_name = 'cifar50_resnet20'
    skip_pair_idxs = [0]
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    raw_config = get_config_from_name(config_name, device=device)
    model_dir = raw_config['model']['dir']
    model_name = raw_config['model']['name']
    run_pairs = find_runable_pairs(model_dir, model_name, skip_pair_idxs=skip_pair_idxs)
    csv_file = os.path.join(
        './csvs',
        raw_config['dataset']['name'],
        raw_config['model']['name'],
        raw_config['eval_type'],
        'base_models.csv'
    )
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)    

    with torch.no_grad():
        for pair in run_pairs:
            raw_config = inject_pair(raw_config, pair)
            config = prepare_experiment_config(raw_config)

            evaluate_pair_models(
                eval_type=config['eval_type'],
                models=config['models']['bases'],
                config=config,
                csv_file=csv_file
            )