import torch

#保存整个模型的结构信息和参数信息
torch.save(model,'./model.pth')

#只保存模型的状态
torch.save(model.state_dict(),'./model_state.pth')

#加载整个模型
model=torch.load('./model.pth')

#加载模型的参数信息
model=torch.load_state_dict(torch.load('./model_state.pth'))

