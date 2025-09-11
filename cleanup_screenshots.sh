#!/bin/bash
# Script Profissional para Limpeza de Screenshots e Dados Temporários
# YouTube Automation v2.0

set -e  # Sai em caso de erro

# Configurações
SCREENSHOT_DIR="temp_screenshots"
LOG_DIR="logs"
BROWSER_PROFILES_DIR="browser_profiles"
MAX_SCREENSHOTS=50
MAX_LOG_SIZE_MB=100
MAX_PROFILE_AGE_DAYS=30

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}=====================================================${NC}"
    echo -e "${BLUE}🧹 YOUTUBE AUTOMATION - LIMPEZA INTELIGENTE v2.0${NC}"
    echo -e "${BLUE}=====================================================${NC}"
}

print_section() {
    echo -e "
${YELLOW}📁 $1${NC}"
    echo "----------------------------------------"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para limpeza de screenshots
cleanup_screenshots() {
    print_section "LIMPEZA DE SCREENSHOTS"
    
    if [ ! -d "$SCREENSHOT_DIR" ]; then
        print_warning "Diretório de screenshots não encontrado: $SCREENSHOT_DIR"
        return
    fi
    
    # Conta screenshots
    screenshot_count=$(find "$SCREENSHOT_DIR" -name "*.png" 2>/dev/null | wc -l)
    
    if [ $screenshot_count -eq 0 ]; then
        print_warning "Nenhum screenshot encontrado"
        return
    fi
    
    echo "� Screenshots encontrados: $screenshot_count"
    
    # Se exceder o limite, remove os mais antigos
    if [ $screenshot_count -gt $MAX_SCREENSHOTS ]; then
        excess=$((screenshot_count - MAX_SCREENSHOTS))
        echo "🗑️  Removendo $excess screenshots mais antigos..."
        
        find "$SCREENSHOT_DIR" -name "*.png" -type f -printf '%T@ %p
' | 
        sort -n | head -$excess | cut -d' ' -f2- | 
        while read file; do
            rm -f "$file"
            echo "   Removido: $(basename "$file")"
        done
        
        print_success "Screenshots antigos removidos"
    else
        echo "✅ Quantidade de screenshots dentro do limite ($MAX_SCREENSHOTS)"
    fi
    
    # Opção interativa para limpeza manual
    if [ "$1" = "--interactive" ]; then
        echo -n "🗑️  Deseja remover TODOS os screenshots? (s/N): "
        read -r response
        if [[ "$response" =~ ^[sS]$ ]]; then
            rm -f "$SCREENSHOT_DIR"/*.png 2>/dev/null || true
            print_success "Todos os screenshots removidos"
        fi
    fi
}

# Função para limpeza de logs
cleanup_logs() {
    print_section "LIMPEZA DE LOGS"
    
    if [ ! -d "$LOG_DIR" ]; then
        print_warning "Diretório de logs não encontrado: $LOG_DIR"
        return
    fi
    
    # Verifica tamanho total dos logs
    total_size=$(du -sm "$LOG_DIR" 2>/dev/null | cut -f1)
    
    if [ -z "$total_size" ]; then
        total_size=0
    fi
    
    echo "📊 Tamanho total dos logs: ${total_size}MB"
    
    if [ $total_size -gt $MAX_LOG_SIZE_MB ]; then
        print_warning "Logs excedem limite de ${MAX_LOG_SIZE_MB}MB"
        
        # Remove logs de backup antigos
        find "$LOG_DIR" -name "*.log.*" -type f -mtime +7 -delete 2>/dev/null || true
        
        # Trunca logs principais se muito grandes
        for log_file in "$LOG_DIR"/*.log; do
            if [ -f "$log_file" ]; then
                file_size=$(stat -c%s "$log_file" 2>/dev/null || echo 0)
                file_size_mb=$((file_size / 1024 / 1024))
                
                if [ $file_size_mb -gt 10 ]; then
                    echo "🗜️  Truncando log grande: $(basename "$log_file") (${file_size_mb}MB)"
                    tail -n 1000 "$log_file" > "${log_file}.tmp"
                    mv "${log_file}.tmp" "$log_file"
                fi
            fi
        done
        
        print_success "Logs otimizados"
    else
        echo "✅ Tamanho dos logs dentro do limite"
    fi
}

# Função para limpeza de perfis antigos
cleanup_browser_profiles() {
    print_section "LIMPEZA DE PERFIS DE BROWSER"
    
    if [ ! -d "$BROWSER_PROFILES_DIR" ]; then
        print_warning "Diretório de perfis não encontrado: $BROWSER_PROFILES_DIR"
        return
    fi
    
    # Remove perfis muito antigos
    old_profiles=$(find "$BROWSER_PROFILES_DIR" -type d -mtime +$MAX_PROFILE_AGE_DAYS 2>/dev/null)
    
    if [ -n "$old_profiles" ]; then
        echo "🗑️  Removendo perfis antigos (>${MAX_PROFILE_AGE_DAYS} dias)..."
        echo "$old_profiles" | while read profile; do
            if [ "$profile" != "$BROWSER_PROFILES_DIR" ]; then
                rm -rf "$profile"
                echo "   Removido: $(basename "$profile")"
            fi
        done
        print_success "Perfis antigos removidos"
    else
        echo "✅ Nenhum perfil antigo encontrado"
    fi
    
    # Limpa caches dos perfis
    find "$BROWSER_PROFILES_DIR" -name "*Cache*" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$BROWSER_PROFILES_DIR" -name "*cache*" -type f -delete 2>/dev/null || true
    
    print_success "Caches de perfis limpos"
}

# Função para estatísticas do sistema
show_statistics() {
    print_section "ESTATÍSTICAS DO SISTEMA"
    
    # Screenshots
    if [ -d "$SCREENSHOT_DIR" ]; then
        screenshot_count=$(find "$SCREENSHOT_DIR" -name "*.png" 2>/dev/null | wc -l)
        screenshot_size=$(du -sh "$SCREENSHOT_DIR" 2>/dev/null | cut -f1)
        echo "📸 Screenshots: $screenshot_count arquivos ($screenshot_size)"
    fi
    
    # Logs
    if [ -d "$LOG_DIR" ]; then
        log_size=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
        log_files=$(find "$LOG_DIR" -name "*.log*" 2>/dev/null | wc -l)
        echo "📝 Logs: $log_files arquivos ($log_size)"
    fi
    
    # Perfis
    if [ -d "$BROWSER_PROFILES_DIR" ]; then
        profile_size=$(du -sh "$BROWSER_PROFILES_DIR" 2>/dev/null | cut -f1)
        profile_count=$(find "$BROWSER_PROFILES_DIR" -maxdepth 1 -type d 2>/dev/null | wc -l)
        echo "🌐 Perfis: $((profile_count - 1)) perfis ($profile_size)"
    fi
    
    # Espaço total
    total_size=$(du -sh . 2>/dev/null | cut -f1)
    echo "💾 Tamanho total do projeto: $total_size"
}

# Função de limpeza completa
full_cleanup() {
    print_section "LIMPEZA COMPLETA"
    
    cleanup_screenshots "$1"
    cleanup_logs
    cleanup_browser_profiles
    
    # Remove arquivos temporários diversos
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Limpeza completa finalizada"
}

# Função de ajuda
show_help() {
    echo "🧹 YouTube Automation - Script de Limpeza Inteligente"
    echo ""
    echo "Uso:"
    echo "  $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  --screenshots     Limpa apenas screenshots"
    echo "  --logs           Limpa apenas logs"
    echo "  --profiles       Limpa apenas perfis de browser"
    echo "  --stats          Mostra apenas estatísticas"
    echo "  --interactive    Modo interativo para confirmações"
    echo "  --full           Limpeza completa (padrão)"
    echo "  --help           Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0                          # Limpeza completa automática"
    echo "  $0 --interactive           # Limpeza com confirmações"
    echo "  $0 --screenshots           # Limpa apenas screenshots"
    echo "  $0 --stats                 # Mostra estatísticas"
}

# Função principal
main() {
    print_header
    
    case "$1" in
        --screenshots)
            cleanup_screenshots "$2"
            ;;
        --logs)
            cleanup_logs
            ;;
        --profiles)
            cleanup_browser_profiles
            ;;
        --stats)
            show_statistics
            ;;
        --interactive)
            full_cleanup "--interactive"
            ;;
        --full|"")
            full_cleanup
            ;;
        --help|-h)
            show_help
            return 0
            ;;
        *)
            print_error "Opção inválida: $1"
            show_help
            return 1
            ;;
    esac
    
    echo ""
    show_statistics
    
    echo ""
    print_success "Limpeza concluída! 🎉"
}

# Executa função principal
main "$@"
