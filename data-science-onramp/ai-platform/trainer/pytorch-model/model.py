import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.linear(x)


if __name__ == '__main__':
    from util import CitibikeDataset

    dataset = CitibikeDataset(download=False)

    data, target = dataset[0]
    print('DATA')
    print(len(data), data)
    print('TARGET')
    print(len(target), target)

    input_dim, output_dim = len(dataset[0][0]), len(dataset[0][1])
    model = Net(input_dim, output_dim)
    model = model

    output = model(data)

    print('OUTPUT')
    print(len(output), output)
    