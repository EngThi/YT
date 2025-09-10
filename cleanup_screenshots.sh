#!/bin/bash
# Script para limpeza manual de screenshots temporários

SCREENSHOT_DIR="temp_screenshots"

echo "🧹 Limpeza manual de screenshots temporários..."

if [ -d "$SCREENSHOT_DIR" ]; then
    count=$(ls -1 "$SCREENSHOT_DIR"/*.png 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
        echo "📁 Encontrados $count screenshots em $SCREENSHOT_DIR"
        rm -f "$SCREENSHOT_DIR"/*.png
        echo "✅ Screenshots removidos com sucesso!"
    else
        echo "ℹ️ Nenhum screenshot encontrado para remover"
    fi
else
    echo "ℹ️ Diretório $SCREENSHOT_DIR não existe"
fi

echo "🏁 Limpeza concluída!"
