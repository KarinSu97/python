import torch

#计算输入张量的每个元素绝对值
torch.abs(torch.FloatTensor([-1,-2,3]))

#对输入张量input逐元素加上标量值value，并返回结果到一个新的张量out
a=torch.randn(4)
a
torch.add(a,20)

#用tensor2对tensor1逐元素相除，然后乘以标量值value 并加到tensor
t = torch.randn(2, 3)
t1 = torch.randn(1, 6)
t2 = torch.randn(6, 1)
torch.addcdiv(t, 0.1, t1, t2)

#用tensor2对tensor1逐元素相乘，并对结果乘以标量值value然后加到tensor。 张量的形状不需要匹配，但元素数量必须一致
t = torch.randn(2, 3)
t1 = torch.randn(1, 6)
t2 = torch.randn(6, 1)
torch.addcmul(t, 0.1, t1, t2)

#反正弦函数
a=torch.randn(4,4)
a
torch.asin(a)

#反正切函数
torch.atan(a)
torch.atan2(a,a)   #带两个输入的反正切函数

#余弦函数
torch.cos(a)

#双曲余弦
torch.cosh(a)

#向上取整函数，对输入input张量每个元素向上取整, 即取不小于每个元素的最小整数，并返回结果到输出。
torch.ceil(a)

#向下取整函数
torch.floor(a)

#将输入input张量每个元素的夹紧到区间 [min,max]，并返回结果到一个新张量。
torch.clamp(a,min=0,max=1)
torch.clamp(a,min=0)   #只对最小值进行限制

#将input逐元素除以标量值value，并返回结果到输出张量out
torch.div(a,0.1)
torch.div(a,torch.randn(4,4))   #两个矩阵元素相除

#指数函数，返回一个新张量，包含输入input张量每个元素的指数
torch.exp(a)

#计算余数
torch.fmod(torch.Tensor([1,2,3]),2)

#返回每个元素的小数部分
torch.frac(torch.Tensor([1,2.4,-3.5]))

#自然对数
torch.log(torch.Tensor([1,5,10]))

#计算input+1的自然对数yi=log(xi+1)
torch.log1p(torch.Tensor([1,5,10]))

#乘法，用标量值value乘以输入input的每个元素，并返回一个新的结果张量
torch.mul(a,value=2)

#取负值
torch.neg(torch.Tensor([-1,2,-3]))

#求n次幂
torch.pow(x,2)

#计算倒数
torch.reciprocal(torch.Tensor([2]))

#四舍五入
torch.round(a)

#平方根倒数
torch.rsqrt(a)

#计算每个元素的sigmoid值
torch.sigmoid(a)

#符号函数
torch.sign(a)

#截断函数
torch.trunc(a)

#累积
torch.cumprod(torch.Tensor([1,2,3,4,5]),dim=0)

#返回所有元素的乘积
torch.prod(torch.Tensor([1,2,3]))

#累加
torch.cumsum(torch.arange(1,10),dim=0)

#返回所有元素的和
torch.sum(torch.arange(10))

#计算a-b的范数
a=torch.Tensor([1,2,3])
b=torch.Tensor([4,5,6])
torch.dist(a,b,p=2)

#返回输入张量input的p范数
torch.norm(a,p=2)

#计算均值
torch.mean(a)

#计算中位数
torch.median(a)

#计算标准差
a=torch.randn(4,4)
torch.std(a,dim=1)

#计算方差
torch.var(a,dim=1)
