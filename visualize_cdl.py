import matplotlib.pyplot as plt
import segmentation_models_pytorch as smp
import torch

from torchgeo.datamodules import Sentinel2CDLDataModule
from torchgeo.datasets import unbind_samples
import time

device = torch.device("cpu")

path = "/Users/yc/Downloads/log/checkpoints/epoch=9-step=96370.ckpt"
state_dict = torch.load(path, map_location=device)["state_dict"]
state_dict = {key.replace("model.", ""): value for key, value in state_dict.items()}


model = smp.Unet(encoder_name="resnet18", in_channels=13, classes=9)
model.to(device)
model.load_state_dict(state_dict, strict=True)

datamodule = Sentinel2CDLDataModule(
    crs="epsg:3857",
    batch_size=64,
    patch_size=256,
    cdl_paths="/Users/yc/Datasets/cdl_everything",
    sentinel2_paths="/Users/yc/Datasets/pub-956f3eb0f5974f37b9228e0a62f449bf.r2.dev/crop_type_mapping_sentinel2/cdl_2023_chipped",
)

datamodule.setup("test")

for batch in datamodule.test_dataloader():
    image = batch["image"]
    mask = batch["mask"]
    image.to(device)

    # Make a prediction
    start_time = time.time()
    print("start prediction")

    prediction = model(image)
    prediction = prediction.argmax(dim=1)
    prediction.detach().to("cpu")

    batch["prediction"] = prediction

    print("Finish prediction in {} seconds".format(time.time() - start_time))

    for sample in unbind_samples(batch):
        # Skip nodata pixels
        if 0 in sample["mask"]:
            continue

        # Skip boring images
        # if len(sample["mask"].unique()) < 3:
        #     continue

        # Plot
        datamodule.plot(sample)
        plt.show()



# Load weights
# path = "data/l7irish/checkpoint-epoch=26-val_loss=0.68.ckpt"
# state_dict = torch.load(path, map_location=device)["state_dict"]
# state_dict = {key.replace("model.", ""): value for key, value in state_dict.items()}

# Initialize model
# task = SemanticSegmentationTask(
#     loss="ce",
#     model="unet",
#     backbone="resnet18",
#     weights=weights,
#     in_channels=13,
#     num_classes=134,
#     num_filters=1,
#     ignore_index=0,
#     lr=0.001,
#     freeze_backbone=True,
# )
