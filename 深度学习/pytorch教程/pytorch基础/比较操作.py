import torch

#比较元素相等性。第二个参数可为一个数或与第一个参数同类型形状的张量,不等用ne
a=torch.Tensor([[1,2,3],[2,1,3]])
b=torch.Tensor([[1,3,2],[2,3,1]])
torch.eq(a,1)
torch.eq(a,b)

#比较两个张量是否完全相等，是则返回True,否则返回False
torch.equal(a,b)

#大于等于比较,小于等于用le
torch.ge(a,b)

#大于比较,小于用lt
torch.gt(a,b)

#计算第k个最小值
torch.kthvalue(a,dim=0,k=2)

#计算最大值
torch.max(a)

#排序
torch.sort(a,dim=0)   #按行排序

#返回前k个数
c=torch.arange(10)
torch.topk(c,k=3)
torch.topk(c,k=3,largest=False)   #largest指定返回最小的k个值还是最大的k个值

