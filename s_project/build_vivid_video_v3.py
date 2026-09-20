import os
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\malgunbd.ttf"

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size)

ASSETS_DIR = r"C:\Users\master\vet_animal_hospital\s_project\assets"
BASE_DIR = r"C:\Users\master\vet_animal_hospital\s_project"
FRAMES_DIR = os.path.join(BASE_DIR, "frames_v3")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_v3")

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

# 21 Detailed Shots Configuration
SHOTS = [
    # --- SCENE 1 (Total ~31.3s) ---
    {
        "scene_id": 1, "shot_idx": 1, "dur": 10.0,
        "image": os.path.join(ASSETS_DIR, "grain_market_volatility_1789881820210.jpg"),
        "tag": "CRISIS ALERT | 원가 비상", "tag_col": (220, 38, 38),
        "headline": "대한민국 축산의 위기, 원료곡 급등과 열 스트레스",
        "stat_num": "+35%", "stat_label": "국제 곡물가 상승",
        "card_bullets": ["국제 옥수수·대두박 시세 급등으로 사료 원가 압박 심화", "하절기 폭염 일수 증가로 섭취량 급감 및 증체 정체", "소화기·호흡기 질병 상시화로 농가 수익 악화"],
        "subtitle": "최근 수입 곡물 가격의 급격한 변동과 이상기후에 따른 열 스트레스...",
        "dots": (1, 3)
    },
    {
        "scene_id": 1, "shot_idx": 2, "dur": 10.0,
        "image": os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg"),
        "tag": "PRODUCTION INFRA | 18,000톤 라인", "tag_col": (30, 58, 138),
        "headline": "S-NACF 한일사료 임가공 라인의 당면 과제",
        "stat_num": "18,000 M/T", "stat_label": "월간 임가공 배합 규모",
        "card_bullets": ["서울축산농협 한일사료 임가공 월 18,000톤 대규모 배합 설비", "사료 제조원가는 철저히 방어하면서 품질 혁신 달성 요구", "기존 다량 부형제 첨가제의 한계 극복 필수"],
        "subtitle": "서울축산농협의 한일사료 임가공 월 18,000톤 배합 라인!",
        "dots": (2, 3)
    },
    {
        "scene_id": 1, "shot_idx": 3, "dur": 11.3,
        "image": os.path.join(ASSETS_DIR, "bio_livestock_mascot_1789881785483.jpg"),
        "tag": "SOLUTION PARADIGM | 혁신 처방", "tag_col": (16, 185, 129),
        "headline": "원가 방어 + 생산성 극대화 = 삼원팜텍 고농축 솔루션",
        "stat_num": "500g", "stat_label": "톤당 초고농축 투입",
        "card_bullets": ["조합원 농가의 증체율과 면역력을 압도적으로 견인", "사료 톤당 단 3,000원! 월 최대 1억원 원가 절감", "(주)삼원팜텍 단독 책임하에 무결점 공급 약속"],
        "subtitle": "이제 사료 원가는 사수하고 농가 면역력을 끌어올릴 혁신 처방이 필요한 때입니다.",
        "dots": (3, 3)
    },

    # --- SCENE 2 (Total ~31.4s) ---
    {
        "scene_id": 2, "shot_idx": 1, "dur": 10.0,
        "image": os.path.join(ASSETS_DIR, "premix_product_packaging_1789881875376.jpg"),
        "tag": "500G INNOVATION | 부형제 탈피", "tag_col": (16, 185, 129),
        "headline": "더 이상 톤당 1~2kg 부형제를 사료에 섞지 마십시오",
        "stat_num": "500g/t", "stat_label": "초고농축 표준 규격",
        "card_bullets": ["시중 일반 첨가제: 80~90% 무의미한 부형제(밀기울) 투입", "사료 1톤 내 옥수수·대두박 주영양소 배합 공간 잠식", "삼원팜텍: 불필요한 부형제를 전면 배제한 고농축 혁신"],
        "subtitle": "기존 시중 첨가제는 부형제 함량이 높아 톤당 1kg에서 2kg을 투입해야 했고...",
        "dots": (1, 3)
    },
    {
        "scene_id": 2, "shot_idx": 2, "dur": 10.0,
        "image": os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg"),
        "tag": "MOLECULAR DENSITY | 유효 활성 집약", "tag_col": (5, 150, 105),
        "headline": "핵심 활성 분자만을 집약한 마이크로 프리믹스 기술",
        "stat_num": "100%", "stat_label": "주영양소 공간 보존",
        "card_bullets": ["글로벌 1등급 고순도 원료 엄선으로 유효 분자 밀도 400% 극대화", "단 500g 투입만으로 기존 1~2kg 제품 이상의 약리 효과 발휘", "배합 공간 1.0kg 이상 확보로 단백질/에너지 스펙 100% 보존"],
        "subtitle": "주식회사 삼원팜텍은 핵심 활성 성분만을 정밀 농축한 마이크로 프리믹스 기술로...",
        "dots": (2, 3)
    },
    {
        "scene_id": 2, "shot_idx": 3, "dur": 11.4,
        "image": os.path.join(ASSETS_DIR, "feed_pellet_extrusion.jpg"),
        "tag": "1:1 BATCH MATCH | 0.05% 정밀", "tag_col": (16, 185, 129),
        "headline": "사료 톤당 단 500g(0.05%) 투입으로 약리 효과 극대화",
        "stat_num": "1 : 1", "stat_label": "파우치 1포 = 사료 1톤",
        "card_bullets": ["500g 전용 고차단성 알루미늄 파우치 1포 = 사료 1톤 완벽 매칭", "현장 계량 및 투입 실수 원천 방지", "월간 보관 중량 18톤 -> 9톤으로 창고/물류비 50% 절감"],
        "subtitle": "사료 톤당 단 500g, 0.05% 투입만으로 동일 이상의 약리 효과를 완성했습니다.",
        "dots": (3, 3)
    },

    # --- SCENE 3 (Total ~30.6s) ---
    {
        "scene_id": 3, "shot_idx": 1, "dur": 9.8,
        "image": os.path.join(ASSETS_DIR, "chart_cost_comparison.png"),
        "tag": "COST BENEFIT | 압도적 경제성", "tag_col": (16, 185, 129),
        "headline": "사료 톤당 단 3,000원의 파격적인 원가 혁신",
        "stat_num": "3,000원", "stat_label": "사료 톤당 첨가 비용",
        "card_bullets": ["제품 공급 기준가 6,000원/kg 적용 (500g = 3,000원)", "시중 일반 처방(톤당 6,000~8,000원) 대비 50~60% 절감", "톤당 3,000원~5,000원의 즉각적인 원가 세이브 실현"],
        "subtitle": "가장 중요한 것은 바로 압도적인 경제성입니다. 사료 톤당 투입 비용은 단 3,000원!",
        "dots": (1, 3)
    },
    {
        "scene_id": 3, "shot_idx": 2, "dur": 9.8,
        "image": os.path.join(ASSETS_DIR, "chart_livestock_roi.png"),
        "tag": "MACRO ECONOMICS | 월 5,400만원", "tag_col": (5, 150, 105),
        "headline": "월 18,000톤 기준 월 5,400만원 최적 원가 구조 완성",
        "stat_num": "5,400만", "stat_label": "월간 총 공급비용",
        "card_bullets": ["월 18,000톤 배합사료 생산 시 총 공급량 9,000kg (9.0톤)", "시중 처방(월 1억 800만~1억 4,400만) 대비 월 최대 1억원 절감", "연간 12억원 이상의 막대한 사료 제조원가 절감 효과"],
        "subtitle": "월 18,000톤 기준 월 5,400만원 공급가로 기존 대비 월 최대 1억원 절감!",
        "dots": (2, 3)
    },
    {
        "scene_id": 3, "shot_idx": 3, "dur": 11.0,
        "image": os.path.join(ASSETS_DIR, "bio_livestock_mascot_1789881785483.jpg"),
        "tag": "SURPLUS & PROFIT | 조합원 환원", "tag_col": (16, 185, 129),
        "headline": "S-NACF 서울축협 경영 실익 및 조합원 환원 극대화",
        "stat_num": "12억원+", "stat_label": "연간 원가 방어 규모",
        "card_bullets": ["절감된 원가는 서울축협 사료 판매 가격 경쟁력으로 직결", "조합원 환원 사업 재원 확충 및 브랜드 만족도 1위 달성", "단 3,000원의 투자로 사료 품질과 농가 실익 동시 획득"],
        "subtitle": "서울축협의 수익 개선과 조합원 농가 실익 지원으로 직결됩니다.",
        "dots": (3, 3)
    },

    # --- SCENE 4 (Total ~28.4s) ---
    {
        "scene_id": 4, "shot_idx": 1, "dur": 9.0,
        "image": os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg"),
        "tag": "8 CORE SOLUTIONS | 섭취량 & 효소", "tag_col": (30, 58, 138),
        "headline": "01. DDC 복합 향미제 & 02. VTR 고역가 소화효소제",
        "stat_num": "+12%", "stat_label": "사료 섭취량(DMI) 증대",
        "card_bullets": ["DDC 향미·감미제: 고온기 식욕 부진 즉각 극복, 섭취량 12% 증대", "VTR 6종 복합효소제: 비전분 다당류(NSP) 분해, 곡물 전분 용출", "사료 요구율(FCR) 8.5% 개선 및 소화 흡수율 극대화"],
        "subtitle": "초기 섭취량을 끌어올리는 DDC 향미제와 VTR 내열성 소화 효소제...",
        "dots": (1, 3)
    },
    {
        "scene_id": 4, "shot_idx": 2, "dur": 9.0,
        "image": os.path.join(ASSETS_DIR, "dairy_cows_smart_farm_1789881841764.jpg"),
        "tag": "ANTI-HEAT STRESS | GABA & 생균", "tag_col": (16, 185, 129),
        "headline": "03. Jienuo 코팅 GABA & 04. HZM 효모균 & 05. 3종 생균제",
        "stat_num": "-38%", "stat_label": "스트레스 호르몬 감소",
        "card_bullets": ["Jienuo 바이패스 코팅 GABA: 하절기 열 스트레스 호르몬 38% 억제", "HZM 효모균(S. cerevisiae): 반추위 혐기 환경 조성, VFA +18%", "HZM 3종 포자생균제: 유산균+고초균+낙산균 장내 유익균 10배 증식"],
        "subtitle": "폭염 스트레스를 잠재우는 코팅 가바와 HZM 3종 포자 생균제...",
        "dots": (2, 3)
    },
    {
        "scene_id": 4, "shot_idx": 3, "dur": 10.4,
        "image": os.path.join(ASSETS_DIR, "livestock_nutrition_lab.jpg"),
        "tag": "BIO-SECURITY | 나노 흡착 & 항바이러스", "tag_col": (5, 150, 105),
        "headline": "06. 몬모릴로나이트 나노흡착 & 07. VEESURE & 08. DNJ",
        "stat_num": "98%", "stat_label": "아플라톡신 흡착 배출",
        "card_bullets": ["HZM 몬모릴로나이트 나노점토: 아플라톡신·제랄레논 98% 흡착 배출", "VEESURE 천연 식물구충제: 콕시듐 오오시스트 포자 78% 억제", "DNJ 상백피 알칼로이드: 바이러스 증식 억제 및 점막 면역 sIgA 촉진"],
        "subtitle": "나노 곰팡이독소 흡착제와 천연 항바이러스 DNJ까지 사료 품질을 완벽히 높여줍니다.",
        "dots": (3, 3)
    },

    # --- SCENE 5 (Total ~26.9s) ---
    {
        "scene_id": 5, "shot_idx": 1, "dur": 8.5,
        "image": os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg"),
        "tag": "MIXING TECH | 한일사료 최적화", "tag_col": (30, 58, 138),
        "headline": "한일사료 Twin-Shaft 믹서 라인 완벽 공정 일치",
        "stat_num": "90초", "stat_label": "초고속 균질 혼합",
        "card_bullets": ["한일사료 고속 Twin-Shaft 패들 믹서(1톤 배치)에 최적화", "500g 미량 투입에도 1톤 전체에 완벽 균질 분산되는 특수 담체", "마이크로 인그리디언트 자동 투입 빈 완벽 연동"],
        "subtitle": "한일사료 임가공 배합 라인 특성에 맞춰 소량 투입에도 균일 분산되는 특수 담체 적용!",
        "dots": (1, 3)
    },
    {
        "scene_id": 5, "shot_idx": 2, "dur": 8.5,
        "image": os.path.join(ASSETS_DIR, "chart_homogeneity_cv.png"),
        "tag": "HOMOGENEITY | CV < 5% 검증", "tag_col": (16, 185, 129),
        "headline": "초정밀 혼화도 검증: 변이계수(CV) 3.8% 달성",
        "stat_num": "CV 3.8%", "stat_label": "공인 기준(<5%) 통과",
        "card_bullets": ["믹서 내 10개 포인트 샘플링 정밀 분석 결과 CV 3.8% 달성", "배합사료 공정 품질 기준(CV < 5.0%) 완벽 초과 달성", "가축 개체별 첨가제 섭취 편차 원천 제거"],
        "subtitle": "사료 전체에 변이계수 5% 미만으로 균일하게 섞이는 특수 무기 담체 기술 적용!",
        "dots": (2, 3)
    },
    {
        "scene_id": 5, "shot_idx": 3, "dur": 9.9,
        "image": os.path.join(ASSETS_DIR, "chart_pellet_heat.png"),
        "tag": "HEAT STABILITY | 105℃ 펠렛열 극복", "tag_col": (5, 150, 105),
        "headline": "85~110℃ 펠렛 가공열 통과 후 활성 95% 생존",
        "stat_num": "95.2%", "stat_label": "가공열 통과 생존율",
        "card_bullets": ["스팀 컨디셔닝 및 다이스 압출 고열에도 유효 성분 95% 보존", "다중 지질 매트릭스 마이크로 캡슐화 코팅 기술 적용", "안식각 27.5° 자유 유동성 및 하절기 고결(Caking) 제로"],
        "subtitle": "85도에서 110도 스팀 펠렛 가공열에도 활성이 95% 이상 살아남는 공정 적합성 완료!",
        "dots": (3, 3)
    },

    # --- SCENE 6 (Total ~28.2s) ---
    {
        "scene_id": 6, "shot_idx": 1, "dur": 9.0,
        "image": os.path.join(ASSETS_DIR, "korean_cattle_beef_quality.jpg"),
        "tag": "HANWOO BEEF | 1++ 마블링", "tag_col": (217, 119, 6),
        "headline": "한우 비육우 1++등급 출현율 +14.5%p 향상",
        "stat_num": "+14.5%p", "stat_label": "1++ 등급 출현율",
        "card_bullets": ["비육우 초기 섭취량 10% 개선 및 일당증체량 +8.8% 달성", "육질 1++ 등급 출현율 28.3% -> 42.8%로 대폭 상승", "출하 두당 농가 순수익 약 42만원 추가 창출"],
        "subtitle": "실제 현장에서 입증된 놀라운 생산성! 한우 비육우의 1++등급 출현율 향상...",
        "dots": (1, 3)
    },
    {
        "scene_id": 6, "shot_idx": 2, "dur": 9.0,
        "image": os.path.join(ASSETS_DIR, "dairy_cows_smart_farm_1789881841764.jpg"),
        "tag": "DAIRY & SWINE | 산유량 & 설사 제로", "tag_col": (16, 185, 129),
        "headline": "젖소 산유량 +1.8kg & 이유자돈 설사 75% 급감",
        "stat_num": "+1.8kg", "stat_label": "젖소 일평균 산유량",
        "card_bullets": ["낙농: 폭염기 산유량 두당 일 +1.8kg 방어, 체세포수 42% 감소", "양돈: 이유자돈 설사율 18.5% -> 4.6%로 75% 급감", "출하 일령 5.2일 단축 및 사료 요구율(FCR) 0.1 개선"],
        "subtitle": "젖소의 하절기 산유량 유지 및 체세포수 급감, 양돈의 이유자돈 설사 제로화까지!",
        "dots": (2, 3)
    },
    {
        "scene_id": 6, "shot_idx": 3, "dur": 10.2,
        "image": os.path.join(ASSETS_DIR, "chart_livestock_roi.png"),
        "tag": "ROI RETURN | 투자수익 4.8배", "tag_col": (5, 150, 105),
        "headline": "첨가 비용 1원 투자 시 농가 수익 4.8원 회수",
        "stat_num": "1 : 4.8", "stat_label": "농가 경제적 ROI",
        "card_bullets": ["사료 톤당 단 3,000원 투자로 톤당 14,400원 경제 가치 회수", "항생제/구충제 치료비 절감 연간 300~500만원", "S-NACF 사료에 대한 조합원 농가의 두터운 신뢰 형성"],
        "subtitle": "조합원 농가의 핵심 지표들이 개선되며 서울축협 사료에 대한 두터운 신뢰를 만듭니다.",
        "dots": (3, 3)
    },

    # --- SCENE 7 (Total ~25.3s) ---
    {
        "scene_id": 7, "shot_idx": 1, "dur": 8.0,
        "image": os.path.join(ASSETS_DIR, "company_factory_panorama_1789881641339.jpg"),
        "tag": "PUBLIC TRUST | 조달청 관납", "tag_col": (30, 58, 138),
        "headline": "국가 조달청 관납 전국 총판의 검증된 공공 신뢰",
        "stat_num": "100%", "stat_label": "로트별 공인 COA",
        "card_bullets": ["국가 조달청(나라장터) 정식 등록 및 전국 지자체 관납 총판", "로타갈 생물학적 제제 무결점 공급 실적 보유", "충북 옥천 테크노밸리 첨단 GMP/HACCP 제조 공장 직납"],
        "subtitle": "국가 조달청 관납 전국 총판으로서 검증받은 엄격한 품질 관리 체계와...",
        "dots": (1, 3)
    },
    {
        "scene_id": 7, "shot_idx": 2, "dur": 8.0,
        "image": os.path.join(ASSETS_DIR, "livestock_nutrition_lab.jpg"),
        "tag": "RESPONSIBILITY | 단독 책임", "tag_col": (16, 185, 129),
        "headline": "단독 제조·판매원 (주)삼원팜텍의 책임 공급 체계",
        "stat_num": "18톤", "stat_label": "200% 비상 안전재고",
        "card_bullets": ["(주)삼원팜텍 (대표이사 김한호) 단독 품질·공급 책임", "옥천 물류센터에 월 사용량 200%(18 M/T) 상시 비축", "S-NACF 전담 수의·사료영양 기술지원팀 현장 상시 컨설팅"],
        "subtitle": "단독 제조·판매원으로서의 책임감! 새로운 성공 기준을 세워가겠습니다.",
        "dots": (2, 3)
    },
    {
        "scene_id": 7, "shot_idx": 3, "dur": 9.3,
        "image": os.path.join(ASSETS_DIR, "bio_livestock_mascot_1789881785483.jpg"),
        "tag": "PARTNERSHIP | 성공의 동반자", "tag_col": (5, 150, 105),
        "headline": "S-NACF 사료의 새로운 도약, 삼원팜텍이 함께합니다",
        "stat_num": "No.1", "stat_label": "대한민국 축산 파트너",
        "card_bullets": ["톤당 500g 처방 / 사료 톤당 단 3,000원의 원가 혁신", "월 5,400만원으로 연간 12억원 제조원가 방어", "신뢰와 확신의 파트너, 주식회사 삼원팜텍입니다!"],
        "subtitle": "신뢰와 확신의 파트너, 주식회사 삼원팜텍입니다.",
        "dots": (3, 3)
    }
]

def render_vivid_shot_frame(shot_data, out_png):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(10, 25, 47)) # Dark Navy
    draw = ImageDraw.Draw(img)

    # Top emerald line
    draw.rectangle([(0, 0), (width, 8)], fill=(16, 185, 129))

    # Top Brand Bar
    draw.text((70, 32), "주식회사 삼원팜텍  |  SAMWON PHARMTECH", font=get_font(21, bold=True), fill=(16, 185, 129))
    draw.text((1220, 34), "S-NACF 한일사료 임가공(월 18,000톤) 맞춤형 제안", font=get_font(18), fill=(148, 163, 184))
    draw.line([(70, 72), (width - 70, 72)], fill=(30, 58, 138), width=2)

    # Left Column (width ~ 960px)
    # Tag Pill
    tag_col = shot_data["tag_col"]
    draw.rounded_rectangle([(70, 95), (420, 138)], radius=12, fill=(15, 32, 67), outline=tag_col, width=2)
    draw.text((90, 104), f"★ {shot_data['tag']}", font=get_font(17, bold=True), fill=tag_col)

    # Headline
    hl = shot_data["headline"]
    draw.text((70, 155), hl, font=get_font(31, bold=True), fill=(255, 255, 255))

    # Left Main Card Box
    card_top = 230
    card_bottom = 810
    card_w = 950
    draw.rounded_rectangle([(70, card_top), (70 + card_w, card_bottom)], radius=16, fill=(15, 32, 67), outline=(30, 58, 138), width=2)

    # Hero KPI Stat Box inside Left Card (Top of Card)
    stat_box_w = card_w - 60
    draw.rounded_rectangle([(100, card_top + 25), (100 + stat_box_w, card_top + 145)], radius=12, fill=(10, 25, 47), outline=(16, 185, 129), width=2)
    
    # Hero Stat Number & Label
    draw.text((130, card_top + 40), shot_data["stat_num"], font=get_font(52, bold=True), fill=(16, 185, 129))
    draw.text((450, card_top + 55), "▶  " + shot_data["stat_label"], font=get_font(24, bold=True), fill=(241, 245, 249))
    draw.text((450, card_top + 95), "한일사료 18,000톤 라인 표준 특화 스펙", font=get_font(16), fill=(148, 163, 184))

    # Bullet Points
    bullets = shot_data["card_bullets"]
    b_start_y = card_top + 180
    for idx, b_text in enumerate(bullets):
        by = b_start_y + idx * 85
        # Marker
        draw.rounded_rectangle([(105, by + 6), (122, by + 23)], radius=4, fill=(16, 185, 129))
        if len(b_text) > 33:
            t1 = b_text[:33]
            t2 = b_text[33:]
            draw.text((140, by), t1, font=get_font(21, bold=True), fill=(241, 245, 249))
            draw.text((140, by + 28), t2, font=get_font(18), fill=(203, 213, 225))
        else:
            draw.text((140, by + 2), b_text, font=get_font(21, bold=True), fill=(241, 245, 249))

    # Right Column: Big Visual Spotlight (Photo / Chart / Mascot)
    img_x = 1060
    img_y = 95
    img_w = 790
    img_h = 715
    
    p_path = shot_data["image"]
    if os.path.exists(p_path):
        try:
            with Image.open(p_path) as p_img:
                p_resized = p_img.resize((img_w, img_h), Image.Resampling.LANCZOS)
                img.paste(p_resized, (img_x, img_y))
                # Frame
                draw.rectangle([(img_x, img_y), (img_x + img_w, img_y + img_h)], outline=(16, 185, 129), width=3)
        except Exception as e:
            print(f"Error loading image {p_path}: {e}")

    # Subtitle / Lower-Third Caption Banner
    sub_top = 840
    sub_h = 135
    draw.rounded_rectangle([(70, sub_top), (width - 70, sub_top + sub_h)], radius=14, fill=(15, 32, 67), outline=(16, 185, 129), width=2)
    
    # Subtitle Badge
    draw.rounded_rectangle([(95, sub_top + 15), (260, sub_top + 48)], radius=6, fill=(16, 185, 129))
    draw.text((115, sub_top + 20), "NARRATION", font=get_font(15, bold=True), fill=(10, 25, 47))

    # Dots Indicator on right of subtitle banner
    cur_dot, total_dots = shot_data["dots"]
    dots_text = f"Scene 0{shot_data['scene_id']}  " + "● " * cur_dot + "○ " * (total_dots - cur_dot)
    draw.text((width - 320, sub_top + 20), dots_text, font=get_font(18, bold=True), fill=(52, 211, 153))

    # Subtitle Spoken Text
    draw.text((95, sub_top + 62), shot_data["subtitle"], font=get_font(23, bold=True), fill=(255, 255, 255))

    # Bottom Footer
    draw.line([(70, 995), (width - 70, 995)], fill=(30, 58, 138), width=1)
    draw.text((70, 1015), "(주)삼원팜텍 대표이사 김한호  |  충북 옥천 테크노밸리 본사 및 공장  |  국가 조달청 관납 전국 총판", font=get_font(18), fill=(148, 163, 184))
    draw.text((1680, 1015), f"Scene 0{shot_data['scene_id']} / 07", font=get_font(20, bold=True), fill=(16, 185, 129))

    img.save(out_png, quality=95)
    print(f"Generated frame: {os.path.basename(out_png)}")

def build_shot_video(shot_png, out_mp4, duration_sec, zoom_in=True):
    # Apply subtle Ken Burns zoompan filter
    fps = 30
    total_frames = int(duration_sec * fps)
    
    # zoom from 1.0 to 1.06 smoothly
    zoom_expr = "min(zoom+0.0004,1.06)" if zoom_in else "max(1.06-0.0004*on,1.0)"
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", shot_png,
        "-t", str(duration_sec),
        "-vf", f"zoompan=z='{zoom_expr}':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    t0 = time.time()
    print("=== STARTING FULL VIVID VIDEO MASTER PRODUCTION ===")
    
    # Step 1: Render 21 Vivid Frames
    print("\n--- Step 1: Rendering 21 Dynamic 1080p Shot Frames ---")
    shot_clips = []
    for idx, shot in enumerate(SHOTS):
        frame_file = os.path.join(FRAMES_DIR, f"shot_{shot['scene_id']:02d}_{shot['shot_idx']:02d}.png")
        clip_file = os.path.join(CLIPS_DIR, f"shot_{shot['scene_id']:02d}_{shot['shot_idx']:02d}.mp4")
        
        render_vivid_shot_frame(shot, frame_file)
        
        # Build Ken Burns shot video
        zoom_in = (shot['shot_idx'] % 2 == 1)
        print(f"Rendering Ken Burns motion for Shot {shot['scene_id']}-{shot['shot_idx']} ({shot['dur']}s)...")
        build_shot_video(frame_file, clip_file, shot["dur"], zoom_in=zoom_in)
        shot_clips.append(clip_file)

    # Step 2: Concatenate all shot videos into visual master
    print("\n--- Step 2: Concatenating 21 Shots into Master Video Stream ---")
    concat_txt = os.path.join(BASE_DIR, "shots_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in shot_clips:
            clean_c = c.replace("\\", "/")
            f.write(f"file '{clean_c}'\n")

    video_only_mp4 = os.path.join(BASE_DIR, "master_visual_stream.mp4")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        video_only_mp4
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Master visual stream created: {video_only_mp4}")

    # Step 3: Build Unified Master Voice Track with padding
    print("\n--- Step 3: Assembling Unified Master Voice Track ---")
    audio_txt = os.path.join(BASE_DIR, "audio_concat.txt")
    # For each scene, create a padded scene audio
    scene_audios = []
    for i in range(1, 8):
        src_audio = os.path.join(BASE_DIR, "audio", f"scene_{i:02d}.mp3")
        padded_audio = os.path.join(CLIPS_DIR, f"scene_{i:02d}_padded.mp3")
        # Pad 1.2s at the end
        cmd_pad = [
            "ffmpeg", "-y",
            "-i", src_audio,
            "-filter_complex", "apad=pad_dur=1.2",
            "-c:a", "libmp3lame",
            padded_audio
        ]
        subprocess.run(cmd_pad, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scene_audios.append(padded_audio)

    with open(audio_txt, "w", encoding="utf-8") as f:
        for a in scene_audios:
            clean_a = a.replace("\\", "/")
            f.write(f"file '{clean_a}'\n")

    master_voice = os.path.join(BASE_DIR, "master_voice.mp3")
    cmd_audio_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", audio_txt,
        "-c", "copy",
        master_voice
    ]
    subprocess.run(cmd_audio_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Master voice track created: {master_voice}")

    # Step 4: Mix Master Voice with Inspiring BGM and Mux with Master Video
    print("\n--- Step 4: Mixing Master Voice with BGM and Final Video Mux ---")
    bgm_file = os.path.join(ASSETS_DIR, "bgm_inspired.mp3")
    final_output = os.path.join(BASE_DIR, "S-NACF_고농축사료첨가제_제안_홍보영상_삼원팜텍.mp4")

    # Get visual video duration
    probe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_only_mp4]
    v_dur = float(subprocess.check_output(probe_cmd).decode().strip())
    fade_out_start = max(1.0, v_dur - 4.0)

    # Complex filter:
    # 1. BGM volume=0.18, fade in 2s, fade out last 4s
    # 2. Voice volume=1.05
    # 3. amix duration=first (matches voice duration)
    cmd_final = [
        "ffmpeg", "-y",
        "-i", video_only_mp4,
        "-i", master_voice,
        "-i", bgm_file,
        "-filter_complex",
        f"[2:a]volume=0.18,afade=t=in:ss=0:d=2.5,afade=t=out:st={fade_out_start}:d=3.5[bgm];"
        f"[1:a]volume=1.05[voice];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output
    ]
    print("Running final master ffmpeg render...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Check stats
    cmd_stat = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', final_output]
    final_dur = float(subprocess.check_output(cmd_stat).decode().strip())
    mins = int(final_dur // 60)
    secs = int(final_dur % 60)
    size_mb = os.path.getsize(final_output) / (1024 * 1024)

    print("\n=======================================================")
    print("=== FINAL MASTER PROMO VIDEO COMPLETED SUCCESSFULLY ===")
    print(f"Path: {final_output}")
    print(f"Duration: {final_dur:.2f}s ({mins}분 {secs:02d}초)")
    print(f"File Size: {size_mb:.2f} MB")
    print(f"Total Elapsed Time: {time.time() - t0:.1f}s")
    print("=======================================================")

if __name__ == "__main__":
    main()
