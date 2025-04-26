# Experimentos de Reconhecimento Facial com SVM, CNN e PCA

Este projeto faz parte de uma pesquisa acadêmica envolvendo experimentos com modelos de Machine Learning (SVM) e Deep Learning (CNN), aplicados a reconhecimento facial utilizando os datasets **JAFFE**, **CK+** e **FER-2013**.

Os datasets foram organizados na pasta `datasets/`, contendo:

- **ck+/**: Imagens do dataset Extended Cohn-Kanade (CK+).
- **FER2013/**: Imagens convertidas do dataset FER-2013.
- **jaffe/**: Imagens do dataset JAFFE.

Além dos datasets brutos, o projeto conta com a subpasta `data_scince_codes/`, que contém scripts Python para preparação e limpeza dos dados:

- `separa em pastas.py`: Organização das imagens em diretórios por classe de expressão facial.
- `transformaCSV_Png.py`: Conversão de datasets baseados em `.csv` (como o FER2013) para imagens `.png`.

Adicionalmente, dentro de `datasets/` estão disponíveis os arquivos:

- `links dos datasets.txt`: Contém os links oficiais para download dos datasets utilizados.
- `o que foi feito.txt`: Descrição detalhada das etapas realizadas na limpeza e preparação dos dados.

Os resultados experimentais são armazenados automaticamente em um banco de dados SQLite (`resultados.db`) e exportados em formato `.csv` (`resultados_experimentos.csv`) para posterior análise estatística e comparação de desempenho dos modelos.

---

## 📦 Tecnologias Utilizadas

- Python 3.10
- Scikit-learn
- PyTorch (para CNNs)
- PCA
- SQLite3
- Pandas
- Docker (para reprodutibilidade)

---

## 📁 Estrutura do Projeto

```bash
meu_projeto/
├── Dockerfile
├── main_cnn.py
├── main_svm.py
├── README.md
├── requirements.txt
├── resultados.db
├── datasets/
│   ├── ck+/
│   ├── FER2013/
│   ├── jaffe/
│   ├── data_scince_codes/
│   │   ├── separa em pastas.py
│   │   └── transformaCSV_Png.py
│   ├── links dos datasets.txt
│   └── o que foi feito.txt
├── modules/
│   ├── __pycache__/
│   │   └── db_logger.cpython-313.pyc
│   ├── db_logger.py
│   ├── exportador.py
│   ├── monitoramento.py
│   └── pipeline_svm.py
```