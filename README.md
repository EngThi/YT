# 🤖 Automação Stealth Completa no GitHub Codespaces para YouTube

Este projeto implementa uma automação stealth robusta para o YouTube usando **Nodriver** (Python) no ambiente **GitHub Codespaces**.

## 🚀 Configuração Inicial

### 1. Configure suas credenciais

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` com suas credenciais reais:
   ```
   YOUTUBE_EMAIL=seu.email@gmail.com
   YOUTUBE_PASSWORD=suaSenhaSegura
   ```

### 2. Rebuild do Container

Como o arquivo `devcontainer.json` foi corrigido, você precisa reconstruir o container:

1. Abra a **Command Palette** (`Ctrl+Shift+P` ou `Cmd+Shift+P`)
2. Digite e selecione: `Codespaces: Rebuild Container`
3. Aguarde a reconstrução completa

### 3. Execução

Após o rebuild, execute o script:

```bash
python main.py
```

## 🛡️ Recursos de Furtividade

- **Fingerprint realista**: Simula Windows com hardware Intel
- **Digitação humana**: Delays aleatórios entre caracteres
- **Movimentos de mouse**: Simulação de navegação natural
- **Sessão persistente**: Mantém cookies e configurações
- **Múltiplas abas**: Navegação simultânea

## 📁 Estrutura do Projeto

```
├── .devcontainer/
│   └── devcontainer.json    # Configuração do ambiente
├── .env.example             # Modelo de credenciais
├── .env                     # Suas credenciais (não versionado)
├── .gitignore              # Arquivos ignorados pelo Git
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## ⚡ Funcionalidades

- ✅ Login automático no YouTube
- ✅ Abertura de múltiplas abas
- ✅ Pesquisa automática
- ✅ Simulação de comportamento humano
- ✅ Resistência à detecção

## 🔒 Segurança

- Credenciais protegidas no arquivo `.env`
- Arquivo `.gitignore` configurado
- Dados do perfil não versionados

## 📝 Próximos Passos

1. **Configure suas credenciais** no arquivo `.env`
2. **Rebuild o container** usando o comando do Codespaces
3. **Execute o script** e observe a automação funcionando
4. **Personalize** as ações conforme sua necessidade

---

**⚠️ Importante**: Use esta automação responsavelmente e respeitando os termos de serviço do YouTube.
