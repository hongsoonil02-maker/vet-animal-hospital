import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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

def add_styled_heading(doc, text, level):
    p = doc.add_heading(level=level)
    run = p.add_run(text)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    
    if level == 1:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 32, 67) # Deep Navy #0F2043
    elif level == 2:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(5, 150, 105) # Bio Green #059669
    elif level == 3:
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85) # Slate #334155
    return p

def create_document():
    doc = Document()
    
    # Set standard margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("주식회사 삼원팜텍 | S-NACF 맞춤형 고농축 사료첨가제 기술제안서")
        hrun.font.name = 'Malgun Gothic'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(140, 150, 160)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SAMWON PHARMTECH CO., LTD.  |  CONFIDENTIAL")
        frun.font.name = 'Malgun Gothic'
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 150, 160)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Malgun Gothic'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(30, 41, 59) # #1E293B

    # ================= COVER / HEADER BANNER =================
    cover_box = doc.add_table(rows=1, cols=1)
    cover_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = cover_box.rows[0].cells[0]
    set_cell_background(c_cell, "0A192F") # Deep Navy
    set_cell_margins(c_cell, top=280, bottom=280, left=320, right=320)
    
    p = c_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = p.add_run("주식회사 삼원팜텍  |  SAMWON PHARMTECH\n")
    r0.font.name = 'Malgun Gothic'
    r0.font.size = Pt(11)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(16, 185, 129) # Bio Emerald
    
    r1 = p.add_run("[기술 공급 제안서]\n")
    r1.font.name = 'Malgun Gothic'
    r1.font.size = Pt(20)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(255, 255, 255)
    
    r2 = p.add_run("S-NACF 사료 품질 혁신 및 원가 최적화를 위한\n맞춤형 고농축 사료첨가제(Micro-Premix) 공급 제안\n")
    r2.font.name = 'Malgun Gothic'
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(226, 232, 240)
    
    r3 = p.add_run("한일사료 임가공 배합 라인(월 18,000 M/T) 전용 초정밀 500g/ton 처방 솔루션")
    r3.font.name = 'Malgun Gothic'
    r3.font.size = Pt(10)
    r3.font.color.rgb = RGBColor(148, 163, 184)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

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
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)
        set_cell_borders(c0, top="single", bottom="single", left="none", right="none", color="E2E8F0")
        set_cell_borders(c1, top="single", bottom="single", left="none", right="none", color="E2E8F0")
        
        p0 = c0.paragraphs[0]
        r = p0.add_run(label)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(51, 65, 85)
        
        p1 = c1.paragraphs[0]
        r = p1.add_run(val)
        r.font.size = Pt(9.5)
        if "삼원팜텍" in val:
            r.font.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Key Executive Highlight Callout Box
    hi_box = doc.add_table(rows=1, cols=1)
    hi_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cell = hi_box.rows[0].cells[0]
    set_cell_background(h_cell, "ECFDF5") # Mint bg
    set_cell_margins(h_cell, top=140, bottom=140, left=180, right=180)
    set_cell_borders(h_cell, top="none", bottom="none", left="single", right="none", color="10B981", sz="24")
    
    hp = h_cell.paragraphs[0]
    hrun1 = hp.add_run("★ [핵심 제안 요약 - 삼원팜텍 고농축 500g 표준 규격]\n")
    hrun1.font.bold = True
    hrun1.font.size = Pt(10.5)
    hrun1.font.color.rgb = RGBColor(6, 95, 70)
    
    hrun2 = hp.add_run(
        "1. 표준 투입량: 사료 톤당 단 500g (0.05%) 초고농축 마이크로 프리믹스 처방\n"
        "2. 제품 기준단가: 6,000원 / kg  (사료 톤당 투입 비용 단 3,000원)\n"
        "3. 월간 총 공급액: 5,400만원 (월 18,000톤 생산 기준, 총 공급량 9,000 kg)\n"
        "4. 공급 체계: (주)삼원팜텍 단독 제조 및 판매 / 한일사료 임가공 라인 무결점 직납 / 국가 조달청 관납 품질 보증"
    )
    hrun2.font.size = Pt(9.5)
    hrun2.font.color.rgb = RGBColor(6, 78, 59)

    doc.add_page_break()

    # ================= TABLE OF CONTENTS =================
    add_styled_heading(doc, "목 차", level=1)
    toc_items = [
        ("제 1 장. 제안 개요 및 배경 (Executive Summary)", [
            "1.1 제안 배경 및 축산 환경 분석",
            "1.2 S-NACF 맞춤형 고농축 공급 전략",
            "1.3 3자 협력(삼원팜텍-한일사료-S-NACF) 비즈니스 밸류체인"
        ]),
        ("제 2 장. 제안사 역량 및 신뢰도 (Company Credentials)", [
            "2.1 주식회사 삼원팜텍 개요 및 비전",
            "2.2 조달청 관납 전국 총판 실적 및 공공 품질 관리 체계",
            "2.3 고농축 마이크로 프리믹스 제조 인프라"
        ]),
        ("제 3 장. 핵심 경제성 및 투입 메트릭스 (Cost-Benefit Analysis)", [
            "3.1 표준 투입량 500g/ton (0.05%)의 공학적 의의",
            "3.2 사료 톤당 3,000원 최적 원가 구조 분석",
            "3.3 배합 공간(Nutrient Space) 확보에 따른 영양가 보존 이익",
            "3.4 물류·보관 및 재고 회전율 경제성 비교"
        ]),
        ("제 4 장. 삼원팜텍 8대 핵심 솔루션 기술 상세 (Product Specifications)", [
            "4.1 [제1군] 기호성 증진 복합 향미·감미제 (DDC 특화 라인)",
            "4.2 [제2군] 고활성 열안정성 소화 효소제 (VTR 글로벌 라인)",
            "4.3 [제3군] 항스트레스 장관 바이패스 코팅 GABA (Jienuo 마이크로 캡슐)",
            "4.4 [제4군] 고농도 활성 효모균 및 세포벽 면역제 (HZM 효모 복합체)",
            "4.5 [제5군] 장내 정착 고농도 3종 복합 생균제 (HZM 포자 고초균 및 유산균)",
            "4.6 [제6군] 광범위 나노 층상 진균독소 흡착제 (HZM 몬모릴로나이트)",
            "4.7 [제7군] 식물 유래 천연구충제 및 천연 콕시듐 방어제 (VEESURE 솔루션)",
            "4.8 [제8군] 천연 유래 광범위 항바이러스 솔루션 (1-Deoxynojirimycin, DNJ)"
        ]),
        ("제 5 장. 한일사료 임가공 배합 라인 공정 적합성 매뉴얼 (Process QA/QC)", [
            "5.1 500g/ton 초정밀 마이크로 도징(Micro-Dosing) 혼화도(CV < 5%) 검증",
            "5.2 펠렛(Pellet)·익스팬더 고온 가공열 안정성 프로토콜",
            "5.3 자동화 빈(Bin) 투입을 위한 고결 방지(Anti-Caking) 제형 설계"
        ]),
        ("제 6 장. 기대 효과 및 실행 로드맵 (Roadmap & Technical Support)", [
            "6.1 낙농 착유우 및 육성우 생산성 지표 및 경제성 개선 실증",
            "6.2 시험 배합에서 월 18,000톤 전 라인 공급까지의 단계별 일정",
            "6.3 삼원팜텍 품질 보증 및 현장 밀착형 테크니컬 서비스"
        ])
    ]
    
    for chap_title, subs in toc_items:
        cp = doc.add_paragraph()
        crun = cp.add_run(chap_title)
        crun.font.bold = True
        crun.font.size = Pt(10.5)
        crun.font.color.rgb = RGBColor(15, 32, 67)
        cp.paragraph_format.space_before = Pt(4)
        cp.paragraph_format.space_after = Pt(2)
        
        for sub in subs:
            sp = doc.add_paragraph()
            srun = sp.add_run("   • " + sub)
            srun.font.size = Pt(9.5)
            srun.font.color.rgb = RGBColor(71, 85, 105)
            sp.paragraph_format.space_before = Pt(0)
            sp.paragraph_format.space_after = Pt(1)

    doc.add_page_break()

    # ================= CHAPTER 1 =================
    add_styled_heading(doc, "제 1 장. 제안 개요 및 배경 (Executive Summary)", level=1)
    
    add_styled_heading(doc, "1.1 제안 배경 및 축산 환경 분석", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "최근 국내 배합사료 산업 및 축산 농가는 수입 곡물 가격의 높은 변동성, 기후변화에 따른 하절기 극한 열 스트레스, "
        "각종 바이러스 및 소화기 질병의 연중 상시화, 그리고 정부의 항생제 사용 규제 강화 등 복합적인 생산성 저하 위기에 직면해 있습니다.\n\n"
        "이러한 환경에서 서울우유는 한일사료에서 임가공 생산하는 월 18,000톤의 낙농 배합사료 라인에 대해, "
        "사료 제조 원가를 엄격히 방어하면서도 조합원 농가의 증체율, 사료요구율(FCR), 질병 저항력을 획기적으로 향상시킬 수 있는 "
        "차세대 맞춤형 고농축 사료첨가제 도입이 절실한 시점입니다."
    )

    add_styled_heading(doc, "1.2 S-NACF 맞춤형 고농축(High-Concentration) 공급 전략", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "기존 시중의 보조사료 및 첨가제는 저순도 원료와 과도한 부형제로 인해 톤당 1.0kg ~ 2.0kg(0.1~0.2%) 이상을 투입해야 하므로, "
        "투입 비용이 톤당 6,000원~10,000원에 달하고 주원료(옥수수, 대두박 등)의 배합 공간(Nutrient Space)을 잠식하는 한계가 있었습니다.\n\n"
        "이에 주식회사 삼원팜텍은 핵심 유효 활성물질만을 고밀도로 집약한 '초고농축 마이크로 프리믹스(Micro-Premix)' 기술을 적용하여, "
        "사료 톤당 단 500g(0.05%) 투입만으로 동일 이상의 약리 기전과 생산성 개선 효과를 완벽히 구현하는 파격적인 경제형 처방을 제안합니다."
    )

    add_styled_heading(doc, "1.3 3자 협력(삼원팜텍 - 한일사료 - S-NACF) 비즈니스 밸류체인", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "본 사업은 (주)삼원팜텍이 단독 제조·판매원으로서 완제품의 법적·기술적 책임을 전담하며, "
        "한일사료 배합공장과의 공정 연계를 통해 무결점 납품을 진행합니다. "
        "배후의 글로벌 선진 기술력과 풍부한 원료 파트너십을 완벽히 흡수하여 S-NACF 조합원에게 최적의 품질을 공급하는 강력한 3자 밸류체인을 구축합니다."
    )

    # ================= CHAPTER 2 =================
    add_styled_heading(doc, "제 2 장. 제안사 역량 및 신뢰도 (Company Credentials)", level=1)
    
    add_styled_heading(doc, "2.1 주식회사 삼원팜텍 개요 및 경영 비전", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "충청북도 옥천테크노밸리에 본사와 최첨단 제조공장을 보유한 (주)삼원팜텍(대표이사 김한호)은 "
        "동물용의약외품, 보조사료, 친환경 생물학적 제제 전문 제조기업입니다. "
        "지속적인 R&D 투자와 엄격한 GMP 기준의 품질 관리 체계를 바탕으로 축산 농가와 사료업계의 현안 과제를 해결해 왔습니다."
    )

    add_styled_heading(doc, "2.2 조달청 관납 전국 총판 실적 및 공공 품질 관리 체계", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "삼원팜텍은 생물학적 제제인 '로타갈(RotaGal)' 등을 비롯한 엄격한 방역 물품에 대해 "
        "조달청 관납 전국 총판 및 충남·충북 권역 공급을 성공적으로 수행하고 있습니다.\n\n"
        "국가 조달청 관납은 제품의 유효 성분 함량, 보존제 규격, 안정성, 콜드체인 및 적기 납품에 대해 가장 까다로운 검증을 요구합니다. "
        "삼원팜텍이 보유한 공공 조달 무결점 납품 이력은 S-NACF 월 18,000톤 대규모 배합 라인에 투입되는 첨가제의 균일성과 품질 신뢰도를 보증하는 결정적 지표입니다."
    )

    add_styled_heading(doc, "2.3 고농축 마이크로 프리믹스 제조 인프라", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "삼원팜텍 옥천 공장은 마이크로 단위 원료를 정밀 혼합할 수 있는 특수 리본 믹서 및 패들 믹서 시스템, "
        "정전기 방지 및 방습 포장 라인을 완비하고 있습니다. 로트(Lot)별 정밀 분석 성적서(COA)를 매 배치마다 발행하여 "
        "한일사료 공장에 입고되는 모든 원료의 표준화를 완벽하게 보장합니다."
    )

    # ================= CHAPTER 3 =================
    add_styled_heading(doc, "제 3 장. 핵심 경제성 및 투입 메트릭스 (Cost-Benefit Analysis)", level=1)
    
    add_styled_heading(doc, "3.1 표준 투입량 500g/ton (0.05%)의 공학적 의의", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "배합사료 1톤(1,000kg) 기준 500g의 투입량은 전체 중량 대비 0.05%에 해당합니다. "
        "이는 일반 첨가제(1.0~2.0kg) 대비 50~75% 적은 투입량이면서도, 고순도 활성 나노 원료 처방을 통해 약리 활성을 200~300% 이상 끌어올린 공학적 최적 처방입니다."
    )

    add_styled_heading(doc, "3.2 사료 톤당 3,000원 최적 원가 구조 분석", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• 표준 제품 공급 단가: 6,000원 / kg\n"
        "• 사료 톤당 첨가제 투입 원가: 단 3,000원 / ton (500g 투입)\n"
        "• S-NACF 월 18,000톤 생산 시 월간 총 투입비용: 5,400만원 (총 소요량 9,000 kg)\n"
        "기존 시중 처방(톤당 5,000~9,000원) 대비 톤당 2,000~6,000원의 사료 제조 원가를 직접 절감할 수 있어, "
        "월간 최소 3,600만원에서 최대 1억 800만원(연간 4.3억~13억원)의 직접 원가 개선 효과가 발생합니다."
    )

    # Economic Comparison Table
    add_styled_heading(doc, "3.3 경제성 및 운영 지표 비교 분석표", level=2)
    
    econ_table = doc.add_table(rows=7, cols=4)
    econ_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["비교 항목", "시중 일반 첨가제 처방", "삼원팜텍 고농축 프리믹스", "S-NACF 개선 효과"]
    for i, h in enumerate(headers):
        cell = econ_table.rows[0].cells[i]
        set_cell_background(cell, "0F2043")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    data = [
        ("사료 톤당 투입량", "1,000g ~ 2,000g / ton", "500g / ton (0.05%)", "투입량 50~75% 획기적 절감"),
        ("제품 공급 단가(kg)", "3,500원 ~ 4,500원 / kg", "6,000원 / kg", "초고순도 활성 원료 적용"),
        ("사료 톤당 투입 비용", "4,500원 ~ 9,000원 / ton", "단 3,000원 / ton", "톤당 1,500원~6,000원 원가 절감"),
        ("월간 총 비용(18,000톤)", "8,100만원 ~ 1억 6,200만원", "5,400만원", "월 최대 1억 800만원 절감"),
        ("배합 공간(Nutrient Space)", "부형제 1~2kg 영양 잠식", "유효 성분 위주 영양 보존", "조단백/에너지 스펙 100% 사수"),
        ("물류·보관 및 핸들링", "월 18톤~36톤 창고 적재", "월 9톤 초경량 보관", "물류비 및 창고 점유율 50%↓")
    ]
    
    for row_idx, row_data in enumerate(data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = econ_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(5, 150, 105) # Green highlight
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138) # Blue highlight
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "3.4 배합 공간(Nutrient Space) 확보 및 영양가 보존 이익", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "사료 배합 프로그램(Least-Cost Formulation)에서 첨가제가 1.5kg 이상 차지할 경우, "
        "사료의 조단백질(CP), 총가소화영양소(TDN), 가용대에너지(ME)를 충당하기 위해 값비싼 농축 대두박이나 유지(Oil)를 추가 투입해야 합니다. "
        "삼원팜텍의 500g 처방은 1.0kg 이상의 고귀한 배합 스페이스를 곡류 및 단백질 원료에 돌려줌으로써, "
        "보이지 않는 배합비 절감 효과를 톤당 최소 1,500원 이상 추가 창출합니다."
    )

    # ================= CHAPTER 4 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 4 장. 삼원팜텍 8대 핵심 솔루션 기술 상세 (Product Specifications)", level=1)
    
    solutions = [
        ("4.1 [제1군] 기호성 증진 복합 향미·감미제 솔루션 (DDC 특화 라인)",
         "글로벌 향미 전문 DDC社 열안정성 농축 밀크바닐라향, 천연 당밀향, 산딸기향, SX907 복합 감미제(순도 99% 이상)",
         "가축의 후각 및 미각 수용체를 직접 자극하여 타액과 위액 분비를 유도. 원료 곡물 변동에 따른 섭취 거부감을 완벽히 차단.",
         "500g/ton 처방으로 초기 섭취량(ADFI/DMI) 8~15% 개선, 송아지 조기 이유 스트레스 및 착유우 혹서기 섭취 정체 해소."),
        
        ("4.2 [제2군] 고활성 열안정성 소화 효소제 솔루션 (VTR 글로벌 라인)",
         "글로벌 효소 전문 VTR社 내열성 마이크로 코팅 β-Mannanase, Xylanase, 복합 프로테아제·아밀라아제",
         "곡류 내 비전분다당류(NSP)와 세포벽 결합 단백질을 선택 분해하여 장내 점도를 낮추고 사료 내 유효 대사에너지(ME) 용출 극대화.",
         "85~90℃ 펠렛 증기압 통과율 95% 이상. 사료 톤당 ME 50~70 kcal/kg 개선, 분변 배출량 10% 감소."),
        
        ("4.3 [제3군] 항스트레스 장관 바이패스 코팅 GABA (Jienuo 마이크로 캡슐)",
         "Jienuo 특수 지질 마이크로 캡슐 코팅 Gamma-Aminobutyric Acid (GABA, 순도 50% 이상)",
         "중추신경계의 억제성 신경전달물질로 작용하여 부신피질자극호르몬 분비를 조절하고 혈중 코르티솔 수치 억제.",
         "하절기 고온 스트레스 호흡수 안정, 환절기 폐렴 및 수송/군편성 스트레스 억제, 사료 섭취량 감소율 제로화."),
        
        ("4.4 [제4군] 고농도 활성 효모균 및 세포벽 면역제 (HZM 효모 복합체)",
         "HZM 고농도 Saccharomyces cerevisiae 및 세포벽 유래 MOS (Mannan-oligosaccharide), β-Glucan 복합체",
         "반추위 및 맹장 내 용존산소를 소모하여 절대혐기성 미생물 환경 조성. 병원성 대장균·살모넬라의 섬모에 흡착하여 체외 배출.",
         "반추위 섬유소 분해율 증대 및 장내 융모 높이 신장, 면역글로불린(IgA, IgG) 분비 촉진."),
        
        ("4.5 [제5군] 장내 정착 고농도 3종 복합 생균제 (HZM 솔루션)",
         "HZM 엄선 Bacillus subtilis, Bacillus licheniformis (내생포자 형성균 2종) + Lactobacillus plantarum",
         "열과 위산에 내성을 가진 포자 형태로 장관 하부까지 100% 도달하여 발아. 젖산 및 박테리오신(Bacteriocin)을 분비하여 유해균 증식 억제.",
         "송아지 및 육성우 설사 발생률 80% 이상 억제, 우사 내 암모니아 가스 및 축산 악취 획기적 저감."),
        
        ("4.6 [제6군] 광범위 나노 층상 진균독소 흡착제 (HZM 몬모릴로나이트)",
         "HZM 고순도 나노 층상구조 몬모릴로나이트 (Montmorillonite, 고순도 정제 벤토나이트계)",
         "극성화된 층상 구조와 강력한 양이온교환용량(CEC)으로 아플라톡신, 제랄레논, 오크라톡신 분자를 물리화학적으로 영구 포집.",
         "원유 내 아플라톡신 M1 이행을 원천 차단하고 필수 영양소 손실 없이 곰팡이독소만을 선택 배출."),
        
        ("4.7 [제7군] 식물 유래 천연구충제 및 천연 콕시듐 방어제 (VEESURE 솔루션)",
         "인도 VEESURE社 글로벌 표준화 파이토케미컬(Phytochemical) 복합 추출물",
         "원충 세포벽 구성 지질층을 용해하고 난포낭(Oocyst)의 포자 형성을 억제하며, 장내 기생충의 대사 경로를 교란.",
         "항생제 내성 및 휴약 기간 걱정 없는 무항생제 천연 방어선 구축, 송아지 콕시듐성 혈변 및 장염 완벽 방어."),
        
        ("4.8 [제8군] 천연 유래 광범위 항바이러스 솔루션 (1-Deoxynojirimycin, DNJ)",
         "천연 상엽(뽕나무 잎) 추출 고순도 1-Deoxynojirimycin (DNJ)",
         "바이러스 외피 당단백질(Glycoprotein) 합성에 관여하는 알파-글루코시다아제 효소를 특이적으로 저해하여 바이러스 세포 침투 및 증식 차단.",
         "로타바이러스, 코로나바이러스 등 송아지 소화기·호흡기 바이러스 질환 선제적 예방.")
    ]
    
    for title, raw_mat, mech, effect in solutions:
        add_styled_heading(doc, title, level=2)
        p = doc.add_paragraph()
        r1 = p.add_run("• 원료 및 성분 규격: ")
        r1.font.bold = True
        p.add_run(raw_mat + "\n")
        
        r2 = p.add_run("• 작용 약리 기전: ")
        r2.font.bold = True
        p.add_run(mech + "\n")
        
        r3 = p.add_run("• 투입 및 검증 효과: ")
        r3.font.bold = True
        r3_text = p.add_run(effect)
        r3_text.font.color.rgb = RGBColor(5, 150, 105)
        p.paragraph_format.space_after = Pt(6)

    # ================= CHAPTER 5 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 5 장. 한일사료 임가공 배합 라인 공정 적합성 매뉴얼 (Process QA/QC)", level=1)
    
    add_styled_heading(doc, "5.1 500g/ton 초정밀 마이크로 도징(Micro-Dosing) 혼화도(CV < 5%) 검증", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "한일사료 공장의 마이크로 인그리디언트(Micro-Ingredient) 투입 시스템과 메인 믹서(Twin-Shaft Paddle Mixer)에서 "
        "500g의 극미량이 1톤 사료 전체에 완벽히 균질 분포되도록, 삼원팜텍은 특수 유동성 무기 담체(Carrier)를 설계하였습니다.\n\n"
        "• 혼화도(Coefficient of Variation, CV) 보증: 공인 검사 기준 CV 5.0% 미만 (산업 표준 10% 대비 2배 정밀)\n"
        "• 입도 분포: 80~100 mesh(150~180㎛) 정밀 입도 매칭을 통해 혼합 시 편석(Segregation) 현상 원천 차단."
    )

    add_styled_heading(doc, "5.2 펠렛(Pellet)·익스팬더 고온 가공열 안정성 프로토콜", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "배합사료 가공 공정의 스팀 컨디셔닝 및 펠렛 다이(Die) 통과 시 온도는 85℃~105℃, 순간 압력은 수 기압에 달합니다. "
        "삼원팜텍의 효소제 및 생균제는 독자적인 지질-다당류 다중 마이크로 캡슐화 코팅 기술을 적용하여 "
        "펠렛 가공 후에도 유효 활성 잔존율 92~96% 이상을 유지합니다."
    )

    add_styled_heading(doc, "5.3 자동화 빈(Bin) 투입을 위한 고결 방지(Anti-Caking) 제형 설계", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "하절기 고온다습한 환경에서도 한일사료 공장의 투입 호퍼와 저장 사일로 내에서 뭉침이나 브릿지(Bridging) 현상이 발생하지 않도록, "
        "소수성 나노 실리카 표면 처리 기술을 적용하여 우수한 자유유동성(Free-flowing)을 확보하였습니다."
    )

    # ================= CHAPTER 6 =================
    doc.add_page_break()
    add_styled_heading(doc, "제 6 장. 기대 효과 및 실행 로드맵 (Roadmap & Technical Support)", level=1)
    
    add_styled_heading(doc, "6.1 축종별 생산성 및 FCR 개선 목표치", level=2)
    
    result_table = doc.add_table(rows=5, cols=3)
    result_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    r_headers = ["적용 축종", "핵심 기대 효과", "정량적 목표 지표"]
    for i, h in enumerate(r_headers):
        cell = result_table.rows[0].cells[i]
        set_cell_background(cell, "059669") # Green
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    r_data = [
        ("낙농 착유우 (고능력우)", "하절기 고온 스트레스 방어, 건물섭취량(DMI) 유지, 비유곡선 유지", "일 산유량 +1.8kg 방어, 비유 피크 3~4주 연장"),
        ("원유 유질 (체세포수)", "유선 세포 면역 강화, 유방염 예방, 아플라톡신 M1 이행 차단", "체세포수 42% 감소(18.5만/ml 1등급 달성), 폐유 손실 70% 감소"),
        ("송아지 및 육성우", "초기 섭취량 유도, 반추위 융모 조기 발달, 면역 장벽 구축", "송아지 설사 발생 80% 저감, 초산일령 1.5개월 조기 단축"),
        ("목장 경제성 (ROI)", "사료 톤당 단 3,000원 투자 대비 산유량 증대 및 질병 손실 방어", "투입비용 대비 5.2배 회수 (ROI 1 : 5.2 달성)")
    ]
    for row_idx, row_data in enumerate(r_data, start=1):
        bg = "F0FDF4" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            cell = result_table.rows[row_idx].cells[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(6, 95, 70)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_styled_heading(doc, "6.2 3단계 단계별 도입 로드맵", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Phase 1 (1개월차 / 사전 검증): 한일사료 배합공장 현장 설비 점검, 배치별 혼화도(CV) 및 내열성 Lab Test 완료.\n"
        "• Phase 2 (2개월차 / 파일럿 실증): S-NACF 핵심 시범 농가 사료 1,000톤 시험 생산 및 현장 섭취·소화율 모니터링.\n"
        "• Phase 3 (3개월차 이후 / 전면 공급): 월 18,000톤 전 라인 정규 납품 개시 및 삼원팜텍 정기 테크니컬 리포트 제공."
    )

    add_styled_heading(doc, "6.3 삼원팜텍 품질 보증 및 현장 밀착형 테크니컬 서비스", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "주식회사 삼원팜텍은 납품에 그치지 않고 사료 품질의 완성도를 위해 전담 수의·사료영양 기술지원팀을 운영합니다.\n"
        "1. 매 납품 로트(Lot)별 국가 공인 성적서(COA) 동봉 납품\n"
        "2. S-NACF 조합원 농가 현장 방문 및 사료 섭취·소화율 컨설팅 무상 지원\n"
        "3. 분기별 가축 혈청 검사 및 분변 미생물 총 분석 데이터 피드백 제공"
    )

    # ================= SIGNATURE & COMPANY INFO =================
    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    
    sign_box = doc.add_table(rows=1, cols=1)
    sign_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_cell = sign_box.rows[0].cells[0]
    set_cell_background(s_cell, "F8FAFC")
    set_cell_margins(s_cell, top=200, bottom=200, left=250, right=250)
    set_cell_borders(s_cell, top="single", bottom="single", left="single", right="single", color="CBD5E1", sz="12")
    
    sp = s_cell.paragraphs[0]
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    s1 = sp.add_run("본 제안서에 명시된 모든 기술 사양, 품질 기준, 공급 조건은\n주식회사 삼원팜텍의 엄격한 공공 조달 품질 관리 시스템 하에 성실히 이행될 것임을 확약합니다.\n\n")
    s1.font.size = Pt(10)
    s1.font.color.rgb = RGBColor(51, 65, 85)
    
    s2 = sp.add_run("2026년 9월\n\n")
    s2.font.size = Pt(11)
    s2.font.bold = True
    s2.font.color.rgb = RGBColor(15, 23, 42)
    
    s3 = sp.add_run("제조 및 판매원 : 주식회사 삼원팜텍\n")
    s3.font.size = Pt(14)
    s3.font.bold = True
    s3.font.color.rgb = RGBColor(15, 32, 67)
    
    s4 = sp.add_run("대  표  이  사   김   한   호   (직인생략)\n\n")
    s4.font.size = Pt(12)
    s4.font.bold = True
    s4.font.color.rgb = RGBColor(15, 23, 42)
    
    s5 = sp.add_run("본사 및 사업장: 충청북도 옥천군 옥천읍 테크노밸리길  |  고객센터: 043-XXX-XXXX")
    s5.font.size = Pt(8.5)
    s5.font.color.rgb = RGBColor(100, 116, 139)

    output_dir = r"C:\Users\master\vet_animal_hospital\s_project"
    output_path = os.path.join(output_dir, "S-NACF_고농축사료첨가제_공급제안서_삼원팜텍.docx")
    doc.save(output_path)
    print(f"Successfully saved to {output_path}")

if __name__ == "__main__":
    create_document()
