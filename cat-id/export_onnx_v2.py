"""Export cat_model_v2.pth to ONNX for OpenVINO Model Server.

Bakes preprocessing (x/255 then ImageNet Normalize) and softmax into the
graph, so clients keep the same contract as v1: send raw RGB pixels
(float32, 0-255, NCHW 1x3x224x224), read back probabilities.

v2 is 3-class - the extra not_cat class lets the classifier reject
Frigate's false detections on dark objects instead of forcing every
detection into cat_a or cat_b.
"""
import json

import torch
import torch.nn as nn
from torchvision import models

CFG = json.load(open("cat_model_v2.json"))
CLASSES = CFG["classes"]


class CatIDModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18()
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, len(CLASSES))
        # train_v2.py normalises with these, so the graph must match
        self.register_buffer("mean", torch.tensor(CFG["mean"]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor(CFG["std"]).view(1, 3, 1, 1))

    def forward(self, x):
        # x: raw RGB pixels 0-255, shape (N, 3, 224, 224)
        x = x / 255.0
        x = (x - self.mean) / self.std
        return torch.softmax(self.backbone(x), dim=1)


def main():
    model = CatIDModel()
    model.backbone.load_state_dict(
        torch.load("cat_model_v2.pth", map_location="cpu"))
    model.eval()

    dummy = torch.rand(1, 3, 224, 224) * 255
    torch.onnx.export(
        model, dummy, "model_v2.onnx",
        opset_version=17,
        input_names=["image"],
        output_names=["probabilities"],
        dynamo=False,
    )
    print(f"Exported model_v2.onnx  classes={CLASSES}")

    import numpy as np
    import onnxruntime as ort
    sess = ort.InferenceSession("model_v2.onnx")
    x = torch.rand(4, 1, 3, 224, 224) * 255
    for i in range(4):
        with torch.no_grad():
            want = model(x[i]).numpy()
        got = sess.run(None, {"image": x[i].numpy()})[0]
        np.testing.assert_allclose(got, want, rtol=1e-3, atol=1e-5)
    print("Parity check passed: ONNX matches PyTorch")


if __name__ == "__main__":
    main()
