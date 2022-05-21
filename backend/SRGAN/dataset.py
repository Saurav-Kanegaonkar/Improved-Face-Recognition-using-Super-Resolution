import os
import numpy as np
import config
from torch.utils.data import Dataset, DataLoader
from torch import optim
from PIL import Image
from model import Generator
from utils import plot_examples,load_checkpoint
class MyImageFolder(Dataset):
    def __init__(self, root_dir):
        super(MyImageFolder, self).__init__()
        self.data = []
        self.root_dir = root_dir
        #print(os.listdir(self.root_dir))
        for item in os.listdir(self.root_dir):
            self.data.append(item)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        img_file = self.data[index]
        root_and_dir = self.root_dir

        image = np.array(Image.open(os.path.join(root_and_dir, img_file)))
        image = config.both_transforms(image=image)["image"]
        high_res = config.highres_transform(image=image)["image"]
        low_res = config.lowres_transform(image=image)["image"]
        return low_res, high_res


def test():
    dataset = MyImageFolder(root_dir="new_data/")
    loader = DataLoader(dataset, batch_size=1, num_workers=8)

    for low_res, high_res in loader:
        print(low_res.shape)
        print(high_res.shape)
def run():
    gen = Generator(in_channels=3).to(config.DEVICE)
    opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    directory = os.getcwd() +  "/backend/SRGAN/"
    directory.replace("\\","/")
    print(directory)
    load_checkpoint(
            directory + config.CHECKPOINT_GEN,
            gen,
            opt_gen,
            config.LEARNING_RATE,
        )
    directory = os.getcwd() +  "/backend/face_images/"
    directory.replace("\\","/")
    plot_examples(directory, gen)

if __name__ == "__main__":
    #test()
    run()