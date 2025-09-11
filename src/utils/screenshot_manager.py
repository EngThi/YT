"""
Screenshot Manager - Gerenciador Avançado de Screenshots
=======================================================

Sistema avançado para captura, organização e análise de screenshots.
"""

import hashlib
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

from .logger import get_logger


@dataclass
class ScreenshotMetadata:
    """Metadados de screenshot"""
    filename: str
    timestamp: datetime
    url: str
    action: str
    viewport_size: Tuple[int, int]
    file_size: int
    hash_md5: str
    tags: List[str]
    success: bool = True
    error_message: str = None


class ScreenshotManager:
    """Gerenciador avançado de screenshots"""
    
    def __init__(self, base_dir: str = "temp_screenshots"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.logger = get_logger("screenshot_manager")
        self.metadata: List[ScreenshotMetadata] = []
        
        # Cria subdiretórios organizacionais
        self.subdirs = {
            "sessions": self.base_dir / "sessions",
            "errors": self.base_dir / "errors", 
            "success": self.base_dir / "success",
            "debug": self.base_dir / "debug"
        }
        
        for subdir in self.subdirs.values():
            subdir.mkdir(exist_ok=True)
    
    def _generate_filename(self, action: str, timestamp: datetime = None, 
                          extension: str = "png") -> str:
        """Gera nome de arquivo único"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Formatar: YYYYMMDD_HHMMSS_action_uniqueid.png
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        unique_id = str(int(time.time() * 1000))[-6:]  # Últimos 6 dígitos
        safe_action = "".join(c for c in action if c.isalnum() or c in "._-")
        
        return f"{timestamp_str}_{safe_action}_{unique_id}.{extension}"
    
    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calcula hash MD5 do arquivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    async def capture_screenshot(self, page, action: str = "general", 
                                category: str = "session", full_page: bool = False,
                                tags: List[str] = None) -> ScreenshotMetadata:
        """Captura screenshot com metadados completos"""
        timestamp = datetime.now()
        filename = self._generate_filename(action, timestamp)
        
        # Determina diretório baseado na categoria
        if category in self.subdirs:
            screenshot_dir = self.subdirs[category]
        else:
            screenshot_dir = self.base_dir
        
        filepath = screenshot_dir / filename
        
        try:
            # Obtém informações da página
            url = page.url if page else "unknown"
            viewport = await page.evaluate("({width: window.innerWidth, height: window.innerHeight})") if page else {"width": 0, "height": 0}
            
            # Captura screenshot
            if page:
                await page.screenshot(path=str(filepath), full_page=full_page)
            
            # Calcula informações do arquivo
            file_size = filepath.stat().st_size if filepath.exists() else 0
            file_hash = self._calculate_file_hash(filepath)
            
            # Cria metadados
            metadata = ScreenshotMetadata(
                filename=str(filepath),
                timestamp=timestamp,
                url=url,
                action=action,
                viewport_size=(viewport["width"], viewport["height"]),
                file_size=file_size,
                hash_md5=file_hash,
                tags=tags or [],
                success=True
            )
            
            self.metadata.append(metadata)
            self.logger.info(f"📸 Screenshot capturado: {filename} ({file_size} bytes)")
            
            return metadata
            
        except Exception as e:
            error_metadata = ScreenshotMetadata(
                filename="",
                timestamp=timestamp,
                url=page.url if page else "unknown",
                action=action,
                viewport_size=(0, 0),
                file_size=0,
                hash_md5="",
                tags=tags or [],
                success=False,
                error_message=str(e)
            )
            
            self.metadata.append(error_metadata)
            self.logger.error(f"❌ Falha ao capturar screenshot: {e}")
            
            return error_metadata
    
    def add_annotation(self, filepath: str, annotations: List[Dict[str, Any]]) -> str:
        """Adiciona anotações ao screenshot"""
        try:
            # Carrega imagem
            img = Image.open(filepath)
            draw = ImageDraw.Draw(img)
            
            # Tenta carregar fonte
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Adiciona anotações
            for annotation in annotations:
                x = annotation.get("x", 0)
                y = annotation.get("y", 0)
                text = annotation.get("text", "")
                color = annotation.get("color", "red")
                
                # Desenha retângulo de fundo para texto
                bbox = draw.textbbox((x, y), text, font=font)
                draw.rectangle(bbox, fill="white", outline=color)
                draw.text((x, y), text, fill=color, font=font)
            
            # Salva imagem anotada
            annotated_path = filepath.replace(".png", "_annotated.png")
            img.save(annotated_path)
            
            self.logger.info(f"📝 Anotações adicionadas: {annotated_path}")
            return annotated_path
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar anotações: {e}")
            return filepath
    
    def create_comparison(self, before_path: str, after_path: str) -> str:
        """Cria imagem de comparação lado a lado"""
        try:
            img1 = Image.open(before_path)
            img2 = Image.open(after_path)
            
            # Redimensiona para mesmo tamanho se necessário
            max_height = max(img1.height, img2.height)
            img1 = img1.resize((int(img1.width * max_height / img1.height), max_height))
            img2 = img2.resize((int(img2.width * max_height / img2.height), max_height))
            
            # Cria imagem combinada
            combined_width = img1.width + img2.width + 10  # 10px de separação
            combined_img = Image.new('RGB', (combined_width, max_height), 'white')
            
            # Cola imagens
            combined_img.paste(img1, (0, 0))
            combined_img.paste(img2, (img1.width + 10, 0))
            
            # Adiciona labels
            draw = ImageDraw.Draw(combined_img)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((10, 10), "ANTES", fill="blue", font=font)
            draw.text((img1.width + 20, 10), "DEPOIS", fill="green", font=font)
            
            # Salva comparação
            comparison_path = before_path.replace(".png", "_comparison.png")
            combined_img.save(comparison_path)
            
            self.logger.info(f"🔍 Comparação criada: {comparison_path}")
            return comparison_path
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar comparação: {e}")
            return ""
    
    def get_session_screenshots(self, session_id: str = None) -> List[ScreenshotMetadata]:
        """Obtém screenshots de uma sessão"""
        if session_id:
            return [m for m in self.metadata if session_id in m.tags]
        return [m for m in self.metadata]
    
    def cleanup_old_screenshots(self, days_old: int = 7) -> int:
        """Remove screenshots antigos"""
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 3600)
        removed_count = 0
        
        try:
            for screenshot_dir in [self.base_dir] + list(self.subdirs.values()):
                for file_path in screenshot_dir.glob("*.png"):
                    if file_path.stat().st_mtime < cutoff_date:
                        file_path.unlink()
                        removed_count += 1
            
            # Remove metadados correspondentes
            self.metadata = [m for m in self.metadata 
                           if m.timestamp.timestamp() > cutoff_date]
            
            self.logger.info(f"🧹 {removed_count} screenshots antigos removidos")
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro na limpeza: {e}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Estatísticas dos screenshots"""
        if not self.metadata:
            return {"total": 0, "success": 0, "errors": 0}
        
        total = len(self.metadata)
        successful = len([m for m in self.metadata if m.success])
        errors = total - successful
        
        total_size = sum(m.file_size for m in self.metadata if m.success)
        avg_size = total_size / successful if successful > 0 else 0
        
        # Estatísticas por ação
        actions = {}
        for meta in self.metadata:
            action = meta.action
            if action not in actions:
                actions[action] = {"count": 0, "success": 0}
            actions[action]["count"] += 1
            if meta.success:
                actions[action]["success"] += 1
        
        return {
            "total": total,
            "successful": successful,
            "errors": errors,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "total_size_mb": total_size / (1024 * 1024),
            "average_size_kb": avg_size / 1024,
            "actions": actions,
            "directories": {
                name: len(list(path.glob("*.png"))) 
                for name, path in self.subdirs.items()
            }
        }
    
    def export_session_report(self, session_id: str = None) -> Dict[str, Any]:
        """Exporta relatório de sessão com screenshots"""
        screenshots = self.get_session_screenshots(session_id)
        
        report = {
            "session_id": session_id or "all",
            "generated_at": datetime.now().isoformat(),
            "statistics": self.get_statistics(),
            "screenshots": []
        }
        
        for meta in screenshots:
            screenshot_data = {
                "filename": os.path.basename(meta.filename),
                "timestamp": meta.timestamp.isoformat(),
                "action": meta.action,
                "url": meta.url,
                "success": meta.success,
                "size_kb": meta.file_size / 1024,
                "tags": meta.tags
            }
            
            if not meta.success and meta.error_message:
                screenshot_data["error"] = meta.error_message
            
            report["screenshots"].append(screenshot_data)
        
        return report


# Instância global
screenshot_manager = ScreenshotManager()


def get_screenshot_manager() -> ScreenshotManager:
    """Obtém instância do gerenciador de screenshots"""
    return screenshot_manager


if __name__ == "__main__":
    # Teste do sistema de screenshots
    manager = ScreenshotManager()
    
    # Simula captura de screenshot
    import asyncio
    
    async def test_screenshot():
        # Simula metadados (sem página real)
        from unittest.mock import Mock
        
        mock_page = Mock()
        mock_page.url = "https://example.com"
        mock_page.evaluate = lambda x: {"width": 1920, "height": 1080}
        mock_page.screenshot = lambda **kwargs: None
        
        # Testa captura
        metadata = await manager.capture_screenshot(
            None,  # Sem página real
            "test_action",
            "debug",
            tags=["test", "demo"]
        )
        
        # Estatísticas
        stats = manager.get_statistics()
        print("📊 Estatísticas de Screenshots:")
        print(f"Total: {stats['total']}")
        print(f"Sucessos: {stats['successful']}")
        print(f"Erros: {stats['errors']}")
        
        return stats
    
    asyncio.run(test_screenshot())
