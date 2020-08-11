import argparse
import os
import subprocess

import hypertune
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data.sampler import SubsetRandomSampler

from model import Net
from util import CitibikeDataset

MODEL_FILE_NAME = "torch.model"


def get_args():
    """Argument parser. Returns a dictionary of arguments."""
    parser = argparse.ArgumentParser(description='PyTorch model')
    parser.add_argument(
        '--batch-size',
        type=int,
        default=16,
        help='input batch size for training (default: 64)')
    parser.add_argument(
        '--test-batch-size',
        type=int,
        default=1000,
        help='input batch size for testing (default: 1000)')
    parser.add_argument(
        '--test-split',
        type=float,
        default=0.2,
        help='training examples reserved for testing (default: 0.2)')
    parser.add_argument(
        '--epochs',
        type=int,
        default=10,
        help='number of epochs to train (default: 10)')
    parser.add_argument(
        '--lr',
        type=float,
        default=0.01,
        help='learning rate (default: 0.01)')
    parser.add_argument(
        '--momentum',
        type=float,
        default=0.5,
        help='SGD momentum (default: 0.5)')
    parser.add_argument(
        '--no-cuda',
        action='store_true',
        default=False,
        help='disables CUDA training')
    parser.add_argument(
        '--seed',
        type=int,
        default=1,
        help='random seed (default: 1)')
    parser.add_argument(
        '--log-interval',
        type=int,
        default=5,
        help='how many batches to wait before logging training status')
    parser.add_argument(
        '--model-dir',
        default=None,
        help='The directory to store the model')

    args = parser.parse_args()
    return args


def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    print(f'Train Epoch {epoch}:')
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.l1_loss(output, target)
        loss.backward()
        optimizer.step()

        if batch_idx % args.log_interval == 0:
            batch_idx += 1
            print(f'\tBatch {batch_idx}/{len(train_loader)}\tLoss: {loss.item()}')


def test(args, model, device, test_loader, epoch):
    model.eval()
    loss = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss += F.l1_loss(output, target).item()   # sum up batch loss
            
    loss /= len(test_loader)
    print(f'\nTest set average loss: {loss}\n')

    # Use hypertune to report metrics for hyperparameter tuning
    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
        hyperparameter_metric_tag='test_loss',
        metric_value=loss,
        global_step=epoch
    )


def main():
    # Training settings
    args = get_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    torch.manual_seed(args.seed)

    # Download data
    dataset = CitibikeDataset('dataset/citibike.csv', download=False)
    
    # Create random indices for training and testing splits
    indices = list(range(len(dataset)))
    np.random.seed(args.seed)
    np.random.shuffle(indices)

    split = int(args.test_split * len(dataset))
    train_indices = indices[split:]
    test_indices = indices[:split]

    # Create data samplers and data loaders
    train_sampler = SubsetRandomSampler(train_indices)
    test_sampler = SubsetRandomSampler(test_indices)

    train_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=args.batch_size,
        sampler=train_sampler
    )
    test_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=args.test_batch_size,
        sampler=test_sampler
    )

    # Create model and optimizer
    input_dim, output_dim = len(dataset[0][0]), len(dataset[0][1])
    model = Net(input_dim, output_dim).to(device)
    optimizer = optim.SGD(
        model.parameters(),
        lr=args.lr,
        momentum=args.momentum
    )

    # Train model
    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch)
        test(args, model, device, test_loader, epoch)

    # Save model to GCS
    if args.model_dir:
        tmp_model_file = os.path.join('/tmp', MODEL_FILE_NAME)
        torch.save(model.state_dict(), tmp_model_file)
        subprocess.check_call([
            'gsutil', 'cp', tmp_model_file,
            os.path.join(args.model_dir, MODEL_FILE_NAME)
        ])


if __name__ == '__main__':
    main()
