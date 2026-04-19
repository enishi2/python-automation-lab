from pathlib import Path
import shutil

# Dicionário que mapeia: "nome da pasta" → [extensões que pertencem a ela]
CATEGORIAS = {
    "Imagens":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documentos":   [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Videos":       [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio":        [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Compactados":  [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programas":    [".exe", ".msi", ".dmg", ".pkg"],
    "Codigo":       [".py", ".js", ".html", ".css", ".json", ".xml"],
}

#MONTA O CAMINHO DOS DOWNLOADS
pasta_downloads = Path.home() / "Downloads"

#CRIA UM DICIONÁRIO INVERTIDO PARA BUSCA RÁPIDA
extensao_para_pasta = {}
for nome_pasta, extensoes in CATEGORIAS.items():
    for ext in extensoes:
        extensao_para_pasta[ext] = nome_pasta

#PERCORRE OS ARQUIVOS DA PASTA

movidos = 0
ignorados = 0

# Pula subpastas (só queremos arquivos) = se não for arquivo, continua/verifica o proximo
for arquivo in pasta_downloads.iterdir():
    if not arquivo.is_file():
        continue

    # Pega a extensão em minúsculo: ".PDF" → ".pdf"
    extensao = arquivo.suffix.lower()

    # Descobre qual pasta destino usar (ou "Outros" se não souber)
    pasta_destino_nome = extensao_para_pasta.get(extensao, "Outros")

    # Monta o caminho completo da pasta destino
    pasta_destino = pasta_downloads / pasta_destino_nome

    #CRIA A PASTA SE NÃO EXISTIR
    pasta_destino.mkdir(exist_ok=True)
    # exist_ok=True → não dá erro se a pasta já existir

    #MOVE O ARQUIVO
    destino_final = pasta_destino / arquivo.name

    # Evita sobrescrever arquivos com mesmo nome!
    if destino_final.exists():
        print(f"⚠️  Já existe, pulando: {arquivo.name}")
        ignorados += 1
        continue

    shutil.move(str(arquivo), str(destino_final))
    print(f"✅ Movido: {arquivo.name}  →  {pasta_destino_nome}/")
    movidos += 1

# RESUMO FINAL
print(f"\n Concluído! {movidos} arquivos organizados, {ignorados} ignorados.")




