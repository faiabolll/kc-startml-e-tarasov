import torch

def function01(tensor: torch.Tensor, count_over: str) -> torch.Tensor:
    if count_over == 'columns':
        return torch.mean(tensor, dim=0)
    if count_over == 'rows':
        return torch.mean(tensor, dim=1)
    raise ValueError("count_over sholud be either 'columns' or 'rows'")