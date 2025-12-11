from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import os

class ReportGenerator:
    def __init__(self):
        # Dimensiones del reporte (Full HD)
        self.width = 1920
        self.height = 1080
        
        # Colores (basados en More Insight branding)
        self.primary_color = (59, 130, 246)  # Azul índigo
        self.bg_color = (240, 245, 255)  # Azul muy claro
        self.text_dark = (17, 24, 39)  # Gris oscuro
        self.text_light = (107, 114, 128)  # Gris medio
        self.accent_green = (16, 185, 129)  # Verde
        self.accent_red = (239, 68, 68)  # Rojo
        
    def _get_safe_font(self, size=20, bold=False):
        """Intenta cargar una fuente, usa default si falla"""
        try:
            if bold:
                return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            return ImageFont.load_default()
    
    def _draw_rounded_rectangle(self, draw, coords, radius=20, fill=None, outline=None):
        """Dibuja un rectángulo con esquinas redondeadas"""
        x1, y1, x2, y2 = coords
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline)
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill, outline=outline)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill, outline=outline)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill, outline=outline)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill, outline=outline)
    
    def _wrap_text(self, text, font, max_width):
        """Envuelve texto para que quepa en un ancho máximo"""
        lines = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                if bbox[2] - bbox[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
        return lines
    
    def _add_photo(self, img, photo_path, position, size=(300, 300)):
        """Agrega una foto circular al reporte"""
        if not photo_path or not os.path.exists(photo_path):
            # Si no hay foto, dibujar un placeholder
            draw = ImageDraw.Draw(img)
            x, y = position
            w, h = size
            self._draw_rounded_rectangle(draw, [x, y, x + w, y + h], radius=150, fill=(200, 200, 200))
            return
        
        try:
            photo = Image.open(photo_path).convert('RGB')
            photo = photo.resize(size, Image.Resampling.LANCZOS)
            
            # Crear máscara circular
            mask = Image.new('L', size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, size[0], size[1]], fill=255)
            
            # Aplicar máscara
            output = Image.new('RGBA', size, (0, 0, 0, 0))
            output.paste(photo, (0, 0))
            output.putalpha(mask)
            
            # Pegar en imagen principal
            img.paste(output, position, output)
        except Exception as e:
            print(f"Error cargando foto: {e}")
    
    def generate_report(
        self, 
        analysis: dict, 
        session_photo_path: str = None,
        session_number: int = 1,
        total_sessions: int = 8,
        student_name: str = "",
        teacher_name: str = ""
    ) -> str:
        """
        Genera un reporte visual en formato PNG
        
        Args:
            analysis: Diccionario con el análisis pedagógico
            session_photo_path: Path a la foto horizontal de la sesión (ambos participantes)
            session_number: Número de sesión actual
            total_sessions: Total de sesiones
            student_name: Nombre del estudiante
            teacher_name: Nombre del profesor
            
        Returns:
            Path al archivo PNG generado
        """
        # Crear imagen base
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Fonts
        font_title = self._get_safe_font(48, bold=True)
        font_subtitle = self._get_safe_font(24)
        font_heading = self._get_safe_font(32, bold=True)
        font_body = self._get_safe_font(20)
        font_small = self._get_safe_font(16)
        
        # HEADER - Banda superior con degradado simulado
        header_height = 120
        for i in range(header_height):
            alpha = i / header_height
            color = tuple(int(self.primary_color[j] * (1 - alpha * 0.3)) for j in range(3))
            draw.rectangle([0, i, self.width, i + 1], fill=color)
        
        # Logo y título
        title_y = 35
        draw.text((60, title_y), "MORE INSIGHT", font=font_title, fill=(255, 255, 255))
        draw.text((60, title_y + 55), "Auditoría Pedagógica con IA", font=font_subtitle, fill=(220, 230, 255))
        
        # Sesión y fecha
        date_str = datetime.now().strftime("%d de %B de %Y")
        session_text = f"SESIÓN N° {session_number} DE {total_sessions}"
        draw.text((self.width - 500, title_y), session_text, font=font_heading, fill=(255, 255, 255))
        draw.text((self.width - 500, title_y + 50), date_str, font=font_body, fill=(220, 230, 255))
        
        # FOTO DE LA SESIÓN (Horizontal - ambos participantes)
        session_y = header_height + 40
        session_width = 960  # Ancho de la foto (la mitad de 1920)
        session_height = 270  # Altura proporcional 16:9
        
        if session_photo_path and os.path.exists(session_photo_path):
            try:
                session_photo = Image.open(session_photo_path).convert('RGB')
                # Redimensionar manteniendo aspecto
                session_photo.thumbnail((session_width, session_height), Image.Resampling.LANCZOS)
                
                # Calcular posición centrada
                photo_x = (self.width - session_photo.width) // 2
                photo_y = session_y
                
                # Crear rectángulo con bordes redondeados como fondo
                self._draw_rounded_rectangle(
                    draw, 
                    [photo_x - 10, photo_y - 10, photo_x + session_photo.width + 10, photo_y + session_photo.height + 10],
                    radius=15,
                    fill=(255, 255, 255)
                )
                
                # Pegar la foto
                img.paste(session_photo, (photo_x, photo_y))
                
                # Nombres debajo de la foto
                draw.text((photo_x + 50, photo_y + session_photo.height + 15), 
                         f"👨‍🎓 {student_name}", font=font_body, fill=self.text_dark)
                draw.text((photo_x + session_photo.width - 250, photo_y + session_photo.height + 15), 
                         f"👩‍🏫 {teacher_name}", font=font_body, fill=self.text_dark)
                
                content_y = photo_y + session_photo.height + 60
            except Exception as e:
                print(f"Error cargando foto de sesión: {e}")
                # Si falla, usar placeholder
                self._draw_rounded_rectangle(draw, [480, session_y, 1440, session_y + session_height], 
                                            radius=15, fill=(220, 220, 220))
                draw.text((self.width // 2 - 100, session_y + session_height // 2), 
                         "Sin foto de sesión", font=font_body, fill=self.text_light)
                content_y = session_y + session_height + 60
        else:
            # Placeholder cuando no hay foto
            placeholder_y = session_y + 20
            draw.text((self.width // 2 - 150, placeholder_y), 
                     f"👨‍🎓 {student_name}  •  👩‍🏫 {teacher_name}", 
                     font=font_heading, fill=self.primary_color)
            content_y = placeholder_y + 60
        
        # SECCIÓN DE CONTENIDO (en dos columnas)
        col1_x = 80
        col2_x = self.width // 2 + 40
        col_width = (self.width // 2) - 120
        
        # COLUMNA 1: Objetivos
        draw.text((col1_x, content_y), "Objetivos de la Sesión", 
                 font=font_heading, fill=self.primary_color)
        
        objetivos = analysis.get('objetivos', [])
        if isinstance(objetivos, str):
            objetivos = [objetivos]
        
        obj_y = content_y + 50
        for objetivo in objetivos[:4]:  # Máximo 4 objetivos
            lines = self._wrap_text(f"• {objetivo}", font_body, col_width)
            for line in lines[:2]:  # Max 2 líneas por objetivo
                draw.text((col1_x, obj_y), line, font=font_body, fill=self.text_dark)
                obj_y += 28
            obj_y += 5
        
        # COLUMNA 2: Desarrollo
        draw.text((col2_x, content_y), "Desarrollo de la Sesión", 
                 font=font_heading, fill=self.primary_color)
        
        desarrollo = analysis.get('desarrollo', 'Sin información disponible.')
        desarrollo_lines = self._wrap_text(desarrollo, font_body, col_width)
        
        dev_y = content_y + 50
        for line in desarrollo_lines[:6]:  # Máximo 6 líneas
            draw.text((col2_x, dev_y), line, font=font_body, fill=self.text_dark)
            dev_y += 28
        
        # SECCIÓN INFERIOR: Actitud y Recomendaciones
        bottom_y = self.height - 280
        
        # Actitud en Clase (izquierda)
        draw.text((col1_x, bottom_y), "Actitud en Clase", 
                 font=font_heading, fill=self.primary_color)
        
        actitud_score = analysis.get('actitud', 85)
        if isinstance(actitud_score, (int, float)):
            if actitud_score >= 80:
                actitud_text = "⭐ Excelente actitud.\nMuy participativo y enfocado."
                actitud_color = self.accent_green
            elif actitud_score >= 60:
                actitud_text = "✓ Buena actitud.\nParticipación aceptable."
                actitud_color = self.primary_color
            else:
                actitud_text = "⚠ Actitud a mejorar.\nRequiere más participación."
                actitud_color = self.accent_red
        else:
            actitud_text = str(actitud_score)
            actitud_color = self.text_dark
        
        act_y = bottom_y + 50
        for line in actitud_text.split('\n'):
            draw.text((col1_x, act_y), line, font=font_body, fill=actitud_color)
            act_y += 30
        
        # Recomendaciones (derecha)
        draw.text((col2_x, bottom_y), "Recomendaciones", 
                 font=font_heading, fill=self.primary_color)
        
        recomendaciones = analysis.get('recomendaciones', 'Continuar con el plan de estudios.')
        rec_lines = self._wrap_text(recomendaciones, font_body, col_width)
        
        rec_y = bottom_y + 50
        for line in rec_lines[:3]:  # Máximo 3 líneas
            draw.text((col2_x, rec_y), line, font=font_body, fill=self.text_dark)
            rec_y += 30
        
        # Footer
        footer_y = self.height - 50
        draw.text((60, footer_y), 
                 "Generado automáticamente por More Insight Engine", 
                 font=font_small, fill=self.text_light)
        draw.text((self.width - 400, footer_y), 
                 f"© {datetime.now().year} More Academy", 
                 font=font_small, fill=self.text_light)
        
        # Guardar imagen
        output_path = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("reports", exist_ok=True)
        img.save(output_path, 'PNG', quality=95)
        
        return output_path
