import os 
import shutil
import random
from sklearn.model_selection import train_test_split

# Caminhos corretos - VOLTA uma pasta a partir do script
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Configurações
source_ckplus = os.path.join(base_path, 'ck+')
source_jaffe = os.path.join(base_path, 'jaffe')
destino_mix =  os.path.join(base_path, 'mix_jaffe_ck')
random.seed(42)  # Para reprodutibilidade

# Calsses das emoções
classes = { 'anger', 'disgust', 'fear', 'happy', 'neutral','sadness', 'surprise'}

# Criar diretório de destino de treino e teste
def preparar_diretorios(destino):
    for tipo in ['train', 'test']:
        for classe in classes:
            caminho = os.path.join(destino, tipo, classe)
            os.makedirs(caminho, exist_ok=True)

# Função para copiar imagens de um diretório para outro
def coleta_imagens(pasta):
    imagens = []
    for classe in classes:
        caminho_classe = os.path.join(pasta, classe)
        for imagem in os.listdir(caminho_classe):
            imagens.append((os.path.join(caminho_classe, imagem), classe))
    return imagens

# Função para copiar as imagens para os diretórios
def copia_imagens(lista_imagens, destino_base, prefixo = ''):
    for idx, (caminho_imagem, classe) in enumerate(lista_imagens):
        # Define o caminho de destino
        nome_arquivo = f"{prefixo}_{idx}_{os.path.basename(caminho_imagem)}"
        destino_classe = os.path.join(destino_base, classe)
        # Criar pasta da classe se não existir
        os.makedirs(destino_classe, exist_ok=True)
        shutil.copy2(caminho_imagem, os.path.join(destino_classe, nome_arquivo))

# Função principal para executar o processo de cópia e divisão
def main():
    print("Preparando diretórios de destino...")
    preparar_diretorios(destino_mix)

    print("Coletando imagens do CK+...")
    ckplus_imagens = coleta_imagens(source_ckplus)

    print("Coletando imagens do JAFFE...")
    jaffe_imagens = coleta_imagens(source_jaffe)

    print("Balanceando CK+ para 213 imagens...")
    caminhos_ck, classes_ck = zip(*ckplus_imagens)
    caminhos_ck, _, classes_ck, _ = train_test_split(caminhos_ck, classes_ck, train_size=213, stratify=classes_ck, random_state=42)
    imagens_ckplus_balence = list(zip(caminhos_ck, classes_ck))
    
    print("Unindo CK+ e JAFFE...")
    imagens_unidas = jaffe_imagens + imagens_ckplus_balence

    print("Embaralhando imagens...")
    random.shuffle(imagens_unidas)

    print("Copiando imagens para o diretório de destino...")
    copia_imagens(imagens_unidas, destino_mix, prefixo='jaffe_and_ckplus')

    print("Processo concluído!", destino_mix)

if __name__ == "__main__":
    main()