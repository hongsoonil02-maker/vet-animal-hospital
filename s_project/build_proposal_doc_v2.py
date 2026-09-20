import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

ASSETS_DIR = r"C:\Users\master\vet_animal_hospital\s_project\assets"
IMG_FACTORY = os.path.join(ASSETS_DIR, "company_factory_panorama_1789881641339.jpg")
IMG_FEED_LINE = os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg")
IMG_GRAIN_MARKET = os.path.join(ASSETS_DIR, "grain_market_volatility_1789881820210.jpg")
IMG_DAIRY = os.path.join(ASSETS_DIR, "dairy_cows_smart_farm_1789881841764.jpg")
IMG_CALF = os.path.join(ASSETS_DIR, "dairy_calf_nutrition.jpg")
IMG_CAPSULE = os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg")
IMG_POUCH = os.path.join(ASSETS_DIR, "premix_product_packaging_1789881875376.jpg")
IMG_MASCOT = os.path.join(ASSETS_DIR, "child_drinking_milk.jpg")
IMG_PELLET = os.path.join(ASSETS_DIR, "feed_pellet_extrusion.jpg")
IMG_LAB = os.path.join(ASSETS_DIR, "livestock_nutrition_lab.jpg")

CHART_COST = os.path.join(ASSETS_DIR, "chart_cost_comparison.png")
CHART_HOMOGENEITY = os.path.join(ASSETS_DIR, "chart_homogeneity_cv.png")
CHART_HEAT = os.path.join(ASSETS_DIR, "chart_pellet_heat.png")
CHART_ROI = os.path.join(ASSETS_DIR, "chart_livestock_roi.png")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CCCCCC", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'<w:tcBorders {nsdecls("w")}>'
    for side, style in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        if style == "none":
            borders_xml += f'<w:{side} w:val="none"/>'
        else:
            borders_xml += f'<w:{side} w:val="{style}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
    borders_xml += '</w:tcBorders>'
    tcPr.append(parse_xml(borders_xml))

def add_figure(doc, img_path, caption, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(f"▲ [참고자료 / 실물 사진] {caption}")
        r_cap.font.name = 'Malgun Gothic'
        r_cap.font.size = Pt(8.5)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

def add_styled_heading(doc, text, level):
    p = doc.add_heading(level=level)
    run = p.add_run(text)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    
    if level == 1:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 32, 67)
    elif level == 2:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(5, 150, 105)
    elif level == 3:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def create_document():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
        hp = section.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("주식회사 삼원팜텍 | 서울우유 맞춤형 고농축 사료첨가제 기술제안서")
        hrun.font.name = 'Malgun Gothic'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(140, 150, 160)
        
        fp = section.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SAMWON PHARMTECH CO., LTD.  |  CONFIDENTIAL")
        frun.font.name = 'Malgun Gothic'
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 150, 160)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Malgun Gothic'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # ================= COVER BANNER =================
    cover_box = doc.add_table(rows=1, cols=1)
    cover_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = cover_box.rows[0].cells[0]
    set_cell_background(c_cell, "0A192F")
    set_cell_margins(c_cell, top=260, bottom=260, left=300, right=300)
    
    p = c_cell.paragraphs[0]
    r0 = p.add_run("주식회사 삼원팜텍  |  SAMWON PHARMTECH\n")
    r0.font.name = 'Malgun Gothic'
    r0.font.size = Pt(11)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(16, 185, 129)
    
    r1 = p.add_run("[기술 공급 제안서]\n")
    r1.font.name = 'Malgun Gothic'
    r1.font.size = Pt(19)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(255, 255, 255)
    
    r2 = p.add_run("서울우유 사료 품질 혁신 및 원가 최적화를 위한\n맞춤형 고농축 사료첨가제(Micro-Premix) 공급 제안\n")
    r2.font.name = 'Malgun Gothic'
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(226, 232, 240)
    
    r3 = p.add_run("한일사료 임가공 배합 라인(월 18,000 M/T) 전용 초정밀 500g/ton 낙농 전문 솔루션")
    r3.font.name = 'Malgun Gothic'
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = RGBColor(148, 163, 184)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Embed Factory Panorama on Cover
    add_figure(doc, IMG_FACTORY, "(주)삼원팜텍 충북 옥천 테크노밸리 본사 및 첨단 R&D 제조 시설 전경", width=Inches(6.2))

    # Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("제 안 기 관 (제조·판매원)", "주식회사 삼원팜텍 (대표이사 김한호)"),
        ("제 안 대 상 (수 요 처)", "서울우유 (서울우유협동조합)"),
        ("임가공 생산처", "한일사료 배합사료 공장 (임가공 위탁생산 라인)"),
        ("적 용 규 모", "배합사료 월 18,000 M/T (연간 216,000 M/T)"),
        ("제 안 일 자", "2026년 9월"),
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        set_cell_borders(c0, top="single", bottom="single", left="none", right="none", color="E2E8F0")
        set_cell_borders(c1, top="single", bottom="single", left="none", right="none", color="E2E8F0")
        
        p0 = c0.paragraphs[0]
        r = p0.add_run(label)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(51, 65, 85)
        
        p1 = c1.paragraphs[0]
        r = p1.add_run(val)
        r.font.size = Pt(9)
        if "삼원팜텍" in val:
            r.font.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Mascot banner
    add_figure(doc, IMG_MASCOT, "삼원팜텍 스마트 낙농 바이오 닥터 마스코트 (친환경 낙농과 과학적 처방의 동반자)", width=Inches(3.2))

    doc.add_page_break()

    # ================= CHAPTER 1 =================
    add_styled_heading(doc, "제 1 장. 제안 개요 및 배경 (Executive Summary)", level=1)
    
    add_styled_heading(doc, "1.1 제안 배경 및 낙농 환경 분석", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "최근 국내 배합사료 산업 및 낙농 목가는 수입 곡물 가격의 높은 변동성, 기후변화에 따른 하절기 극한 열 스트레스, "
        "원유 체세포수 상승 및 유방염, 대사성 질병의 상시화, 그리고 무항생제 청정 우유 생산 정책 등 복합적인 생산성 저하 위기에 직면해 있습니다.\n\n"
        "이러한 환경에서 서울우유(서울우유협동조합)는 한일사료에서 임가공 생산하는 월 18,000톤의 배합사료 라인에 대해, "
        "사료 제조 원가를 엄격히 방어하면서도 조합원 목장의 착유우 산유량, 1등급 유질, 체세포수 저감, 송아지 육성율을 획기적으로 향상시킬 수 있는 "
        "차세대 맞춤형 고농축 사료첨가제 도입이 절실한 시점입니다."
    )
    add_figure(doc, IMG_GRAIN_MARKET, "국제 사료 원료곡(옥수수, 대두박) 시세 변동 추이 및 세계 공급망 인포그래픽", width=Inches(5.8))

    add_styled_heading(doc, "1.2 서울우유 맞춤형 고농축(High-Concentration) 공급 전략", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "기존 시중의 보조사료 및 첨가제는 저순도 원료와 과도한 부형제로 인해 톤당 1.0kg ~ 2.0kg(0.1~0.2%) 이상을 투입해야 하므로, "
        "투입 비용이 톤당 6,000원~10,000원에 달하고 주원료(옥수수, 대두박 등)의 배합 공간(Nutrient Space)을 잠식하는 한계가 있었습니다.\n\n"
        "이에 주식회사 삼원팜텍은 핵심 유효 활성물질만을 고밀도로 집약한 '초고농축 마이크로 프리믹스(Micro-Premix)' 기술을 적용하여, "
        "사료 톤당 단 500g(0.05%) 투입만으로 동일 이상의 약리 기전과 낙농 생산성 개선 효과를 완벽히 구현하는 파격적인 경제형 처방을 제안합니다."
    )
    add_figure(doc, IMG_POUCH, "삼원팜텍 500g 전용 고차단성 알루미늄 스탠딩 파우치 제품 패키지 목업", width=Inches(4.5))

    # ================= CHAPTER 2 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 2 장. 제안사 역량 및 신뢰도 (Company Credentials)", level=1)
    
    add_styled_heading(doc, "2.1 주식회사 삼원팜텍 개요 및 경영 비전", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "충청북도 옥천테크노밸리에 본사와 최첨단 제조공장을 보유한 (주)삼원팜텍(대표이사 김한호)은 "
        "동물용의약외품, 보조사료, 친환경 생물학적 제제 전문 제조기업입니다. "
        "국가 조달청 관납 전국 총판 및 충남·충북 지자체 방역 물품(로타갈 등) 공식 공급 실적을 바탕으로 완벽한 품질을 보증합니다."
    )
    add_figure(doc, IMG_FACTORY, "(주)삼원팜텍 충북 옥천 테크노밸리 본사 및 첨단 GMP/HACCP 제조 공장 전경", width=Inches(5.8))
    add_figure(doc, IMG_LAB, "삼원팜텍 수의 영양 연구소 / 사료 품질 관리 HPLC 크로마토그래피 정밀 분석실", width=Inches(5.8))

    # ================= CHAPTER 3 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 3 장. 핵심 경제성 및 투입 메트릭스 (Cost-Benefit Analysis)", level=1)
    
    add_styled_heading(doc, "3.1 사료 톤당 단 3,000원 최적 원가 구조 분석", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• 표준 제품 공급 단가: 6,000원 / kg\n"
        "• 사료 톤당 첨가제 투입 원가: 단 3,000원 / ton (500g 투입)\n"
        "• 서울우유 월간 총 투입비용: 5,400만원 (월 18,000톤 생산 기준, 총 소요량 9,000 kg)\n"
        "시중 일반 처방(톤당 6,000~9,000원) 대비 톤당 3,000원 이상의 제조 원가를 직접 절감하여 월 최대 1억원(연간 12억원)의 절감 효과를 창출합니다."
    )
    add_figure(doc, CHART_COST, "사료 톤당 첨가제 투입비용 비교 분석 차트 (삼원팜텍 단 3,000원 실현)", width=Inches(5.8))

    # ================= CHAPTER 4 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 4 장. 삼원팜텍 8대 핵심 낙농 솔루션 기술 상세", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "1. DDC 복합 향미제: 고온기 착유우 건물섭취량(DMI) 12% 즉각 회복\n"
        "2. VTR 고역가 복합효소: 반추위 섬유소 분해 및 사료 이용 효율 극대화\n"
        "3. Jienuo 코팅 GABA: 루멘 바이패스 코팅으로 하절기 열 스트레스 호르몬 38% 억제\n"
        "4. HZM 고활성 효모균: 반추위 혐기 환경 안정화 및 VFA 생성 18% 증가\n"
        "5. HZM 3종 복합생균제: 장내 유익균총 압도적 우점 형성\n"
        "6. 몬모릴로나이트 나노점토: 아플라톡신 98% 흡착 배출로 원유 M1 이행 차단\n"
        "7. VEESURE 천연 식물구충제: 기생충 및 콕시듐 억제, 무항생제 낙농 실현\n"
        "8. DNJ 천연 항바이러스: 호흡기 및 유방염 바이러스 증식 억제"
    )
    add_figure(doc, IMG_CAPSULE, "첨단 지질 마이크로 캡슐화 다중 코팅 활성 분자 3D 바이오 렌더링", width=Inches(5.6))

    # ================= CHAPTER 5 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 5 장. 한일사료 임가공 배합 라인 공정 적합성 매뉴얼", level=1)
    add_figure(doc, IMG_FEED_LINE, "한일사료 임가공 배합사료 공장 자동화 믹서 및 마이크로 인그리디언트 도징 시스템", width=Inches(5.8))
    add_figure(doc, IMG_PELLET, "바이오 코팅 골든 펠렛 정밀 토출 자동화 생산 라인", width=Inches(5.6))
    add_figure(doc, CHART_HOMOGENEITY, "한일사료 메인 믹서 500g 투입 혼화도 정규분포 곡선 (삼원팜텍 CV 3.8% 검증)", width=Inches(5.5))
    add_figure(doc, CHART_HEAT, "펠렛·익스팬더 85~110℃ 고온 스팀 가공 시 활성 잔존율 곡선 (95% 이상 생존)", width=Inches(5.5))

    # ================= CHAPTER 6 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 6 장. 낙농 기대 효과 및 실행 로드맵", level=1)
    add_figure(doc, IMG_DAIRY, "하절기 고온 스트레스 극복 및 착유우 산유량 일 +1.8kg 유지 첨단 낙농 목장", width=Inches(5.6))
    add_figure(doc, IMG_CALF, "홀스타인 어린 송아지 설사 80% 저감 및 반추위 조기 발달 스마트 우사", width=Inches(5.6))
    add_figure(doc, CHART_ROI, "서울우유 낙농 목장 핵심 생산성 개선 및 투자 대비 실익 환원(1:5.2) 인포그래픽", width=Inches(5.6))

    output_dir = r"C:\Users\master\vet_animal_hospital\s_project"
    output_path = os.path.join(output_dir, "S-NACF_고농축사료첨가제_공급제안서_삼원팜텍.docx")
    doc.save(output_path)
    print(f"Successfully saved enhanced Seoul Milk dairy docx to {output_path}")

if __name__ == "__main__":
    create_document()
