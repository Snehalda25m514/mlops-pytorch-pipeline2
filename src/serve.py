import io
import os
import yaml
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from model import ImageClassifierCNN

app = FastAPI(title="MLOps PyTorch Inference Server")

# Load global definitions
config = yaml.safe_load(open("configs/training_config.yaml", "r"))
checkpoint_path = os.path.join(config['training']['save_dir'], config['training']['checkpoint_name'])

# Instantiate and check global model state
model = ImageClassifierCNN(num_classes=config['model']['num_classes'])
model_loaded = False

if os.path.exists(checkpoint_path):
    model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu'), weights_only=True))
    model.eval()
    model_loaded = True
else:
    # Safe evaluation fallback logic
    model.eval()

# CIFAR-10 evaluation transform mapping parameters
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

@app.get("/health")
def health_check():
    if model_loaded:
        return {"status": "healthy", "model_loaded": True}, 200
    raise HTTPException(status_code=500, detail="Inference parameters unassigned.")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model is down or uninitialized.")
    
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        tensor = transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(tensor)
            probabilities = F.softmax(outputs, dim=1).squeeze().tolist()
            
        return {"probabilities": probabilities}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
