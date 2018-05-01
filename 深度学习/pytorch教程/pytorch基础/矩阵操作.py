import torch

#对角矩阵
#如果输入是一个向量(1D 张量)，则返回一个以input为对角线元素的2D方阵
#如果输入是一个矩阵(2D 张量)，则返回一个包含input对角线元素的1D张量
#参数diagonal指定对角线:
#diagonal = 0, 主对角线
#diagonal > 0, 主对角线之上
#diagonal < 0, 主对角线之下
a=torch.randn(4)
torch.diag(a)
b=torch.randn(4,4)
torch.diag(b)
torch.diag(b,diagonal=1)

#计算迹，即矩阵的对角线元素和
a=torch.arange(1,10).view(3,3)
torch.trace(a)

#下三角矩阵
torch.tril(a)

#上三角矩阵
torch.triu(a)

#对矩阵mat1和mat2进行矩阵乘操作。矩阵mat加到最终结果。如果mat1 是一个 n×m张量，mat2 是一个 m×p张量，
# 那么out和mat的形状为n×p。 alpha 和 beta 分别是两个矩阵 mat1@mat2和mat的比例因子，即out=(beta∗M)+(alpha∗mat1@mat2)
M=torch.ones(2,2)
mat1=torch.Tensor([[1,2],[3,4]])
mat2=torch.Tensor([[1,2],[3,4]])
torch.addmm(M,mat1,mat2)

#torch.addmv,对矩阵mat和向量vec对进行相乘操作。向量tensor加到最终结果。如果mat 是一个 n×m维矩阵，vec 是一个 m维向量，
# 那么out和mat的为n元向量。 可选参数_alpha_ 和 beta 分别是 mat∗vec和mat的比例因子，即out=(beta∗tensor)+(alpha∗(mat@vec))
M = torch.randn(2)
mat = torch.randn(2, 3)
vec = torch.randn(3)
torch.addmv(M, mat, vec)

#点乘
torch.dot(torch.Tensor([1,2]),torch.Tensor([1,2]))

#特征分解
torch.eig(torch.randn(4,4),eigenvectors=True)

#最小二乘解
A = torch.Tensor([[1, 1, 1],
                  [2, 3, 4],
                  [3, 5, 2],
                  [4, 2, 5],
                  [5, 4, 3]])
B = torch.Tensor([[-10, -3],
                  [ 12, 14],
                  [ 14, 12],
                  [ 16, 16],
                  [ 18, 16]])
X, _ = torch.gels(B, A)
X

#计算线性方程组AX=B的解
A = torch.Tensor([[6.80, -2.11,  5.66,  5.97,  8.23],
                  [-6.05, -3.30,  5.36, -4.44,  1.08],
                  [-0.45,  2.58, -2.70,  0.27,  9.04],
                  [8.32,  2.71,  4.35,  -7.17,  2.14],
                  [-9.67, -5.14, -7.26,  6.08, -6.87]]).t()
B = torch.Tensor([[4.02,  6.19, -8.22, -7.57, -3.03],
                  [-1.56,  4.00, -8.67,  1.75,  2.86],
                  [9.81, -4.09, -4.57, -8.61,  8.99]]).t()
X, LU = torch.gesv(B, A)

#计算矩阵的逆矩阵
a=torch.randn(4,4)
torch.inverse(a)

#矩阵乘积
a=torch.randn(4,3)
b=torch.randn(3,4)
torch.mm(a,b)

#矩阵向量相乘
a=torch.randn(4,3)
b=torch.randn(3)
torch.m(a,b)

#QR分解,q是半正定矩阵，r是上三角矩阵
a=torch.randn(4,4)
q,r=torch.qr(a)

#SVD分解
u,s,v=torch.svd(a)
