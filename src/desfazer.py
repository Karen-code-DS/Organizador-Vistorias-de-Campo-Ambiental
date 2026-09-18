import json
import shutil
from pathlib import Path

# 01. Selecione a mesma pasta base do script principal
base_dir = Path(r"M:\007 - Produção\Estagiários\Karen\teste_rh3_2024")

# 02. Localiza o arquivo de histórico
caminho_historico = Path(__file__).parent / "historico_movimentacoes.json"
if not caminho_historico.exists():
  print("[ERRO] Arquivo 'historico_movimentacoes.json' não foi encontrado!")
  exit()
with open(caminho_historico, "r", encoding="utf-8") as f:
  historico = json.load(f)

total_restaurados = 0

# 03. DEVOLVE OS ARQUIVOS PARA A ORIGEM
for item in reversed(historico):
  origem = Path(item["origem"])
  destino = Path(item["destino"])

  if destino.exists():
    origem.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(destino), str(origem))
    total_restaurados += 1

# 04. LIMPEZA DE PASTAS VAZIAS DENTRO DO BASE_DIR
pastas_removidas = 0

# 05. Percorre as pastas de baixo para cima (bottom-up) para apagar subpastas vazias primeiro
for pasta in sorted(
    [p for p in base_dir.rglob("*") if p.is_dir()],
    key=lambda p: len(p.parts),
    reverse=True,
):
  try:
    
# 06. rmdir() só apaga se estiver 100% vazia
    pasta.rmdir()
    pastas_removidas += 1
  except OSError:

# 07. Se a pasta contiver arquivos mantidos/originais, é ignorada com segurança
    pass

# 08. Retornar resultado das movimentações
print(
    f"Restauração concluída com sucesso!\n"
    f"--> Total de arquivos devolvidos: {total_restaurados}\n"
    f"--> Total de pastas vazias removidas: {pastas_removidas}"
)
