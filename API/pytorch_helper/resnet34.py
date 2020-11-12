import torch
import torch.nn as nn
from torchvision import transforms, models
import PIL.Image as Image
from models.sfcars import Sfcars
from models.indiacars import Indiacars
from .constants import SFCARS_PARAM, INDCARS_PARAM


def load_model(checkpoint_path, chkpt_model):
    checkpoint = torch.load(checkpoint_path)

    model = models.resnet34(pretrained=True)
    model.cpu()

    num_ftrs = model.fc.in_features

    if chkpt_model.strip() == SFCARS_PARAM:
        model.fc = nn.Linear(num_ftrs, 196)
    elif chkpt_model.strip() == INDCARS_PARAM:
        model.fc = nn.Linear(num_ftrs, 120)

    model.load_state_dict(checkpoint['state_dict'])

    return model


def predict(fileloc, model, chkpt_model):
    model.eval()

    # transforms for the input image
    loader = transforms.Compose([transforms.Resize((244, 244)),
                                 transforms.CenterCrop(224),
                                 transforms.ToTensor(),
                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    image = Image.open(fileloc)
    image = loader(image).float()
    image = torch.autograd.Variable(image, requires_grad=True)
    image = image.unsqueeze(0)
    image = image.cpu()
    output = torch.exp(model.forward(image))
    top_probs, top_labs = output.topk(5)
    results = []
    for labs in top_labs[0]:
        if chkpt_model.strip() == SFCARS_PARAM:
            results.append(Sfcars.get_item_by_id(idno=int(labs) + 1))
        elif chkpt_model.strip() == INDCARS_PARAM:
            results.append(Indiacars.get_item_by_id(idno=int(labs) + 1))

    return results
