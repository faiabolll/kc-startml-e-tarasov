import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer

def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
	model.train()
	# optimizer = optimizer(model.parameters(), lr=1e-5)

	losses = []
	for x, y in data_loader:
		optimizer.zero_grad()
		y_pred = model(x)
		loss = loss_fn(y_pred, y)
		loss.backward()
		losses.append(loss.item())
		print(f"{loss.item():.5f}")
		optimizer.step()

	return sum(losses) / len(losses)