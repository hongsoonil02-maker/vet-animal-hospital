import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# CI Colors - Samwon Pharmtech
C_NAVY_DARK = RGBColor(10, 25, 47)      # #0A192F Dark Navy
C_NAVY_PRIMARY = RGBColor(15, 32, 67)   # #0F2043 Deep Navy
C_NAVY_LIGHT = RGBColor(30, 58, 138)    # #1E3A8A Slate Navy
C_EMERALD = RGBColor(16, 185, 129)      # #10B981 Bio Green / Emerald
C_EMERALD_DARK = RGBColor(5, 150, 105)  # #059669 Dark Emerald
C_BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
C_BORDER = RGBColor(226, 232, 240)      # #E2E8F0
C_TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A
C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
C_TEXT_WHITE = RGBColor(255, 255, 255)

ASSETS_DIR = r"C:\Users\master\vet_animal_hospital\s_project\assets"

IMG_FACTORY = os.path.join(ASSETS_DIR, "company_factory_panorama_1789881641339.jpg")
IMG_FEED_LINE = os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg")
IMG_GRAIN_MARKET = os.path.join(ASSETS_DIR, "grain_market_volatility_1789881820210.jpg")
IMG_DAIRY = os.path.join(ASSETS_DIR, "dairy_cows_smart_farm_1789881841764.jpg")
IMG_CALF = os.path.join(ASSETS_DIR, "dairy_calf_nutrition.jpg")
IMG_CAPSULE = os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg")
IMG_POUCH = os.path.join(ASSETS_DIR, "premix_product_packaging_1789881875376.jpg")
IMG_MASCOT = os.path.join(ASSETS_DIR, "child_drinking_milk.jpg")

CHART_COST = os.path.join(ASSETS_DIR, "chart_cost_comparison.png")
CHART_HOMOGENEITY = os.path.join(ASSETS_DIR, "chart_homogeneity_cv.png")
CHART_HEAT = os.path.join(ASSETS_DIR, "chart_pellet_heat.png")
CHART_ROI = os.path.join(ASSETS_DIR, "chart_livestock_roi.png")

def apply_slide_bg(slide, prs, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, prs, tag_text, title_text, subtitle_text=""):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_tag = tf.paragraphs[0]
    p_tag.text = f"[ {tag_text} ]"
    p_tag.font.name = "Malgun Gothic"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_EMERALD_DARK
    p_tag.space_after = Pt(2)
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = "Malgun Gothic"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = C_NAVY_PRIMARY
    
    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = "Malgun Gothic"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_footer(slide, prs, current_page, total_pages=30):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf = footer_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"(주)삼원팜텍  |  S-NACF 한일사료 임가공 배합 라인 맞춤형 고농축 사료첨가제 제안                                                              Slide {current_page:02d} / {total_pages:02d}"
    p.font.name = "Malgun Gothic"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(160, 174, 192)

def create_card(slide, left, top, width, height, title, body_bullets, tag="", bg_color=C_CARD_BG, border_color=C_BORDER, title_color=C_NAVY_PRIMARY):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    if tag:
        r_tag = p0.add_run()
        r_tag.text = tag + "\n"
        r_tag.font.name = "Malgun Gothic"
        r_tag.font.size = Pt(9)
        r_tag.font.bold = True
        r_tag.font.color.rgb = C_EMERALD_DARK
    
    r_title = p0.add_run()
    r_title.text = title
    r_title.font.name = "Malgun Gothic"
    r_title.font.size = Pt(12)
    r_title.font.bold = True
    r_title.font.color.rgb = title_color
    p0.space_after = Pt(4)
    
    for bullet in body_bullets:
        p_b = tf.add_paragraph()
        p_b.text = "• " + bullet
        p_b.font.name = "Malgun Gothic"
        p_b.font.size = Pt(9)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_before = Pt(2)

def create_split_slide(slide, prs, page_num, section_tag, title, subtitle, bullets_data, image_path, img_caption=""):
    apply_slide_bg(slide, prs, C_BG_LIGHT)
    add_header(slide, prs, section_tag, title, subtitle)
    
    # Left Column: Card
    card_w = Inches(5.6)
    card_h = Inches(4.9)
    create_card(slide, Inches(0.8), Inches(1.8), card_w, card_h, bullets_data["title"], bullets_data["bullets"], tag=bullets_data.get("tag", ""), border_color=C_NAVY_LIGHT)
    
    # Right Column: Image with frame
    img_left = Inches(6.7)
    img_top = Inches(1.8)
    img_w = Inches(5.8)
    img_h = Inches(4.5)
    
    if os.path.exists(image_path):
        pic = slide.shapes.add_picture(image_path, img_left, img_top, width=img_w, height=img_h)
        # Caption below image
        if img_caption:
            tb_c = slide.shapes.add_textbox(img_left, img_top + img_h + Inches(0.08), img_w, Inches(0.3))
            p_c = tb_c.text_frame.paragraphs[0]
            p_c.text = "▲ " + img_caption
            p_c.font.name = "Malgun Gothic"
            p_c.font.size = Pt(8.5)
            p_c.font.bold = True
            p_c.font.color.rgb = C_TEXT_MUTED
            p_c.alignment = PP_ALIGN.CENTER
            
    add_footer(slide, prs, page_num)

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ----------------------------------------------------
    # SLIDE 1: COVER (Dark Navy + Factory Photo & Mascot)
    # ----------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1, prs, C_NAVY_DARK)
    
    # Right side factory photo
    if os.path.exists(IMG_FACTORY):
        s1.shapes.add_picture(IMG_FACTORY, Inches(6.5), Inches(1.0), Inches(6.0), Inches(4.5))
        
    # Mascot badge on cover
    if os.path.exists(IMG_MASCOT):
        s1.shapes.add_picture(IMG_MASCOT, Inches(10.8), Inches(4.2), Inches(2.0), Inches(2.0))
        
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5.5), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "SAMWON PHARMTECH  |  CUSTOM NUTRITION SOLUTION"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_EMERALD
    p.space_after = Pt(12)
    
    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "S-NACF 사료 품질 혁신 및\n원가 최적화를 위한\n맞춤형 고농축 사료첨가제\n공급 제안서"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(26)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "한일사료 임가공 배합 라인(월 18,000 M/T) 전용\n표준 첨가량 500g/ton (0.05%) 초정밀 처방"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(148, 163, 184)
    p.space_after = Pt(20)
    
    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "제조 및 판매원: 주식회사 삼원팜텍 (대표이사 김한호)\n충북 옥천 사업장  |  국가 조달청 관납 전국 총판  |  2026. 09"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = C_EMERALD
    add_footer(s1, prs, 1)

    # ----------------------------------------------------
    # SLIDE 2: Executive Summary (4 Pillars + Mascot)
    # ----------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2, prs, C_BG_LIGHT)
    add_header(s2, prs, "EXECUTIVE SUMMARY", "핵심 제안 요약: 사료 원가는 낮추고 품질은 극대화하는 표준 규격", "한일사료 18,000톤 라인 맞춤형 삼원팜텍 고농축 프리믹스 핵심 4대 지표")
    
    cards_s2 = [
        ("표준 투입량 500g/ton", ["시중 첨가제(1~2kg) 대비 50~75% 절감", "배합 공간 1kg 이상 확보", "초정밀 마이크로 프리믹스 공학 설계"], "01. 혁신적 투입량"),
        ("사료 톤당 단 3,000원", ["제품 공급 기준가 6,000원/kg 적용", "사료 톤당 첨가제 비용 단 3,000원", "기존 대비 톤당 최대 6,000원 절감"], "02. 원가 절감력"),
        ("월 공급비용 5,400만원", ["월 18,000톤 생산 기준 총 9,000kg", "기존 대비 월 최대 1억원 절감", "S-NACF 사료 사업 경쟁력 강화"], "03. 거시적 경제성"),
        ("조달 관납 공공 품질", ["조달청 관납 전국 총판의 검증된 신뢰", "로트별 분석 성적서(COA) 발행", "초정밀 혼화도 (CV < 5%) 무결점 보증"], "04. 절대적 신뢰도")
    ]
    for i, (title, bullets, tag) in enumerate(cards_s2):
        create_card(s2, Inches(0.8 + i * 2.95), Inches(1.8), Inches(2.8), Inches(3.6), title, bullets, tag=tag, border_color=C_EMERALD_DARK)
        
    # Mascot + Banner at Bottom
    if os.path.exists(IMG_MASCOT):
        s2.shapes.add_picture(IMG_MASCOT, Inches(0.8), Inches(5.6), Inches(1.2), Inches(1.2))
        
    banner = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(5.6), Inches(10.3), Inches(1.2))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(236, 253, 245)
    banner.line.color.rgb = C_EMERALD_DARK
    tf_b = banner.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "★ 삼원팜텍 스마트 바이오 약속 : S-NACF 조합원 농가의 건강과 축산 생산성 1위를 함께 만들어갑니다!"
    p_b.font.name = "Malgun Gothic"
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(6, 95, 70)
    add_footer(s2, prs, 2)

    # ----------------------------------------------------
    # SLIDE 3: Table of Contents
    # ----------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3, prs, C_BG_LIGHT)
    add_header(s3, prs, "AGENDA", "제안서 목차 및 프레젠테이션 진행 순서", "체계적인 6개 부문 분석 및 실행 로드맵")
    
    tocs = [
        ("Part I", "제안 배경 및 축산 환경 분석", "수입 곡물가 변동, 하절기 고온 스트레스, S-NACF 과제"),
        ("Part II", "제안사 역량 및 신뢰도", "(주)삼원팜텍 소개, 조달청 관납 실적, 첨단 제조 설비"),
        ("Part III", "핵심 경제성 및 밸류 분석", "500g/ton 처방의 공학적 의의, 톤당 3,000원 원가 비교"),
        ("Part IV", "8대 핵심 솔루션 상세 매트릭스", "기호성, 소화효소, GABA, 효모, 생균제, 곰팡이독소, 천연약제"),
        ("Part V", "한일사료 임가공 공정 적합성", "초정밀 혼화도(CV<5%), 펠렛 내열성, 고결방지(Anti-Caking)"),
        ("Part VI", "기대효과 및 실행 로드맵", "낙농(착유우/육성우) 생산성 지표, 3단계 도입 일정")
    ]
    for i, (part, title, desc) in enumerate(tocs):
        row = i // 3
        col = i % 3
        create_card(s3, Inches(0.8 + col * 3.95), Inches(1.8 + row * 2.4), Inches(3.8), Inches(2.2), f"{part}. {title}", [desc], tag="SECTION", border_color=C_NAVY_LIGHT)
    add_footer(s3, prs, 3)

    # ----------------------------------------------------
    # SLIDE 4: Livestock Industry Crisis (WITH GRAIN MARKET PHOTO)
    # ----------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    create_split_slide(s4, prs, 4, "PART I. 제안 배경", "축산업계 3중고(三重苦)와 S-NACF의 당면 과제",
                       "원료곡 가격 폭등 및 열 스트레스 속 사료 원가 방어 전략",
                       {"title": "사료업계 및 축산농가 3대 현안",
                        "tag": "CRISIS FACTORS",
                        "bullets": [
                            "국제 옥수수·대두박 시세 급등으로 사료 제조원가 압박 심화",
                            "기후변화에 따른 하절기 폭염 일수 증가 및 사료 섭취량 급감",
                            "혹서기 착유우 산유량 급감, 번식 장애, 송아지 설사 폐사율 증가",
                            "무항생제 축산 정책 강화로 친환경 면역 물질 도입 시급",
                            "사료 원가는 철저히 사수하면서 품질을 높일 혁신 처방 필수"
                        ]},
                       IMG_GRAIN_MARKET, "국제 사료 원료곡 가격 변동 추이 및 세계 해상 공급망 동향 대시보드")

    # ----------------------------------------------------
    # SLIDE 5: Hanil Feed Line Status (WITH FEED PRODUCTION LINE PHOTO)
    # ----------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    create_split_slide(s5, prs, 5, "PART I. 제안 배경", "한일사료 임가공 배합 라인(월 18,000 M/T) 현황",
                       "대규모 임가공 생산 체계에 완벽히 부합하는 전용 첨가제 처방의 필요성",
                       {"title": "월 18,000톤 임가공 라인 핵심 요구",
                        "tag": "PRODUCTION INFRA",
                        "bullets": [
                            "생산 규모: 배합사료 월 18,000 M/T (연간 216,000 M/T 대형 설비)",
                            "공정 특성: 고속 Twin-Shaft 패들 믹서 및 마이크로 인그리디언트 자동 빈",
                            "가공 형태: 가루사료(Mash), 펠렛(Pellet), 익스팬더 사료 동시 가공",
                            "핵심 요구 1: 500g 미량 투입 시 1톤 믹서 내 CV 5% 이내 균질 혼화",
                            "핵심 요구 2: 85~105℃ 스팀 펠렛 가공열 통과 후 유효 활성 95% 생존"
                        ]},
                       IMG_FEED_LINE, "한일사료 임가공 배합사료 공장 자동화 믹서 및 마이크로 도징 시스템")

    # ----------------------------------------------------
    # SLIDE 6: Limitations of Conventional Additives (Comparative Cards)
    # ----------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6, prs, C_BG_LIGHT)
    add_header(s6, prs, "PART I. 제안 배경", "기존 시중 첨가제의 구조적 한계와 비효율", "왜 기존 1.0kg ~ 2.0kg/ton 처방은 사료 공장과 농가에 손해인가?")
    create_card(s6, Inches(0.8), Inches(1.8), Inches(3.8), Inches(4.7), "과도한 부형제 투입 손실", 
                ["시중 제품은 저순도 원료로 80~90%가 무의미한 부형제(밀기울, 석회석)",
                 "톤당 1.0~2.0kg을 넣어도 실제 유효 성분은 극소량에 불과",
                 "불필요한 원료 운송비, 포장비, 적재 창고 비용 매몰"], tag="낮은 활성도")
    create_card(s6, Inches(4.75), Inches(1.8), Inches(3.8), Inches(4.7), "배합 공간 잠식 손실", 
                ["첨가제가 1.5kg 차지하면 옥수수·대두박 1.5kg이 빠져나감",
                 "조단백(CP) 및 대사에너지(ME) 스펙 하락 발생",
                 "빠진 영양소를 메우기 위해 고가 원료를 추가 투입하는 숨은 비용 발생"], tag="영양가 손실")
    create_card(s6, Inches(8.7), Inches(1.8), Inches(3.8), Inches(4.7), "비싼 투입 원가 부담", 
                ["톤당 첨가제 비용이 5,000원 ~ 9,000원에 육박",
                 "월 18,000톤 기준 월 1억~1억 6천만원의 막대한 원가 부담",
                 "사료 가격 경쟁력 약화 및 조합원 환원 사업 축소 유발"], tag="원가 압박")
    add_footer(s6, prs, 6)

    # ----------------------------------------------------
    # SLIDE 7: High-Concentration Paradigm (WITH PRODUCT PACKAGING MOCKUP)
    # ----------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    create_split_slide(s7, prs, 7, "PART I. 솔루션 혁신", "삼원팜텍 패러다임: 초고농축 마이크로 프리믹스 혁신",
                       "사료 톤당 단 500g(0.05%) 투입으로 동일 이상의 극대화된 약리 효과 구현",
                       {"title": "사료 톤당 500g 처방의 공학적 장점",
                        "tag": "500G/TON INNOVATION",
                        "bullets": [
                            "글로벌 1등급 고순도 원료만을 엄선하여 유효 분자 밀도 극대화",
                            "무의미한 부형제를 전면 배제하여 500g 투입만으로 충분한 약리 효과",
                            "톤당 1.0kg 이상의 배합 공간 확보 -> 옥수수/대두박 주영양소 100% 보존",
                            "월간 보관 중량 18톤 -> 9톤으로 50% 급감 (창고 및 물류비 반감)",
                            "전용 500g 고차단성 알루미늄 포장으로 12개월 무변질 품질 보증"
                        ]},
                       IMG_POUCH, "삼원팜텍 500g 전용 고차단성 알루미늄 스탠딩 파우치 패키지 디자인")

    # ----------------------------------------------------
    # SLIDE 8: 3-Party Value Chain (3 Columns)
    # ----------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8, prs, C_BG_LIGHT)
    add_header(s8, prs, "PART I. 협력 구조", "3자 협력(삼원팜텍 - 한일사료 - S-NACF) 비즈니스 밸류체인", "명확한 역할 분담과 완벽한 신뢰 기반의 협력 파트너십")
    create_card(s8, Inches(0.8), Inches(1.8), Inches(3.8), Inches(4.7), "(주)삼원팜텍 (제조·판매원)", 
                ["단독 제조·공급원으로서 모든 법적·품질 책임 총괄",
                 "국가 조달 관납 기준의 무결점 완제품 생산 (옥천 공장)",
                 "글로벌 최고 수준 원료 파트너십 흡수 및 R&D 지원",
                 "한일사료 공장 직납 및 S-NACF 전담 기술팀 운영"], tag="주관 기관 (단독 책임)", border_color=C_NAVY_PRIMARY)
    create_card(s8, Inches(4.75), Inches(1.8), Inches(3.8), Inches(4.7), "한일사료 (임가공 생산처)", 
                ["월 18,000톤 배합사료 정밀 임가공 생산 전담",
                 "삼원팜텍 500g 전용 공정 프로토콜 준수 (CV<5%)",
                 "마이크로 인그리디언트 자동 투입 라인 연계",
                 "로트별 품질 성적서 상호 검증 및 공정 모니터링"], tag="임가공 배합처", border_color=C_NAVY_LIGHT)
    create_card(s8, Inches(8.7), Inches(1.8), Inches(3.8), Inches(4.7), "서울우유협동조합 (수요처)", 
                ["사료 원가 절감(월 최대 1억원)을 통한 수익성 극대화",
                 "조합원 낙농 목장에 최상급 고품질 사료 공급",
                 "낙농 생산성(산유량 방어, 체세포수 1등급, 유방염 예방) 극대화",
                 "서울우유 낙농 사료 브랜드의 시장 리더십 확립"], tag="수요처 / 목장", border_color=C_EMERALD_DARK)
    add_footer(s8, prs, 8)

    # ----------------------------------------------------
    # SLIDE 9: Samwon Pharmtech Credentials (WITH FACTORY PHOTO)
    # ----------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    create_split_slide(s9, prs, 9, "PART II. 제안사 역량", "주식회사 삼원팜텍 개요 및 경영 비전",
                       "신뢰와 기술력으로 축산의 미래를 선도하는 동물용의약외품·보조사료 전문 제조기업",
                       {"title": "주식회사 삼원팜텍 기업 개요",
                        "tag": "CORPORATE PROFILE",
                        "bullets": [
                            "회사명: 주식회사 삼원팜텍 (SAMWON PHARMTECH CO., LTD.)",
                            "대표이사: 김 한 호",
                            "본사 및 제조공장: 충청북도 옥천군 옥천읍 테크노밸리길",
                            "주요 사업: 보조사료, 동물용의약외품, 친환경 방역제제 전문 제조",
                            "핵심 인프라: 마이크로 프리믹스 정밀 혼합 믹서 및 클린룸 충진 라인",
                            "공공 신뢰: 국가 조달청 등록 공급업체, 충북 거점 파트너"
                        ]},
                       IMG_FACTORY, "충북 옥천테크노밸리 소재 (주)삼원팜텍 본사 및 첨단 제조 공장 전경")

    # ----------------------------------------------------
    # SLIDE 10: Public Procurement Credentials (WITH MASCOT BADGE)
    # ----------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10, prs, C_BG_LIGHT)
    add_header(s10, prs, "PART II. 제안사 역량", "국가 조달청 관납 전국 총판 실적 및 공공 품질 관리", "로타갈(RotaGal) 등 엄격한 국가 방역 생물학적 제제 납품 실적으로 입증된 품질 관리 체계")
    
    create_card(s10, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.7), "조달청 관납 전국 총판", 
                ["국가 조달청 공식 계약 등록 업체",
                 "콜드체인 및 생물학적 제제(로타갈) 전국 총판",
                 "충남·충북 지자체 및 축협 방역 사업 전담",
                 "공공 검증 완료된 납품 실적 보유"], tag="관납 실적")
    create_card(s10, Inches(4.55), Inches(1.8), Inches(3.6), Inches(4.7), "가장 까다로운 품질 검사", 
                ["국가 검정 기준 로트별 유효성분 분석",
                 "보존제, 중금속, 미생물 안전성 무결점",
                 "보관·유통 전 과정 정밀 온도 추적 관리",
                 "사료 첨가제에도 동일 기준 100% 적용"], tag="품질 기준")
                 
    # Right Column: Mascot with badge
    if os.path.exists(IMG_MASCOT):
        s10.shapes.add_picture(IMG_MASCOT, Inches(8.4), Inches(1.8), Inches(4.1), Inches(4.1))
        tb_m = s10.shapes.add_textbox(Inches(8.4), Inches(6.0), Inches(4.1), Inches(0.5))
        p_m = tb_m.text_frame.paragraphs[0]
        p_m.text = "▲ 삼원팜텍 스마트 바이오 닥터 마스코트 (검증된 품질 보증)"
        p_m.font.name = "Malgun Gothic"
        p_m.font.size = Pt(9)
        p_m.font.bold = True
        p_m.font.color.rgb = C_TEXT_MUTED
        p_m.alignment = PP_ALIGN.CENTER
        
    add_footer(s10, prs, 10)

    # ----------------------------------------------------
    # SLIDE 11: Manufacturing Infrastructure & COA
    # ----------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s11, prs, C_BG_LIGHT)
    add_header(s11, prs, "PART II. 제안사 역량", "옥천 공장 첨단 제조 인프라 및 로트별 분석(COA) 시스템", "원료 입고부터 출하까지 전 공정 원스톱 품질 보증 체계")
    create_card(s11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "옥천 공장 특화 생산 설비", 
                ["정밀 리본 & 패들 믹서: 마이크로 단위 활성 성분의 완벽한 균질화",
                 "정전기 방지 및 방습 충진 시스템: 미세 분말의 응집 방지 및 정량 포장",
                 "에어 샤워 및 청정 클린룸: 미생물 오염 원천 차단된 위생 가공 환경",
                 "일일 최대 20톤 프리믹스 생산 능력: S-NACF 월 9톤 소요량 완벽 대응"], tag="제조 인프라")
    create_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "매 배치별 공인 성적서(COA) 동봉", 
                ["유효 활성 함량(Assay) 정밀 크로마토그래피(HPLC) 분석",
                 "입도 분석기(Particle Size Analyzer)를 통한 80~100 mesh 규격 검증",
                 "수분 함량 8.0% 이하 엄격 제어",
                 "한일사료 공장 입고 시마다 배치별 성적서 1:1 필수 제출"], tag="품질 보증 시스템")
    add_footer(s11, prs, 11)

    # ----------------------------------------------------
    # SLIDE 12: Economic Analysis 1 - 500g/ton Engineering
    # ----------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s12, prs, C_BG_LIGHT)
    add_header(s12, prs, "PART III. 경제성 분석", "표준 투입량 500g/ton (0.05%)의 공학적 의의", "왜 500g인가? 활성 분자 밀도 최적화와 균질 혼화도의 황금 비율")
    create_card(s12, Inches(0.8), Inches(1.8), Inches(3.8), Inches(4.7), "1. 과부하 없는 최적 투입량", 
                ["사료 1톤(1,000kg) 중 500g은 0.05%의 정밀 농도",
                 "가축 위장관 내에서 생체 이용률 100% 발휘",
                 "불필요한 과잉 흡수 및 체외 배설 낭비 차단"], tag="생리 최적화")
    create_card(s12, Inches(4.75), Inches(1.8), Inches(3.8), Inches(4.7), "2. 공정 혼화도 달성의 상한선", 
                ["한일사료 메인 믹서에서 편석 없이 분산되는 최적 질량",
                 "삼원팜텍 특수 무기 담체(Carrier) 매칭 기술 적용",
                 "변이계수(CV) 5% 미만 균질 혼화 입증"], tag="공학적 정밀성")
    create_card(s12, Inches(8.7), Inches(1.8), Inches(3.8), Inches(4.7), "3. 배합 공간의 완전한 회복", 
                ["기존 1.5kg 투입 대비 1.0kg의 영양 공간 확보",
                 "옥수수, 소이빈밀 등 고영양 주원료 배합 보존",
                 "사료 퀄리티를 저해하지 않는 완벽한 포뮬러"], tag="포뮬러 혁신")
    add_footer(s12, prs, 12)

    # ----------------------------------------------------
    # SLIDE 13: Economic Analysis 2 - 3,000 KRW/ton (WITH CHART_COST)
    # ----------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    create_split_slide(s13, prs, 13, "PART III. 경제성 분석", "사료 톤당 단 3,000원 최적 원가 구조 분석",
                       "월 18,000톤 생산 시 월 5,400만원 투입으로 사료 가치 극대화",
                       {"title": "투입 원가 세부 산출식 및 효과",
                        "tag": "COST CALCULATION",
                        "bullets": [
                            "제품 기준 공급 단가: 6,000원 / kg (고농축 활성 원료 처방)",
                            "사료 톤당 표준 투입량: 500g (0.5kg / ton)",
                            "사료 톤당 첨가제 투입 원가: 6,000원 × 0.5kg = 단 3,000원 / ton",
                            "S-NACF 월간 총 소요량: 18,000톤 × 0.5kg = 9,000 kg (9.0 M/T)",
                            "S-NACF 월간 총 공급 금액: 9,000 kg × 6,000원 = 54,000,000원",
                            "시중 일반 처방(톤당 6,000~9,000원) 대비 월 최대 1억원 원가 절감"
                        ]},
                       CHART_COST, "사료 톤당 첨가제 투입 비용 비교 분석 (삼원팜텍 단 3,000원 실현)")

    # ----------------------------------------------------
    # SLIDE 14: Economic Comparison Table
    # ----------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s14, prs, C_BG_LIGHT)
    add_header(s14, prs, "PART III. 경제성 분석", "경제성 비교 분석표: 시중 처방 vs 삼원팜텍 처방", "월 최대 1억 800만원, 연간 최대 13억원의 직접 원가 절감 효과")
    
    table_shape = s14.shapes.add_table(6, 4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.7))
    table = table_shape.table
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.2)
    
    headers = ["비교 항목", "시중 일반 첨가제 처방", "삼원팜텍 고농축 프리믹스", "S-NACF 절감 및 개선 효과"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Malgun Gothic"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER
        
    t_rows = [
        ("사료 톤당 투입량", "1,000g ~ 2,000g / ton", "500g / ton (0.05%)", "투입량 50~75% 획기적 절감"),
        ("제품 공급 단가", "3,500원 ~ 4,500원 / kg", "6,000원 / kg", "초고순도 정밀 원료 처방"),
        ("사료 톤당 투입비용", "4,500원 ~ 9,000원 / ton", "단 3,000원 / ton", "톤당 1,500원 ~ 6,000원 절감"),
        ("월간 총 비용(18,000톤)", "8,100만원 ~ 1억 6,200만원", "5,400만원", "월 2,700만 ~ 1억 800만원 절감"),
        ("배합 공간(Nutrient Space)", "부형제 1~2kg 영양 잠식", "유효 성분 위주 배합 보존", "조단백/에너지 스펙 100% 사수")
    ]
    for i, row in enumerate(t_rows, start=1):
        bg = RGBColor(241, 245, 249) if i % 2 == 1 else RGBColor(255, 255, 255)
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Malgun Gothic"
            p.font.size = Pt(10)
            if j == 0:
                p.font.bold = True
                p.alignment = PP_ALIGN.LEFT
            elif j == 2:
                p.font.bold = True
                p.font.color.rgb = C_EMERALD_DARK
                p.alignment = PP_ALIGN.CENTER
            elif j == 3:
                p.font.bold = True
                p.font.color.rgb = C_NAVY_LIGHT
                p.alignment = PP_ALIGN.CENTER
            else:
                p.alignment = PP_ALIGN.CENTER
    add_footer(s14, prs, 14)

    # ----------------------------------------------------
    # SLIDE 15: Nutrient Space & Logistics Benefit
    # ----------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s15, prs, C_BG_LIGHT)
    add_header(s15, prs, "PART III. 경제성 분석", "배합 공간 확보 및 물류·보관 운영 이익", "눈에 보이지 않는 배합비 절감 효과와 창고 운영비 반감 혁신")
    create_card(s15, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "배합 공간(Nutrient Space) 확보 이익", 
                ["기존 첨가제(1.5kg) 대비 톤당 1.0kg 이상의 배합 스페이스 확보",
                 "사료 1톤 당 옥수수 1.0kg을 더 넣을 수 있어 에너지(ME) 자동 상승",
                 "부족한 단백질/칼로리를 맞추기 위해 값비싼 유지를 추가하지 않아도 됨",
                 "배합비(Least-Cost) 시뮬레이션 결과 사료 톤당 최소 1,500원 추가 절감 효과"], tag="포뮬러 이익")
    create_card(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "물류·보관 및 창고 운영비 50% 절감", 
                ["월간 입고 물량 비교:",
                 "• 기존 처방: 월 18톤 ~ 36톤의 막대한 파렛트 적재 공간 필요",
                 "• 삼원팜텍 처방: 월 단 9톤 (9,000kg) 소포장/톤백 보관",
                 "창고 보관 면적 50% 축소, 지게차 상하차 횟수 반감",
                 "장기 보관에 따른 변질 및 고결(Caking) 리스크 원천 해소"], tag="물류 혁신")
    add_footer(s15, prs, 15)

    # ----------------------------------------------------
    # SLIDE 16: 8 Strategic Solutions Overview (WITH 3D CAPSULE PHOTO)
    # ----------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    create_split_slide(s16, prs, 16, "PART IV. 8대 핵심 솔루션", "삼원팜텍 8대 핵심 솔루션 기술 상세 총괄",
                       "글로벌 검증 원료와 나노 제형 기술이 집약된 8대 카테고리 솔루션 매트릭스",
                       {"title": "8대 전략 카테고리 라인업",
                        "tag": "8 STRATEGIC CATEGORIES",
                        "bullets": [
                            "01. DDC 향미·감미제: 초기 섭취량 ADFI 8~15% 극대화",
                            "02. VTR 복합소화효소: ME 50~70kcal 개선, 분변 10% 감소",
                            "03. Jienuo 코팅 GABA: 하절기 고온 스트레스 호흡수 안정",
                            "04. HZM 고농도효모: 반추위 혐기 발효 & 세포벽 면역(MOS/β-Glucan)",
                            "05. HZM 3종 생균제: 내생포자 고초균 2종, 설사율 70% 억제",
                            "06. HZM 나노흡착제: 몬모릴로나이트 곰팡이독소 영구 포집",
                            "07. VEESURE 식물구충: 무항생제 천연 콕시듐/기생충 방어",
                            "08. DNJ 항바이러스: 상엽추출 천연 알파-글루코시다아제 억제"
                        ]},
                       IMG_CAPSULE, "삼원팜텍 마이크로 캡슐화 활성 분자 3D 바이오 시각화 렌더링")

    # ----------------------------------------------------
    # SLIDE 17: Solution 1 - DDC Flavor
    # ----------------------------------------------------
    s17 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s17, prs, C_BG_LIGHT)
    add_header(s17, prs, "솔루션 01", "기호성 증진 복합 향미·감미제 솔루션 (DDC 특화 라인)", "사료 교체기 및 원료 변동 시 섭취 거부감 제로화 & 초기 섭취량 극대화")
    create_card(s17, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 약리 기전", 
                ["원료: 글로벌 향미 전문 DDC社 열안정성 농축 밀크바닐라향, 천연 당밀향, 산딸기향, SX907 고순도 감미제",
                 "순도: 유효 감미도 99% 이상, 설탕 대비 수백 배의 깊고 부드러운 단맛",
                 "기전: 가축의 후각·미각 수용체를 즉각 자극하여 침샘 및 위액 분비 유도",
                 "식욕 중추를 활성화하여 섭취 지연 현상 원천 차단"], tag="SPEC & MECHANISM")
    create_card(s17, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 실증 데이터", 
                ["초기 사료 섭취량(ADFI/DMI) 8~15% 대폭 개선",
                 "송아지 이유 초기 사료 섭취 지연으로 인한 위축 발생 예방",
                 "착유우 혹서기 고온기 사료 섭취 거부 완벽 방어",
                 "가루사료 및 펠렛 가공 후에도 지속되는 롱래스팅(Long-lasting) 잔향"], tag="PROVEN RESULTS")
    add_footer(s17, prs, 17)

    # ----------------------------------------------------
    # SLIDE 18: Solution 2 - VTR Enzymes
    # ----------------------------------------------------
    s18 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s18, prs, C_BG_LIGHT)
    add_header(s18, prs, "솔루션 02", "고활성 열안정성 소화 효소제 솔루션 (VTR 글로벌 라인)", "비전분다당류(NSP) 분해 및 영양소 이용률 극대화로 사료 효율 혁신")
    create_card(s18, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 약리 기전", 
                ["원료: 글로벌 효소 선도기업 VTR社 내열성 코팅 복합 효소제",
                 "구성: β-Mannanase, Xylanase, 복합 프로테아제(Protease), 아밀라아제",
                 "기전: 곡류 내 소화 저해 인자인 아라비노자일란 및 만난을 강력 분해",
                 "장내 점도를 신속히 낮추어 영양소와 소화액의 접촉 면적 극대화"], tag="SPEC & MECHANISM")
    create_card(s18, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 실증 데이터", 
                ["사료 톤당 유효 대사에너지(ME) 50~70 kcal/kg 개선",
                 "동일 배합비 기준 사료요구율(FCR) 0.05~0.08 포인트 개선",
                 "미소화 단백질의 장내 부패 차단 및 연변·설사 발생률 급감",
                 "가축 분변 배출량 10% 이상 감소로 축사 환경 개선"], tag="PROVEN RESULTS")
    add_footer(s18, prs, 18)

    # ----------------------------------------------------
    # SLIDE 19: Solution 3 - GABA (WITH DAIRY COW PHOTO)
    # ----------------------------------------------------
    s19 = prs.slides.add_slide(blank_layout)
    create_split_slide(s19, prs, 19, "솔루션 03", "항스트레스 장관 바이패스 코팅 GABA (Jienuo 마이크로 캡슐)",
                       "하절기 극한 폭염 및 환경 스트레스에 따른 생산성 저하 방어",
                       {"title": "GABA 작용 기전 및 착유우 효과",
                        "tag": "HEAT STRESS SOLUTION",
                        "bullets": [
                            "원료: Jienuo 특수 지질 마이크로 캡슐 코팅 Gamma-Aminobutyric Acid",
                            "코팅: 위산과 반추위 분해를 견디고 소장에서 흡수되는 바이패스(Bypass) 제형",
                            "기전: 중추신경계 억제성 신경전달물질 작용으로 혈중 Cortisol 농도 정상화",
                            "착유우: 하절기 고온기 건물섭취량(DMI) 유지 및 산유 피크 연장",
                            "체세포수 25% 급감으로 유질 등급 및 유대 수익 개선"
                        ]},
                       IMG_DAIRY, "하절기 고온 스트레스 방어로 산유 피크를 유지하는 첨단 낙농 축사")

    # ----------------------------------------------------
    # SLIDE 20: Solution 4 - HZM Yeast
    # ----------------------------------------------------
    s20 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s20, prs, C_BG_LIGHT)
    add_header(s20, prs, "솔루션 04", "고농도 활성 효모균 및 세포벽 면역제 (HZM 효모 복합체)", "반추위 혐기 환경 안정화 및 병원균 흡착 배출을 통한 전신 면역 증강")
    create_card(s20, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 약리 기전", 
                ["원료: HZM 고농도 활성 Saccharomyces cerevisiae + 세포벽 유래 MOS & β-Glucan",
                 "기전 1: 반추위 및 장관 내 용존산소를 소모하여 절대혐기성 유익 미생물 번식 환경 조성",
                 "기전 2: 만난올리고당(MOS)이 대장균, 살모넬라균의 섬모에 결합하여 장벽 부착 차단",
                 "기전 3: 베타글루칸이 대식세포를 활성화하여 전신 면역글로불린 분비 유도"], tag="SPEC & MECHANISM")
    create_card(s20, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 실증 데이터", 
                ["낙농 젖소 및 육성우 반추위 섬유소 분해 미생물 증식 촉진 (소화율 7%↑)",
                 "반추위 산독증(Subacute Ruminal Acidosis, SARA) 완벽 예방",
                 "혈중 면역글로불린(IgG, IgA) 분비 촉진으로 질병 감염 저항력 극대화",
                 "장내 융모 높이(Villus Height) 신장으로 영양 흡수 면적 확대"], tag="PROVEN RESULTS")
    add_footer(s20, prs, 20)

    # ----------------------------------------------------
    # SLIDE 21: Solution 5 - HZM 3 Probiotics (WITH CALF PHOTO)
    # ----------------------------------------------------
    s21 = prs.slides.add_slide(blank_layout)
    create_split_slide(s21, prs, 21, "솔루션 05", "장내 정착 고농도 3종 복합 생균제 (HZM 포자 고초균 및 유산균)",
                       "열과 위산에 내성을 가진 내생포자 균주 처방으로 장관 끝까지 살아있는 생균 공급",
                       {"title": "3종 생균제 복합 처방 및 송아지 설사 억제",
                        "tag": "GUT HEALTH & IMMUNITY",
                        "bullets": [
                            "균주 구성: Bacillus subtilis + Bacillus licheniformis + L. plantarum",
                            "보증 균수: 총 유익 생균수 1.0 × 10^10 CFU/g 이상 초고농도 보증",
                            "펠렛 가공열(90℃) 및 위산 통과 후 소장·대장에서 100% 발아",
                            "어린 송아지 설사 발생률 80% 이상 억제 및 폐사율 제로화 달성",
                            "우사 내 암모니아 가스 40~50% 저감으로 쾌적한 환경 조성"
                        ]},
                       IMG_CALF, "설사 억제를 통해 건강하고 균일한 성장을 보이는 홀스타인 어린 송아지")

    # ----------------------------------------------------
    # SLIDE 22: Solution 6 - HZM Nano Mycotoxin Binder
    # ----------------------------------------------------
    s22 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s22, prs, C_BG_LIGHT)
    add_header(s22, prs, "솔루션 06", "광범위 나노 층상 진균독소 흡착제 (HZM 몬모릴로나이트)", "영양소 흡착 손실 없이 곰팡이독소만을 선택적으로 영구 포집·배출")
    create_card(s22, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 흡착 메커니즘", 
                ["원료: HZM 초고순도 나노 층상구조 몬모릴로나이트 (Montmorillonite)",
                 "물성: 고순도 정제 알루미노실리케이트, 비표면적 800㎡/g 이상",
                 "기전: 극성화된 나노 층간에 곰팡이독소 분자를 물리화학적 결합(포집)",
                 "선택 흡착: 비타민, 아미노산 등 필수 영양소는 흡착하지 않고 독소만 선별 포집"], tag="SPEC & MECHANISM")
    create_card(s22, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 독소 제거율", 
                ["아플라톡신(Aflatoxin B1) 흡착 제거율 98% 이상",
                 "번식 장애를 유발하는 제랄레논(Zearalenone) 및 오크라톡신 포집",
                 "곡류 보관 중 곰팡이 독소 오염 사료 섭취 시 간 기능 보호",
                 "착유우 번식 장애 방지 및 원유 내 아플라톡신 M1 전이 완벽 차단"], tag="PROVEN RESULTS")
    add_footer(s22, prs, 22)

    # ----------------------------------------------------
    # SLIDE 23: Solution 7 - VEESURE Dewormer
    # ----------------------------------------------------
    s23 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s23, prs, C_BG_LIGHT)
    add_header(s23, prs, "솔루션 07", "식물 유래 천연구충제 및 천연 콕시듐 방어제 (VEESURE 솔루션)", "항생제 내성 및 휴약기간 걱정 없는 식물 파이토케미컬 천연 방어막")
    create_card(s23, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 약리 기전", 
                ["원료: 인도 천연 추출물 전문 VEESURE社 표준화 파이토케미컬 복합 추출물",
                 "지표 성분: 알리신(Allicin), 티몰(Thymol), 피페린(Piperine), 탄닌 복합체",
                 "기전 1: 원충 세포벽 구성 지질층을 용해하고 난포낭(Oocyst) 포자 형성 저해",
                 "기전 2: 내부 기생충(선충, 십이지장충 등)의 신경계를 마비시켜 장벽 탈락 유도"], tag="SPEC & MECHANISM")
    create_card(s23, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 안전성", 
                ["콕시듐성 혈변 및 괴사성 장염 발생률 제로화 수준 방어",
                 "화학 합성 구충제 대체: 항생제 내성 균주 발생 원천 차단",
                 "휴약 기간(Withdrawal Period) 제로: 출하 직전까지 안전 급여 가능",
                 "장벽 점막 보호 및 장 상피세포 재생 속도 30% 촉진"], tag="PROVEN RESULTS")
    add_footer(s23, prs, 23)

    # ----------------------------------------------------
    # SLIDE 24: Solution 8 - DNJ Antiviral
    # ----------------------------------------------------
    s24 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s24, prs, C_BG_LIGHT)
    add_header(s24, prs, "솔루션 08", "천연 유래 광범위 항바이러스 솔루션 (1-Deoxynojirimycin, DNJ)", "상엽(뽕나무 잎) 추출 천연 유효 물질로 바이러스의 침투와 증식을 선제적 차단")
    create_card(s24, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "원료 규격 및 약리 기전", 
                ["원료: 천연 상엽(Morus alba) 추출 고순도 1-Deoxynojirimycin (DNJ)",
                 "기전: 바이러스 외피 당단백질(Envelope Glycoprotein) 합성에 필수적인 알파-글루코시다아제 효소 저해",
                 "숙주 세포 표면의 수용체와 바이러스의 융합 및 세포 내 침투 차단",
                 "감염 초기 바이러스 복제(Replication)를 강력히 억제"], tag="SPEC & MECHANISM")
    create_card(s24, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "적용 효과 및 질병 방어", 
                ["소 로타바이러스(Rotavirus) 및 코로나바이러스 감염 억제",
                 "어린 송아지 바이러스성 설사증 및 장염 선제적 예방",
                 "환절기 송아지 복합 호흡기 증후군(BRD) 발병률 70% 이상 저감",
                 "바이러스성 폐사 리스크 차단으로 낙농 목장 경제 손실 원천 방어"], tag="PROVEN RESULTS")
    add_footer(s24, prs, 24)

    # ----------------------------------------------------
    # SLIDE 25: Process QA/QC 1 - Micro-Dosing (WITH CHART_HOMOGENEITY)
    # ----------------------------------------------------
    s25 = prs.slides.add_slide(blank_layout)
    create_split_slide(s25, prs, 25, "PART V. 임가공 공정 적합성", "500g/ton 초정밀 마이크로 도징 혼화도 (CV < 5%) 검증",
                       "1톤 거대 믹서에서도 한 톨의 사료까지 균일하게 도달하는 분산성",
                       {"title": "초정밀 혼화도 검증 결과",
                        "tag": "MIXING HOMOGENEITY",
                        "bullets": [
                            "특수 무기 담체(Carrier) 매칭으로 믹서 투입 후 45초 내 완전 분산",
                            "공인 검사 기준 CV 10% 대비 2배 이상 우수한 CV 3.8% ~ 4.6% 실현",
                            "80~100 mesh 균일 입도 매칭으로 혼합 편석(Segregation) 원천 차단",
                            "사료 1톤 어느 지점을 채취해도 균일한 약리 활성 검출 보증",
                            "가축 개체별 사료 섭취 불균형 및 투약 편차 완전 해소"
                        ]},
                       CHART_HOMOGENEITY, "한일사료 메인 믹서 500g 투입 시 정규분포 곡선 (삼원팜텍 CV 3.8%)")

    # ----------------------------------------------------
    # SLIDE 26: Process QA/QC 2 - Heat Stability (WITH CHART_HEAT)
    # ----------------------------------------------------
    s26 = prs.slides.add_slide(blank_layout)
    create_split_slide(s26, prs, 26, "PART V. 임가공 공정 적합성", "펠렛(Pellet)·익스팬더 85~110℃ 가공열 안정성",
                       "고온 스팀 압력을 견뎌내는 다중 마이크로 캡슐화 코팅 기술",
                       {"title": "고온 가공열 내열성 데이터",
                        "tag": "THERMAL STABILITY",
                        "bullets": [
                            "한일사료 펠렛 공정 조건: 스팀 컨디셔닝 85~90℃, 다이 통과 시 순간 고온",
                            "1차 내열 고분자 쉘 + 2차 지질 매트릭스 다중 캡슐화 코팅",
                            "VTR 소화 효소제(β-Mannanase): 90℃ 펠렛 통과 후 활성 95.4% 유지",
                            "HZM 포자 형성 생균제: 100℃ 익스팬더 통과 후 생존율 96.8%",
                            "완제품 펠렛 사료에서도 보증 성분 100% 충족 확인"
                        ]},
                       CHART_HEAT, "펠렛·익스팬더 스팀 가공 온도별 활성 잔존율 곡선 (95% 이상 생존)")

    # ----------------------------------------------------
    # SLIDE 27: Process QA/QC 3 - Anti-Caking
    # ----------------------------------------------------
    s27 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s27, prs, C_BG_LIGHT)
    add_header(s27, prs, "PART V. 임가공 공정 적합성", "자동화 빈(Bin) 투입 및 고결 방지(Anti-Caking) 설계", "하절기 고온 다습 환경에서도 막힘 없는 유동성(Free-Flowing) 확보")
    create_card(s27, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.7), "나노 소수성 실리카 표면 개질", 
                ["공기 중 수분 흡수로 인한 분말의 뭉침(Caking) 및 굳음 방지",
                 "마이크로 입자 표면에 나노 실리카 피막 형성으로 입자 간 마찰 감소",
                 "휴식각(Angle of Repose) 32도 이하: 액체에 준하는 매끄러운 흐름성",
                 "한일사료 자동화 투입 호퍼의 브릿지(Bridging) 현상 원천 차단"], tag="유동성 설계")
    create_card(s27, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.7), "완벽한 포장 및 현장 편의성", 
                ["포장 규격: 1톤 배합 전용 500g 소포장 파우치 또는 25kg / 500kg 톤백 맞춤 공급",
                 "내습 알루미늄 포장: 12개월 장기 보관 시에도 품질 변질 제로",
                 "바코드 및 배치 번호 관리: 원료 추적성 100% 확보",
                 "한일사료 작업자의 투입 편의성 극대화 및 분진 발생 억제"], tag="포장 및 편의성")
    add_footer(s27, prs, 27)

    # ----------------------------------------------------
    # SLIDE 28: Livestock Outcomes (WITH HANWOO PHOTO)
    # ----------------------------------------------------
    s28 = prs.slides.add_slide(blank_layout)
    create_split_slide(s28, prs, 28, "PART VI. 기대효과 및 로드맵", "낙농 목장 정량적 기대효과 및 생산성 향상",
                       "착유우 및 육성우 목장의 실질적인 소득 증대와 서울우유 브랜드 가치 제고",
                       {"title": "낙농 목장 핵심 실증 목표치",
                        "tag": "PRODUCTIVITY OUTCOMES",
                        "bullets": [
                            "낙농 착유우: 하절기 산유량 +1.8kg 유지, 비유 피크 3~4주 연장",
                            "원유 유질 개선: 체세포수(SCC) 42% 급감, 1등급 원유 안정 수령",
                            "유방염 예방: 임상형 유방염 65% 저감, 폐유 손실 및 치료비 70% 절감",
                            "육성우·송아지: 설사 80% 억제, 초산일령 1.5개월 단축, 육성비 절감",
                            "첨가제 1원 투자 대비 목장 환원 실익 5.2배 창출 (ROI 1:5.2)"
                        ]},
                       IMG_DAIRY, "하절기 산유량 방어 및 1등급 유질을 유지하는 서울우유 스마트 낙농 목장")

    # ----------------------------------------------------
    # SLIDE 29: Implementation Roadmap (WITH CHART_ROI)
    # ----------------------------------------------------
    s29 = prs.slides.add_slide(blank_layout)
    create_split_slide(s29, prs, 29, "PART VI. 기대효과 및 로드맵", "단계별 도입 로드맵 및 농가 실익 환원 효과",
                       "철저한 사전 검증부터 월 18,000톤 전 라인 공급까지 체계적인 실행 일정",
                       {"title": "3단계 단계별 실행 계획",
                        "tag": "3-PHASE ROADMAP",
                        "bullets": [
                            "Phase 1 (1개월차 / 사전 검증): 한일사료 라인 점검, CV 혼화도 & 펠렛 내열성 Lab Test 완료",
                            "Phase 2 (2개월차 / 파일럿 실증): S-NACF 시범 농가 1,000톤 파일럿 생산 및 섭취/설사 모니터링",
                            "Phase 3 (3개월차 이후 / 전면 공급): 월 18,000톤 전 라인 정규 납품 개시",
                            "삼원팜텍 옥천 공장 월 9톤 정기 직납 및 매 로트별 COA 성적서 동봉",
                            "전담 수의·영양 기술지원팀의 농가 무상 현장 방문 컨설팅 상시 가동"
                        ]},
                       CHART_ROI, "축종별 정량적 개선 효과 및 투자 대비 실익 환원 지표 인포그래픽")

    # ----------------------------------------------------
    # SLIDE 30: Conclusion & Commitment (WITH MASCOT & FACTORY)
    # ----------------------------------------------------
    s30 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s30, prs, C_NAVY_DARK)
    
    # Factory photo
    if os.path.exists(IMG_FACTORY):
        s30.shapes.add_picture(IMG_FACTORY, Inches(6.8), Inches(1.2), Inches(5.7), Inches(4.5))
        
    # Mascot on Slide 30
    if os.path.exists(IMG_MASCOT):
        s30.shapes.add_picture(IMG_MASCOT, Inches(10.8), Inches(4.2), Inches(2.0), Inches(2.0))
        
    tb30 = s30.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5.8), Inches(5.2))
    tf30 = tb30.text_frame
    tf30.word_wrap = True
    
    p = tf30.paragraphs[0]
    r = p.add_run()
    r.text = "SAMWON PHARMTECH QUALITY ASSURANCE & COMMITMENT"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_EMERALD
    p.space_after = Pt(12)
    
    p = tf30.add_paragraph()
    r = p.add_run()
    r.text = "S-NACF의 든든한 사료 품질 파트너,\n(주)삼원팜텍이 책임지고 성공시키겠습니다."
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(16)
    
    p = tf30.add_paragraph()
    r = p.add_run()
    r.text = (
        "• 사료 톤당 단 3,000원의 파격적 원가 혁신 (월 5,400만원, 연간 최대 13억원 절감)\n"
        "• 500g/ton 초고농축 처방으로 영양소 스페이스 보존 및 물류비 50% 반감\n"
        "• 국가 조달청 관납 전국 총판의 검증된 공공 품질 관리 기준 무결점 적용\n"
        "• 제조·판매원 단독 책임 하에 한일사료 임가공 배합 라인의 완벽한 공정 일치 약속\n"
        "• 조합원 낙농가의 산유량 증대, 체세포수 저감 및 질병 방어로 서울우유 브랜드 가치 극대화"
    )
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(226, 232, 240)
    p.space_after = Pt(20)
    
    p = tf30.add_paragraph()
    r = p.add_run()
    r.text = "주식회사 삼원팜텍  대표이사  김  한  호"
    r.font.name = "Malgun Gothic"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = C_EMERALD
    add_footer(s30, prs, 30)

    output_dir = r"C:\Users\master\vet_animal_hospital\s_project"
    output_path = os.path.join(output_dir, "S-NACF_고농축사료첨가제_제안_30장덱_삼원팜텍.pptx")
    prs.save(output_path)
    print(f"Successfully created 30-slide presentation at {output_path}")

if __name__ == "__main__":
    build_deck()
