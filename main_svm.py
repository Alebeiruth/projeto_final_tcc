import os
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from PIL import Image
import time
import psutil

# Configuracoes
dataset_dir = ".\datasets\jaffe"
image_size = (48, 48)  # Tamanho das imagens treinar 48x48 e 256x256
pca_components = 100  # Número de componentes principais para PCA

# Carrega imagens e labels
x = []
y = []

print("Carregando imagens...")

for label_name in os.listdir(dataset_dir):
    label_path = os.path.join(dataset_dir, label_name)
    if os.path.isdir(label_path):
        for img_file in os.listdir(label_path):
            img_path = os.path.join(label_path, img_file)
            try:
                img = Image.open(img_path)
                img = img.resize(image_size)  # Redimensiona a imagem
                img_array = np.array(img).ravel()
                x.append(img_array)
                y.append(label_name)
            except Exception as e:
                print(f"Erro ao processar {img_path}: {e}")

x = np.array(x)
y = np.array(y)
print(f"Total de imagens carregadas: {len(x)}")

# Codificar labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)


# Separa treino/teste
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42)

# Aplicar PCA
print("Aplicando PCA...")
pca = PCA(n_components=pca_components, whiten=True, random_state=42)
x_train_pca = pca.fit_transform(x_train)
x_test_pca = pca.transform(x_test)

# Treinar SVM
print("Treinando modelo SVM com PCA...")
model = SVC(kernel='linear', probability=True, random_state=42)
model.fit(x_train_pca, y_train)

# Avaliacao no conjunto de teste
print("Avaliação no conjunto de teste...")
y_pred = model.predict(x_test_pca)

print("Relatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

print("Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

# Avaliação com Cross-Validation
print("Avaliação com Cross-Validation (5 folds)...")
scores = cross_val_score(model, x_train_pca, y_train, cv=5)
print(f"Acurácia média na validação cruzada: {scores.mean():.4f} (+/- {scores.std():.4f})")