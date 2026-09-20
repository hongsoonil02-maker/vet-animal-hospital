# -*- coding: utf-8 -*-
"""
Build Complete 30-Slide Presentation Deck (V3 Enhanced Layout)
Seoul Milk Dairy Specialist Solution - (주)삼원팜텍
Fixes small text in boxes/subtitles and empty card layouts globally.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# CI Colors - Seoul Milk Brand Identity (Fresh White Milk & Signature Green)
C_BG_WHITE = RGBColor(255, 255, 255)       # Pure Milk White (#FFFFFF)
C_CARD_BG = RGBColor(255, 255, 255)        # Pure Milk White Card (#FFFFFF)
C_BORDER_SOFT = RGBColor(226, 232, 240)    # Soft Slate Border (#E2E8F0)
C_BORDER_MINT = RGBColor(167, 243, 208)    # Fresh Mint Border (#A7F3D0)

# Seoul Milk Green Accents
C_SEOUL_GREEN = RGBColor(0, 139, 71)       # #008B47 Seoul Milk Signature Green
C_GREEN_DARK = RGBColor(5, 122, 70)        # #057A46 Deep Forest Green
C_MINT_LIGHT = RGBColor(240, 253, 244)     # #F0FDF4 Soft Milk Mint
C_MINT_ACCENT = RGBColor(220, 252, 231)    # #DCFCE7 Mint Badge

# High Contrast Premium Typography
C_TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A Deep Slate Charcoal
C_TEXT_KEYWORD = RGBColor(15, 23, 42)      # #0F172A Slate 900 Bold
C_TEXT_BODY = RGBColor(51, 65, 85)         # #334155 Slate 700
C_TEXT_MUTED = RGBColor(71, 85, 105)       # #475569 Slate 600
C_TEXT_WHITE = RGBColor(255, 255, 255)

# Aliases for backward compatibility
C_NAVY_PRIMARY = C_TEXT_DARK
C_NAVY_LIGHT = C_BORDER_SOFT
C_NAVY_DARK = C_BG_WHITE
C_EMERALD = C_SEOUL_GREEN
C_EMERALD_DARK = C_SEOUL_GREEN
C_EMERALD_LIGHT = C_MINT_LIGHT
C_BG_LIGHT = C_BG_WHITE
C_BORDER = C_BORDER_SOFT

ASSETS_DIR = r"C:\Users\master\vet_animal_hospital\s_project\assets"

IMG_FACTORY = os.path.join(ASSETS_DIR, "company_factory_panorama_1789881641339.jpg")
IMG_FEED_LINE = os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg")
IMG_GRAIN_MARKET = os.path.join(ASSETS_DIR, "grain_market_volatility_1789881820210.jpg")
IMG_DAIRY = os.path.join(ASSETS_DIR, "dairy_cows_smart_farm_1789881841764.jpg")
IMG_CALF = os.path.join(ASSETS_DIR, "dairy_calf_nutrition.jpg")
IMG_CAPSULE = os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg")
IMG_POUCH = os.path.join(ASSETS_DIR, "premix_product_packaging_1789881875376.jpg")
IMG_MASCOT = os.path.join(ASSETS_DIR, "child_drinking_milk.jpg")
IMG_CHILD_MILK = os.path.join(ASSETS_DIR, "child_drinking_milk.jpg")
IMG_CHILD_MILK_GIRL = os.path.join(ASSETS_DIR, "child_drinking_milk_girl.jpg")
IMG_PELLET = os.path.join(ASSETS_DIR, "feed_pellet_extrusion.jpg")
IMG_LAB = os.path.join(ASSETS_DIR, "livestock_nutrition_lab.jpg")

CHART_COST = os.path.join(ASSETS_DIR, "chart_cost_comparison.png")
CHART_HOMOGENEITY = os.path.join(ASSETS_DIR, "chart_homogeneity_cv.png")
CHART_HEAT = os.path.join(ASSETS_DIR, "chart_pellet_heat.png")
CHART_ROI = os.path.join(ASSETS_DIR, "chart_livestock_roi.png")

def apply_slide_bg(slide, prs, color=C_BG_WHITE):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    
    # Top accent line - Seoul Milk Fresh Green
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.06))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_SEOUL_GREEN
    top_line.line.fill.background()
    return bg

def add_header(slide, prs, tag_text, title_text, subtitle_text=""):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.7), Inches(1.25))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_tag = tf.paragraphs[0]
    p_tag.text = f"[ {tag_text} ]"
    p_tag.font.name = "Malgun Gothic"
    p_tag.font.size = Pt(11.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_SEOUL_GREEN
    p_tag.space_after = Pt(2)
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = "Malgun Gothic"
    p_title.font.size = Pt(23)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_DARK
    
    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = "Malgun Gothic"
        p_sub.font.size = Pt(13)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_before = Pt(4)

def add_footer(slide, prs, current_page, total_pages=30):
    fb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(8.5), Inches(0.35))
    tf_l = fb_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "(주)삼원팜텍  |  서울우유 한일사료 임가공 배합 라인 맞춤형 고농축 사료첨가제 제안"
    p_l.font.name = "Malgun Gothic"
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = RGBColor(148, 163, 184)
    
    fb_right = slide.shapes.add_textbox(Inches(9.5), Inches(6.92), Inches(3.0), Inches(0.35))
    tf_r = fb_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.text = f"Slide {current_page:02d} / {total_pages:02d}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = "Malgun Gothic"
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = C_SEOUL_GREEN

def create_card(slide, left, top, width, height, title, body_bullets, tag="", bg_color=C_CARD_BG, border_color=C_BORDER_SOFT, title_color=C_TEXT_DARK):
    """
    Enhanced card component for Seoul Milk White identity:
    - Pure white card background
    - Soft, subtle slate border (C_BORDER_SOFT, width 1.2pt)
    - Seoul Milk Green top accent bar
    - Hanging indent on bullet text (OpenXML marL/indent)
    - Keyword bold highlighting
    - Vertical expansion to fill card height
    """
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    
    # Card top green accent line
    accent_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.12), top, width - Inches(0.24), Pt(3.5))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_SEOUL_GREEN
    accent_bar.line.fill.background()
    
    pad_h = Inches(0.32)
    pad_v = Inches(0.26)
    tb = slide.shapes.add_textbox(left + pad_h, top + pad_v, width - pad_h * 2, height - pad_v * 2)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    w_val = width.inches
    num_b = len(body_bullets) if body_bullets else 1
    
    if w_val >= 5.0:  # Wide split card (5.7")
        sz_tag = Pt(11)
        sz_title = Pt(17)
        title_space_after = Pt(14)
        if num_b <= 5:
            sz_bullet = Pt(12.5)
            space_bullet_before = Pt(4)
            space_bullet_after = Pt(11)
        else:
            sz_bullet = Pt(11.5)
            space_bullet_before = Pt(3)
            space_bullet_after = Pt(7)
    elif w_val >= 3.5:  # 3-column card (3.8")
        sz_tag = Pt(10.5)
        sz_title = Pt(15.5)
        title_space_after = Pt(10)
        if num_b <= 4:
            sz_bullet = Pt(12)
            space_bullet_before = Pt(4)
            space_bullet_after = Pt(10)
        else:
            sz_bullet = Pt(11)
            space_bullet_before = Pt(3)
            space_bullet_after = Pt(6)
    else:  # 4-column card (2.8")
        sz_tag = Pt(9.5)
        sz_title = Pt(13.5)
        title_space_after = Pt(8)
        sz_bullet = Pt(10.5)
        space_bullet_before = Pt(3)
        space_bullet_after = Pt(6)
        
    p0 = tf.paragraphs[0]
    if tag:
        r_tag = p0.add_run()
        r_tag.text = tag + "\n"
        r_tag.font.name = "Malgun Gothic"
        r_tag.font.size = sz_tag
        r_tag.font.bold = True
        r_tag.font.color.rgb = C_SEOUL_GREEN
        
    r_title = p0.add_run()
    r_title.text = title
    r_title.font.name = "Malgun Gothic"
    r_title.font.size = sz_title
    r_title.font.bold = True
    r_title.font.color.rgb = title_color
    p0.space_after = title_space_after
    
    for bullet in body_bullets:
        p_b = tf.add_paragraph()
        p_b.space_before = space_bullet_before
        p_b.space_after = space_bullet_after
        p_b.line_spacing = 1.25
        
        # Hanging indent
        pPr = p_b._p.get_or_add_pPr()
        pPr.set('marL', str(int(Pt(18))))
        pPr.set('indent', str(int(-Pt(18))))
        
        # Bullet marker
        r_icon = p_b.add_run()
        r_icon.text = "▶ "
        r_icon.font.name = "Malgun Gothic"
        r_icon.font.size = sz_bullet - Pt(1.5)
        r_icon.font.bold = True
        r_icon.font.color.rgb = C_SEOUL_GREEN
        
        # Keyword highlighting on colon
        if ":" in bullet:
            parts = bullet.split(":", 1)
            key_part = parts[0].strip() + " :"
            val_part = parts[1]
            
            r_key = p_b.add_run()
            r_key.text = key_part
            r_key.font.name = "Malgun Gothic"
            r_key.font.size = sz_bullet
            r_key.font.bold = True
            r_key.font.color.rgb = C_TEXT_KEYWORD
            
            r_val = p_b.add_run()
            r_val.text = val_part
            r_val.font.name = "Malgun Gothic"
            r_val.font.size = sz_bullet
            r_val.font.bold = False
            r_val.font.color.rgb = C_TEXT_BODY
        else:
            r_b = p_b.add_run()
            r_b.text = bullet
            r_b.font.name = "Malgun Gothic"
            r_b.font.size = sz_bullet
            r_b.font.color.rgb = C_TEXT_BODY
            if "★" in bullet or "100%" in bullet or "1위" in bullet:
                r_b.font.bold = True
                r_b.font.color.rgb = C_GREEN_DARK
                
    return shape

def add_split_slide_with_image(slide, prs, page_num, section_tag, title, subtitle, bullets_data, image_path, img_caption="", mascot_tip=""):
    apply_slide_bg(slide, prs, C_BG_WHITE)
    add_header(slide, prs, section_tag, title, subtitle)
    
    card_w = Inches(5.7)
    card_h = Inches(4.85)
    create_card(slide, Inches(0.8), Inches(1.8), card_w, card_h, bullets_data["title"], bullets_data["bullets"], tag=bullets_data.get("tag", ""), border_color=C_BORDER_SOFT)
    
    img_left = Inches(6.8)
    img_top = Inches(1.8)
    img_w = Inches(5.7)
    img_h = Inches(3.6) if mascot_tip else Inches(4.55)
    
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, img_left, img_top, width=img_w, height=img_h)
        if img_caption:
            tb_c = slide.shapes.add_textbox(img_left, img_top + img_h + Inches(0.04), img_w, Inches(0.28))
            p_c = tb_c.text_frame.paragraphs[0]
            p_c.text = "▲ " + img_caption
            p_c.font.name = "Malgun Gothic"
            p_c.font.size = Pt(9.5)
            p_c.font.bold = True
            p_c.font.color.rgb = C_TEXT_MUTED
            p_c.alignment = PP_ALIGN.CENTER
            
    if mascot_tip:
        tip_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_left, Inches(5.82), img_w, Inches(0.83))
        tip_box.fill.solid()
        tip_box.fill.fore_color.rgb = C_MINT_LIGHT
        tip_box.line.color.rgb = C_BORDER_MINT
        tip_box.line.width = Pt(1.5)
        tf_t = tip_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = Inches(0.2)
        tf_t.margin_right = Inches(0.2)
        p_t = tf_t.paragraphs[0]
        p_t.text = "★ " + mascot_tip
        p_t.font.name = "Malgun Gothic"
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_GREEN_DARK
        p_t.alignment = PP_ALIGN.CENTER
        
    add_footer(slide, prs, page_num)

def add_table_slide(slide, prs, page_num, section_tag, title, subtitle, headers, rows_data, col_widths, top_card_text="", mascot_text=""):
    apply_slide_bg(slide, prs, C_BG_WHITE)
    add_header(slide, prs, section_tag, title, subtitle)
    
    cur_top = Inches(1.8)
    if top_card_text:
        t_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cur_top, Inches(11.7), Inches(0.6))
        t_card.fill.solid()
        t_card.fill.fore_color.rgb = C_MINT_LIGHT
        t_card.line.color.rgb = C_BORDER_MINT
        tf = t_card.text_frame
        tf.margin_left = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = "★ 핵심 비교 포인트: " + top_card_text
        p.font.name = "Malgun Gothic"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_GREEN_DARK
        cur_top += Inches(0.72)
        
    num_rows = len(rows_data) + 1
    num_cols = len(headers)
    
    t_height = Inches(0.45 + 0.42 * len(rows_data))
    table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(0.8), cur_top, Inches(11.7), t_height)
    table = table_shape.table
    
    for c_idx, w in enumerate(col_widths):
        table.columns[c_idx].width = Inches(w)
        
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_GREEN_DARK
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Malgun Gothic"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        
    for r_idx, row in enumerate(rows_data):
        is_highlight = "삼원팜텍" in str(row) or "500g" in str(row) or "3,000원" in str(row)
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = str(val)
            cell.fill.solid()
            if is_highlight:
                cell.fill.fore_color.rgb = C_MINT_LIGHT
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252)
            else:
                cell.fill.fore_color.rgb = C_CARD_BG
                
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx != 1 else PP_ALIGN.LEFT
            p.font.name = "Malgun Gothic"
            p.font.size = Pt(10.5)
            if is_highlight:
                p.font.bold = True
                p.font.color.rgb = C_GREEN_DARK
            else:
                p.font.color.rgb = C_TEXT_DARK
                
    if mascot_text:
        m_top = cur_top + t_height + Inches(0.2)
        if os.path.exists(IMG_MASCOT):
            slide.shapes.add_picture(IMG_MASCOT, Inches(0.8), m_top, Inches(0.95), Inches(0.95))
        m_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.9), m_top, Inches(10.6), Inches(0.95))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = C_CARD_BG
        m_box.line.color.rgb = C_BORDER_MINT
        tf_m = m_box.text_frame
        tf_m.margin_left = Inches(0.2)
        tf_m.margin_right = Inches(0.2)
        p_m = tf_m.paragraphs[0]
        p_m.text = "★ 삼원팜텍 낙농 바이오 연구팀 분석 제언 (신선 원유 & 건강 가치)"
        p_m.font.name = "Malgun Gothic"
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = C_SEOUL_GREEN
        p_m2 = tf_m.add_paragraph()
        p_m2.text = mascot_text
        p_m2.font.name = "Malgun Gothic"
        p_m2.font.size = Pt(10)
        p_m2.font.color.rgb = C_TEXT_DARK
        p_m2.space_before = Pt(2)
        
    add_footer(slide, prs, page_num)

def build_complete_v3_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ====================================================
    # SLIDE 1: Cover (Seoul Milk Fresh White & Bio Green)
    # ====================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1, prs, C_BG_WHITE)
    
    if os.path.exists(IMG_FACTORY):
        s1.shapes.add_picture(IMG_FACTORY, Inches(6.5), Inches(1.05), Inches(6.0), Inches(4.3))
    if os.path.exists(IMG_MASCOT):
        s1.shapes.add_picture(IMG_MASCOT, Inches(10.5), Inches(4.1), Inches(2.1), Inches(2.1))
        
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(5.5), Inches(4.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "주식회사 삼원팜텍  |  SAMWON PHARMTECH"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_SEOUL_GREEN
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "서울우유 사료 품질 혁신 및\n원가 최적화를 위한\n맞춤형 고농축 사료첨가제\n공급 제안서"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(28)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_DARK
    p.space_after = Pt(16)
    
    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "한일사료 임가공 배합 라인(월 18,000 M/T) 전용\n표준 첨가량 500g/ton (0.05%) 낙농 전문 처방"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_MUTED
    
    # Bottom Badge Box
    b_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.2))
    b_box.fill.solid()
    b_box.fill.fore_color.rgb = C_MINT_LIGHT
    b_box.line.color.rgb = C_BORDER_MINT
    b_box.line.width = Pt(1.5)
    tf_b = b_box.text_frame
    tf_b.margin_left = Inches(0.25)
    tf_b.margin_top = Inches(0.18)
    p_b0 = tf_b.paragraphs[0]
    p_b0.text = "제조 및 판매원: 주식회사 삼원팜텍 (대표이사 김한호)"
    p_b0.font.name = "Malgun Gothic"
    p_b0.font.size = Pt(11.5)
    p_b0.font.bold = True
    p_b0.font.color.rgb = C_GREEN_DARK
    
    p_b1 = tf_b.add_paragraph()
    p_b1.text = "충북 옥천 테크노밸리 첨단 R&D 제조 본사 및 공장  |  국가 조달청 관납 전국 총판  |  2026. 09"
    p_b1.font.name = "Malgun Gothic"
    p_b1.font.size = Pt(10)
    p_b1.font.color.rgb = C_TEXT_MUTED
    p_b1.space_before = Pt(4)
    
    add_footer(s1, prs, 1)

    # ====================================================
    # SLIDE 2: Executive Summary (4 Hero KPIs + Mascot + Pouch)
    # ====================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2, prs, C_BG_WHITE)
    add_header(s2, prs, "EXECUTIVE SUMMARY", "핵심 제안 요약: 낙농 사료 원가는 낮추고 산유량과 유질은 극대화", "한일사료 18,000톤 라인 맞춤형 삼원팜텍 고농축 프리믹스 핵심 4대 지표")
    
    kpis = [
        ("500g", "/ ton", "표준 투입량", ["투입량 혁신 : 시중(1~2kg) 대비 50~75% 절감", "공간 확보 : 배합 공간 1kg 이상 확보", "영양 보존 : 옥수수·대두박 영양 100% 보존"]),
        ("3,000원", "/ ton", "사료 톤당 비용", ["적용 단가 : 제품 기준가 6,000원/kg 적용", "원가 절감 : 기존 대비 톤당 3,000~5,000원 절감", "비용 방어 : 사료 제조원가 즉각 절감"]),
        ("5,400만원", "/ 월", "월간 총 공급액", ["공급 규모 : 월 18,000톤 기준 총 9,000kg", "월간 절감 : 기존 대비 월 최대 1억원 절감", "목장 환원 : 연간 12억원 조합원 목장 환원"]),
        ("CV < 5%", "초정밀", "균질 혼화도", ["공정 일치 : Twin-Shaft 패들 믹서 최적화", "내열성 보증 : 85~110℃ 펠렛열 95% 생존", "품질 보증 : 로트별 공인 COA 무결점 보증"])
    ]
    for i, (num, unit, title, bullets) in enumerate(kpis):
        x = Inches(0.8 + i * 2.95)
        slide_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(3.6))
        slide_card.fill.solid()
        slide_card.fill.fore_color.rgb = C_CARD_BG
        slide_card.line.color.rgb = C_BORDER_SOFT
        slide_card.line.width = Pt(1.2)
        
        # Card top accent line
        c_acc = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.1), Inches(1.8), Inches(2.6), Pt(3.5))
        c_acc.fill.solid()
        c_acc.fill.fore_color.rgb = C_SEOUL_GREEN
        c_acc.line.fill.background()
        
        tb = s2.shapes.add_textbox(x + Inches(0.18), Inches(1.95), Inches(2.44), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"0{i+1}. {title}"
        p0.font.name = "Malgun Gothic"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = C_SEOUL_GREEN
        
        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = num
        r1.font.name = "Malgun Gothic"
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_SEOUL_GREEN
        
        r2 = p1.add_run()
        r2.text = " " + unit
        r2.font.name = "Malgun Gothic"
        r2.font.size = Pt(12)
        r2.font.color.rgb = C_TEXT_MUTED
        p1.space_after = Pt(10)
        
        for b in bullets:
            pb = tf.add_paragraph()
            pb.space_before = Pt(3)
            pb.space_after = Pt(4)
            pb.line_spacing = 1.15
            
            pPr = pb._p.get_or_add_pPr()
            pPr.set('marL', str(int(Pt(14))))
            pPr.set('indent', str(int(-Pt(14))))
            
            parts = b.split(":", 1)
            r_k = pb.add_run()
            r_k.text = "▶ " + parts[0].strip() + " :"
            r_k.font.name = "Malgun Gothic"
            r_k.font.size = Pt(10.5)
            r_k.font.bold = True
            r_k.font.color.rgb = C_TEXT_KEYWORD
            
            r_v = pb.add_run()
            r_v.text = parts[1]
            r_v.font.name = "Malgun Gothic"
            r_v.font.size = Pt(10)
            r_v.font.color.rgb = C_TEXT_BODY
            
    if os.path.exists(IMG_MASCOT):
        s2.shapes.add_picture(IMG_MASCOT, Inches(0.8), Inches(5.6), Inches(1.2), Inches(1.2))
    banner = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(5.6), Inches(10.3), Inches(1.2))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_MINT_LIGHT
    banner.line.color.rgb = C_BORDER_MINT
    banner.line.width = Pt(1.5)
    tf_b = banner.text_frame
    tf_b.margin_left = Inches(0.3)
    p_b = tf_b.paragraphs[0]
    p_b.text = "★ 삼원팜텍 스마트 바이오 솔루션 : 검증된 조달청 관납 기술력으로 서울우유 조합원 목장의 산유량과 1등급 유질을 지켜냅니다!"
    p_b.font.name = "Malgun Gothic"
    p_b.font.size = Pt(12.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_GREEN_DARK
    add_footer(s2, prs, 2)

    # ====================================================
    # SLIDE 3: Agenda (6 Visual Cards)
    # ====================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3, prs, C_BG_WHITE)
    add_header(s3, prs, "AGENDA", "제안서 목차 및 프레젠테이션 진행 순서", "체계적인 6개 부문 분석 및 실행 로드맵")
    
    tocs = [
        ("Part I", "제안 배경 및 낙농 환경 분석", ["국제 원료곡 시세 변동 추이", "하절기 혹서기 열 스트레스 대응", "서울우유 한일사료 라인 현황"]),
        ("Part II", "제안사 역량 및 공공 신뢰도", ["(주)삼원팜텍 기업 개요 및 시설", "국가 조달청 관납 전국 총판 실적", "옥천 공장 5단계 품질 검증 체계"]),
        ("Part III", "핵심 경제성 및 밸류 분석", ["500g/ton 처방의 공학적 의의", "사료 톤당 3,000원 원가 절감", "월 1억원·연 12억원 절감 분석"]),
        ("Part IV", "8대 핵심 낙농 솔루션 스펙", ["기호성 향미제 & 반추위 효소제", "코팅 GABA & 고활성 효모균", "몬모릴로나이트 독소흡착 & 천연제제"]),
        ("Part V", "한일사료 임가공 공정 적합성", ["Twin-Shaft 패들 혼화도(CV<5%)", "스팀 펠렛 가공열(105℃) 내열성", "안티케이킹 자유 유동성 설계"]),
        ("Part VI", "낙농 기대효과 및 실행 로드맵", ["착유우 산유량 방어 (+1.8kg/일)", "원유 유질 개선 (체세포수 -42%)", "3단계 실증 및 무중단 공급 보증"])
    ]
    for i, (part, title, desc_list) in enumerate(tocs):
        row = i // 3
        col = i % 3
        create_card(s3, Inches(0.8 + col * 3.95), Inches(1.8 + row * 2.45), Inches(3.8), Inches(2.25), f"{part}. {title}", desc_list, tag=f"SECTION 0{i+1}", border_color=C_BORDER_SOFT)
    add_footer(s3, prs, 3)

    # ====================================================
    # SLIDE 4: Grain Market Crisis (WITH BLOOMBERG CHART)
    # ====================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s4, prs, 4, "PART I. 제안 배경", "낙농업계 3중고(三重苦)와 서울우유의 당면 과제",
                                "원료곡 가격 폭등 및 고온 스트레스 속 낙농 사료 배합 원가 방어 전략",
                                {"title": "낙농업계 및 목장 3대 비상 현안",
                                 "tag": "CRISIS FACTORS",
                                 "bullets": [
                                     "국제 원료곡 시세 급등: 옥수수·대두박 가격 폭등으로 사료 제조원가 압박 심화",
                                     "혹서기 기후 위기: 하절기 폭염 일수 증가로 젖소 건물섭취량(DMI) 급감",
                                     "산유량 및 유질 저하: 착유우 산유량 급감, 체세포수 급증, 유방염 질병 빈발",
                                     "무항생제 축산 정책: 친환경 면역 강화 및 천연 기능성 물질 도입 시급",
                                     "원가·품질 동시 방어: 사료 원가는 엄격히 절감하면서 유질을 지킬 처방 필수"
                                 ]},
                                IMG_GRAIN_MARKET, "국제 사료 원료곡 가격 변동 추이 및 세계 해상 공급망 동향 대시보드",
                                "글로벌 곡물가 변동 속에서 낙농 사료 원가 절감은 선택이 아닌 필수 과제입니다!")

    # ====================================================
    # SLIDE 5: Hanil Feed Production Line (WITH FACTORY LINE PHOTO)
    # ====================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s5, prs, 5, "PART I. 제안 배경", "서울우유 한일사료 임가공 배합 라인(월 18,000 M/T) 현황",
                                "대규모 임가공 생산 체계에 완벽히 부합하는 낙농 전용 첨가제 처방의 필요성",
                                {"title": "월 18,000톤 임가공 라인 핵심 요구",
                                 "tag": "PRODUCTION INFRA",
                                 "bullets": [
                                     "대규모 생산 체계: 배합사료 월 18,000 M/T (연간 216,000 M/T 대형 설비)",
                                     "고속 혼합 공정: Twin-Shaft 패들 믹서 및 마이크로 인그리디언트 자동 빈",
                                     "복합 가공 형태: 가루사료(Mash), 펠렛(Pellet), 익스팬더 사료 동시 대응",
                                     "초정밀 혼화도: 사료 톤당 500g 미량 투입 시 1톤 믹서 내 CV 5% 이내 균질 분산",
                                     "고온 가공열 내열성: 85~105℃ 스팀 펠렛 가공열 통과 후 유효 활성 95% 보존"
                                 ]},
                                IMG_FEED_LINE, "한일사료 임가공 배합사료 공장 자동화 믹서 및 마이크로 도징 시스템",
                                "한일사료의 고속 믹서 공정에 100% 최적화된 마이크로 유동성 설계 적용!")

    # ====================================================
    # SLIDE 6: Comparative Table (Real Formatted PPT Table)
    # ====================================================
    s6 = prs.slides.add_slide(blank_layout)
    headers_s6 = ["구분 항목", "시중 일반 첨가제 (기존)", "삼원팜텍 고농축 프리믹스 (제안)", "개선 효과 및 차별화"]
    rows_s6 = [
        ["표준 투입량", "1,000g ~ 2,000g / ton", "500g / ton (0.05%)", "투입량 50~75% 절감, 배합공간 확보"],
        ["유효 원료 순도", "저순도 원료 (부형제 80~90%)", "글로벌 1등급 고순도 원료 엄선", "불필요한 부형제 배제, 활성 극대화"],
        ["사료 배합 영향", "부형제가 옥수수/대두박 공간 잠식", "주영양소 공간 1kg 이상 확보", "사료 본연의 영양 스펙 100% 보존"],
        ["톤당 첨가 비용", "5,000원 ~ 8,000원 / ton", "단 3,000원 / ton (6,000원/kg)", "톤당 2,000원 ~ 5,000원 원가 절감"],
        ["월간 공급 비용", "9,000만원 ~ 1억 4,400만원", "5,400만원 (월 18,000톤 기준)", "월 3,600만 ~ 9,000만원 원가 절감"],
        ["물류 및 보관", "월 18~36톤 보관 (부피 과대)", "월 9.0톤 (500g 알루미늄 파우치)", "창고 보관 공간 및 물류비 50% 절감"]
    ]
    add_table_slide(s6, prs, 6, "PART I. 제안 배경", "기존 시중 첨가제 vs 삼원팜텍 고농축 프리믹스 비교",
                    "저순도 다량 투입의 비효율을 극복하고 고농축 소량 투입으로 패러다임 전환",
                    headers_s6, rows_s6, [2.0, 3.2, 3.2, 3.3],
                    top_card_text="기존 첨가제는 부형제(밀기울)가 대부분이라 사료 영양을 깎아먹고 비용만 가중시킵니다.",
                    mascot_text="삼원팜텍 500g 처방은 불필요한 부형제를 완전히 걷어내고 순수 유효 성분만 농축하여 사료 품질과 원가를 동시 해결합니다!")

    # ====================================================
    # SLIDE 7: High-Concentration Paradigm (WITH POUCH MOCKUP)
    # ====================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s7, prs, 7, "PART I. 솔루션 혁신", "삼원팜텍 패러다임: 초고농축 마이크로 프리믹스 혁신",
                                "사료 톤당 단 500g(0.05%) 투입으로 동일 이상의 극대화된 약리 효과 구현",
                                {"title": "사료 톤당 500g 처방의 공학적 장점",
                                 "tag": "500G/TON INNOVATION",
                                 "bullets": [
                                     "고순도 원료 농축: 글로벌 1등급 고순도 원료만을 엄선하여 유효 분자 밀도 극대화",
                                     "부형제 제로화: 무의미한 부형제를 전면 배제하여 500g 투입만으로 충분한 약리 효과",
                                     "배합 스페이스 확보: 톤당 1.0kg 이상의 영양 공간 확보 (옥수수/대두박 100% 보존)",
                                     "물류·보관비 절감: 월간 보관 중량 18톤 -> 9톤으로 50% 급감 (물류비 반감)",
                                     "품질 안정성 보증: 전용 500g 고차단성 알루미늄 포장으로 12개월 무변질 보증"
                                 ]},
                                IMG_POUCH, "삼원팜텍 500g 전용 고차단성 알루미늄 스탠딩 파우치 패키지 디자인",
                                "500g 1포가 사료 1톤에 1:1 완벽 매칭되어 현장 투입 실수를 원천 차단합니다!")

    # ====================================================
    # SLIDE 8: 3-Party Value Chain (3 Connected Cards)
    # ====================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8, prs, C_BG_LIGHT)
    add_header(s8, prs, "PART I. 협력 구조", "3자 협력(삼원팜텍 - 한일사료 - 서울우유) 비즈니스 밸류체인", "명확한 역할 분담과 완벽한 신뢰 기반의 협력 파트너십")
    create_card(s8, Inches(0.8), Inches(1.8), Inches(3.8), Inches(4.7), "(주)삼원팜텍 (제조·판매원)", 
                ["단독 제조·공급원: 모든 법적·품질·사후관리 책임 총괄",
                 "공공 품질 기준: 국가 조달 관납 기준의 무결점 옥천 완제품 생산",
                 "R&D 기술 지원: 글로벌 최고 수준 원료 파트너십 및 학술 지원",
                 "현장 밀착 전담: 한일사료 공장 직납 및 서울우유 전담 기술팀 가동"], tag="주관 기관 (단독 책임)", border_color=C_NAVY_PRIMARY)
    create_card(s8, Inches(4.75), Inches(1.8), Inches(3.8), Inches(4.7), "한일사료 (임가공 생산처)", 
                ["정밀 임가공 전담: 월 18,000톤 배합사료 라인 안정 생산",
                 "공정 일치 준수: 삼원팜텍 500g 전용 공정 프로토콜 준수 (CV<5%)",
                 "자동화 빈 연계: 마이크로 인그리디언트 자동 투입 라인 일치",
                 "품질 상호 검증: 로트별 분석 성적서(COA) 상호 대조 및 모니터링"], tag="임가공 배합처", border_color=C_NAVY_LIGHT)
    create_card(s8, Inches(8.7), Inches(1.8), Inches(3.8), Inches(4.7), "서울우유 (수요처)", 
                ["사료 원가 절감: 월 최대 1억원 절감을 통한 조합 및 목장 수익성 극대화",
                 "최상급 사료 공급: 조합원 낙농 목장에 최고 품질 프리미엄 사료 공급",
                 "낙농 생산성 극대화: 착유우 산유량 방어, 1등급 유질, 체세포수 급감 달성",
                 "브랜드 신뢰 확립: 서울우유 낙농 사료 브랜드의 시장 리더십 수호"], tag="수요처 / 낙농목장", border_color=C_EMERALD_DARK)
    add_footer(s8, prs, 8)

    # ====================================================
    # SLIDE 9: Samwon Credentials (WITH FACTORY PHOTO)
    # ====================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s9, prs, 9, "PART II. 제안사 역량", "주식회사 삼원팜텍 회사 개요 및 제조 인프라",
                                "충북 옥천 테크노밸리 본사 및 첨단 GMP/HACCP 생산 시설 보유",
                                {"title": "(주)삼원팜텍 핵심 역량 지표",
                                 "tag": "COMPANY OVERVIEW",
                                 "bullets": [
                                     "회사 개요: 주식회사 삼원팜텍 (대표이사 김한호)",
                                     "소재지: 충청북도 옥천군 옥천읍 테크노밸리로 본사 및 제1공장",
                                     "주요 사업: 동물용의약품, 보조사료, 단미사료, 기능성 프리믹스 제조",
                                     "공인 인증: KVGMP(동물용의약품 우수제조기준), 사료 HACCP 인증",
                                     "시설 규모: 마이크로 믹싱 타워, 무균 포장 라인, 정밀 분석 연구소",
                                     "생산 역량: 월간 300 M/T 고농축 프리믹스 자동화 대량 생산 체계"
                                 ]},
                                IMG_FACTORY, "충북 옥천 삼원팜텍 본사 및 첨단 R&D 제조 공장 전경",
                                "삼원팜텍의 최첨단 자동화 설비가 월 18,000톤용 프리믹스를 한 치의 오차 없이 생산합니다.")

    # ====================================================
    # SLIDE 10: Public Procurement Track Record (WITH MASCOT)
    # ====================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10, prs, C_BG_LIGHT)
    add_header(s10, prs, "PART II. 공공 신뢰도", "국가 조달청 관납 전국 총판 및 공공 품질 검증",
               "까다로운 국가 공공 조달 품질 심사를 통과한 최고의 신뢰성")
    cards_s10 = [
        ("조달청 관납 전국 총판", ["국가 조달청(나라장터) 정식 등록 공급원", "전국 시·군 방역 본부 및 축협 관납 납품", "공공기관 감사 무결점 통과 기업"], "01. 공공 납품 실적"),
        ("로타갈(생물학적 제제)", ["송아지 설사 예방 생물학적 제제 관납", "냉장 유통 및 엄격한 생균 역가 관리", "전국 수의사 및 낙농 목장 신뢰 입증"], "02. 대표 관납 품목"),
        ("철저한 사후 관리", ["공급 제품 로트별 전수 품질 보증", "불량률 0.00% 달성 운영 체계", "클레임 발생 시 24시간 내 현장 출동"], "03. 품질 보증 체계")
    ]
    for i, (title, bullets, tag) in enumerate(cards_s10):
        create_card(s10, Inches(0.8 + i * 3.95), Inches(1.8), Inches(3.8), Inches(3.6), title, bullets, tag=tag, border_color=C_EMERALD_DARK)
        
    if os.path.exists(IMG_MASCOT):
        s10.shapes.add_picture(IMG_MASCOT, Inches(0.8), Inches(5.6), Inches(1.2), Inches(1.2))
    b_s10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(5.6), Inches(10.3), Inches(1.2))
    b_s10.fill.solid()
    b_s10.fill.fore_color.rgb = C_EMERALD_LIGHT
    b_s10.line.color.rgb = C_EMERALD_DARK
    tf_b10 = b_s10.text_frame
    tf_b10.margin_left = Inches(0.3)
    p_b10 = tf_b10.paragraphs[0]
    p_b10.text = "★ 공공 기관이 보증하는 삼원팜텍 품질 : 조달청 관납 전국 총판의 엄격한 품질 관리 프로토콜이 적용됩니다!"
    p_b10.font.name = "Malgun Gothic"
    p_b10.font.size = Pt(12)
    p_b10.font.bold = True
    p_b10.font.color.rgb = RGBColor(6, 95, 70)
    add_footer(s10, prs, 10)

    # ====================================================
    # SLIDE 11: Quality Assurance Lab (WITH LAB PHOTO)
    # ====================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s11, prs, 11, "PART II. 품질 보증", "옥천 공장 품질 관리 체계 및 매 배치별 성분 분석(COA)",
                                "입고부터 출하까지 5단계 정밀 스크리닝 및 국가 공인 성적서 동봉",
                                {"title": "삼원팜텍 5단계 무결점 품질 검증",
                                 "tag": "QUALITY CONTROL",
                                 "bullets": [
                                     "1단계 원료 입고: 수입 원료 통관 시 HPLC 유효 성분 순도 100% 전수 분석",
                                     "2단계 사전 검사: 미생물/생균 역가(CFU/g) 및 곰팡이독소 사전 스크리닝",
                                     "3단계 공정 모니터링: 옥천 공장 마이크로 정밀 계량 및 배치 혼합 실시간 제어",
                                     "4단계 성적서 발행: 완제품 로트별 국가 공인 시험기관 성분 분석 성적서(COA) 발행",
                                     "5단계 동봉 출하: 매 납품 시 COA 원본 한일사료 품질팀 및 서울우유 동시 제출"
                                 ]},
                                IMG_LAB, "삼원팜텍 수의 영양 연구소 / 사료 품질 관리 크로마토그래피 정밀 분석실",
                                "원료부터 완제품까지 5단계 전수 검사를 거친 무결점 제품만 출하됩니다.")

    # ====================================================
    # SLIDE 12: 500g/ton Engineering (WITH PELLET PHOTO)
    # ====================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s12, prs, 12, "PART III. 경제성 분석", "표준 투입량 500g/ton (0.05%) 처방의 공학적 의의",
                                "생리 활성 밀도 극대화와 배합 공간 보존의 시너지 효과",
                                {"title": "왜 500g/ton이 가장 이상적인가?",
                                 "tag": "500G/TON VALUE",
                                 "bullets": [
                                     "원료 분자 농축: 일반 2kg 제품과 동일한 유효 활성 분자를 500g에 완벽 응축",
                                     "영양소 치환 제로: 불필요한 부형제 투입 방지로 조단백/가소화에너지 손실 0%",
                                     "물류비 50% 절감: 월 18톤 운송 -> 9톤 운송으로 운송비 및 보관비 50% 절감",
                                     "현장 작업 편의성: 500g 파우치 1포 = 1톤 믹서 1배치 투입으로 작업 간소화",
                                     "친환경 폐기물 저감: 포장재 및 부형제 폐기물 75% 이상 대폭 감축"
                                 ]},
                                IMG_PELLET, "바이오 코팅 골든 펠렛 정밀 토출 자동화 생산 라인",
                                "500g 포장 1포가 1톤 배합기 1배치에 정확히 1:1로 대응하여 계량 오류가 없습니다.")

    # ====================================================
    # SLIDE 13: Direct Cost Comparison (WITH COST CHART)
    # ====================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s13, prs, 13, "PART III. 경제성 분석", "사료 톤당 첨가 비용 3,000원과 가격 경쟁력",
                                "제품 공급 기준가 6,000원/kg 적용에 따른 압도적 경제성 비교",
                                {"title": "사료 톤당 첨가제 비용 비교",
                                 "tag": "COST SAVINGS",
                                 "bullets": [
                                     "시중 A사 일반 처방 (1.5kg/t x 4,000원): 사료 톤당 6,000원 투입",
                                     "시중 B사 프리미엄 처방 (1.0kg/t x 8,000원): 사료 톤당 8,000원 투입",
                                     "삼원팜텍 고농축 프리믹스 (0.5kg/t x 6,000원): 사료 톤당 단 3,000원 투입!",
                                     "★ 비용 절감 성과: 톤당 3,000원 ~ 5,000원 순수 제조원가 절감 효과 달성",
                                     "단가 정책: 한일사료 임가공 배합 라인 전용 파격적 맞춤 특화 공급가 적용"
                                 ]},
                                CHART_COST, "사료 톤당 첨가제 투입 비용 및 월간 총비용 절감 비교 차트",
                                "톤당 단 3,000원으로 시중 8,000원대 프리미엄 첨가제 이상의 약리 효과를 실현합니다.")

    # ====================================================
    # SLIDE 14: Seoul Milk Financial Table (Real Table)
    # ====================================================
    s14 = prs.slides.add_slide(blank_layout)
    headers_s14 = ["공급 옵션", "톤당 투입량", "제품 kg단가", "사료 톤당 비용", "월간 총비용 (18,000t)", "연간 환산 비용", "서울우유 연간 절감액"]
    rows_s14 = [
        ["시중 A사 처방", "1.5 kg / ton", "4,000 원", "6,000 원", "1억 800 만원", "12억 9,600 만원", "기준 대비 0원"],
        ["시중 B사 처방", "1.0 kg / ton", "8,000 원", "8,000 원", "1억 4,400 만원", "17억 2,800 만원", "-4억 3,200 만원 손실"],
        ["삼원팜텍 제안", "0.5 kg / ton", "6,000 원", "3,000 원", "5,400 만원", "6억 4,800 만원", "+6억 4,800 만원 절감!"]
    ]
    add_table_slide(s14, prs, 14, "PART III. 경제성 분석", "서울우유 월간 18,000톤 생산 시 거시적 경제 효과 분석",
                    "월 5,400만원 공급으로 기존 대비 월 최대 1억원, 연간 12억원 이상 절감",
                    headers_s14, rows_s14, [1.8, 1.4, 1.4, 1.5, 1.9, 1.9, 1.8],
                    top_card_text="삼원팜텍 공급 시 연간 최소 6억 4,800만원에서 최대 10억 8,000만원의 실질 예산 절감 달성",
                    mascot_text="절감된 사료 제조원가는 서울우유 조합원 목장 환원 사업 및 사료 판매 가격 경쟁력으로 직결됩니다!")

    # ====================================================
    # SLIDE 15: 8 Core Solutions Matrix (8 Grid Cards)
    # ====================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s15, prs, C_BG_LIGHT)
    add_header(s15, prs, "PART IV. 핵심 솔루션", "삼원팜텍 8대 복합 기능성 핵심 낙농 원료 매트릭스",
               "기호성, 반추위효소, 항열스트레스, 효모, 생균, 독소흡착, 천연약제를 1포에 집약")
    sol_cards = [
        ("01. DDC 복합 향미제", "천연 바닐라/밀크 향", "건물섭취량(DMI) +12%", C_NAVY_LIGHT),
        ("02. VTR 고역가 복합효소", "NSP/섬유소 분해", "사료 이용 효율 +8.5%", C_NAVY_LIGHT),
        ("03. Jienuo 코팅 GABA", "루멘 바이패스 GABA", "하절기 열 스트레스 -38%", C_EMERALD_DARK),
        ("04. HZM 고활성 효모균", "S. cerevisiae 활성균", "반추위 VFA 생성 +18%", C_EMERALD_DARK),
        ("05. HZM 3종 복합생균", "유산균+고초균+낙산균", "장내 유익균 총 10배 증식", C_EMERALD_DARK),
        ("06. 몬모릴로나이트 나노", "천연 규산염 나노점토", "아플라톡신 98% 흡착 배출", C_NAVY_PRIMARY),
        ("07. VEESURE 식물구충제", "천연 사포닌/에센셜오일", "장내 기생충 및 원충 억제", C_NAVY_PRIMARY),
        ("08. DNJ 천연 항바이러스", "상백피 천연 알칼로이드", "호흡기/유방염 바이러스 방어", C_NAVY_PRIMARY)
    ]
    for i, (title, spec, effect, col) in enumerate(sol_cards):
        r_idx = i // 4
        c_idx = i % 4
        x = Inches(0.8 + c_idx * 2.95)
        y = Inches(1.8 + r_idx * 2.45)
        c_box = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(2.25))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CARD_BG
        c_box.line.color.rgb = col
        c_box.line.width = Pt(1.5)
        
        tb = s15.shapes.add_textbox(x + Inches(0.18), y + Inches(0.18), Inches(2.44), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Malgun Gothic"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(6)
        
        p1 = tf.add_paragraph()
        p1.text = "주요 성분: " + spec
        p1.font.name = "Malgun Gothic"
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_TEXT_MUTED
        
        p2 = tf.add_paragraph()
        p2.text = "★ 효과: " + effect
        p2.font.name = "Malgun Gothic"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_before = Pt(6)
    add_footer(s15, prs, 15)

    # ====================================================
    # SLIDE 16: DDC Flavor & VTR Enzyme (WITH PELLET PHOTO)
    # ====================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s16, prs, 16, "PART IV. 솔루션 상세", "01. DDC 향미제 & 02. VTR 복합효소제",
                                "기호성 극대화로 젖소 건물섭취량을 유도하고 반추위 섬유소 소화율 극대화",
                                {"title": "섭취량 증대 및 소화율 혁신 메커니즘",
                                 "tag": "INTAKE & ENZYMES",
                                 "bullets": [
                                     "DDC 복합 향미제: 반추동물 후각을 자극하는 천연 에센셜 오일 정밀 배합",
                                     "하절기 섭취 회복: 폭염 시 식욕 부진 젖소 건물섭취량(DMI) 8~12% 즉각 회복",
                                     "VTR 복합효소제: 자일라나아제, 글루카나아제, 셀룰라아제 등 6종 복합 처방",
                                     "섬유소 분해 혁신: 조사료 및 농후사료 세포벽 분해로 에너지·단백질 이용률 극대화",
                                     "반추위 환경 개선: 아급성 과산증(SARA) 완화 및 영양소 흡수 표면적 25% 확대"
                                 ]},
                                IMG_PELLET, "바이오 코팅 골든 펠렛 및 고역가 복합효소제 배합 공정",
                                "고온 다습기 젖소의 사료 섭취 거부를 예방하고 반추위 발효 환경을 최적화합니다.")

    # ====================================================
    # SLIDE 17: Coated GABA (WITH DAIRY COW PHOTO)
    # ====================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s17, prs, 17, "PART IV. 솔루션 상세", "03. Jienuo 코팅 GABA: 하절기 고온 스트레스 차단",
                                "루멘 바이패스 코팅 기술로 혈중 스트레스 호르몬 코르티솔 38% 억제",
                                {"title": "GABA의 항스트레스 및 산유량 방어 효과",
                                 "tag": "HEAT STRESS RELIEF",
                                 "bullets": [
                                     "2중 마이크로 코팅: 고순도 γ-아미노낙산(GABA)을 특수 지질 매트릭스로 보호",
                                     "루멘 바이패스 90%: 반추위 미생물 분해를 우회하여 소장에서 100% 흡수",
                                     "체온 상승 억제: 하절기 열 스트레스 지수(THI) 78 이상에서 체온 0.4~0.6℃ 저하",
                                     "산유량 80% 방어: 폭염 기간 젖소 산유량 저하 80% 방어 및 유지율·유단백율 유지",
                                     "번식 장애 예방: 호흡수 안정화 및 헐떡임(Panting) 45% 감소, 번식률 정상화"
                                 ]},
                                IMG_DAIRY, "스마트 낙농 로봇 착유 및 하절기 쿨링 환기 시스템 목장",
                                "폭염 기간 중 젖소 산유량 감소를 막고 번식 간격을 정상화시킵니다.")

    # ====================================================
    # SLIDE 18: HZM Active Yeast & 3 Probiotics (WITH CAPSULE PHOTO)
    # ====================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s18, prs, 18, "PART IV. 솔루션 상세", "04. HZM 고활성 효모균 & 05. 3종 복합생균제",
                                "반추위 혐기 환경 안정화 및 장내 유익균총 압도적 우점 형성",
                                {"title": "반추위 및 장내 마이크로바이옴 정상화",
                                 "tag": "MICROBIOME CARE",
                                 "bullets": [
                                     "HZM 효모균(S. cerevisiae): 반추위 내 잔존 산소를 소비하여 혐기 상태 극대화",
                                     "VFA 생성 18% 증가: 섬유소 분해균 증식 촉진으로 휘발성지방산(VFA) +18% 증가",
                                     "HZM 3종 복합 생균: 유산균 + 고초균(내생포자) + 낙산균 최적 배합",
                                     "장내 도달률 95%: 마이크로 캡슐화로 위산·담즙산을 통과하여 소장/대장 95% 정착",
                                     "병원균 부착 차단: 병원성 대장균 및 살모넬라 차단, 장벽 밀착연접(Tight Junction) 강화"
                                 ]},
                                IMG_CAPSULE, "첨단 마이크로 캡슐화 다중 코팅 생체 분자 3D 구조 렌더링",
                                "장내 면역 세포를 자극하여 무항생제 사양 환경에서도 설사와 연변을 근본 예방합니다.")

    # ====================================================
    # SLIDE 19: Montmorillonite Nano Adsorbent (WITH LAB PHOTO)
    # ====================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s19, prs, 19, "PART IV. 솔루션 상세", "06. HZM 몬모릴로나이트 나노 곰팡이독소 흡착제",
                                "나노 층상 구조의 물리적 정전기 흡착으로 아플라톡신 98% 배출",
                                {"title": "사료 곰팡이독소 및 원유 M1 이행 완벽 차단",
                                 "tag": "MYCOTOXIN BINDER",
                                 "bullets": [
                                     "나노 층상 규산염: 고순도 천연 몬모릴로나이트를 나노 단위로 박리 정제",
                                     "원유 M1 전이 차단: 극성 아플라톡신(B1)을 포집하여 원유 내 아플라톡신 M1 전이 원천 방지",
                                     "간 독성 완벽 방어: 소화기관 내 흡착 후 체외로 100% 안전 배출",
                                     "영양소 손실 1.2% 미만: 비타민, 미네랄, 아미노산 등 필수 영양소 손실 극소화",
                                     "원료곡 안전판: 수입 옥수수/대두박 보관 중 곰팡이독소 위험 완벽 해소"
                                 ]},
                                IMG_LAB, "수의 영양 연구소 / 사료 품질 관리 크로마토그래피 정밀 분석실",
                                "원료곡 품질 편차에 상관없이 서울우유 원유의 안전성을 100% 보장합니다.")

    # ====================================================
    # SLIDE 20: VEESURE & DNJ Natural Actives (WITH MASCOT)
    # ====================================================
    s20 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s20, prs, C_BG_LIGHT)
    add_header(s20, prs, "PART IV. 솔루션 상세", "07. VEESURE 천연 식물구충제 & 08. DNJ 천연 항바이러스제",
               "무항생제 청정 낙농을 실현하는 식물성 파이토케미컬 바이오 시큐리티")
    cards_s20 = [
        ("VEESURE 천연 식물구충제", [
            "원료 성분: 사포닌 및 천연 에센셜 오일 복합 파이토케미컬",
            "작용 기전: 선충, 콕시듐(Coccidia) 등 내부 기생충 생활사 차단",
            "실증 효과: 송아지 콕시듐 설사 발생률 78% 대폭 감소",
            "안전성: 휴약 기간 및 착유 중단이 전혀 없는 100% 안전 제제"
        ], "07. PARASITE DEFENSE"),
        ("DNJ 천연 항바이러스제", [
            "원료 성분: 상백피 추출 1-Deoxynojirimycin 천연 알칼로이드",
            "작용 기전: 바이러스 당단백질 합성 효소(Glucosidase) 특이적 억제",
            "실증 효과: 로타바이러스, 코로나바이러스 등 외피 바이러스 증식 차단",
            "면역 증강: 호흡기 및 소화기 점막 면역 글로불린(sIgA) 분비 촉진"
        ], "08. VIRAL SHIELD"),
        ("청정 낙농 시너지", [
            "항생제 대체: 화학 구충제 및 합성 항생제 완전 대체 효과",
            "비용 절감: 목장 약품 구입비 및 개체 치료 투약 노동력 절감",
            "브랜드 가치: 서울우유의 친환경 청정 브랜드 가치 극대화",
            "소비자 신뢰: 소비자 선호 무항생제 청정 1등급 원유 생산 최적화"
        ], "SYNERGY VALUE")
    ]
    for i, (title, bullets, tag) in enumerate(cards_s20):
        create_card(s20, Inches(0.8 + i * 3.95), Inches(1.8), Inches(3.8), Inches(3.6), title, bullets, tag=tag, border_color=C_EMERALD_DARK)
    if os.path.exists(IMG_MASCOT):
        s20.shapes.add_picture(IMG_MASCOT, Inches(0.8), Inches(5.6), Inches(1.2), Inches(1.2))
    b_s20 = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(5.6), Inches(10.3), Inches(1.2))
    b_s20.fill.solid()
    b_s20.fill.fore_color.rgb = C_EMERALD_LIGHT
    b_s20.line.color.rgb = C_EMERALD_DARK
    tf_b20 = b_s20.text_frame
    tf_b20.margin_left = Inches(0.3)
    p_b20 = tf_b20.paragraphs[0]
    p_b20.text = "★ 친환경 낙농의 종결자 : 항생제 없이도 질병과 기생충을 안전하게 제어하는 프리미엄 처방입니다!"
    p_b20.font.name = "Malgun Gothic"
    p_b20.font.size = Pt(12)
    p_b20.font.bold = True
    p_b20.font.color.rgb = RGBColor(6, 95, 70)
    add_footer(s20, prs, 20)

    # ====================================================
    # SLIDE 21: Mixing Homogeneity (WITH HOMOGENEITY CHART)
    # ====================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s21, prs, 21, "PART V. 공정 적합성", "한일사료 라인 혼화도 검증: 변이계수(CV) 3.8% 달성",
                                "사료 톤당 500g 투입 시 1톤 패들 믹서 내 CV 5% 이내 무결점 균질 분산",
                                {"title": "마이크로 도징 혼화도 공학 시험 결과",
                                 "tag": "HOMOGENEITY CV<5%",
                                 "bullets": [
                                     "시험 조건: 한일사료 Twin-Shaft 고속 패들 믹서 (1.0 M/T 배치 시험)",
                                     "혼합 시간: 90초 ~ 120초 표준 가동 조건에서 완벽 혼화",
                                     "정밀 채취: 믹서 상/중/하/전/후 10개 포인트 전수 시료 채취",
                                     "공인 검증: 변이계수(CV) 3.8% 달성 (공정 기준 CV < 5.0% 완벽 충족)",
                                     "공학적 원리: 유효 원료 미세 분말화 및 정전기 방지 특수 담체 적용"
                                 ]},
                                CHART_HOMOGENEITY, "혼합 시간에 따른 변이계수(CV%) 감소 곡선 및 10개 포인트 분포도",
                                "한일사료의 고속 배합 공정에서 90초 만에 완벽한 균질 분산을 실현합니다.")

    # ====================================================
    # SLIDE 22: Pellet Heat Stability (WITH HEAT CHART)
    # ====================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s22, prs, 22, "PART V. 공정 적합성", "펠렛 가공열(85~110℃) 내열성 및 생존율 95% 보증",
                                "스팀 컨디셔닝 및 다이스 압출 고열에도 유효 활성 성분 95% 이상 안정 잔존",
                                {"title": "펠렛 및 익스팬더 가공열 생존 메커니즘",
                                 "tag": "HEAT RESISTANCE",
                                 "bullets": [
                                     "가공 조건: 85~95℃ 스팀 컨디셔닝 및 105℃ 다이스 압출 펠렛 공정",
                                     "다중 코팅: 융점 85℃ 지질 매트릭스 + 열차단 미네랄 외벽 2중 보호",
                                     "효소제 생존율: 90℃ 고열 통과 후 상대 잔존 역가 94.8% 유지",
                                     "생균·효모 생존: 펠렛 압출 통과 후 유효 생균수 95.2% 생존 확인",
                                     "전 라인 호환: 펠렛 사료뿐만 아니라 가루(Mash) 및 익스팬더 전 라인 호환"
                                 ]},
                                CHART_HEAT, "온도별 가공열 노출에 따른 효소 역가 및 생균 생존율 곡선",
                                "고온·고압의 펠렛 가공 공정을 완벽하게 견뎌내어 목장 급여 시점까지 활성을 보존합니다.")

    # ====================================================
    # SLIDE 23: Anti-Caking & Fluidity (WITH POUCH PHOTO)
    # ====================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s23, prs, 23, "PART V. 공정 적합성", "고결 방지(Anti-Caking) 및 자유 유동성 설계",
                                "하절기 다습 조건에서도 굳지 않고 빈(Bin) 브릿지 현상을 원천 방지",
                                {"title": "물리적 안정성 및 보관 편의성",
                                 "tag": "PHYSICAL STABILITY",
                                 "bullets": [
                                     "자유 유동성: 안식각(Angle of Repose) 27.5° 달성 (우수한 자유 유동)",
                                     "투입 관로 보호: 마이크로 빈 투입 시 관로 막힘이나 브릿지 현상 제로",
                                     "안티케이킹 처방: 식품용 친환경 침강 실리카 1.5% 배합으로 수분 흡착 차단",
                                     "3중 알루미늄 포장: 고차단 스탠딩 파우치로 장마철 습기 100% 완벽 차단",
                                     "상온 12개월 품질: 유통기한 12개월 보증 및 로트별 유통기한 인자"
                                 ]},
                                IMG_POUCH, "삼원팜텍 500g 전용 고차단성 알루미늄 스탠딩 파우치 패키지 디자인",
                                "장마철 다습한 환경에서도 굳지 않아 자동 투입 라인의 작동 에러를 원천 차단합니다.")

    # ====================================================
    # SLIDE 24: Dairy Lactating Cows (WITH DAIRY COW PHOTO)
    # ====================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s24, prs, 24, "PART VI. 기대효과", "낙농(착유우) 산유량 방어 및 비유곡선 유지 실증",
                                "하절기 산유량 두당 일 +1.8kg 유지 및 착유 피크 기간 3~4주 연장",
                                {"title": "낙농 착유우 급여 시험 실증 데이터",
                                 "tag": "DAIRY LACTATION",
                                 "bullets": [
                                     "시험 대상: 고능력 착유우 120두 하절기(THI 78~82 폭염기) 급여 시험",
                                     "건물 섭취량(DMI): 대조군 대비 두당 일평균 +1.5kg 안정 유지",
                                     "일일 산유량: 대조군 대비 두당 일평균 +1.8kg 산유량 방어",
                                     "착유 피크 지속: 분만 후 비유 피크 기간 2~3주 추가 지속 확인",
                                     "유성분 개선: 유지율 3.85% -> 4.02%, 유단백 3.15% -> 3.28% 상승",
                                     "경제성 가치: 착유우 50두 목장 기준 월 약 240만원 순수익 증대"
                                 ]},
                                IMG_DAIRY, "스마트 낙농 로봇 착유 및 하절기 쿨링 환기 시스템 목장",
                                "하절기 폭염에도 산유량 감소를 완벽 방어하여 목장의 여름철 유대를 사수합니다.")

    # ====================================================
    # SLIDE 25: Milk Quality & SCC (WITH LAB PHOTO)
    # ====================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s25, prs, 25, "PART VI. 기대효과", "원유 유질 개선: 체세포수(SCC) 42% 급감 및 유방염 예방",
                                "평균 체세포수 32만 -> 18.5만/ml 저감으로 최고 등급 1등급 유대 획득",
                                {"title": "원유 체세포수 및 유방염 저감 실증 데이터",
                                 "tag": "MILK QUALITY & SCC",
                                 "bullets": [
                                     "시험 대상: 체세포수 30만 이상 준임상형 유방염 위험 착유우 80두",
                                     "체세포수(SCC) 변화: 평균 32만/ml -> 18.5만/ml로 42.2% 급감",
                                     "원유 등급 획득: 전 두수 서울우유 1등급 원유 스펙 안정적 유지",
                                     "유방염 억제: 급여 기간 중 임상형 유방염 발생 65% 대폭 저감",
                                     "치료비 손실 방어: 항생제 투약 비용 및 폐유 손실 70% 감소",
                                     "최고 유대 인센티브: 체세포수 1등급 유지에 따른 리터당 최고 유대 수령"
                                 ]},
                                IMG_LAB, "삼원팜텍 수의 영양 연구소 / 사료 품질 관리 크로마토그래피 정밀 분석실",
                                "유방염 치료비와 폐유 손실을 막고 최고 등급 유대 인센티브를 안정적으로 확보합니다.")

    # ====================================================
    # SLIDE 26: Dairy Heifers & Calves (WITH CALF PHOTO)
    # ====================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s26, prs, 26, "PART VI. 기대효과", "육성우 및 송아지 육성: 설사 80% 저감 & 초산일령 단축",
                                "어린 송아지 반추위 조기 발달 및 초산 도달 일령 1.5개월 단축",
                                {"title": "송아지 및 육성우 급여 시험 실증 데이터",
                                 "tag": "HEIFER & CALF",
                                 "bullets": [
                                     "시험 대상: 홀스타인 어린 송아지 및 육성우 150두 (생후 1일령~14개월령)",
                                     "설사 발생률: 대조군 24.5% -> 급여군 4.8%로 80.4% 급감",
                                     "반추위 융모 발달: 효모 및 복합효소 작용으로 반추위 유두 길이 35% 증대",
                                     "이유 체중 증체: 생후 60일령 이유 체중 대조군 대비 평균 +4.8kg 증체",
                                     "초산 일령 단축: 번식 적정 체중 조기 도달로 초산 24개월 -> 22.5개월 단축",
                                     "육성비 절감: 미경산우 사양 기간 단축으로 두당 육성비 45만원 절감"
                                 ]},
                                IMG_CALF, "깨끗한 톱밥 우사에서 로봇 포유기로 자라는 홀스타인 송아지 및 육성우",
                                "어린 송아지의 설사 폐사를 막고 튼튼한 고능력 후대 착유우로 조기 육성합니다.")

    # ====================================================
    # SLIDE 27: Dairy ROI Analysis (WITH ROI CHART)
    # ====================================================
    s27 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s27, prs, 27, "PART VI. 기대효과", "서울우유 낙농 목장 투자 수익률(ROI) 종합 분석",
                                "첨가 비용 1원 투자 시 조합원 목장 실익 5.2원 회수 (ROI 1 : 5.2)",
                                {"title": "거시적 투자 대비 가치 분석",
                                 "tag": "DAIRY ROI METRICS",
                                 "bullets": [
                                     "사료 첨가 비용: 사료 톤당 단 3,000원 투자",
                                     "목장 생산성 가치: 산유량 증대 및 유질 개선으로 톤당 15,600원 경제 가치 회수",
                                     "투자 회수율: 투자 비용 대비 5.2배의 압도적 목장 순익 창출",
                                     "질병 예방 가치: 유방염 및 송아지 설사 치료비 절감 연간 목장당 300~500만원",
                                     "서울우유 브랜드 가치: 서울우유 사료에 대한 조합원 목장 만족도 99% 달성"
                                 ]},
                                CHART_ROI, "낙농 착유우 및 육성우 생산성 가치 회수 종합 ROI 분석 차트",
                                "사료 공장과 낙농 목장 모두가 윈-윈(Win-Win)하는 지속 가능한 모델을 구축합니다.")

    # ====================================================
    # SLIDE 28: 3-Stage Implementation Roadmap
    # ====================================================
    s28 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s28, prs, C_BG_LIGHT)
    add_header(s28, prs, "PART VI. 실행 계획", "단계별 도입 로드맵 및 3단계 실증 프로세스",
               "리스크 제로를 위한 체계적인 파일럿 테스트 및 전 라인 확대 일정")
    phases = [
        ("Phase 1: 시험 배합 & 공정 검증", "1~2주차 (준비 단계)", [
            "프로토콜 수립: 한일사료 라인 500g 투입 기준 확정",
            "혼화도 측정: Twin-Shaft 믹서 혼화도(CV) 현장 실측",
            "내열성 검사: 펠렛 가공열 통과 후 유효 성분 잔존 검사",
            "물성 최종 승인: 배합 물성 및 안티케이킹 유동성 최종 승인"
        ], C_NAVY_LIGHT),
        ("Phase 2: 조합원 목장 필드 실증", "3~6주차 (실증 단계)", [
            "시범 목장 선정: 서울우유 대표 낙농 목장 10개소 선정",
            "지표 모니터링: 착유우 산유량, 체세포수(SCC), 연변 추적",
            "스트레스 분석: 하절기 열 스트레스 저감 지표 비교 분석",
            "실증 보고서: 참여 목장 만족도 설문 및 종합 보고서 발행"
        ], C_EMERALD_DARK),
        ("Phase 3: 전 라인 표준 공급 확대", "7주차 이후 (정규화)", [
            "표준 처방 확정: 한일사료 월 18,000톤 라인 표준 적용",
            "정기 직납 가동: 월간 9,000kg 정기 발주 및 직납 체계 가동",
            "COA 동봉 체계: 매 배치별 공인 시험 성적서(COA) 동봉",
            "전담 기술 지원: 삼원팜텍-서울우유 사후 기술 지원팀 상시 가동"
        ], C_NAVY_PRIMARY)
    ]
    for i, (title, period, bullets, col) in enumerate(phases):
        create_card(s28, Inches(0.8 + i * 3.95), Inches(1.8), Inches(3.8), Inches(4.7), title, bullets, tag=period, border_color=col)
    add_footer(s28, prs, 28)

    # ====================================================
    # SLIDE 29: Emergency Supply SLA (WITH FACTORY PHOTO)
    # ====================================================
    s29 = prs.slides.add_slide(blank_layout)
    add_split_slide_with_image(s29, prs, 29, "PART VI. 신뢰 보증", "공급 안정성 및 SLA(서비스 수준 협약) 보증",
                                "월 18,000톤 무중단 생산을 위한 안전 재고 18톤 상시 비축 및 전담팀",
                                {"title": "삼원팜텍 4대 무결점 공급 약속",
                                 "tag": "SLA & BACKUP",
                                 "bullets": [
                                     "200% 안전 재고 비축: 옥천 물류센터에 월 사용량의 200%(18 M/T) 상시 유지",
                                     "24시간 직납 물류: 발주 후 24시간 이내 한일사료 공장 직송 납품 시스템",
                                     "서울우유 전담팀: 가축 질병 및 목장 클레임 시 24시간 내 현장 출동",
                                     "품질 무한 책임제: 품질 결함 확인 시 해당 로트 100% 무상 교환 및 보상",
                                     "낙농 R&D 세미나: 서울우유 지도계 및 조합원 목장 대상 사양 관리 교육"
                                 ]},
                                IMG_FACTORY, "충북 옥천 삼원팜텍 본사 및 첨단 R&D 제조 공장 전경",
                                "기상 이변이나 물류 파동 시에도 한일사료의 사료 생산 라인이 멈추는 일은 결코 없습니다.")

    # ====================================================
    # SLIDE 30: Conclusion & Official Closing (Seoul Milk Fresh White)
    # ====================================================
    s30 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s30, prs, C_BG_WHITE)
    
    if os.path.exists(IMG_FACTORY):
        s30.shapes.add_picture(IMG_FACTORY, Inches(6.5), Inches(1.05), Inches(6.0), Inches(4.3))
    if os.path.exists(IMG_MASCOT):
        s30.shapes.add_picture(IMG_MASCOT, Inches(10.5), Inches(4.1), Inches(2.1), Inches(2.1))
        
    tb30 = s30.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(5.5), Inches(4.4))
    tf30 = tb30.text_frame
    tf30.word_wrap = True
    
    p = tf30.paragraphs[0]
    r = p.add_run()
    r.text = "CONCLUSION & PARTNERSHIP"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_SEOUL_GREEN
    p.space_after = Pt(12)
    
    p = tf30.add_paragraph()
    r = p.add_run()
    r.text = "서울우유 사료의 새로운 도약,\n(주)삼원팜텍이 최고의 품질과\n경제성으로 함께하겠습니다!"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(25)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_DARK
    p.space_after = Pt(14)
    
    closing_bullets = [
        "표준 투입량 혁신 : 서울우유 월 18,000톤 라인 맞춤형 500g/ton (단 3,000원) 처방",
        "압도적 제조원가 방어 : 월 5,400만원 공급으로 연간 12억원 제조원가 방어",
        "실증된 낙농 생산성 : 하절기 산유량 방어(+1.8kg) 및 체세포수 42% 급감 실증",
        "공공 조달 최고 신뢰 : 조달청 관납 전국 총판의 검증된 공공 신뢰도"
    ]
    for cb in closing_bullets:
        p = tf30.add_paragraph()
        p.space_before = Pt(3)
        p.space_after = Pt(5)
        
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(int(Pt(16))))
        pPr.set('indent', str(int(-Pt(16))))
        
        parts = cb.split(":", 1)
        
        r_k = p.add_run()
        r_k.text = "▶ " + parts[0].strip() + " :"
        r_k.font.name = "Malgun Gothic"
        r_k.font.size = Pt(11)
        r_k.font.bold = True
        r_k.font.color.rgb = C_SEOUL_GREEN
        
        r_v = p.add_run()
        r_v.text = parts[1]
        r_v.font.name = "Malgun Gothic"
        r_v.font.size = Pt(10.5)
        r_v.font.color.rgb = C_TEXT_BODY
    
    # Bottom Contact Box
    b_c30 = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(5.5), Inches(1.0))
    b_c30.fill.solid()
    b_c30.fill.fore_color.rgb = C_MINT_LIGHT
    b_c30.line.color.rgb = C_BORDER_MINT
    b_c30.line.width = Pt(1.5)
    tf_c30 = b_c30.text_frame
    tf_c30.margin_left = Inches(0.2)
    tf_c30.margin_top = Inches(0.14)
    p_c0 = tf_c30.paragraphs[0]
    p_c0.text = "공식 제조 및 공급원: 주식회사 삼원팜텍  |  대표이사 김한호"
    p_c0.font.name = "Malgun Gothic"
    p_c0.font.size = Pt(11)
    p_c0.font.bold = True
    p_c0.font.color.rgb = C_GREEN_DARK
    
    p_c1 = tf_c30.add_paragraph()
    p_c1.text = "충북 옥천 테크노밸리 첨단 R&D 제조 본사 및 공장  |  전국 조달청 관납 총판"
    p_c1.font.name = "Malgun Gothic"
    p_c1.font.size = Pt(9.5)
    p_c1.font.color.rgb = C_TEXT_MUTED
    p_c1.space_before = Pt(3)
    
    add_footer(s30, prs, 30)

    out_file = r"C:\Users\master\vet_animal_hospital\s_project\S-NACF_고농축사료첨가제_제안_30장덱_삼원팜텍.pptx"
    prs.save(out_file)
    print(f"=== Successfully generated Seoul Milk Dairy 30-slide PPTX deck ===")
    print(f"File: {out_file}")
    print(f"File size: {os.path.getsize(out_file) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    build_complete_v3_deck()
