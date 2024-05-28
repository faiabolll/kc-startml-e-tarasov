from torch import nn

def create_conv_model():
	return nn.Sequential(
		nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
		nn.ReLU(),
		# nn.MaxPool2d(kernel_size=2),

		nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
		nn.ReLU(),
		nn.AvgPool2d(kernel_size=2),

		nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3),
		nn.ReLU(),
		nn.AvgPool2d(kernel_size=2),

		nn.Flatten(),
		nn.Linear(512, 256),
		# nn.Linear(128, 256),
		nn.ReLU(),
		nn.Linear(256, 10)
	)