# Organizador Vistorias de Campo Ambiental
Código em Python para padronização e organização automática de pastas de vistorias de campo.

---

## Visão Geral do Projeto
1. **`manin.py`**: Código principal, responsável pela padronização e movimentação de pastas;
2. **`RH3_2024.py`**: Código auxiliar focando exclusivamente na pasta 2024 da RH III, que possui uma estrutura diferente das demais;
3. **`desfazer.py`**: Código de segurança para devolver reverter as movimentações caso necessário.

---

## Código Auxiliar - RH3_2024.py:

### Problema Encontrado:
A estrutura da pasta da *RHIII em 2024* difere das demais em relação da organização das pastas, pois não há pastas separando frentes manuais e mecânicas.

* **Frentes Manuais**: Barra do Piraí - córrego dos Santanas (Manual) - Finalizado
* **Frentes Mecânicas**: Piraí - Ribeirão Caximbau - Finalizado

Como o script principal (`main.py`) não funcionaria corretamente nessa estrutura específica, o `RH3_2024.py` atua como um pré-tratamento.

---

## Código Principal - main.py

### Etapas do processo:
* **1. Padronização:** Limpeza e tratamento dos nomes dos municípios.
* **2. Classificação:** Agrupamento por tipo de vistoria (manual ou mecânico).
* **3. Estruturação:** Criação do modelo padrão de subpastas.
* **4. Hierarquia Geográfica:** Separação na estrutura Município (pasta principal) --> Corpo Hídrico (subpasta).
* **5. Movimentação:** Reorganização final dos documentos dentro da nova estrutura.

* Nota: A varredura e a movimentação são aplicadas exclusivamente às pastas de período no formato 
DD.MM.AAAA a DD.MM.AAAA, 2024 e 2025 e ignora as demais pastas do diretório.


### Estrutura de Destino Esperada
```text
LIMPARIO 2024 (M:)/
└── [Pasta de Vistoria de Campo]/
    └── [Município]/
         ├── Cartão Técnico de Obra/
         │       └── (Arquivos/Subpastas originais)
         ├── Manual/
         │    ├── [Corpo Hídrico]/
         │    │    ├── 01 - Docs. INEA
         │    │    ├── 02 - Boletins de Vistoria
         │    │    ├── 03 - Fotos
         │    │    ├── 04 - KMZ
         │    │    ├── 05 - PDF Medição
         │    │    └── 06 - Obsoleto *
         │    ├── Vacall/ *
         │    │    ├── 01 - Docs. INEA
         │    │    ├── 02 - Boletins de Vistoria
         │    │    ├── 03 - Fotos
         │    │    └── 04 - Obsoleto *
         │    └── Socioambiental/ *
         │         ├── 01 - Docs. INEA
         │         ├── 02 - Boletins de Vistoria
         │         ├── 03 - Fotos
         │         └── 04 - Obsoleto *
         └── Mecânico/
              └── [Corpo Hídrico]/
                  ├── 01 - Docs. INEA
                  ├── 02 - Boletins de Vistoria
                  ├── 03 - Fotos
                  ├── 04 - KMZ
                  ├── 05 - PDF Medição
                  ├── 06 - Apontamento *
                  └── 07 - Obsoleto *
```
* Notas sobre a estrutura:
- **Pastas Condicionais:** Os diretórios marcados com asterisco (*), assim como subpastas específicas como Vacall ou Socioambiental, são gerados dinamicamente apenas se houver documentos correspondentes detectados durante o processamento. Caso contrário, são omitidos.

---

## Código de Segurança - desfazer.py

Tem o objetivo de garantir a segurança operacional do projeto. Caso ocorra qualquer inconsistência na organização automática realizada pelo `main.py` ou pelo `RH3_2024.py`, este script utiliza o registro gerado para **restaurar os arquivos e pastas aos seus diretórios originais**.

### Modo de Funcionamento
1. **Leitura do Histórico:** O script lê o arquivo `historico_movimentacoes.json`, que armazena o mapeamento exato de cada origem e destino de item movimentado.
2. **Processo Inverso:** Ele percorre os registros de forma decrescente, movendo os arquivos de volta para as pastas de onde vieram originalmente.
3. **Validação de Segurança:** Valida a existência dos caminhos para evitar erros de diretório inexistente durante a restauração.
