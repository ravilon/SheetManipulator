# 📊 SheetManager - CSV Splitter

**SheetManager** é uma ferramenta desktop desenvolvida em Python para facilitar o gerenciamento de grandes volumes de dados. Ela permite dividir arquivos CSV gigantescos (com milhões de linhas) em arquivos menores, mantendo os cabeçalhos originais e oferecendo saída nos formatos **CSV** ou **Excel (XLSX)**.

O diferencial desta ferramenta é a capacidade de lidar com campos de texto extremamente longos e a detecção automática de delimitadores (`,` ou `;`), garantindo que o arquivo Excel gerado já venha formatado corretamente em colunas.

## ✨ Funcionalidades

- **Divisão Inteligente:** escolha dividir por quantidade total de arquivos ou por um número fixo de linhas por arquivo.
- **Suporte a Grandes Campos:** configurado para processar células que excedem o limite padrão do Python (erro de *field limit*).
- **Detecção Automática:** identifica se o seu CSV original usa vírgula ou ponto e vírgula.
- **Saída Formatada:** gera arquivos `.xlsx` reais, com colunas separadas e prontos para análise.
- **Compactação Automática:** gera um arquivo `.zip` contendo todas as partes divididas para facilitar o compartilhamento.
- **Interface Intuitiva:** interface gráfica (GUI) simples e amigável.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior instalado.
- Ambiente virtual (recomendado).

### Instalação

1. Clone o repositório ou baixe os arquivos.
2. Crie e ative seu ambiente virtual:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

### Execução

Para abrir a interface gráfica, execute:

```powershell
python app.py
```

## 📦 Gerando o Executável (.exe)

Se você deseja transformar o script em um aplicativo independente para Windows:

1. Instale o PyInstaller:

```powershell
pip install pyinstaller
```

2. Gere o executável:

```powershell
pyinstaller --onefile --windowed --name="SheetManager" app.py
```

O arquivo `.exe` será gerado na pasta `dist/`.

## 🛠️ Tecnologias Utilizadas

- **Python**: linguagem base.
- **Tkinter**: interface gráfica nativa.
- **Openpyxl**: manipulação e geração de arquivos Excel.
- **Threading**: para garantir que a interface não trave durante o processamento de arquivos pesados.

## 📝 Estrutura do Projeto

```text
SheetManager/
├── app.py              # Código principal da aplicação
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação
└── .venv/              # Ambiente virtual (não incluído no versionamento)
```

## ⚠️ Limites Importantes

- **Excel (XLSX):** o limite máximo de linhas do Excel é de **1.048.576**. O aplicativo avisará se você tentar criar um arquivo Excel que exceda esse limite. Para arquivos maiores, utilize a saída em **CSV**.

---

Desenvolvido para otimizar o fluxo de trabalho com análise de dados.
