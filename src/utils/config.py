"""
Configuration Manager - Configurações Centralizadas
===================================================

Sistema centralizado de configurações para o projeto.
"""

import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class StealthMode(Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


@dataclass
class BrowserConfig:
    """Configurações do browser"""
    headless: bool = False
    user_data_dir: str = "browser_profiles/default"
    viewport_width: int = 1366
    viewport_height: int = 768
    language: str = "pt-BR,pt;q=0.9,en;q=0.8"
    timezone: str = "America/Sao_Paulo"
    stealth_mode: StealthMode = StealthMode.ADVANCED
    context_rotation: bool = True
    
    
@dataclass
class AutomationConfig:
    """Configurações de automação"""
    human_simulation: bool = True
    typing_speed_range: tuple = (80, 200)
    mouse_movement_natural: bool = True
    scroll_simulation: bool = True
    random_pauses: bool = True
    screenshot_enabled: bool = True
    max_retry_attempts: int = 3


@dataclass
class SecurityConfig:
    """Configurações de segurança"""
    encrypt_credentials: bool = True
    session_persistence: bool = True
    fingerprint_spoofing: bool = True
    anti_detection: bool = True
    clear_cookies_on_exit: bool = False
    use_proxy: bool = False
    proxy_url: Optional[str] = None


@dataclass
class LoggingConfig:
    """Configurações de logging"""
    level: LogLevel = LogLevel.INFO
    file_logging: bool = True
    console_logging: bool = True
    log_file: str = "logs/yt_automation.log"
    max_log_size: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class AppConfig:
    """Configuração principal da aplicação"""
    browser: BrowserConfig
    automation: AutomationConfig
    security: SecurityConfig
    logging: LoggingConfig
    
    # Configurações gerais
    app_name: str = "YT Automation"
    version: str = "2.0.0"
    debug_mode: bool = False


class ConfigManager:
    """Gerenciador de configurações"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / "app_config.yaml"
        self.browser_profiles_file = self.config_dir / "browser_profiles.json"
        self.stealth_configs_file = self.config_dir / "stealth_configs.yaml"
        
        self._config: Optional[AppConfig] = None
    
    def load_config(self) -> AppConfig:
        """Carrega configurações do arquivo"""
        
        if self._config is None:
            if self.config_file.exists():
                self._config = self._load_from_file()
            else:
                self._config = self._create_default_config()
                self.save_config(self._config)
        
        return self._config
    
    def _load_from_file(self) -> AppConfig:
        """Carrega configurações do arquivo YAML"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Reconstrói os objetos de configuração
            browser_config = BrowserConfig(**data.get('browser', {}))
            automation_config = AutomationConfig(**data.get('automation', {}))
            security_config = SecurityConfig(**data.get('security', {}))
            logging_config = LoggingConfig(**data.get('logging', {}))
            
            config = AppConfig(
                browser=browser_config,
                automation=automation_config,
                security=security_config,
                logging=logging_config,
                app_name=data.get('app_name', 'YT Automation'),
                version=data.get('version', '2.0.0'),
                debug_mode=data.get('debug_mode', False)
            )
            
            return config
            
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> AppConfig:
        """Cria configuração padrão"""
        return AppConfig(
            browser=BrowserConfig(),
            automation=AutomationConfig(),
            security=SecurityConfig(),
            logging=LoggingConfig()
        )
    
    def save_config(self, config: AppConfig) -> bool:
        """Salva configurações no arquivo"""
        try:
            # Converte para dict
            config_dict = {
                'app_name': config.app_name,
                'version': config.version,
                'debug_mode': config.debug_mode,
                'browser': asdict(config.browser),
                'automation': asdict(config.automation),
                'security': asdict(config.security),
                'logging': asdict(config.logging)
            }
            
            # Converte enums para strings
            config_dict['browser']['stealth_mode'] = config.browser.stealth_mode.value
            config_dict['logging']['level'] = config.logging.level.value
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            
            print(f"✅ Configurações salvas: {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def create_browser_profiles(self):
        """Cria arquivo de perfis de browser"""
        profiles = {
            "profiles": [
                {
                    "name": "Windows_Chrome_118",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    "viewport": {"width": 1920, "height": 1080},
                    "platform": "Win32",
                    "language": "pt-BR,pt;q=0.9,en;q=0.8",
                    "timezone": "America/Sao_Paulo",
                    "webgl_vendor": "Google Inc. (Intel)",
                    "webgl_renderer": "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"
                },
                {
                    "name": "Windows_Chrome_117",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                    "viewport": {"width": 1366, "height": 768},
                    "platform": "Win32",
                    "language": "pt-BR,pt;q=0.9,en;q=0.8",
                    "timezone": "America/Sao_Paulo",
                    "webgl_vendor": "Google Inc. (NVIDIA)",
                    "webgl_renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)"
                },
                {
                    "name": "macOS_Chrome_118",
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    "viewport": {"width": 1440, "height": 900},
                    "platform": "MacIntel",
                    "language": "pt-BR,pt;q=0.9,en;q=0.8",
                    "timezone": "America/Sao_Paulo",
                    "webgl_vendor": "Apple Inc.",
                    "webgl_renderer": "Apple GPU"
                }
            ]
        }
        
        with open(self.browser_profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Perfis de browser criados: {self.browser_profiles_file}")
    
    def create_stealth_configs(self):
        """Cria arquivo de configurações stealth"""
        stealth_configs = {
            "anti_detection": {
                "remove_webdriver_property": True,
                "mock_plugins": True,
                "mock_languages": True,
                "mock_permissions": True,
                "spoof_canvas": True,
                "spoof_webgl": True,
                "block_webrtc": True
            },
            "browser_args": {
                "basic": [
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--disable-dev-shm-usage"
                ],
                "advanced": [
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-extensions-except=uBlock",
                    "--disable-plugins-discovery",
                    "--disable-default-apps",
                    "--no-first-run",
                    "--disable-web-security",
                    "--disable-features=TranslateUI,VizDisplayCompositor",
                    "--disable-ipc-flooding-protection"
                ],
                "maximum": [
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-extensions-except=uBlock",
                    "--disable-plugins-discovery",
                    "--disable-default-apps",
                    "--no-first-run",
                    "--disable-web-security",
                    "--allow-running-insecure-content",
                    "--disable-features=TranslateUI,VizDisplayCompositor",
                    "--disable-ipc-flooding-protection",
                    "--disable-renderer-backgrounding",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-field-trial-config",
                    "--disable-background-timer-throttling",
                    "--disable-hang-monitor",
                    "--disable-prompt-on-repost",
                    "--disable-sync",
                    "--metrics-recording-only",
                    "--no-report-upload",
                    "--disable-domain-reliability",
                    "--disable-component-extensions-with-background-pages"
                ]
            },
            "human_behavior": {
                "typing_delays": {
                    "min": 80,
                    "max": 200,
                    "pause_chance": 0.05,
                    "correction_chance": 0.03
                },
                "mouse_movement": {
                    "speed": 1.5,
                    "acceleration": 0.8,
                    "deceleration": 0.6,
                    "curve_intensity": 0.3
                },
                "scroll_patterns": {
                    "speed_range": [100, 300],
                    "pause_range": [200, 800],
                    "back_scroll_chance": 0.1
                }
            }
        }
        
        with open(self.stealth_configs_file, 'w', encoding='utf-8') as f:
            yaml.dump(stealth_configs, f, default_flow_style=False)
        
        print(f"✅ Configurações stealth criadas: {self.stealth_configs_file}")
    
    def setup_environment(self):
        """Configura ambiente inicial"""
        
        # Cria diretórios necessários
        directories = [
            "logs",
            "temp_screenshots", 
            "browser_profiles",
            "sessions"
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
        
        # Cria arquivos de configuração
        self.create_browser_profiles()
        self.create_stealth_configs()
        
        # Carrega e salva configuração padrão
        config = self.load_config()
        
        print("✅ Ambiente configurado com sucesso")
        return config
    
    def get_config(self) -> AppConfig:
        """Retorna configuração atual"""
        return self.load_config()
    
    def update_config(self, **kwargs) -> bool:
        """Atualiza configurações específicas"""
        try:
            config = self.load_config()
            
            # Atualiza campos específicos
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
                elif '.' in key:
                    # Suporte para configurações aninhadas (ex: 'browser.headless')
                    parts = key.split('.')
                    obj = config
                    for part in parts[:-1]:
                        obj = getattr(obj, part)
                    setattr(obj, parts[-1], value)
            
            return self.save_config(config)
            
        except Exception as e:
            print(f"❌ Erro ao atualizar configuração: {e}")
            return False


# Instância global do gerenciador de configurações
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Função utilitária para obter configurações"""
    return config_manager.get_config()


def setup_project():
    """Configura projeto inicial"""
    print("🔧 Configurando projeto...")
    return config_manager.setup_environment()


if __name__ == "__main__":
    # Demonstração/configuração inicial
    print("🔧 CONFIGURAÇÃO INICIAL DO PROJETO")
    print("=" * 40)
    
    config = setup_project()
    
    print(f"\n✅ Projeto configurado!")
    print(f"📁 Diretório de configuração: {config_manager.config_dir}")
    print(f"🔧 Arquivo de configuração: {config_manager.config_file}")
    print(f"🌐 Perfis de browser: {config_manager.browser_profiles_file}")
    print(f"🛡️  Configurações stealth: {config_manager.stealth_configs_file}")
