# 🤖 YouTube Automation v2.0

> Sistema profissional de automação para YouTube com anti-detecção avançada e simulação de comportamento humano.

## 🚀 Características Principais

### 🛡️ **Anti-Detecção Avançada**
- **Fingerprint Spoofing**: Mascaramento completo de propriedades do browser
- **Context Rotation**: Rotação automática de contextos para evitar padrões
- **Stealth Engine**: Engine sofisticada com múltiplos níveis de proteção
- **Session Persistence**: Manutenção inteligente de sessões válidas

### 🎭 **Simulação Humana Realista**
- **Typing Patterns**: Padrões brasileiros de digitação com erros ocasionais
- **Mouse Movement**: Movimentos naturais com curvas bezier
- **Scroll Behavior**: Comportamento de scroll variável e realista
- **Reading Simulation**: Pausas baseadas em velocidade de leitura humana

### 🔐 **Segurança e Credenciais**
- **Encrypted Storage**: Armazenamento criptografado de credenciais
- **Multiple Strategies**: Múltiplas estratégias de login (automático, manual, híbrido)
- **Session Management**: Gerenciamento inteligente de sessões
- **Fallback Systems**: Sistemas de backup para máxima confiabilidade

### 📊 **Monitoramento e Logs**
- **Structured Logging**: Sistema de logs estruturado com JSON
- **Performance Metrics**: Métricas detalhadas de performance
- **Error Tracking**: Rastreamento avançado de erros
- **Real-time Monitoring**: Monitoramento em tempo real

## 🏗️ **Arquitetura Modular**

```
YT/
├── src/
│   ├── core/                    # Núcleo do sistema
│   │   ├── browser_manager.py   # Gerenciamento stealth do browser
│   │   └── session_manager.py   # Persistência de sessões
│   ├── automation/              # Automação específica
│   │   ├── youtube_automator.py # Automação YouTube
│   │   ├── login_handler.py     # Estratégias de login
│   │   └── human_simulator.py   # Simulação comportamento humano
│   ├── security/                # Segurança
│   │   ├── credential_manager.py# Gestão segura credenciais
│   │   └── fingerprint_spoofing.py # Anti-detecção
│   └── utils/                   # Utilitários
│       ├── logger.py            # Sistema de logs
│       ├── config.py            # Configurações
│       └── screenshot_manager.py# Gestão de screenshots
├── tests/                       # Testes automatizados
├── config/                      # Configurações
├── main_v2.py                   # Entry point principal
└── emergency_fix.py             # Script de emergência
```

## 🛠️ **Instalação**

### Pré-requisitos
- Python 3.8+
- pip
- Git

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/YT.git
cd YT

# Instale dependências
pip install -r requirements.txt

# Configuração inicial
python main_v2.py --setup

# Configure credenciais (opcional - recomendado)
python main_v2.py --credentials
```

## 🚀 **Uso**

### **Execução Básica**
```bash
# Execução padrão (estratégia híbrida)
python main_v2.py

# Login manual assistido (mais seguro)
python main_v2.py --strategy manual

# Manter browser aberto para uso
python main_v2.py --keep-open
```

### **Opções Avançadas**
```bash
# Execução headless
python main_v2.py --headless

# Profile específico
python main_v2.py --profile stealth_max

# Debug completo
python main_v2.py --log-level DEBUG

# Script de emergência
python emergency_fix.py
```

### **Estratégias de Login**

| Estratégia | Descrição | Segurança | Automação |
|------------|-----------|-----------|-----------|
| `session` | Usa sessão existente | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `manual` | Login manual assistido | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| `auto` | Login automático | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `hybrid` | Combina todas | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔧 **Configuração**

### **Configuração Inicial**
```bash
python main_v2.py --setup
```

### **Configuração de Credenciais**
```bash
# Método seguro (recomendado)
python main_v2.py --credentials

# Ou via .env (menos seguro)
cp .env.example .env
# Edite .env com suas credenciais
```

### **Configurações Avançadas**
Edite `config/app_config.yaml` para personalizar:
- Comportamento do browser
- Parâmetros de automação
- Configurações de segurança
- Níveis de logging

## 🐳 **Docker Support**

### **Ambiente de Desenvolvimento**
```bash
docker-compose --profile dev up
```

### **Ambiente de Produção**
```bash
docker-compose --profile prod up -d
```

### **Testes**
```bash
docker-compose --profile test up
```

## 🧪 **Testes**

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_stealth_engine.py -v

# Com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

## 📊 **Monitoramento**

### **Logs**
- **Estruturados**: `logs/yt_automation.log`
- **Erros**: `logs/yt_automation_errors.log`
- **Debug**: Console com cores

### **Métricas**
- Tempo de execução
- Taxa de sucesso
- Performance do browser
- Eventos de segurança

### **Screenshots**
Capturas automáticas em `temp_screenshots/`:
- Estados importantes
- Erros críticos
- Confirmações de sucesso

## 🛡️ **Segurança**

### **Práticas Implementadas**
- ✅ Credenciais criptografadas
- ✅ Rotação de contexto
- ✅ Anti-detecção multicamada
- ✅ Headers realistas
- ✅ Fingerprint brasileiro
- ✅ Comportamento humano

### **Configurações de Segurança**
```yaml
security:
  encrypt_credentials: true
  session_persistence: true
  fingerprint_spoofing: true
  anti_detection: true
  use_proxy: false  # Configure se necessário
```

## 🔄 **Estratégias Anti-Detecção**

### **1. Fingerprint Spoofing**
- User-Agent realista brasileiro
- Viewport e resolução comum
- Timezone América/São_Paulo
- Plugins e fontes realistas

### **2. Comportamento Humano**
- Digitação com erros ocasionais
- Movimentos de mouse naturais
- Pausas para "leitura"
- Scroll exploratório

### **3. Context Rotation**
- Múltiplos perfis de browser
- Rotação automática
- Sessões persistentes
- Cache isolado

## 📈 **Performance**

### **Benchmarks**
- Inicialização: ~3-5 segundos
- Login híbrido: ~10-15 segundos
- Navegação: ~2-3 segundos
- CPU: Baixo impacto
- Memória: ~150-200MB

### **Otimizações**
- Carregamento lazy de módulos
- Cache de configurações
- Pool de conexões
- Compressão de logs

## 🐛 **Troubleshooting**

### **Problemas Comuns**

#### **1. Erro de Dependência**
```bash
pip install -r requirements.txt
```

#### **2. Browser não Abre**
```bash
# Verificar nodriver
pip install --upgrade nodriver

# Tentar modo headless
python main_v2.py --headless
```

#### **3. Login Falha**
```bash
# Usar modo manual
python main_v2.py --strategy manual

# Reconfigurar credenciais
python main_v2.py --credentials
```

#### **4. Detecção do Google**
```bash
# Usar script de emergência
python emergency_fix.py

# Limpar perfils
rm -rf browser_profiles/
python main_v2.py --setup
```

### **Debug Avançado**
```bash
# Logs detalhados
python main_v2.py --log-level DEBUG

# Manter browser aberto
python main_v2.py --keep-open

# VNC para debug visual
docker-compose --profile debug up
# Acesse: http://localhost:6080
```

## 🤝 **Contribuição**

### **Como Contribuir**
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### **Padrões de Código**
```bash
# Formatação
black src/ tests/

# Linting
flake8 src/ tests/

# Testes
pytest tests/ -v
```

## 📄 **Licença**

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ **Aviso Legal**

Este software é destinado apenas para fins educacionais e de pesquisa. O uso responsável e em conformidade com os Termos de Serviço do YouTube é de responsabilidade do usuário.

## 🆘 **Suporte**

- 📖 **Documentação**: [Wiki do Projeto](wiki)
- 🐛 **Issues**: [GitHub Issues](issues)
- 💬 **Discussões**: [GitHub Discussions](discussions)
- 📧 **Email**: automation@example.com

## 🎯 **Roadmap**

### **v2.1 (Próxima Release)**
- [ ] Interface Web para configuração
- [ ] Suporte a múltiplas contas
- [ ] API REST para integração
- [ ] Dashboard de métricas

### **v2.2 (Futuro)**
- [ ] Machine Learning para detecção de padrões
- [ ] Integração com proxies rotativos
- [ ] Suporte a outros navegadores
- [ ] Modo distribuído

---

<div align="center">

**🤖 YouTube Automation v2.0**

*Sistema Profissional de Automação com Anti-Detecção Avançada*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/docker-supported-blue.svg)](docker-compose.yml)

</div>
