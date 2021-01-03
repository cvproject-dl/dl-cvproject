import torch
import torch.nn as nn
from torchvision import transforms, models
import PIL.Image as Image
from dbmodels.sfcars import Sfcars
from dbmodels.indiacars import Indiacars
from .constants import SFCARS_PARAM, INDCARS_PARAM
from multiclass import get_imgs


def load_model(checkpoint_path, chkpt_model):
    f"""
    :param checkpoint_path: path to the saved model
    :param chkpt_model: model name (stanford cars | indian cars) ({SFCARS_PARAM}/{INDCARS_PARAM})
    :return: 
    """
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


def getpred(images, model, chkpt_model):
    model.eval()
    # transforms for the input image
    loader = transforms.Compose([transforms.Resize((244, 244)),
                                 transforms.CenterCrop(224),
                                 transforms.ToTensor(),
                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    preds = []
    for image in images:
        image = loader(image).float()
        image = torch.autograd.Variable(image, requires_grad=True)
        image = image.unsqueeze(0)
        image = image.cpu()
        output = model(image)
        p = torch.nn.functional.softmax(output)
        top_probs, top_labs = p.topk(3)
        results = []
        for (lab, prob) in zip(top_labs[0], top_probs[0]):
            car_info = dict()
            car_info["confidence"] = float(prob)
            if chkpt_model.strip() == SFCARS_PARAM:
                car_info["car_details"] = Sfcars.get_item_by_id(idno=int(lab) + 1)
            elif chkpt_model.strip() == INDCARS_PARAM:
                car_info["car_details"] = Indiacars.get_item_by_id(idno=int(lab) + 1)
            results.append(car_info)
        preds.append(results)
    return preds


def predict(fileloc, model, chkpt_model):
    f"""
     :param fileloc: path to the image
     :param model: pass model after loading
     :param chkpt_model: model name (stanford cars | indian cars) ({SFCARS_PARAM}/{INDCARS_PARAM})
     :return: 
    """
    images, total_cars = get_imgs(fileloc)
    return getpred(images, model, chkpt_model), total_cars
