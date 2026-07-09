"""Export cat_model.pth to ONNX for OpenVINO Model Server.

Bakes preprocessing (x/255) and softmax into the graph so clients only send
raw RGB pixels (float32, 0-255, NCHW 1x3x224x224) and read back two
probabilities [cat_a, cat_b].
"""
import torch, torch.nn as nn
from torchvision import models

CLASSES = ["cat_a", "cat_b"]


class CatIDModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18()
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, len(CLASSES))

    def forward(self, x):
        # x: raw RGB pixels 0-255, shape (N, 3, 224, 224)
        x = x / 255.0
        # The current checkpoint was trained WITHOUT ImageNet Normalize()
        # (train.py uses ToTensor only), so none is applied here. If a future
        # retrain adds Normalize to the transforms, subtract mean
        # [0.485, 0.456, 0.406] and divide by std [0.229, 0.224, 0.225] here
        # to keep the "raw pixels in" contract for clients.
        return torch.softmax(self.backbone(x), dim=1)


def main():
    model = CatIDModel()
    model.backbone.load_state_dict(torch.load("cat_model.pth", map_location="cpu"))
    model.eval()

    dummy = torch.rand(1, 3, 224, 224) * 255
    torch.onnx.export(
        model, dummy, "model.onnx",
        opset_version=17,
        input_names=["image"],
        output_names=["probabilities"],
        dynamo=False,
    )
    print("Exported model.onnx")

    # Parity check: ONNX output must match PyTorch on the same input
    import onnxruntime as ort
    import numpy as np
    sess = ort.InferenceSession("model.onnx")
    x = (torch.rand(4, 1, 3, 224, 224) * 255)
    for i in range(4):
        with torch.no_grad():
            want = model(x[i]).numpy()
        got = sess.run(None, {"image": x[i].numpy()})[0]
        np.testing.assert_allclose(got, want, rtol=1e-3, atol=1e-5)
    print("Parity check passed: ONNX matches PyTorch")


if __name__ == "__main__":
    main()
