# Experimentos de Reconhecimento Facial com SVM, CNN e PCA

Este projeto faz parte de uma pesquisa acadêmica envolvendo experimentos com modelos de Machine Learning (SVM) e Deep Learning (CNN), aplicados a reconhecimento facial com os datasets JEFF, CK+ e FER-2013.

Os resultados são armazenados automaticamente em um banco de dados SQLite e exportados em formato `.csv` para posterior análise estatística.

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
├── requirements.txt
├── main_svm.py
├── resultados_experimentos.csv
├── resultados.db
└── modules/
    ├── __init__.py
    ├── pipeline_svm.py
    ├── db_logger.py
    ├── monitoramento.py
    └── exportador.py
```
