from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from collections import Counter
import locale
import os
import random

class ReportGenerator:
    def __init__(self):
        self.width = 1920
        self.bg_red = (220, 38, 38)
        self.card_white = (255, 255, 255)
        self.text_red = (220, 38, 38)
        self.text_dark = (31, 41, 55)
        self.text_light = (107, 114, 128)
        
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'es_ES')
            except:
                pass
        
    def generate_report(
        self, 
        analysis: dict, 
        session_photo_path: str = None,
        logo_path: str = None,
        session_number: int = 1,
        total_sessions: int = 8,
        student_name: str = "",
        teacher_name: str = "",
        session_date: str = None
    ) -> str:
        border_color = self._extract_logo_color(logo_path)
        font_set = self._create_fonts()
        dimensions = self._calculate_dimensions(analysis, session_photo_path, font_set)
        
        img = self._create_base_image(dimensions['height'], border_color)
        draw = ImageDraw.Draw(img)
        
        card_coords = self._calculate_card_coords(dimensions['height'])
        self._draw_card(draw, card_coords)
        self._draw_header(draw, card_coords, session_number, total_sessions, session_date, font_set)
        
        if logo_path and os.path.exists(logo_path):
            self._draw_logo(img, card_coords, logo_path)
        
        photo_y = self._draw_session_photo(img, draw, card_coords, session_photo_path, student_name, teacher_name, font_set)
        content_y = photo_y + 60 if session_photo_path and os.path.exists(session_photo_path) else card_coords['y1'] + 170
        
        col_margin = 100
        col_width = (card_coords['x2'] - card_coords['x1'] - 3 * col_margin) // 2
        
        max_y = self._draw_content_sections(draw, card_coords, content_y, col_margin, col_width, analysis, font_set)
        self._draw_bottom_sections(draw, card_coords, max_y, col_margin, col_width, analysis, font_set)
        self._draw_footer(draw, card_coords, font_set)
        
        return self._save_report(img)
    
    def _get_safe_font(self, size=20, bold=False):
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except Exception:
            return ImageFont.load_default()
    
    def _create_fonts(self):
        return {
            'banner': self._get_safe_font(56, True),
            'date': self._get_safe_font(28),
            'heading': self._get_safe_font(36, True),
            'body': self._get_safe_font(22),
            'small': self._get_safe_font(18)
        }
    
    def _calculate_dimensions(self, analysis, session_photo_path, fonts):
        card_margin = 80
        col_margin = 100
        col_width = (self.width - 2 * card_margin - 3 * col_margin) // 2
        
        header_space = 170
        photo_space = 225 + 60 if session_photo_path and os.path.exists(session_photo_path) else 0
        
        obj_space = self._calculate_section_space(analysis.get('objetivos', []), fonts['body'], col_width, 3)
        dev_bullets = analysis.get('desarrollo', '').split('.')[:4]
        dev_space = self._calculate_section_space(dev_bullets, fonts['body'], col_width, 4, is_sentences=True)
        
        rec_lines = self._wrap_text(analysis.get('recomendaciones', ''), fonts['body'], col_width)
        rec_space = 50 + (min(len(rec_lines), 8) * 30)
        
        act_lines = self._wrap_text(analysis.get('actitud', ''), fonts['body'], col_width)
        act_space = 50 + (min(len(act_lines), 8) * 30)
        
        content_space = max(obj_space, dev_space)
        bottom_space = max(rec_space, act_space)
        total_height = header_space + photo_space + content_space + 60 + bottom_space + 100
        
        calculated_height = max(1080, total_height + 2 * card_margin + 100)
        
        return {'height': calculated_height}
    
    def _calculate_section_space(self, items, font, max_width, max_items, is_sentences=False):
        if isinstance(items, str):
            items = [items]
        
        lines_count = 0
        for item in items[:max_items]:
            if is_sentences and not item.strip():
                continue
            prefix = f"• {item.strip()}." if is_sentences else f"• {item}"
            lines = self._wrap_text(prefix, font, max_width)
            lines_count += min(len(lines), 2)
        
        return 50 + (lines_count * 30) + (len(items[:max_items]) * 5)
    
    def _extract_logo_color(self, logo_path):
        if not logo_path or not os.path.exists(logo_path):
            return self.bg_red
        try:
            logo = Image.open(logo_path).convert('RGB')
            logo.thumbnail((100, 100))
            pixels = list(logo.getdata())
            return Counter(pixels).most_common(1)[0][0]
        except Exception:
            return self.bg_red
    
    def _create_base_image(self, height, border_color):
        img = Image.new('RGB', (self.width, height), border_color)
        draw = ImageDraw.Draw(img)
        
        for i in range(height):
            alpha = abs(i - height // 2) / (height // 2)
            color = tuple(int(border_color[j] * (1 - alpha * 0.3)) for j in range(3))
            draw.rectangle([0, i, 100, i + 1], fill=color)
            draw.rectangle([self.width - 100, i, self.width, i + 1], fill=color)
        
        self._draw_math_background(draw, height)
        return img
    
    def _draw_math_background(self, draw, height):
        font_math = self._get_safe_font(40)
        formulas = ["β", "∫", "+", "÷", "α", "π", "Σ", "∞", "√", "≠", "≤", "≥",
                   "x²", "y", "sin", "cos", "θ", "∂", "∆", "λ", "μ", "σ"]
        
        for _ in range(30):
            formula = random.choice(formulas)
            x = random.randint(50, self.width - 100)
            y = random.randint(50, height - 100)
            draw.text((x, y), formula, font=font_math, fill=(255, 255, 255))
    
    def _calculate_card_coords(self, height):
        margin = 80
        return {
            'x1': margin,
            'y1': margin,
            'x2': self.width - margin,
            'y2': height - margin
        }
    
    def _draw_card(self, draw, coords):
        self._draw_rounded_rectangle(draw, 
                                     [coords['x1'], coords['y1'], coords['x2'], coords['y2']], 
                                     radius=30, fill=self.card_white)
    
    def _draw_rounded_rectangle(self, draw, coords, radius=20, fill=None, outline=None, width=1):
        x1, y1, x2, y2 = coords
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill, outline=outline, width=width)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill, outline=outline, width=width)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill, outline=outline, width=width)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill, outline=outline, width=width)
    
    def _draw_header(self, draw, coords, session_number, total_sessions, session_date, fonts):
        banner_coords = [coords['x1'] + 40, coords['y1'] + 20, coords['x1'] + 580, coords['y1'] + 120]
        self._draw_rounded_rectangle(draw, banner_coords, radius=15, fill=self.text_red)
        
        session_text = f"SESIÓN N° {session_number} DE {total_sessions}"
        draw.text((coords['x1'] + 70, coords['y1'] + 55), session_text, 
                 font=fonts['banner'], fill=(255, 255, 255))
        
        date_str = self._format_date(session_date)
        draw.text((coords['x1'] + 630, coords['y1'] + 60), date_str, 
                 font=fonts['date'], fill=self.text_dark)
    
    def _format_date(self, session_date):
        if session_date:
            try:
                date_obj = datetime.strptime(session_date, "%Y-%m-%d")
                return date_obj.strftime("%d de %B de %Y")
            except:
                pass
        return datetime.now().strftime("%d de %B de %Y")
    
    def _draw_logo(self, img, coords, logo_path):
        try:
            logo_img = Image.open(logo_path).convert('RGBA')
            logo_size = 120
            logo_img.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            mask = Image.new('L', (logo_size, logo_size), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, logo_size, logo_size], fill=255)
            
            output = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
            output.paste(logo_img.resize((logo_size, logo_size)), (0, 0))
            output.putalpha(mask)
            
            img.paste(output, (coords['x2'] - 180, coords['y1'] + 20), output)
        except Exception as e:
            print(f"Error loading logo: {e}")
    
    def _draw_session_photo(self, img, draw, coords, photo_path, student_name, teacher_name, fonts):
        photo_y = coords['y1'] + 170
        
        if not photo_path or not os.path.exists(photo_path):
            return photo_y
        
        try:
            photo = Image.open(photo_path).convert('RGB')
            photo.thumbnail((800, 225), Image.Resampling.LANCZOS)
            
            photo_x = (self.width - photo.width) // 2
            img.paste(photo, (photo_x, photo_y))
            
            name_y = photo_y + photo.height + 10
            draw.text((photo_x + 30, name_y), student_name, font=fonts['small'], fill=self.text_dark)
            draw.text((photo_x + photo.width - 200, name_y), teacher_name, font=fonts['small'], fill=self.text_dark)
            
            return name_y
        except Exception:
            return photo_y
    
    def _draw_content_sections(self, draw, coords, content_y, col_margin, col_width, analysis, fonts):
        obj_x = coords['x1'] + col_margin
        dev_x = coords['x1'] + 2 * col_margin + col_width
        section_y = content_y + 20
        
        max_obj_y = self._draw_section(draw, obj_x, section_y, "Objetivos de la Sesión",
                                       analysis.get('objetivos', []), col_width, fonts, max_items=3)
        
        dev_bullets = analysis.get('desarrollo', '').split('.')[:4]
        max_dev_y = self._draw_section(draw, dev_x, section_y, "Desarrollo de la Sesión",
                                       dev_bullets, col_width, fonts, max_items=4, is_sentences=True)
        
        return max(max_obj_y, max_dev_y)
    
    def _draw_section(self, draw, x, y, title, items, max_width, fonts, max_items=3, is_sentences=False):
        draw.text((x, y), title, font=fonts['heading'], fill=self.text_red)
        
        if isinstance(items, str):
            items = [items]
        
        text_y = y + 50
        max_y = text_y
        
        for item in items[:max_items]:
            if is_sentences and not item.strip():
                continue
            
            prefix = f"• {item.strip()}." if is_sentences else f"• {item}"
            lines = self._wrap_text(prefix, fonts['body'], max_width)
            
            for line in lines[:2]:
                draw.text((x, text_y), line, font=fonts['body'], fill=self.text_dark)
                text_y += 30
                max_y = max(max_y, text_y)
            text_y += 5
        
        return max_y
    
    def _draw_bottom_sections(self, draw, coords, max_y, col_margin, col_width, analysis, fonts):
        bottom_y = max_y + 60
        
        obj_x = coords['x1'] + col_margin
        dev_x = coords['x1'] + 2 * col_margin + col_width
        
        self._draw_text_section(draw, obj_x, bottom_y, "Recomendación y Próximos Pasos",
                               analysis.get('recomendaciones', ''), col_width, fonts, coords['y2'])
        
        self._draw_text_section(draw, dev_x, bottom_y, "Actitud en Clase",
                               analysis.get('actitud', ''), col_width, fonts, coords['y2'])
    
    def _draw_text_section(self, draw, x, y, title, text, max_width, fonts, max_y):
        draw.text((x, y), title, font=fonts['heading'], fill=self.text_red)
        
        lines = self._wrap_text(text, fonts['body'], max_width)
        text_y = y + 50
        
        for line in lines[:8]:
            if text_y + 30 < max_y - 80:
                draw.text((x, text_y), line, font=fonts['body'], fill=self.text_dark)
                text_y += 30
    
    def _draw_footer(self, draw, coords, fonts):
        footer_y = coords['y2'] - 40
        draw.text((coords['x1'] + 100, footer_y), 
                 "Generado automáticamente por More Insight Engine", 
                 font=fonts['small'], fill=self.text_light)
        draw.text((coords['x2'] - 350, footer_y), 
                 f"© {datetime.now().year} More Academy", 
                 font=fonts['small'], fill=self.text_light)
    
    def _wrap_text(self, text, font, max_width):
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
    
    def _save_report(self, img):
        output_path = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("reports", exist_ok=True)
        img.save(output_path, 'PNG', quality=95)
        return output_path
