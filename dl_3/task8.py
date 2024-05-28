def count_parameters_conv(in_channels: int, out_channels: int, kernel_size: int, bias: bool):
	return (in_channels * kernel_size ** 2 + int(bias)) * out_channels