config = {
    'dataset': {
        'name': 'cifar50',
        'shuffle_train': True
    },
    'model': {
        'name': 'resnet20x16',
        'dir': './checkpoints/cifar50_logits/resnet20x16/pairsplits',
        'bases': []
    },
    'merging_fn': 'match_tensors_zipit',
    'eval_type': 'logits',
    'merging_metrics': ['covariance', 'mean'],
}