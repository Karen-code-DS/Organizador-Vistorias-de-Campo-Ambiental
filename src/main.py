import json              # Permite contruir um histórico para as alterações
import os                # Interagir com o sistema operacional do computador
import re                # Identificar pastas com padrão de caracteres. EX.: data (AAAA.MM.DD)
import shutil            # Manipular arquivos e pastas
from pathlib import Path # Manipular caminhos de arquivos e pastas
import unicodedata       # Consultar e verificar caracteres

# _________________________________________________________________________________________________________________________

"""
ORGANIZADOR DE ARQUIVOS DE VISTORIA:

Estrutura arquivos de vistorias de campo em pastas padronizadas por município garantindo a padronizalçao
e organização dos documetos.

Etapas do processo:
  1. Padronização: Limpeza e tratamento dos nomes dos municípios.
  2. Classificação: Agrupamento por tipo de vistoria (manual ou mecânico).
  3. Estruturação: Criação do modelo padrão de subpastas.
  4. Hierarquia Geográfica: Separação na estrutura Município (pasta principal) --> Corpo Hídrico (subpasta).
  5. Movimentação: Reorganização final dos documentos dentro da nova estrutura.

* Nota: A varredura e a movimentação são aplicadas exclusivamente às pastas de período no formato 
DD.MM.AAAA a DD.MM.AAAA, 2024 e 2025 e ignora as demais pastas do diretório.
  
"""

# _________________________________________________________________________________________________________________________
#                                                 SELECIONANDO O DIRETÓRIO
# _________________________________________________________________________________________________________________________

base_dir = Path(r"M:\001 - Vistorias de Campo\01 - Vistorias de Campo RH I e II")
# _________________________________________________________________________________________________________________________
#                                         PADRONIZAÇÃO DA NOMENCLATURA DOS MUNICÍPIOS
# _________________________________________________________________________________________________________________________

nome_padrao_municipios = {
    # RH I e II -----------------------------------------------
    "eng. p. frontin"        : "Engenheiro Paulo de Frontin"  ,
    "eng p. frontin"         : "Engenheiro Paulo de Frontin"  ,
    "engenheiro p. frontin"  : "Engenheiro Paulo de Frontin"  ,
    "eng. paulo frotin"      : "Engenheiro Paulo de Frontin"  ,
    "engenheiro paulo f."    : "Engenheiro Paulo de Frontin"  ,
    "engenheiro paulo frotin": "Engenheiro Paulo de Frontin"  ,
    "eng. paulo de frontin"  : "Engenheiro Paulo de Frontin"  ,
    "eng. paulo de frotin"   : "Engenheiro Paulo de Frontin"  ,
    "eng. p. de frontin"     : "Engenheiro Paulo de Frontin"  ,
    "eng. pedreira"          : "Engenheiro Pedreira"          ,
    "eng pedreira"           : "Engenheiro Pedreira"          ,
    "pirai"                  : 'Piraí'                        ,  # Correção de acentuação
    "barra do pirai"         : 'Barra do Piraí'               ,  # Correção de acentuação
    "itaguai"                : "Itaguaí"                      ,  # Correção de acentuação
    "nova iguacu"            : "Nova Iguaçu"                  ,  # Correção de acentuação
    "seropedica"             : "Seropédica"                   ,  # Correção de acentuação
    "japerí"                 : "Japeri"                       ,  # Correção de acentuação
    # RH III --------------------------------------------------
    "c. levy gasparian "     : "Comendador Levy Gasparian"    ,
    "levy gasparian"         : "Comendador Levy Gasparian"    ,
    "c. l. gasparian"        : "Comendador Levy Gasparian"    ,
    "tres rios"              : "Três Rios"                    ,  # Correção de acentuação
    "valenca"                : "Valença"                      ,  # Correção de acentuação
    "paty alferes"           : "Paty do Alferes"              ,
    "paty de alferes"        : "Paty do Alferes"              ,
    "p. alferes"             : "Paty do Alferes"              ,
    "p. de alferes"          : "Paty do Alferes"              , 
    "p. do alferes"          : "Paty do Alferes"              ,
    "p alferes"              : "Paty do Alferes"              ,
    "p de alferes"           : "Paty do Alferes"              , 
    "p do alferes"           : "Paty do Alferes"              ,
    "p dos alferes"          : "Paty do Alferes"              ,
    "paraiba do sul"         : "Paraíba do Sul"               ,      
    # RH IV e VII ---------------------------------------------
    "n. friburgo"            : "Nova Friburgo"                ,
    "n friburgo"             : "Nova Friburgo"                ,
    "sjvrp"                  : "São José do Vale do Rio Preto",
    "são j. v. r. preto"     : "São José do Vale do Rio Preto",
    "s. j. v. do rio preto"  : "São José do Vale do Rio Preto",
    "petropolis"             : "Petrópolis"                   ,  # Correção de acentuação
    "sta. maria madalena"    : "Santa Maria Madalena"         ,
    "santa m. madalena"      : "Santa Maria Madalena"         ,
    "snt. m. madalena"       : "Santa Maria Madalena"         ,  
    "s. maria madalena"      : "Santa Maria Madalena"         ,  
    "teresopolis"            : "Teresópolis"                  ,  # Correção de acentuação
    "traj. de moraes"        : "Trajano de Moraes"            ,
    "s. s. do alto"          : "São Sebastião do Alto"        ,
    "s.s. do alto"           : "São Sebastião do Alto"        ,
    "s. s. alto"             : "São Sebastião do Alto"        ,
    "s sebastião do alto"    : "São Sebastião do Alto"        ,
    "s. sebastião do alto"   : "São Sebastião do Alto"        ,
    "são s. do alto"         : "São Sebastião do Alto"        ,
    "são seb. do alto"       : "São Sebastião do Alto"        ,
    "b. jardim"              : "Bom Jardim"                   ,   
    "d. barras"              : "Duas Barras"                  ,
    "p. de alferes"          : "Paty de Alferes"              ,
    # RH V ----------------------------------------------------
    "b. roxo"                : "Belford Roxo"                 ,
    "b roxo"                 : "Belford Roxo"                 ,
    "belf. roxo"             : "Belford Roxo"                 ,
    "belf roxo"              : "Belford Roxo"                 ,
    "belf.roxo"              : "Belford Roxo"                 ,
    "dq. caxias"             : "Duque de Caxias"              ,
    "d. caxias"              : "Duque de Caxias"              ,
    "dq caxias"              : "Duque de Caxias"              ,
    "d caxias"               : "Duque de Caxias"              ,
    "itaborai"               : "Itaboraí"                     ,  # Correção de acentuação
    "rj"                     : "Rio de Janeiro"               ,  
    "c. macacu"              : "Cachoeiras de Macacu"         ,
    "c. de macacu"           : "Cachoeiras de Macacu"         ,
    "cachoeiras de m"        : "Cachoeiras de Macacu"         ,
    "n iguaçu"               : "Nova Iguaçu"                  ,
    "n. iguaçu"              : "Nova Iguaçu"                  ,
    "sjm"                    : "São João de Meriti"           ,
    # RH VI e VIII ---------------------------------------------
    "spa"                    : "São Pedro da Aldeia"          ,
    "s. p. a"                : "São Pedro da Aldeia"          ,
    "s.p.a"                  : "São Pedro da Aldeia"          ,
    "buzios"                 : "Armação dos Búzios"           ,
    "búzios"                 : "Armação dos Búzios"           ,
    # RH IX ---------------------------------------------------
    "b j do itabapoana"      : "Bom Jesus do Itabapoana"      ,
    "b. j. do itabapoana"    : "Bom Jesus do Itabapoana"      ,
    "card moreira"           : "Cardoso Moreira"              ,
    "card. moreira"          : "Cardoso Moreira"              ,
    "s a padua"              : "Santo Antônio de Pádua"       ,
    "s. a. padua"            : "Santo Antônio de Pádua"       ,
    "s a pádua"              : "Santo Antônio de Pádua"       ,
    "s. a. pádua"            : "Santo Antônio de Pádua"       ,
    "s fidélis"              : "São Fidélis"                  ,
    "s. fidélis"             : "São Fidélis"                  ,
    "l do muriae"            : "Laje do Muriaé"               ,
    "l. do muriae"           : "Laje do Muriaé"               ,
    "l do muriaé"            : "Laje do Muriaé"               ,
    "l. do muriaé"           : "Laje do Muriaé"               ,
    "s j ubá"                : "São José do Ubá"              ,
    "s. j. ubá"              : "São José do Ubá"              ,
    "s f de itabapoana"      : "São Fidélis de Itabapoana"    ,
    "s. f. de itabapoana"    : "São Fidélis de Itabapoana"    ,
    "s j da barra"           : "São João da Barra"            ,
    "s. j. da barra"         : "São João da Barra"            ,
    "s.j. da barra"          : "São João da Barra"            ,
    "c de macabu"            : "Campos de Macabu"             ,
    "c. de macabu"           : "Campos de Macabu"             ,
    "conc de macabu"         : "Campos de Macabu"             ,
    "conc. de macabu"        : "Campos de Macabu"             ,
    "s m madalena"           : "Santa Maria Madalena"         ,
    "s. m. madalena"         : "Santa Maria Madalena"         ,
    "campos"                 : "Campos dos Goytacazes"        ,
}

# _________________________________________________________________________________________________________________________
#                                                  ESTRUTURA E PADRONIZAÇÃO DAS PASTAS 
# _________________________________________________________________________________________________________________________

tipos_vistoria = ["Manual", "Mecânico", "Mecanico", "Mecânica"]

mapeamento_subpastas = {
    "fotos"                     : "Fotos"                 ,
    "foto"                      : "Fotos"                 ,
    "imagens"                   : "Fotos"                 ,
    "imagem"                    : "Fotos"                 ,
    # -------------------------------------------------------
    "boletins"                  : "Boletins de Vistoria"  ,
    "boletim"                   : "Boletins de Vistoria"  ,
    "boletim de vistoria prévia": "Boletins de Vistoria"  ,
    "boletim de vistoria previa": "Boletins de Vistoria"  ,
    "vistoria prévia"           : "Boletins de Vistoria"  ,
    # -------------------------------------------------------
    "recebidos inea"            : "Docs. INEA"            ,
    "recebidos"                 : "Docs. INEA"            ,    
    # -------------------------------------------------------
    "boletins de inspeção"      : "Boletins de Vistoria"  ,
    "boletim de inspeção"       : "Boletins de Vistoria"  ,
    "vistorias de campo"        : "Boletins de Vistoria"  ,
    "vistoria de campo"         : "Boletins de Vistoria"  ,
    # -------------------------------------------------------
    "kmz": "KMZ"                                          ,
    "kml": "KMZ"                                          ,
    # -------------------------------------------------------
    "recebidos"                 : "Docs. INEA"            , 
    "recebidos inea"            : "Docs. INEA"            ,
    "docs. inea"                : "Docs. INEA"            , 
    "docs inea"                 : "Docs. INEA"            ,   
    "inea"                      : "Docs. INEA"            ,
    "estudo previo"             : "Docs. INEA"            ,
    "estudo prévio"             : "Docs. INEA"            ,
    "ordens de serviço"         : "Docs. INEA"            ,
    "ordem de serviço"          : "Docs. INEA"            ,
    "ordem de servico"          : "Docs. INEA"            ,
    # -------------------------------------------------------
    "medição"                   : "PDF Medição"           ,
    "medicao"                   : "PDF Medição"           ,
    "equipamentos por rh"       : "PDF Medição"           ,
    "controle medição"          : "PDF Medição"           ,
    # -------------------------------------------------------
    "apontamentos"              : "Apontamento"           ,
    "apontamento"               : "Apontamento"           ,
    # -------------------------------------------------------
    "cartão de obras"           : "Cartão Técnico de Obra",
    "cartao de obras"           : "Cartão Técnico de Obra",
    "cartão de obra"            : "Cartão Técnico de Obra",
    "cartao de obra"            : "Cartão Técnico de Obra",
    "cartão técnico de obras"   : "Cartão Técnico de Obra",
    "cartão técnico de obra"    : "Cartão Técnico de Obra",
    "placas de obra"            : "Cartão Técnico de Obra",
    "placa de obra"             : "Cartão Técnico de Obra",
    # -------------------------------------------------------
    "controle boletins"         : "Obsoleto"              ,
    "controle boletim"          : "Obsoleto"              ,
    "volante"                   : "Obsoleto"              ,
    "arquivos"                  : "Obsoleto"              ,
    "arquivo"                   : "Obsoleto"              ,
    "obsoletos"                 : "Obsoleto"              ,
    "obsoleto"                  : "Obsoleto"              ,
    # SIGLAS ------------------------------------------------
    "btv"                       : "Boletins de Vistoria"  ,
    "bvp"                       : "Boletins de Vistoria"  ,
    "bv"                        : "Boletins de Vistoria"  ,
    "vp"                        : "Boletins de Vistoria"  ,
    "os"                        : "Docs. INEA"            , # os == ordem de serviço
    "bi"                        : "Boletins de Vistoria"  ,
    "ep"                        : "Docs. INEA"            ,
    "cto"                       : "Cartão Técnico de Obra",
    "co"                        : "Cartão Técnico de Obra",
    "pdf"                       : "Obsoleto"              ,
    "eng"                       : "Obsoleto"              ,
}

categorias_obrigatorias = [
    "Docs. INEA",
    "Boletins de Vistoria",
    "Fotos",
    "KMZ",
    "PDF Medição",
]

# _________________________________________________________________________________________________________________________
#                                       FUNÇÕES AUXILIARES DE PROCESSAMENTO
# _________________________________________________________________________________________________________________________

""" 00. Função auxiliar para remover acentos de textos --> Será usada para remover o acentos indevidos. """
def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# -------------------------------------------------------------------------------------------------------------------------
""" 01. Função que padroniza os nomes dos municípios. Caso o nome não encaixar nas pastas anteriormente definidas,
ou for nome vazio/nulo, o script criatá uma pasta chamada "A Classificar". """
def padronizar_municipio(nome):
    if not nome or not nome.strip():
        return "A Classificar"

    nome_limpo = nome.lower().strip()
    nome_sem_ponto = nome_limpo.replace(".", "")

    for chave, nome_oficial in nome_padrao_municipios.items():
        chave_limpa = chave.lower().strip()
        chave_sem_ponto = chave_limpa.replace(".", "")

        if (
            nome_limpo == chave_limpa
            or nome_sem_ponto == chave_sem_ponto
            or nome_limpo.startswith(chave_limpa)
        ):
            return nome_oficial

    return nome.strip().title()

# -------------------------------------------------------------------------------------------------------------------------
""" 02. Pdronização dos nomes das pastas de tipo de vistoria. """
def padronizar_tipo_vistoria(nome_tipo):
    if not nome_tipo:
        return "Manual"
    
    nome_limpo = nome_tipo.lower().strip()
    # Remove acentos e caracteres indesejados para comparação segura
    if any(m in nome_limpo for m in ["mecanic", "mecânic"]):
        return "Mecânico"
    return "Manual"

# -------------------------------------------------------------------------------------------------------------------------
""" 03. Define pastas em que vão acontecer o tratamento de dados (período "DD.MM.AAAA a DD.MM.AAAA", "2025" e "2024"). """
def pastas_validas(nome_pasta):
    if nome_pasta.isdigit() and len(nome_pasta) == 4:
        return True
    padrao_data = r"(\d{4}[\.\-_]\d{2}[\.\-_]\d{2}|\d{2}[\.\-_]\d{2}[\.\-_]\d{4})"
    return bool(re.search(padrao_data, nome_pasta))

# -------------------------------------------------------------------------------------------------------------------------
""" 04. Define a estutura das subpastas do corpo hídrico e socioambiental/vacall/emergencial(obsoleto). """
def obter_regras_pastas(tipos_vistoria, corpo_hidrico=""): # tipos_vistoria está sublinhado pois não chamamos ele na função
    ch_lower = corpo_hidrico.lower()
    if ch_lower in ["socioambiental", "vacall", "emergencial(obsoleto)"]:
        return {
            "Boletins de Vistoria": "01 - Boletim"   ,
            "Fotos"               : "02 - Fotos"     ,
            "KMZ"                 : "03 - KMZ"       ,
        }
    else:
        return {
            "Docs. INEA"          : "01 - Docs. INEA"          ,
            "Boletins de Vistoria": "02 - Boletins de Vistoria",
            "Fotos"               : "03 - Fotos"               ,
            "KMZ"                 : "04 - KMZ"                 ,
            "PDF Medição"         : "05 - PDF Medição"         ,
        }

# -------------------------------------------------------------------------------------------------------------------------
""" 05. Se exixstir pastas além das cinco principais, como obsoleto e/ou apontamento, essa pasta deve manter a orgem numérica. """
def obter_pasta_destino(destino_corpo, categoria_conceitual, regras_base):
    if categoria_conceitual in regras_base:
        nome_pasta = regras_base[categoria_conceitual]
    else:
        pasta_existente = None
        if destino_corpo.exists():
            for p in destino_corpo.iterdir():
                if p.is_dir() and categoria_conceitual.lower() in p.name.lower():
                    pasta_existente = p.name
                    break

        if pasta_existente:
            nome_pasta = pasta_existente
        else:
            maior_num = 0
            if destino_corpo.exists():
                for p in destino_corpo.iterdir():
                    if p.is_dir():
                        match = re.match(r"^(\d+)", p.name)
                        if match:
                            maior_num = max(maior_num, int(match.group(1)))

            proximo_num = maior_num + 1
            nome_pasta = f"{proximo_num:02d} - {categoria_conceitual}"

    return destino_corpo / nome_pasta

# -------------------------------------------------------------------------------------------------------------------------
""" 06. Move documento apenas se existir para evitar erro no programa. """
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
""" 07. Analisar todas as pastas do caminho relativo para definir a categoria correta."""
def identificar_categoria(caminho_relativo, arquivo_name):
    partes_caminho = [p.lower() for p in caminho_relativo.parts]

    # Checa primeiro os nomes das pastas no caminho (do diretório mais interno ao mais externo)
    # Exemplo: se o caminho for 'Fotos/10.05.2025/imagem.jpg', ele identifica 'fotos' na pasta pai.
    for parte in reversed(partes_caminho[:-1] if len(partes_caminho) > 1 else partes_caminho):
        palavras = re.findall(r'\b\w+\b', parte)
        
        for chave, nome_padrao in mapeamento_subpastas.items():
            # regra para siglas (palavras menor ou igual a três letras)
            if len(chave) <= 3:
                # Siglas curtas (ex: 'os', 'vp') exigem palavra inteira
                if chave in palavras:
                    return nome_padrao
            else:
                # Termos com mais letras como 'fotos', 'boletim', 'inea'
                if chave in parte:
                    return nome_padrao

    # Segurança extra (Fallback): se a pasta não tinha nome identificável, checa pela extensão
    ext = Path(arquivo_name).suffix.lower()
    if ext in [".jpeg", ".jpg", ".png", ".webp", ".heic"]:
        return "Fotos"
    if ext in [".kmz", ".kml"]:
        return "KMZ"

    return "Obsoleto"

# -------------------------------------------------------------------------------------------------------------------------
""" 08. Garante a esturura, percorre todos os arquivos, descobre a categoria, pasta de destino e executa a movimentação.  """
def processar_varredura_recursiva(subitem_origem, destino_corpo, tipo, corpo_hidrico, historico):
    regras_atuais = obter_regras_pastas(tipo, corpo_hidrico)

    # Garantir criação prévia das pastas estruturadas
    for cat, nome_p in regras_atuais.items():
        if cat != "Obsoleto":
            (destino_corpo / nome_p).mkdir(parents=True, exist_ok=True)

    # Varre todos os arquivos (sem limite de profundidade de pasta)
    for r_sub, _, arquivos in os.walk(subitem_origem):
        if not arquivos:
            continue

        caminho_r = Path(r_sub)
        rel_path = caminho_r.relative_to(subitem_origem)

        for arq in arquivos:
            caminho_arquivo_rel = rel_path / arq
            categoria_conceitual = identificar_categoria(caminho_arquivo_rel, arq)

            # Definir Cartão Técnico de Obra no mesmo nível que Manual e Mecânico
            if categoria_conceitual == "Cartão Técnico de Obra":
                pasta_destino_cat = base_dir / municipio / "Cartão Técnico de Obra"
            else:
                pasta_destino_cat = obter_pasta_destino(
                    destino_corpo, categoria_conceitual, regras_atuais
                )
            m = re.search(r"(\d{2}[\.\-_]\d{2}[\.\-_]\d{4}|\d{4}[\.\-_]\d{2}[\.\-_]\d{2})", str(rel_path))
            
            # Definir estutura da pasta "Fotos" 
            if m and categoria_conceitual == "Fotos":
                pasta_destino_final = pasta_destino_cat / m.group(1)
            else:
                pasta_destino_final = pasta_destino_cat

            mover_item_seguro(
                caminho_r / arq,
                pasta_destino_final / arq,
                historico
            )

# -------------------------------------------------------------------------------------------------------------------------

historico = []

# _________________________________________________________________________________________________________________________
#                                             VARREDURA PRINCIPAL
# _________________________________________________________________________________________________________________________

try:
    pastas_tipo_encontradas = []

    for raiz, diretorios, _ in os.walk(base_dir):
        caminho_raiz = Path(raiz)

        if caminho_raiz != base_dir and not pastas_validas(caminho_raiz.name):
            if any(caminho_raiz.name == m for m in nome_padrao_municipios.values()):
                diretorios.clear()
                continue

        for d in diretorios:
            if d in tipos_vistoria:
                pastas_tipo_encontradas.append(Path(raiz) / d)

    if not pastas_tipo_encontradas:
        pastas_tipo_encontradas = [base_dir]

    for pasta_tipo in pastas_tipo_encontradas:
        tipo = padronizar_tipo_vistoria(pasta_tipo.name) if pasta_tipo.name in tipos_vistoria else "Manual"

        for item in list(pasta_tipo.iterdir()):
            if not item.is_dir():
                continue

            if item.name in nome_padrao_municipios.values():
                continue

            nome_tratado = item.name.replace("—", "-").replace("–", "-")
            nome_tratado = re.sub(
                r"\s*(\((manual|mecânico|mecanico|mecanica|F|P|OS|VP|M)\)|[_-]\s*(finalizado|finalizada))",
                "",
                nome_tratado,
                flags=re.IGNORECASE,
            ).strip()

            palavras = nome_tratado.split()

            # 01 - VACALL e SOCIOAMBIENTAL
            nome_item_normalizado = remover_acentos(item.name.lower())
            if any(x in nome_item_normalizado for x in ["socioambiental", "vacall"]):
                corpo_hidrico = (
                    "Socioambiental" if "socioambiental" in nome_item_normalizado else "Vacall"
                )

                for subitem in list(item.iterdir()):
                    if subitem.is_dir():
                        municipio = padronizar_municipio(subitem.name)
                        destino_corpo = base_dir / municipio / tipo / corpo_hidrico
                        processar_varredura_recursiva(
                            subitem, destino_corpo, tipo, corpo_hidrico, historico
                        )

                shutil.rmtree(item, ignore_errors=True)
                continue

            # 02 - LIMPEZA URBANA / RELATÓRIOS EMERGENCIAIS
            elif palavras and palavras[0].lower() in ["limpeza", "emg", "emergencial", "emergenciais"]:
                raw_muni = (
                    nome_tratado.lower()
                    .replace("limpeza urbana", "")
                    .replace("limpeza"       , "")
                    .replace("relatórios"    , "")
                    .replace("relatorios"    , "")
                    .replace("relatório"     , "")
                    .replace("relatorio"     , "")
                    .replace("emg"           , "")
                    .replace("eng"           , "")
                    .replace("emergenciais"  , "")
                    .replace("emergencial"   , "")
                    .strip(" ---")
                )
                raw_muni = raw_muni.split("-", 1)[0].strip() if "-" in raw_muni else raw_muni.strip()
                municipio = padronizar_municipio(raw_muni)
                corpo_hidrico = "Emergencial (Obsoleto)"

            # 03 - SEPARADORES POR HÍFEN
            elif "-" in nome_tratado:
                partes = nome_tratado.split("-", 1)
                municipio = padronizar_municipio(partes[0])
                corpo_hidrico = partes[1].strip()

            # 04 - PASTAS SIMPLES
            else:
                municipio = padronizar_municipio(nome_tratado)
                corpo_hidrico = municipio

            destino_corpo = base_dir / municipio / tipo / corpo_hidrico
            processar_varredura_recursiva(item, destino_corpo, tipo, corpo_hidrico, historico)

            try:
                shutil.rmtree(item, ignore_errors=True)
            except OSError:
                pass

finally:
    caminho_historico = Path(__file__).parent / "historico_movimentacoes.json"
    with open(caminho_historico, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

print("Organização concluída com sucesso! Total de itens movidos:", len(historico))
