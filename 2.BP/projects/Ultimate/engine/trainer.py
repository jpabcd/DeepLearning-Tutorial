



import numpy as np
import os.path as osp

from ..data import Dataset, DataLoader
from ..models.nn import Module, ModuleList, Linear, ReLU, Dropout
from ..models.loss import SigmoidCrossEntropy
from ..models.optim import Adam
from ..models.model import Model


    
def train(epochs = 10, lr=1e-2, batch_size = 64, classes = 10):
    np.random.seed(3)
    numdata, data_dims = train_images.shape  # 60000, 784

    # 定义dataloader和dataset，用于数据抓取
    train_data = DataLoader(Dataset(train_images, one_hot(train_labels, classes)), batch_size, shuffle=True)
    model = Model(data_dims, 256, classes)
    #loss_func = SoftmaxCrossEntropy()
    loss_func = SigmoidCrossEntropy(model.params(), 0)
    optim = Adam(model, lr)
    iters = 0   # 定义迭代次数，因为我们需要展示loss曲线，那么x将会是iters

    lr_schedule = {
        5: 1e-3,
        15: 1e-4,
        18: 1e-5
    }

    # 开始进行 epoch 循环，总数是 epochs 次
    for epoch in range(epochs):
        
        if epoch in lr_schedule:
            lr = lr_schedule[epoch]
            optim.set_lr(lr)
        
        model.train()
        # 对一个批次内的数据进行迭代，每一次迭代都是一个batch（即256）
        for index, (images, labels) in enumerate(train_data):
            
            x = model(images)
            
            # 计算loss值
            loss = loss_func(x, labels)
            
            optim.zero_grad()
            G = loss_func.backward()
            model.backward(G)
            optim.step()   # 应用梯度，更新参数
            iters += 1
        if epoch % 200 == 0:
            print("Epoch: {} / {}, Iter: {}, Loss: {:.3f}, LR: {:g}".format(
                epoch, epochs, iters, loss, lr
            ))
        
        model.eval()
        val_accuracy, val_loss = estimate_val(model(test_images), test_labels, classes, loss_func)
        print("\nTest Result: Acc: {:.2f}%, Loss: {:.3f}\n".format(
            val_accuracy*100, val_loss
        ))
        
        

    

if __name__ == '__main__':
    pass



    