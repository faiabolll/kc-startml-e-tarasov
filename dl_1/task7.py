import torch

def function03(X: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    w = torch.rand(X.shape[1], requires_grad=True)

    for i in range(1000):
        pred = X @ w
        loss = torch.mean((y - pred) ** 2)

        if loss < 1:
            break
        else:
            loss.backward()
            with torch.no_grad():
                w -= w.grad * 1e-2
            w.grad.zero_()

    return w
