# 🤖 Automação Stealth Completa no GitHub Codespaces para YouTube

Este projeto implementa uma automação stealth robusta para o YouTube usando **Nodriver** (Python) no ambiente **GitHub Codespaces**.

## 🚀 Status do Projeto

✅ **Configuração corrigida!** O arquivo `devcontainer.json` foi reparado e o ambiente está funcional.

## 🔧 Configuração Atual

O projeto está configurado para:
- ✅ Acessar **YouTube diretamente** (sem login do Google)
- ✅ Rodar em **modo headless** (adequado para Codespaces)
- ✅ Usar **Chromium** instalado no container Alpine Linux
- ✅ **Navegação stealth** com movimentos humanos simulados
- ✅ **Múltiplas abas** para navegação avançada

## 🛠️ Como Usar

### 1. Reconstruir o Container (Necessário!)

Como o arquivo `devcontainer.json` foi corrigido, você **DEVE** reconstruir o container:

1. Abra a **Command Palette** (`Ctrl+Shift+P` ou `Cmd+Shift+P`)
2. Digite e selecione: `Codespaces: Rebuild Container`
3. Aguarde a reconstrução completa

### 2. Configuração Opcional de Credenciais

Se quiser usar login (opcional):
```bash
cp .env.example .env
# Edite .env com suas credenciais reais
```

### 3. Execução

```bash
python main.py
```

## � Ambiente Recovery

**Nota importante**: Como estamos em um container de recovery, algumas funcionalidades podem ser limitadas. Para melhor experiência:

1. **Rebuild o container** como indicado acima
2. **Use o ambiente Python 3.11** configurado no devcontainer.json
3. **As dependências serão instaladas automaticamente** após o rebuild

## 📁 Estrutura do Projeto

```
├── .devcontainer/
│   └── devcontainer.json    # ✅ CORRIGIDO - Configuração do ambiente
├── .env.example             # Modelo de credenciais (opcional)
├── .gitignore              # Proteção de arquivos sensíveis
├── main.py                 # ✅ Script principal (YouTube direto)
├── requirements.txt        # Dependências Python
├── cleanup_screenshots.sh  # 🧹 Script de limpeza manual
├── temp_screenshots/       # 📸 Screenshots temporários (auto-removidos)
└── README.md              # Este arquivo
```

## 🎯 Funcionalidades Implementadas

- ✅ **Acesso direto ao YouTube** (sem Google accounts)
- ✅ **Navegação stealth** com scrolls aleatórios
- ✅ **Múltiplas abas** (página principal + trending)
- ✅ **Configuração para container** (headless + no-sandbox)
- ✅ **Tratamento de erros** robusto
- ✅ **Logs informativos** para debug
- 📸 **Screenshots temporários** em pontos essenciais
- 🧹 **Auto-limpeza** de screenshots (5 minutos)

### 📸 Sistema de Screenshots Temporários

O script agora tira screenshots automáticos nos pontos essenciais:

1. **Acesso inicial** ao YouTube
2. **Verificação de login** (logado/não logado)
3. **Após navegação** humana
4. **Segunda aba** (trending)
5. **Navegação final**

**🛡️ Proteção de Armazenamento:**
- Screenshots são **automaticamente removidos** após 5 minutos
- Limpeza no **início** e **fim** de cada execução
- Script manual: `./cleanup_screenshots.sh`

### 📋 Pontos Essenciais Monitorados

- ✅ **Inicialização** do browser stealth
- ✅ **Carregamento** da página do YouTube
- ✅ **Status de login** (detecta se logado ou anônimo)
- ✅ **Navegação humana** (scrolls, interações)
- ✅ **Múltiplas abas** funcionando
- ✅ **Finalização** sem erros

## 🐛 Troubleshooting

**Se encontrar erros:**

1. **Primeiro**: Rebuild o container (comando acima)
2. **Dependências**: `pip install --break-system-packages -r requirements.txt`
3. **Chromium**: `sudo apk add chromium chromium-chromedriver`
4. **Limpeza manual**: `./cleanup_screenshots.sh` (remove screenshots temporários)

## 🔒 Segurança

- Credenciais protegidas no arquivo `.env` (opcional)
- Arquivo `.gitignore` configurado
- Dados do perfil não versionados

---

**🎉 Projeto pronto para uso!** Após o rebuild do container, execute `python main.py` e observe a automação funcionando.
