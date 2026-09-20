# -*- coding: utf-8 -*-
"""
Generate Video Frames for S-Project
Seoul Milk Brand Identity: Fresh White & Seoul Milk Green (#008B47)
Crisp typography, proper Korean text wrapping, hanging indents, and balanced spacing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    return ImageFont.truetype(path, size)

# Brand Color Palette - Seoul Milk Fresh White & Bio Green
C_BG = (255, 255, 255)                  # Pure Milk White
C_BG_CARD = (255, 255, 255)             # Crisp Pure White Card
C_BORDER_CARD = (218, 225, 233)         # Soft Slate Border
C_GREEN_PRIMARY = (0, 139, 71)          # #008B47 Seoul Milk Signature Green
C_GREEN_DARK = (5, 122, 70)             # #057A46 Dark Green
C_GREEN_LIGHT = (240, 253, 244)         # #F0FDF4 Soft Milk Mint
C_GREEN_BORDER = (167, 243, 208)        # #A7F3D0 Fresh Mint Outline
C_TEXT_TITLE = (15, 23, 42)             # Slate 900 Deep Charcoal
C_TEXT_KEYWORD = (15, 23, 42)           # Slate 900 Bold
C_TEXT_BODY = (51, 65, 85)              # Slate 700
C_TEXT_MUTED = (100, 116, 139)          # Slate 500
C_LINE_DIVIDER = (226, 232, 240)        # #E2E8F0 Soft Divider

def draw_wrapped_bullet(draw, bullet_text, x_marker, x_text, y_start, max_width, f_bold, f_reg, line_h=38):
    """
    Renders bullet text with:
    - Seoul Milk Green bullet pill at (x_marker, y_start)
    - Bold keyword before ':'
    - Clean word-wrapping and hanging indent for subsequent lines
    Returns the total height consumed.
    """
    # Draw green bullet pill
    pill_w, pill_h = 16, 16
    draw.rounded_rectangle(
        [(x_marker, y_start + 6), (x_marker + pill_w, y_start + 6 + pill_h)],
        radius=4, fill=C_GREEN_PRIMARY
    )

    if ":" in bullet_text:
        parts = bullet_text.split(":", 1)
        key_str = parts[0].strip() + " : "
        val_str = parts[1].strip()

        # Measure keyword width
        key_bbox = draw.textbbox((0, 0), key_str, font=f_bold)
        key_w = key_bbox[2] - key_bbox[0]

        # Draw keyword
        draw.text((x_text, y_start), key_str, font=f_bold, fill=C_TEXT_KEYWORD)

        # Word wrap the value part
        words = val_str.split(" ")
        line1_words = []
        remaining_words = []
        cur_w = key_w

        for idx, w in enumerate(words):
            w_bbox = draw.textbbox((0, 0), " " + w if line1_words else w, font=f_reg)
            word_w = w_bbox[2] - w_bbox[0]
            if cur_w + word_w <= max_width:
                line1_words.append(w)
                cur_w += word_w
            else:
                remaining_words = words[idx:]
                break

        draw.text((x_text + key_w, y_start), " ".join(line1_words), font=f_reg, fill=C_TEXT_BODY)

        if remaining_words:
            # Line 2 with hanging indent at x_text
            line2_str = " ".join(remaining_words)
            draw.text((x_text, y_start + line_h), line2_str, font=f_reg, fill=C_TEXT_BODY)
            return line_h * 2
        return line_h
    else:
        # No colon: regular wrap
        words = bullet_text.split(" ")
        lines = []
        cur_line = []
        cur_w = 0

        for w in words:
            w_bbox = draw.textbbox((0, 0), " " + w if cur_line else w, font=f_reg)
            word_w = w_bbox[2] - w_bbox[0]
            if cur_w + word_w <= max_width:
                cur_line.append(w)
                cur_w += word_w
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
                cur_w = word_w
        if cur_line:
            lines.append(" ".join(cur_line))

        for idx, l in enumerate(lines):
            draw.text((x_text, y_start + idx * line_h), l, font=f_reg, fill=C_TEXT_BODY)
        return line_h * len(lines)

def render_scene_image(scene_data, scene_num, total_scenes=7, output_path="frame.png"):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=C_BG)
    draw = ImageDraw.Draw(img)

    # Top accent line - Seoul Milk Fresh Green
    draw.rectangle([(0, 0), (width, 10)], fill=C_GREEN_PRIMARY)

    # Top brand bar
    font_brand = get_font(21, bold=True)
    draw.text((80, 38), "(주)삼원팜텍  |  SAMWON PHARMTECH", font=font_brand, fill=C_GREEN_PRIMARY)
    
    font_sub_brand = get_font(20, bold=False)
    sub_title = "서울우유 한일사료 임가공(월 18,000톤) 맞춤형 제안"
    sub_bbox = draw.textbbox((0, 0), sub_title, font=font_sub_brand)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text((width - 80 - sub_w, 38), sub_title, font=font_sub_brand, fill=C_TEXT_MUTED)

    # Divider
    draw.line([(80, 80), (width - 80, 80)], fill=C_LINE_DIVIDER, width=2)

    # Scene Tag Pill
    tag_font = get_font(18, bold=True)
    tag_text = scene_data["header_tag"]
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    pill_right = 96 + tag_w + 24
    draw.rounded_rectangle([(80, 108), (pill_right, 148)], radius=12, fill=C_GREEN_LIGHT, outline=C_GREEN_PRIMARY, width=2)
    draw.text((92, 116), tag_text, font=tag_font, fill=C_GREEN_DARK)

    # Headline - Large Deep Slate
    hl_font = get_font(40, bold=True)
    draw.text((80, 170), scene_data["headline"], font=hl_font, fill=C_TEXT_TITLE)

    # Subheadline - Seoul Milk Green
    sub_font = get_font(24, bold=True)
    draw.text((80, 235), scene_data["subheadline"], font=sub_font, fill=C_GREEN_PRIMARY)

    # Main Card Box (Pure White with Soft Subtle Border and Top Accent)
    card_top = 295
    card_bottom = 855
    # Soft backplate shadow/border
    draw.rounded_rectangle([(78, card_top - 2), (width - 78, card_bottom + 2)], radius=20, fill=(245, 247, 250))
    draw.rounded_rectangle([(80, card_top), (width - 80, card_bottom)], radius=18, fill=C_BG_CARD, outline=C_BORDER_CARD, width=2)
    # Card top green accent line
    draw.rounded_rectangle([(80, card_top), (width - 80, card_top + 6)], radius=4, fill=C_GREEN_PRIMARY)

    # Bullets inside card
    f_bullet_reg = get_font(25, bold=False)
    f_bullet_bold = get_font(25, bold=True)
    
    bullets = scene_data["bullets"]
    num_b = len(bullets)
    
    # Dynamic vertical spacing based on bullet count
    if num_b <= 4:
        start_y = card_top + 45
        gap_y = 96
    else:
        start_y = card_top + 32
        gap_y = 80

    for idx, bullet in enumerate(bullets):
        by = start_y + idx * gap_y
        draw_wrapped_bullet(
            draw=draw,
            bullet_text=bullet,
            x_marker=125,
            x_text=165,
            y_start=by,
            max_width=1620,
            f_bold=f_bullet_bold,
            f_reg=f_bullet_reg,
            line_h=38
        )

    # Highlight Banner at Bottom of Card
    draw.rounded_rectangle([(110, 755), (width - 110, 830)], radius=14, fill=C_GREEN_LIGHT, outline=C_GREEN_BORDER, width=2)
    hi_font = get_font(23, bold=True)
    hi_text = "★  " + scene_data["highlight"]
    hi_bbox = draw.textbbox((0, 0), hi_text, font=hi_font)
    hi_w = hi_bbox[2] - hi_bbox[0]
    hi_x = (width - hi_w) // 2
    draw.text((hi_x, 775), hi_text, font=hi_font, fill=C_GREEN_DARK)

    # Bottom Footer
    draw.line([(80, 990), (width - 80, 990)], fill=C_LINE_DIVIDER, width=1)
    footer_font = get_font(18, bold=False)
    draw.text((80, 1015), "(주)삼원팜텍 대표이사 김한호  |  충북 옥천 테크노밸리 첨단 R&D 제조 공장  |  국가 조달청 관납 전국 총판", font=footer_font, fill=C_TEXT_MUTED)
    
    page_font = get_font(20, bold=True)
    page_text = f"Scene {scene_num:02d} / {total_scenes:02d}"
    p_bbox = draw.textbbox((0, 0), page_text, font=page_font)
    p_w = p_bbox[2] - p_bbox[0]
    draw.text((width - 80 - p_w, 1015), page_text, font=page_font, fill=C_GREEN_PRIMARY)

    img.save(output_path, quality=98)
    print(f"Generated frame: {output_path}")

def generate_all_frames():
    from generate_audio import SCENES
    out_dir = r"C:\Users\master\vet_animal_hospital\s_project\frames"
    os.makedirs(out_dir, exist_ok=True)
    for i, scene in enumerate(SCENES, start=1):
        out_path = os.path.join(out_dir, f"scene_{i:02d}.png")
        render_scene_image(scene, i, len(SCENES), out_path)

if __name__ == "__main__":
    generate_all_frames()
