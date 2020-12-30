import torch
from PIL import Image


def get_imgs(fileloc):
    """

    :param fileloc: Directory of the image
    :return: Cropped Images ( Pillow )
    """
    img = Image.open(fileloc)
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    yolo_model.autoshape()
    yolo_model.cpu()
    imgs = [img]
    result = yolo_model(imgs, size=700)
    cars = process_image(result=result)
    if cars["total_cars"] <= 1:
        return [img], 1
    else:
        images = []
        for cr in cars["predictions"]:
            new_img = img.crop((cr["x1"], cr["y1"], cr["x2"], cr["y2"]))
            images.append(new_img)
        return images, cars["total_cars"]


def process_image(result):
    """

    :param result: Yolo Model prediction results
    :return: structured info of predictions

    Parameter info:
    tensr:

    Example of a single image prediction (yolo output)

    #          x1 (pixels)  y1 (pixels)  x2 (pixels)  y2 (pixels)   confidence        class
    # tensor([[7.47613e+02, 4.01168e+01, 1.14978e+03, 7.12016e+02, 8.71210e-01, 0.00000e+00],
    #         [1.17464e+02, 1.96875e+02, 1.00145e+03, 7.11802e+02, 8.08795e-01, 0.00000e+00],
    #         [4.23969e+02, 4.30401e+02, 5.16833e+02, 7.20000e+02, 7.77376e-01, 2.70000e+01],
    #         [9.81310e+02, 3.10712e+02, 1.03111e+03, 4.19273e+02, 2.86850e-01, 2.70000e+01]])

    """
    tensr = result.xyxy[0]
    listofpredictions = list()
    output = dict()
    cars = 0

    for detection in tensr:
        if int(detection[-1]) != 2 and int(detection[-1]) != 7:
            continue
        if float(detection[-2]) < 0.30:
            continue
        cars += 1
        car_info = dict()
        car_info["x1"] = float(detection[0])
        car_info["y1"] = float(detection[1])
        car_info["x2"] = float(detection[2])
        car_info["y2"] = float(detection[3])
        car_info["confidence"] = float(detection[4])
        listofpredictions.append(car_info)
    output["predictions"] = listofpredictions
    output["total_cars"] = cars
    return output
