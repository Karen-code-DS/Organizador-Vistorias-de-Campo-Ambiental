import pandas as pd
import os
import re
import shutil
from pathlib import Path
import json 

# _________________________________________________________________________________________________________________________

'''                        PRÉ TRATAMENTO DE DADOS PARA A PASTA 2024 DA RH III 

Problema encontrado: Estutura das pastas diferente das demais. Não há pastas separando as frentes
manuais e mecânicas.

ESTRUTURA ATUAL: ----------------------------------------------------------------------------------------------------------
  -> Para frentes manuais: Município - Corpo Hídrico (Manual) - Finaliado(a) ou Município - Corpo Hídrico (Manual)
  -> Para frentes mecanicas: Município - Corpo Hídrico - Finalizado(a)

ETAPAS DO PROCESSO: -------------------------------------------------------------------------------------------------------
  1) Separar as frentes manuais das mecânicas usando if e else. Se a frente tem "Manual" ou "manual" no nome
  ela será considerada manual, caso contrário, será mecânico.;
  2) Padronização do nome do município e pré estuturação das pastas, mantendo assim, igual a estutura das 
  outras pastas antes do tratamento; 
     OBS: nessa etapa é realizada a remoção de sufixos como (P), (F), (VP), (OS), (M), Finalizado(a), Manual e manual.

RESULTADO FINAL: ----------------------------------------------------------------------------------------------------------
LIMPARIO 2024 (M:)/
└── 02 - Vistorias de Campo RH III/
    └── 2024/
        └── [Período] (ex: 22.04.2024 a 21.05.2024)/
            ├── Manual/
            │   └── Município - Corpo Hídrico/
            │       └── (Arquivos/Subpastas originais)
            └── Mecânico/
                └── Município - Corpo Hídrico/
                    └── (Arquivos/Subpastas originais)

-> O Script retornará duas pastas (Manual e Mecânico) com suas respectivas frentes (formato Município - Corpo Hídrico) 
  dentro e sem sufixos. '''

# _________________________________________________________________________________________________________________________

""" Definir diretório """
base_dir = Path(r"M:\007 - Produção\Estagiários\Karen\teste_rh3_2024 -- OK")

""" Definir diretório teste"""
# base_dir = Path.home() / "Downloads" / "teste_rh3_2024"



#                                       FUNÇÕES AUXILIARES DE PROCESSAMENTO
# _________________________________________________________________________________________________________________________


""" 01. Define pastas em que vão acontecer o tratamento de dados (período "DD.MM.AAAA a DD.MM.AAAA", "2025" e "2024"). """
def pastas_validas(nome_pasta):
    if nome_pasta.isdigit() and len(nome_pasta) == 4:
        return True
    padrao_data = r"(\d{4}[\.\-_]\d{2}[\.\-_]\d{2}|\d{2}[\.\-_]\d{2}[\.\-_]\d{4})"
    return bool(re.search(padrao_data, nome_pasta))

# -------------------------------------------------------------------------------------------------------------------------
""" 02. Move documento apenas se existir para evitar erro no programa. """
def mover_item_seguro(origem, destino, historico_lista):
    origem_path = Path(origem).resolve()
    destino_path = Path(destino).resolve()

    if str(origem_path).lower() == str(destino_path).lower() or not origem_path.exists():
        return

    destino_path.parent.mkdir(parents=True, exist_ok=True)

    if destino_path.exists() and destino_path.is_file():
        destino_path.unlink()

    try:
        shutil.move(str(origem_path), str(destino_path))
        historico_lista.append({"origem": str(origem_path), "destino": str(destino_path)})
    except (PermissionError, OSError):
        try:
            if origem_path.is_dir():
                shutil.copytree(str(origem_path), str(destino_path), dirs_exist_ok=True)
                shutil.rmtree(str(origem_path), ignore_errors=True)
            else:
                shutil.copy2(str(origem_path), str(destino_path))
                origem_path.unlink()

            historico_lista.append({"origem": str(origem_path), "destino": str(destino_path)})
        except Exception as err:
            print(f"[ATENÇÃO] Não foi possível mover '{origem_path.name}': {err}")

# -------------------------------------------------------------------------------------------------------------------------

historico = []
        
        
#                                      PRÉ-VARREDURA EXCLUSIVA: RH III (Apenas pasta "2024")
# _________________________________________________________________________________________________________________________

""" LISTA: Pastas específicas em que o script deve decorrer """
pastas_alvo = [
    "22.04.2024 a 21.05.2024",
    "22.05.2024 a 21.06.2024",
    "22.06.2024 a 21.07.2024",
    "22.07.2024 a 21.08.2024",
    "22.08.2024 a 21.09.2024",
    "22.09.2024 a 21.10.2024",
    "22.10.2024 a 21.11.2024",
]

# -------------------------------------------------------------------------------------------------------------------------
""" DICIONÁRIO: Pradronizar nome dos tipos de vistoria"""
tipos_vistoria = ["Manual", "Mecânico", "Mecanico", "Mecânica", "Mecanica"]

# ------------------------------------------------------------------------------------------------------------------------
try:
    for raiz, diretorios, _ in os.walk(base_dir):
        caminho_atual = Path(raiz)
        
        """ Garante que vai encontrar a pasta 2024 dentro do caminho base. """
        if caminho_atual.name == "2024":            
            
            for pasta_periodo in list(caminho_atual.iterdir()):
                """ Realiza a varredura apenas nas pastas válidas, especificamente a 2024
                Só aceita as pastas pré definidas"""
                if not pasta_periodo.is_dir() or pasta_periodo.name not in pastas_alvo:
                    continue
 
                for item in list(pasta_periodo.iterdir()):
                    if not item.is_dir():
                        continue
                   
                    nome_item_lower = item.name.lower().strip()
                    if nome_item_lower in tipos_vistoria:
                        if tipos_vistoria[nome_item_lower] == "Mecânico" and item.name != "Mecânico":
                            destino_unificado = pasta_periodo / "Mecânico"
                            for sub in list(item.iterdir()):
                                mover_item_seguro(sub, destino_unificado / sub.name, historico)
                            shutil.rmtree(item, ignore_errors=True)
                        continue
                    
                    nome_lower = item.name.lower()
                    if "manual" in nome_lower:
                        tipo_vistoria_detectado = "Manual"
                    else:
                        tipo_vistoria_detectado = "Mecânico"
                        
                    nome_tratado = item.name.replace("—", "-").replace("–", "-")    
                    nome_limpo = re.sub(
                        r"\s*(\((manual|mecânico|mecanico|F|P|OS|VP|M)\)|[_-]\s*(finalizado|finalizada))",
                        "",
                        nome_tratado,
                        flags=re.IGNORECASE,
                    ).strip()
                        
                        
                    # tipo_vistoria_detectado = "Manual" if "manual" in item.name.lower() else "Mecânico"
                    # nome_tratado = item.name.replace("—", "-").replace("–", "-")
                    
                    # """ Remove termos específicos do nome da pasta. """
                    # nome_limpo = re.sub(
                    #     r"\s*(\((manual|mecânico|mecanico|F|P|OS|VP|M)\)|[_-]\s*(finalizado|finalizada))",
                    #     "",
                    #     nome_tratado,
                    #     flags=re.IGNORECASE,
                    # ).strip()
                    
                    """ Remove eventuais hífens ou espaços sobrantes na ponta do nome. """
                    nome_limpo = re.sub(r"[_-]\s*$", "", nome_limpo).strip()
                    pasta_formatada = nome_limpo
                    
                    """ Garantir caminho: 
                    2024 --> Período --> Manual/Mecânico. --> Municipio - Corpo Hídrico  """
                    destino_temp = pasta_periodo / tipo_vistoria_detectado / pasta_formatada
                    
                    """ Move o conteúdo mantendo a estrutura orginal da pasta. """
                    for sub_elem in list(item.iterdir()):
                        mover_item_seguro(sub_elem, destino_temp / sub_elem.name, historico)
                        
                    """ Remove a pasta de origem após esvaziar"""
                    try:
                        shutil.rmtree(item, ignore_errors=True)
                    except OSError:
                        pass

finally:
    caminho_historico = Path(__file__).parent / "historico_movimentacoes.json"
    with open(caminho_historico, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

print("Organização concluída com sucesso! Total de itens movidos:", len(historico))
    