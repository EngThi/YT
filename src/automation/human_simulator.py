"""
Human Behavior Simulator - Simulação de Comportamento Humano
============================================================

Simula padrões realistas de comportamento humano para evitar detecção.
"""

import asyncio
import math
import random
import time


class HumanBehaviorSimulator:
    """Simula comportamento humano realista"""
    
    def __init__(self):
        self.typing_patterns = self._load_brazilian_typing_patterns()
        self.mouse_patterns = self._load_mouse_patterns()
        self.scroll_patterns = self._load_scroll_patterns()
    
    def _load_brazilian_typing_patterns(self) -> dict:
        """Padrões de digitação brasileiros"""
        return {
            'speed_range': (80, 200),  # ms entre caracteres
            'pause_chance': 0.05,      # 5% chance de pausa
            'correction_chance': 0.03, # 3% chance de correção
            'common_delays': {
                ' ': (150, 300),       # Espaços mais lentos
                '.': (200, 400),       # Pontuação mais lenta
                '@': (100, 250),       # Símbolos especiais
                'shift_keys': (50, 150) # Teclas com shift
            }
        }
    
    def _load_mouse_patterns(self) -> dict:
        """Padrões de movimento do mouse"""
        return {
            'base_speed': 1.5,
            'acceleration': 0.8,
            'deceleration': 0.6,
            'curve_intensity': 0.3,
            'pause_probability': 0.1,
            'overshoot_chance': 0.15
        }
    
    def _load_scroll_patterns(self) -> dict:
        """Padrões de scroll"""
        return {
            'scroll_speed': (100, 300),
            'pause_between_scrolls': (200, 800),
            'variable_speed': True,
            'scroll_back_chance': 0.1
        }
    
    async def human_typing(self, element, text: str, simulate_mistakes: bool = True):
        """Digitação com padrões humanos brasileiros"""
        if not text:
            return
        
        # Limpa campo antes de digitar
        await element.click(click_count=3)  # Seleciona tudo
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        for i, char in enumerate(text):
            # Simula pausas ocasionais (como pensar)
            if random.random() < self.typing_patterns['pause_chance']:
                await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Determina delay baseado no caractere
            if char in self.typing_patterns['common_delays']:
                delay_range = self.typing_patterns['common_delays'][char]
            elif char.isupper() or char in '!@#$%^&*()':
                delay_range = self.typing_patterns['common_delays']['shift_keys']
            else:
                delay_range = self.typing_patterns['speed_range']
            
            delay = random.randint(*delay_range) / 1000.0
            
            # Simula correções ocasionais
            if simulate_mistakes and random.random() < self.typing_patterns['correction_chance']:
                # Digita caractere errado
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                await element.type(wrong_char, delay=delay)
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
                # Corrige (backspace + caractere correto)
                await element.press('Backspace')
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await element.type(char, delay=delay)
            else:
                # Digita caractere correto
                await element.type(char, delay=delay)
            
            # Variação adicional no timing
            if i % 10 == 0:  # A cada 10 caracteres
                await asyncio.sleep(random.uniform(0.05, 0.2))
    
    async def human_mouse_movement(self, page, start_x: int, start_y: int, 
                                 end_x: int, end_y: int, duration: float = None):
        """Movimentos de mouse com aceleração/desaceleração natural"""
        
        if duration is None:
            distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            duration = max(0.3, min(2.0, distance / 500))  # Duração baseada na distância
        
        steps = max(10, int(duration * 60))  # 60 FPS
        
        for step in range(steps):
            progress = step / (steps - 1)
            
            # Curva de aceleração/desaceleração (ease-in-out)
            eased_progress = self._ease_in_out_cubic(progress)
            
            # Posição base na linha reta
            current_x = start_x + (end_x - start_x) * eased_progress
            current_y = start_y + (end_y - start_y) * eased_progress
            
            # Adiciona curva natural (movimento não linear)
            curve_offset = self._calculate_curve_offset(progress, distance/4)
            current_x += curve_offset['x']
            current_y += curve_offset['y']
            
            # Adiciona pequena variação aleatória
            current_x += random.uniform(-2, 2)
            current_y += random.uniform(-2, 2)
            
            await page.mouse.move(current_x, current_y)
            await asyncio.sleep(duration / steps)
            
            # Pausas ocasionais durante movimento longo
            if random.random() < 0.05 and step < steps - 5:
                await asyncio.sleep(random.uniform(0.05, 0.15))
    
    def _ease_in_out_cubic(self, t: float) -> float:
        """Função de easing cúbica para movimento natural"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _calculate_curve_offset(self, progress: float, intensity: float) -> dict:
        """Calcula offset para criar movimento curvado"""
        # Curva sinusoidal sutil
        curve_factor = math.sin(progress * math.pi) * intensity * self.mouse_patterns['curve_intensity']
        
        return {
            'x': curve_factor * random.uniform(-1, 1),
            'y': curve_factor * random.uniform(-1, 1)
        }
    
    async def human_click(self, page, element, click_type: str = 'single'):
        """Click com timing humano"""
        
        # Move mouse para o elemento com movimento natural
        box = await element.bounding_box()
        if box:
            # Calcula posição aleatória dentro do elemento
            click_x = box['x'] + random.uniform(0.2, 0.8) * box['width']
            click_y = box['y'] + random.uniform(0.2, 0.8) * box['height']
            
            current_pos = await page.evaluate('() => ({ x: window.mouseX || 0, y: window.mouseY || 0 })')
            
            await self.human_mouse_movement(
                page, 
                current_pos.get('x', 0), 
                current_pos.get('y', 0),
                click_x, 
                click_y
            )
            
            # Pausa antes do click
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            if click_type == 'single':
                await element.click()
            elif click_type == 'double':
                await element.dblclick()
            
            # Pequena pausa após click
            await asyncio.sleep(random.uniform(0.1, 0.2))
    
    async def human_scroll(self, page, direction: str = 'down', amount: int = None):
        """Scroll com padrões humanos"""
        
        if amount is None:
            amount = random.randint(2, 5)
        
        scroll_patterns = self.scroll_patterns
        
        for i in range(amount):
            # Velocidade variável
            if scroll_patterns['variable_speed']:
                scroll_delta = random.randint(*scroll_patterns['scroll_speed'])
            else:
                scroll_delta = scroll_patterns['scroll_speed'][0]
            
            if direction == 'down':
                await page.mouse.wheel(0, scroll_delta)
            else:
                await page.mouse.wheel(0, -scroll_delta)
            
            # Pausa entre scrolls
            pause = random.randint(*scroll_patterns['pause_between_scrolls']) / 1000.0
            await asyncio.sleep(pause)
            
            # Ocasionalmente scroll para trás (como humano verificando algo)
            if random.random() < scroll_patterns['scroll_back_chance']:
                small_back = scroll_delta // 3
                await page.mouse.wheel(0, -small_back if direction == 'down' else small_back)
                await asyncio.sleep(random.uniform(0.2, 0.5))
    
    async def simulate_reading_pause(self, content_length: int = 100):
        """Simula tempo de leitura baseado no comprimento do conteúdo"""
        # Fórmula baseada em velocidade média de leitura (200-300 palavras/min)
        words_estimate = content_length / 5  # Estimativa: 5 caracteres por palavra
        reading_time = words_estimate / random.uniform(3, 5)  # 3-5 palavras por segundo
        
        # Adiciona variação humana
        pause_time = max(0.5, reading_time + random.uniform(-0.5, 1.0))
        
        await asyncio.sleep(pause_time)
    
    async def simulate_decision_pause(self):
        """Simula pausa de tomada de decisão"""
        await asyncio.sleep(random.uniform(0.8, 2.5))
    
    async def random_mouse_movement(self, page, viewport_width: int = 1366, viewport_height: int = 768):
        """Movimento aleatório do mouse para simular atividade humana"""
        current_pos = await page.evaluate('() => ({ x: window.mouseX || 500, y: window.mouseY || 300 })')
        
        # Movimento próximo à posição atual
        new_x = max(0, min(viewport_width, current_pos.get('x', 500) + random.randint(-100, 100)))
        new_y = max(0, min(viewport_height, current_pos.get('y', 300) + random.randint(-100, 100)))
        
        await self.human_mouse_movement(page, current_pos.get('x', 500), current_pos.get('y', 300), new_x, new_y)
    
    async def simulate_multitasking_behavior(self, page):
        """Simula comportamento de multitasking (mudança de abas, etc.)"""
        behaviors = [
            self._simulate_tab_switch,
            self._simulate_window_resize,
            self._simulate_page_refresh_check,
            self._simulate_scroll_exploration
        ]
        
        behavior = random.choice(behaviors)
        await behavior(page)
    
    async def _simulate_tab_switch(self, page):
        """Simula mudança rápida de aba"""
        await page.keyboard.press('Alt+Tab')
        await asyncio.sleep(random.uniform(0.5, 2.0))
        await page.keyboard.press('Alt+Tab')
    
    async def _simulate_window_resize(self, page):
        """Simula pequeno ajuste de janela"""
        # Simula movimento sutil da janela
        await asyncio.sleep(random.uniform(1.0, 3.0))
    
    async def _simulate_page_refresh_check(self, page):
        """Simula verificação de atualização da página"""
        await page.keyboard.press('F5')
        await asyncio.sleep(random.uniform(2.0, 4.0))
    
    async def _simulate_scroll_exploration(self, page):
        """Simula exploração da página com scroll"""
        await self.human_scroll(page, 'down', random.randint(2, 4))
        await asyncio.sleep(random.uniform(1.0, 3.0))
        await self.human_scroll(page, 'up', random.randint(1, 2))


class BrazilianBehaviorProfile:
    """Profile específico de comportamento brasileiro"""
    
    def __init__(self):
        self.activity_patterns = {
            'morning': {'energy': 0.7, 'speed_multiplier': 0.9},
            'afternoon': {'energy': 1.0, 'speed_multiplier': 1.0},
            'evening': {'energy': 0.8, 'speed_multiplier': 0.85},
            'night': {'energy': 0.6, 'speed_multiplier': 0.7}
        }
    
    def get_current_behavior_modifier(self) -> dict:
        """Retorna modificador baseado no horário brasileiro"""
        current_hour = time.localtime().tm_hour
        
        if 6 <= current_hour < 12:
            period = 'morning'
        elif 12 <= current_hour < 18:
            period = 'afternoon'
        elif 18 <= current_hour < 22:
            period = 'evening'
        else:
            period = 'night'
        
        return self.activity_patterns[period]
    
    def apply_brazilian_timing(self, base_delay: float) -> float:
        """Aplica modificadores de timing brasileiro"""
        modifier = self.get_current_behavior_modifier()
        adjusted_delay = base_delay * modifier['speed_multiplier']
        
        # Adiciona variação baseada na "energia" do período
        energy_factor = modifier['energy']
        variation = random.uniform(0.8, 1.2) * energy_factor
        
        return adjusted_delay * variation
