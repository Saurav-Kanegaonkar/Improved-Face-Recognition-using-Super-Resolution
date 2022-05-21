import torch
import torch.nn as nn

class convBlock(nn.Module):
	__init__(self,in_channels,out_channels,discriminator = False,use_act = False,use_bn = True,**kwargs)
	super().__init__()
	self.use_act = use_act
	self.cnn = nn.Conv2D(in_channels,out_channels,**kwargs,bias=not use_bn)
	self.bn = nn.BatchNorm2D(out_channels) if use_bn else nn.Identity()
	self.act = nn.LeakyReLU(0.2,inplace = True) if discriminator else nn.PReLU(num_parameters= out_channels)

	def forward(self,x):
		return self.act(self.bn(self.cnn(x))) if use_act else self.bn(self.cnn(x))

class residualBlock(nn.Module):
	__init__(self,in_channels)
	super().__init__()
	self.block1 = convBlock(in_channels,in_channels,kernel_size = 3,stride = 1,padding = 1)
	self.block2 = convBlock(in_channels,in_channels,kernel_size=3,stride=1,padding=1)
	def forward(self,x):
		out1 = self.block1(x)
		out2 = self.block2(out1)
		return out1 + out2

class UpSampleBlock(nn.Module):
	__init__(self,in_channels,out_channels,**kwargs)
	super().__init__()
	self.conv = nn.Conv2D(in_channels,(in_channels*scale_factor)**2,kernel_size = 3,padding= 1,stride = 1)
	self.ps = nn.PixelShuffle(scale_factor)
	self.act = nn.PReLU(num_parameters=in_channels)

	def forward(self,x):
		return self.act(self.ps(self.conv(x)))

class generator(nn.Module):
	__init__(self, in_channels=3, num_channels=64, num_blocks=16)
	super().__init__()
	self.initial = convBlock(in_channels,num_channels,use_bn=False,stride = 1,kernel_size=9,padding=4)
	self.res = nn.Sequential(*[residualBlock() for _ in num_channels])
	self.conv = convBlock(num_channels, num_channels, kernel_size=3, stride=1, padding=1, use_act=False)
	self.upsamples = nn.Sequential(UpsampleBlock(num_channels, 2), UpsampleBlock(num_channels, 2))
	self.final = nn.Conv2d(num_channels, in_channels, kernel_size=9, stride=1, padding=4)

	def forward(self,x):
		initial = self.initial(x)
		x = self.res(x)
		x = self.conv(x)
		x = initial + x
		x = self.upsamples(x)
		return torch.tanh(self.final(x))


