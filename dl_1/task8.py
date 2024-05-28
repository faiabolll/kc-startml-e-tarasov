import torch

def function04(X: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    layer = torch.nn.Linear(in_features=X.shape[1], out_features=1)

    for i in range(1000):
        pred = layer(X).ravel()
        loss = torch.mean((y - pred) ** 2)

        if loss < 0.3:
            break
        else:
            loss.backward()
            with torch.no_grad():
                layer.weight -= layer.weight.grad * 1e-2
                layer.bias -= layer.bias.grad * 1e-2
            layer.zero_grad()

    return layer
