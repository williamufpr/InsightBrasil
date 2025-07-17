
#!/usr/bin/env bash

# === CONFIGURAÇÃO ===
REPO_URL="git@github-williamufpr:williamufpr/InsightBrasil.git"

echo "===> Clonando repositório em modo mirror para limpeza..."
git clone --mirror "$REPO_URL"

cd InsightBrasil.git || { echo "Falha ao entrar na pasta InsightBrasil.git"; exit 1; }

echo "===> Executando BFG para remover .RDataTmp e .venv..."
bfg --delete-files .RDataTmp
bfg --delete-folders .venv --no-blob-protection

echo "===> Limpando refs pendentes e objetos mortos..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "===> Enviando de volta ao GitHub com push forçado..."
git push --force

echo "===> Limpeza completa."
echo "Agora execute no SEU repositório local:"
echo "    git fetch origin"
echo "    git reset --hard origin/main"
echo "para alinhar seu repositório local ao histórico limpo no GitHub."


