import torch

#连接操作
x=torch.rand(2,3)
torch.cat((x,x,x),dim=0)   #按行合并
torch.cat((x,x,x),dim=1)   #按列合并

#对张量进行分块操作
y=torch.cat((x,x,x),dim=0)
torch.chunk(y,chunks=3,dim=0)

#沿着指定维度对输入进行切片，取index中指定的相应项(index为一个LongTensor)，然后返回到一个新的张量
x=torch.randn(4,4)
x
torch.index_select(x,dim=0,index=torch.LongTensor([0,2]))

#返回一个包含输入input中非零元素索引的张量
torch.nonzero(torch.Tensor([1,2,3,0,4]))

#将输入张量分割成相等形状的chunks（如果可分）。 如果沿指定维的张量形状大小不能被split_size 整分， 则最后一个分块会小于其它分块。
x=torch.randn(5,4)
torch.split(x,split_size=2,dim=0)

#将输入张量形状中的1 去除并返回。 如果输入是形如(A×1×B×1×C×1×D)，那么输出形状就为： (A×B×C×D)
#当给定dim时，那么挤压操作只在给定维度上。例如，输入形状为: (A×1×B), squeeze(input, 0) 将会保持张量不变，
#只有用 squeeze(input, 1)，形状会变成 (A×B)。
x=torch.randn(2,1,2,1,2)
x.size()
y=torch.squeeze(x)
y.size()

#转置
x=torch.randn(2,3)
torch.t(x)
torch.transpose(x,0,1)

#移除指定的维数，返回数组
torch.unbind(x,dim=0)

