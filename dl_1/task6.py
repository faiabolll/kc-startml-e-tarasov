import torch 

def function02(ds: torch.Tensor) -> torch.Tensor:
    return torch.rand(ds.shape[1], requires_grad=True)