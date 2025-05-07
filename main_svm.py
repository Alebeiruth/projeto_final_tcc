import os
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA 
from PIL import Image 
import time
import psutil

# Configuracoes
train_dir = "./datasets/ck+_LOSO/train"  # Pasta com os dados de treino
test_dir = "./datasets/ck+_LOSO/test"    # Pasta com os dados de teste
image_size = (48, 48)  # Tamanho das imagens
pca_components = 100  # Número de componentes principais para PCA

# Função para carregar imagens de um diretório
def carregar_imagens(diretorio):
    x = []
    y = []
    print(f"Carregando imagens de {diretorio}...")
    
    for label_name in os.listdir(diretorio):
        label_path = os.path.join(diretorio, label_name)
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
                    
    return np.array(x), np.array(y)

# Carrega dados de treino
x_train, y_train = carregar_imagens(train_dir)
print(f"Total de imagens de treino carregadas: {len(x_train)}")

# Carrega dados de teste
x_test, y_test = carregar_imagens(test_dir)
print(f"Total de imagens de teste carregadas: {len(x_test)}")

# Codificar labels - importante treinar o encoder com todas as labels possíveis
le = LabelEncoder()
# Combinar labels de treino e teste para garantir que todas as classes sejam consideradas
todas_labels = np.concatenate((y_train, y_test))
le.fit(todas_labels)
# Agora codificar separadamente
y_train_encoded = le.transform(y_train)
y_test_encoded = le.transform(y_test)

# Aplicar PCA
print("Aplicando PCA...")
pca = PCA(n_components=pca_components, whiten=True, random_state=42)
x_train_pca = pca.fit_transform(x_train)  # Fit e transform nos dados de treino
x_test_pca = pca.transform(x_test)  # Apenas transform nos dados de teste

# Treinar SVM
print("Treinando modelo SVM com PCA...")
model = SVC(kernel='linear', probability=True, random_state=42)
model.fit(x_train_pca, y_train_encoded)

# Avaliacao no conjunto de teste
print("Avaliação no conjunto de teste...")
y_pred = model.predict(x_test_pca)

print("Relatório de Classificação:")
print(classification_report(y_test_encoded, y_pred, target_names=le.classes_))

print("Matriz de Confusão:")
print(confusion_matrix(y_test_encoded, y_pred))

# Registro de desempenho
print(f"Quantidade de componentes PCA: {pca_components}")
print(f"Tamanho das imagens: {image_size}")
print(f"Uso de memória: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.2f} MB")