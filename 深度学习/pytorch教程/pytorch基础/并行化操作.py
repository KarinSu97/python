import torch

#获得用于并行化CPU操作的OpenMP线程数
torch.get_num_threads()

#设定用于并行化CPU操作的OpenMP线程数
torch.set_num_threads(1)