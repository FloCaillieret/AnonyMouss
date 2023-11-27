import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import pandas as pd
from sklearn.model_selection import train_test_split
import timm
from sklearn.metrics import classification_report
import warnings
from torchvision.datasets.folder import default_loader


num_classes = 33014

# Fonctions de perte et de l'optimiseur

train_losses = []
train_accuracies = []

num_epochs = 

# Passer en mode entraînement
.train()

for epoch in range(num_epochs):
    running_loss = 0.0
    correct_train = 0
    total_train = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = effnet(inputs)

        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(outputs.data, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()
    
    # Calcul de la perte moyenne sur l'époque
    epoch_loss_train = running_loss / len(train_loader)
    train_losses.append(epoch_loss_train)

    # Calcul de la précision
    accuracy_train = 100 * correct_train / total_train
    train_accuracies.append(accuracy_train)

    print(f"Époque [{epoch + 1}/{num_epochs}] - Perte (entraînement) : {epoch_loss_train:.4f} - Précision (entraînement) : {accuracy_train:.2f}%")


# Sauvegarder les données
result_data = pd.DataFrame({
    'train_loss': train_losses,
    'train_accuracy': train_accuracies
})
result_data.to_csv('training_results.csv', index=False)

print("Entraînement terminé.")

# Sauvegarder le modèle
