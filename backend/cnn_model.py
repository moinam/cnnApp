import os
import torch
import torch.nn as nn
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.transforms import ToTensor


PATH = os.path.join(os.getcwd(), "backend", "cnn_model.pt")

class CNN(nn.Module):
    """
        CNN Class

        Initial Configuration of the CNN model to be trained and tested
    """
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        # fully connected layer, output 10 classes
        self.out = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.conv1(x)
        # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        output = self.out(x)
        return output, x    # return x for visualization


def load_data():
    """
        Load MNIST data
        
        Returns 
            loaders: Object contatining train adn test data of MNIST
    """
    train_data = datasets.MNIST(
        root='data',
        train=True,
        transform=ToTensor(),
        download=True,
    )

    test_data = datasets.MNIST(
        root='data',
        train=False,
        transform=ToTensor()
    )
    loaders = {
        'train': DataLoader(train_data,
                            batch_size=100,
                            shuffle=True,
                            num_workers=1),

        'test': DataLoader(test_data,
                           batch_size=100,
                           shuffle=True,
                           num_workers=1),
    }
    return loaders

def train_model(n_epochs, cnn: CNN, loaders):
    """
        Train the CNN model on train data and print results
        Parameters
            n_epochs: number of iterations
            cnn: CNN object
            loaders: loaded MNIST data
    """
    loss_func = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=0.01)
    cnn.train()
    # Train the model
    total_step = len(loaders['train'])
    for epoch in range(n_epochs):
        for i, (images, labels) in enumerate(loaders['train']):
            # gives batch data, normalize x when iterate train_loader
            b_x = torch.autograd.Variable(images)   # batch x
            b_y = torch.autograd.Variable(labels)   # batch y

            output = cnn(b_x)[0]
            loss = loss_func(output, b_y)

            # clear gradients for this training step
            optimizer.zero_grad()

            # backpropagation, compute gradients
            loss.backward()

            # apply gradients
            optimizer.step()

            if (i+1) % 1000 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, n_epochs, i + 1, total_step, loss.item()))
    print(loss, optimizer)

def test_model(cnn: CNN, loaders):
    """
        Test the CNN model on test data and print results
        Parameters
            cnn: CNN object
            loaders: loaded MNIST data
    """
    # Test the model
    cnn.eval()

    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in loaders['test']:
            test_output, last_layer = cnn(images)
            pred_y = torch.max(test_output, 1)[1].data.squeeze()
            accuracy = (pred_y == labels).sum().item() / float(labels.size(0))

        print('Test Accuracy of the model on the 10000 test images: %.2f' % accuracy)
        sample = next(iter(loaders['test']))
        imgs, lbls = sample
        actual_number = lbls[:10].numpy()
        test_output, last_layer = cnn(imgs[:10])
        pred_y = torch.max(test_output, 1)[1].data.numpy().squeeze()
        print(f'Prediction number: {pred_y}')
        print(f'Actual number: {actual_number}')

def predict_image(image):
    """
        Returns the recognized digit from the cnn model from the Input image
        Parameters
            image: Image of type PIL

        Returns: 
            pred_y: predicted value from CNN
    """
    # Load cnn model
    cnn = torch.load(PATH)
    cnn.eval()
    transform_img = transforms.Compose([transforms.Resize(28), transforms.ToTensor(),])
    image_tensor = transform_img(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = torch.autograd.Variable(image_tensor)
    with torch.no_grad():
        output, last_layer = cnn(input)
        pred_y = torch.max(output, 1)[1].data.numpy().squeeze()
    return pred_y


def make_cnn_model():
    """
        Trains the CNN model and the saves it in the local storage
    """
    cnn = CNN()
    loaders = load_data()
    train_model(10, cnn, loaders)
    test_model(cnn, loaders)
    # Save cnn model
    torch.save(cnn, PATH)