"""
Advanced Stealth Engine - Engine Avançada de Anti-Detecção
==========================================================

Engine sofisticada para mascarar automação e simular comportamento humano real.
"""

import random
import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class BrowserFingerprint:
    """Fingerprint realista de browser brasileiro"""
    user_agent: str
    viewport: Dict[str, int]
    language: str
    timezone: str
    platform: str
    plugins: List[str]
    fonts: List[str]
    webgl_vendor: str
    webgl_renderer: str


class AdvancedStealthEngine:
    """Engine avançada de anti-detecção"""
    
    def __init__(self):
        self.brazilian_fingerprints = self._load_brazilian_fingerprints()
        self.current_fingerprint: Optional[BrowserFingerprint] = None
    
    def _load_brazilian_fingerprints(self) -> List[BrowserFingerprint]:
        """Carrega fingerprints realistas baseados em dados brasileiros"""
        return [
            BrowserFingerprint(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                viewport={"width": 1366, "height": 768},
                language="pt-BR,pt;q=0.9,en;q=0.8",
                timezone="America/Sao_Paulo",
                platform="Win32",
                plugins=["Chrome PDF Plugin", "Native Client"],
                fonts=["Arial", "Times New Roman", "Courier New", "Verdana"],
                webgl_vendor="Google Inc. (Intel)",
                webgl_renderer="ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"
            ),
            BrowserFingerprint(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                language="pt-BR,pt;q=0.9,en;q=0.8",
                timezone="America/Sao_Paulo",
                platform="Win32",
                plugins=["Chrome PDF Plugin", "Native Client"],
                fonts=["Arial", "Times New Roman", "Calibri", "Segoe UI"],
                webgl_vendor="Google Inc. (NVIDIA)",
                webgl_renderer="ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)"
            ),
            BrowserFingerprint(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                viewport={"width": 1440, "height": 900},
                language="pt-BR,pt;q=0.9,en;q=0.8",
                timezone="America/Sao_Paulo",
                platform="MacIntel",
                plugins=["Chrome PDF Plugin", "Native Client"],
                fonts=["Arial", "Helvetica", "Times", "Courier"],
                webgl_vendor="Apple Inc.",
                webgl_renderer="Apple GPU"
            )
        ]
    
    def select_random_fingerprint(self) -> BrowserFingerprint:
        """Seleciona um fingerprint aleatório realista"""
        self.current_fingerprint = random.choice(self.brazilian_fingerprints)
        return self.current_fingerprint
    
    async def setup_realistic_browser(self) -> Dict[str, Any]:
        """Configura browser com fingerprint humano realista"""
        fingerprint = self.select_random_fingerprint()
        
        options = {
            'user_agent': fingerprint.user_agent,
            'viewport': fingerprint.viewport,
            'language': fingerprint.language,
            'timezone': fingerprint.timezone,
            'platform': fingerprint.platform,
            'webrtc': 'block',
            'canvas': 'noise',
            'webgl': 'noise',
            'fonts': fingerprint.fonts,
            'plugins': fingerprint.plugins,
            'headers': self._get_human_headers(),
            'geolocation': self._get_brazilian_geolocation()
        }
        return options
    
    def _get_human_headers(self) -> Dict[str, str]:
        """Headers realistas para requisições"""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    
    def _get_brazilian_geolocation(self) -> Dict[str, float]:
        """Geolocalização brasileira aleatória"""
        brazilian_cities = [
            {"lat": -23.5505, "lon": -46.6333},  # São Paulo
            {"lat": -22.9068, "lon": -43.1729},  # Rio de Janeiro
            {"lat": -15.7942, "lon": -47.8822},  # Brasília
            {"lat": -12.9714, "lon": -38.5014},  # Salvador
            {"lat": -25.4284, "lon": -49.2733},  # Curitiba
        ]
        
        city = random.choice(brazilian_cities)
        # Adiciona pequena variação para parecer mais real
        return {
            "latitude": city["lat"] + random.uniform(-0.1, 0.1),
            "longitude": city["lon"] + random.uniform(-0.1, 0.1),
            "accuracy": random.randint(100, 1000)
        }
    
    async def inject_stealth_scripts(self, page) -> None:
        """Injeta scripts de stealth para mascarar automação"""
        
        # Remove detecção de webdriver
        await page.evaluate("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            delete navigator.__proto__.webdriver;
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    }
                ],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['pt-BR', 'pt', 'en'],
            });
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Mock screen properties
            Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
            Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
            
            // Mock canvas fingerprint
            const getContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type) {
                if (type === '2d') {
                    const context = getContext.call(this, type);
                    const originalFillText = context.fillText;
                    context.fillText = function() {
                        // Adiciona ruído sutil ao canvas
                        const noise = Math.random() * 0.001;
                        arguments[1] += noise;
                        arguments[2] += noise;
                        return originalFillText.apply(this, arguments);
                    };
                    return context;
                }
                return getContext.call(this, type);
            };
            
            // Console clear
            console.clear();
        """)
    
    def get_stealth_browser_args(self) -> List[str]:
        """Argumentos avançados para browser stealth"""
        return [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--disable-extensions-except=uBlock',
            '--disable-plugins-discovery',
            '--disable-default-apps',
            '--no-first-run',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--disable-features=TranslateUI,VizDisplayCompositor',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-field-trial-config',
            '--disable-background-timer-throttling',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-report-upload',
            '--disable-domain-reliability',
            '--disable-component-extensions-with-background-pages'
        ]


class ContextRotator:
    """Rotaciona contexto de browser para evitar detecção"""
    
    def __init__(self):
        self.browser_contexts = [
            {
                'os': 'Windows 10',
                'browser': 'Chrome 118',
                'resolution': '1920x1080',
                'timezone': 'America/Sao_Paulo',
                'profile_dir': 'profile_win_chrome118'
            },
            {
                'os': 'Windows 11',
                'browser': 'Chrome 117',
                'resolution': '1366x768',
                'timezone': 'America/Sao_Paulo',
                'profile_dir': 'profile_win11_chrome117'
            },
            {
                'os': 'macOS 14',
                'browser': 'Chrome 118',
                'resolution': '1440x900',
                'timezone': 'America/Sao_Paulo',
                'profile_dir': 'profile_mac_chrome118'
            }
        ]
        self.current_context_index = 0
    
    def get_next_context(self) -> Dict[str, str]:
        """Retorna o próximo contexto na rotação"""
        context = self.browser_contexts[self.current_context_index]
        self.current_context_index = (self.current_context_index + 1) % len(self.browser_contexts)
        return context
    
    def get_random_context(self) -> Dict[str, str]:
        """Retorna um contexto aleatório"""
        return random.choice(self.browser_contexts)
