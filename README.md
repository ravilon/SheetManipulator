# 📊 SheetManager - CSV Splitter

**SheetManager** é uma ferramenta desktop profissional desenvolvida em Python para gerenciar grandes volumes de dados. Ela permite dividir arquivos CSV gigantescos (com milhões de linhas) em partes menores, mantendo os cabeçalhos originais e oferecendo saída formatada em **CSV** ou **Excel (XLSX)**.

Esta versão foi otimizada para estabilidade, utilizando o modo de distribuição em diretório para evitar conflitos de permissões do Windows e suporte a campos de texto extremamente longos.

## ✨ Funcionalidades

- **Divisão Inteligente:** Escolha dividir por quantidade total de arquivos ou por um número fixo de linhas por arquivo.
- **Suporte a Grandes Campos:** Configurado com `sys.maxsize` para processar células que excedem o limite padrão do Python.
- **Detecção Automática de Delimitador:** Identifica automaticamente se o CSV original utiliza vírgula (`,`) ou ponto e vírgula (`;`).
- **Saída Formatada para Excel:** Gera arquivos `.xlsx` reais com colunas separadas, prontos para uso imediato.
- **Compactação Automática:** Gera um arquivo `.zip` contendo todas as partes divididas para facilitar o compartilhamento.
- **Interface Moderna:** Interface gráfica (GUI) intuitiva com feedback de progresso.

## 🚀 Como Instalar (Usuário Final)

1. Baixe o arquivo `SheetManager_Setup_v1.0.0.exe` na aba de [Releases](#).
2. Execute o instalador e siga as instruções na tela.
3. O atalho será criado na sua **Área de Trabalho** e no **Menu Iniciar**.

## 🛠️ Desenvolvimento e Build

### Pré-requisitos
- Python 3.12 (Recomendado para estabilidade do executável).
- Ambiente virtual configurado.

### Instalação para Desenvolvedores
```powershell
# Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt