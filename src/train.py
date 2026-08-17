import os
import json
import sys
import yaml
import torch
import torch.nn as nn
from dataset import get_dataloaders
from model import ImageClassifierCNN

def load_config(config_path="configs/training_config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def log_metrics_jsonl(epoch, loss, accuracy):
    # Structured standard output console stream formatted as JSON lines
    log_data = {"epoch": epoch, "loss": round(loss, 4), "accuracy": round(accuracy, 4)}
    sys.stdout.write(json.dumps(log_data) + "\n")
    sys.stdout.flush()

def train_pipeline():
    config = load_config()
    os.makedirs(config['training']['save_dir'], exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_loader, test_loader = get_dataloaders(
        batch_size=config['data']['batch_size'],
        num_workers=config['data']['num_workers']
    )

    model = ImageClassifierCNN(num_classes=config['model']['num_classes']).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config['training']['learning_rate'])

    best_loss = float('inf')
    patience_counter = 0
    checkpoint_path = os.path.join(config['training']['save_dir'], config['training']['checkpoint_name'])

    for epoch in range(1, config['training']['epochs'] + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        epoch_loss = running_loss / total
        epoch_acc = (correct / total) * 100
        
        # Log to stdout in structured format (JSON lines)
        log_metrics_jsonl(epoch, epoch_loss, epoch_acc)

        # Early Stopping check
        if epoch_loss < best_loss:
            best_loss = epoch_loss
            patience_counter = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            patience_counter += 1
            if patience_counter >= config['training']['patience']:
                sys.stdout.write(json.dumps({"info": f"Early stopping triggered at epoch {epoch}"}) + "\n")
                break

if __name__ == "__main__":
    train_pipeline()
