import torch
from torch import nn
from torch.utils.data import DataLoader

def evaluate(model: nn.Module, data_loader: DataLoader, loss_fn):
	model.eval()
	losses = []
	with torch.no_grad():
		for x,y in data_loader:
			y_pred = model(x)
			loss = loss_fn(y_pred, y)
			losses.append(loss.item())

	model.train()

	return sum(losses) / len(losses)