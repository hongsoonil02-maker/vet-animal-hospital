import os
from PIL import Image, ImageDraw, ImageFont
import math

FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\malgunbd.ttf"

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size)

out_dir = r"C:\Users\master\vet_animal_hospital\s_project\assets"
os.makedirs(out_dir, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Cost Comparison Bar Chart (1200 x 700)
# ----------------------------------------------------------------------
def make_cost_comparison_chart():
    img = Image.new("RGB", (1200, 700), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((60, 40), "사료 톤(ton)당 첨가제 투입 비용 비교 분석", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((60, 80), "시중 일반 처방(1~2kg 투입) vs 삼원팜텍 초고농축 마이크로 프리믹스(500g 투입)", font=get_font(18), fill=(148, 163, 184))
    
    # Chart Area
    x0, y0, x1, y1 = 120, 160, 1100, 560
    draw.rectangle([(x0, y0), (x1, y1)], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    
    # Grid lines
    for val in [2000, 4000, 6000, 8000, 10000]:
        y = y1 - int((val / 10000) * (y1 - y0))
        draw.line([(x0, y), (x1, y)], fill=(51, 65, 85), width=1)
        draw.text((40, y - 10), f"{val:,}원", font=get_font(14), fill=(148, 163, 184))
        
    bars = [
        ("시중 처방 A (1.0kg)", 4500, (148, 163, 184), "4,500원"),
        ("시중 처방 B (1.5kg)", 6750, (100, 116, 139), "6,750원"),
        ("시중 처방 C (2.0kg)", 9000, (71, 85, 105), "9,000원"),
        ("삼원팜텍 (500g)", 3000, (16, 185, 129), "단 3,000원 (50~67% 절감!)")
    ]
    
    bw = 140
    gap = 80
    start_x = x0 + 80
    
    for i, (name, val, col, label) in enumerate(bars):
        bx = start_x + i * (bw + gap)
        bh = int((val / 10000) * (y1 - y0))
        by = y1 - bh
        
        # Draw bar
        draw.rounded_rectangle([(bx, by), (bx + bw, y1)], radius=8, fill=col)
        
        # Value on top
        is_highlight = "삼원팜텍" in name
        v_font = get_font(18 if is_highlight else 16, bold=True)
        v_col = (52, 211, 153) if is_highlight else (255, 255, 255)
        
        # Text above bar
        draw.text((bx - 20 if is_highlight else bx + 20, by - 35), label, font=v_font, fill=v_col)
        
        # Label below bar
        draw.text((bx - 10, y1 + 20), name, font=get_font(15, bold=is_highlight), fill=(255, 255, 255) if is_highlight else (203, 213, 225))

    # Bottom summary badge
    draw.rounded_rectangle([(120, 600), (1100, 660)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((150, 618), "★ S-NACF 월 18,000톤 기준: 월 최대 1억 800만원 절감 / 연간 13억원 원가 개선 확약", font=get_font(18, bold=True), fill=(255, 255, 255))
    
    out_path = os.path.join(out_dir, "chart_cost_comparison.png")
    img.save(out_path)
    print(f"Saved: {out_path}")

# ----------------------------------------------------------------------
# 2. Homogeneity CV < 5% Bell Curve (1200 x 700)
# ----------------------------------------------------------------------
def make_homogeneity_chart():
    img = Image.new("RGB", (1200, 700), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    draw.text((60, 40), "한일사료 메인 믹서 500g 초정밀 혼화도 검증 (CV < 5%)", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((60, 80), "사료 1톤 배합 시 마이크로 담체 분산 특성에 따른 농도 분포 비교", font=get_font(18), fill=(148, 163, 184))
    
    x0, y0, x1, y1 = 120, 160, 1100, 560
    draw.rectangle([(x0, y0), (x1, y1)], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    
    # Draw industry curve (broad)
    pts_ind = []
    pts_sam = []
    for px in range(x0, x1 + 1):
        x_val = 350 + (px - x0) / (x1 - x0) * 300 # 350g to 650g
        # Ind: mean 500, sd 50
        y_ind = math.exp(-0.5 * ((x_val - 500) / 50)**2)
        py_ind = y1 - int(y_ind * 220)
        pts_ind.append((px, py_ind))
        
        # Samwon: mean 500, sd 18
        y_sam = math.exp(-0.5 * ((x_val - 500) / 18)**2)
        py_sam = y1 - int(y_sam * 340)
        pts_sam.append((px, py_sam))
        
    draw.line(pts_ind, fill=(148, 163, 184), width=3)
    draw.line(pts_sam, fill=(16, 185, 129), width=5)
    
    # Center vertical target line
    cx = x0 + int((500 - 350) / 300 * (x1 - x0))
    draw.line([(cx, y0), (cx, y1)], fill=(245, 158, 11), width=2)
    draw.text((cx - 40, y1 + 15), "목표 500g/ton", font=get_font(15, bold=True), fill=(245, 158, 11))
    
    # Callout boxes
    draw.rounded_rectangle([(cx + 40, y0 + 40), (cx + 360, y0 + 120)], radius=8, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((cx + 55, y0 + 55), "삼원팜텍 초정밀 분산 (CV 3.8%)", font=get_font(16, bold=True), fill=(52, 211, 153))
    draw.text((cx + 55, y0 + 85), "• 1톤 내 전 지점 99% 균일 약효 보증", font=get_font(14), fill=(241, 245, 249))

    draw.rounded_rectangle([(cx + 120, y0 + 180), (cx + 430, y0 + 260)], radius=8, fill=(51, 65, 85), outline=(100, 116, 139), width=1)
    draw.text((cx + 135, y0 + 195), "일반 사료공장 기준 (CV 10.0%)", font=get_font(15, bold=True), fill=(203, 213, 225))
    draw.text((cx + 135, y0 + 225), "• 지점별 첨가제 농도 편차 심화", font=get_font(14), fill=(148, 163, 184))

    # Bottom footer
    draw.rounded_rectangle([(120, 600), (1100, 660)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((150, 618), "★ 특수 유동성 무기 담체(Carrier) 매칭 기술: 믹서 투입 후 45초 이내 완전 혼합", font=get_font(18, bold=True), fill=(255, 255, 255))

    out_path = os.path.join(out_dir, "chart_homogeneity_cv.png")
    img.save(out_path)
    print(f"Saved: {out_path}")

# ----------------------------------------------------------------------
# 3. Pellet Heat Stability Chart (1200 x 700)
# ----------------------------------------------------------------------
def make_heat_stability_chart():
    img = Image.new("RGB", (1200, 700), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    draw.text((60, 40), "펠렛·익스팬더 85~110℃ 가공열 효소·생균제 생존율", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((60, 80), "스팀 컨디셔닝 및 펠렛 다이(Die) 고온 통과 시 활성 잔존율 비교", font=get_font(18), fill=(148, 163, 184))
    
    x0, y0, x1, y1 = 120, 160, 1100, 560
    draw.rectangle([(x0, y0), (x1, y1)], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    
    # 85~105 Zone
    z_x0 = x0 + int((85 - 70) / 45 * (x1 - x0))
    z_x1 = x0 + int((105 - 70) / 45 * (x1 - x0))
    draw.rectangle([(z_x0, y0), (z_x1, y1)], fill=(45, 55, 72))
    draw.text((z_x0 + 20, y0 + 15), "한일사료 펠렛 스팀 가공 구간 (85~105℃)", font=get_font(14, bold=True), fill=(245, 158, 11))

    # Grid
    for pct in [20, 40, 60, 80, 100]:
        y = y1 - int((pct / 100) * (y1 - y0))
        draw.line([(x0, y), (x1, y)], fill=(51, 65, 85), width=1)
        draw.text((60, y - 10), f"{pct}%", font=get_font(14), fill=(148, 163, 184))

    # Data points
    temps = [75, 80, 85, 90, 95, 100, 105, 110]
    samwon = [99.5, 99.0, 98.2, 96.8, 95.5, 94.2, 92.8, 91.5]
    general = [95.0, 88.0, 78.0, 65.0, 48.0, 32.0, 18.0, 8.0]
    
    sam_pts = []
    gen_pts = []
    for i, t in enumerate(temps):
        px = x0 + int((t - 70) / 45 * (x1 - x0))
        py_s = y1 - int((samwon[i] / 100) * (y1 - y0))
        py_g = y1 - int((general[i] / 100) * (y1 - y0))
        sam_pts.append((px, py_s))
        gen_pts.append((px, py_g))
        draw.text((px - 15, y1 + 15), f"{t}℃", font=get_font(14), fill=(203, 213, 225))

    draw.line(gen_pts, fill=(239, 68, 68), width=3)
    draw.line(sam_pts, fill=(16, 185, 129), width=5)

    for px, py in sam_pts:
        draw.ellipse([(px - 6, py - 6), (px + 6, py + 6)], fill=(52, 211, 153), outline=(255, 255, 255), width=2)
    for px, py in gen_pts:
        draw.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=(239, 68, 68), outline=(255, 255, 255), width=2)

    # Callouts
    draw.text((sam_pts[3][0] - 80, sam_pts[3][1] - 40), "삼원팜텍 코팅: 96.8% 생존", font=get_font(16, bold=True), fill=(52, 211, 153))
    draw.text((gen_pts[3][0] + 15, gen_pts[3][1] + 10), "일반 원료: 65% 급감", font=get_font(15, bold=True), fill=(248, 113, 113))

    # Bottom footer
    draw.rounded_rectangle([(120, 600), (1100, 660)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((150, 618), "★ 다중 지질-다당류 마이크로 캡슐화 기술로 100℃ 고온 압력에도 활성 완벽 보존", font=get_font(18, bold=True), fill=(255, 255, 255))

    out_path = os.path.join(out_dir, "chart_pellet_heat.png")
    img.save(out_path)
    print(f"Saved: {out_path}")

# ----------------------------------------------------------------------
# 4. Livestock ROI Gains Chart (1200 x 700)
# ----------------------------------------------------------------------
def make_livestock_roi_chart():
    img = Image.new("RGB", (1200, 700), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    draw.text((60, 40), "축종별 핵심 생산성 개선 및 농가 실익 환원 효과", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((60, 80), "한우 비육우, 낙농 젖소, 양돈 농가 실증 모니터링 정량 데이터", font=get_font(18), fill=(148, 163, 184))
    
    # 4 Big Cards
    card_data = [
        ("한우 / 비육우", "+12%p", "1++등급 출현율 향상", "• 마리당 지육 경락가 70만원 상승\n• 육성기 초기 섭취량(ADFI) 10%↑\n• 반추위 발효 안정화 & 마블링 극대화", (16, 185, 129)),
        ("낙농 (착유우)", "-25%", "체세포수 급감 (1등급)", "• 하절기 고온기 건물섭취량 1.5kg 유지\n• 산유 피크 기간 2~3주 추가 지속\n• 유질 등급 상승에 따른 유대 보너스", (59, 130, 246)),
        ("양돈 (자돈/비육)", "ZERO", "이유자돈 설사 폐사율", "• 자돈 설사 폐사율 완전 제로화\n• 출하 일령 5~7일 단축\n• 사료요구율(FCR) 0.10 포인트 개선", (245, 158, 11)),
        ("경제적 환원율", "1 : 7.2", "투자 대비 농가 회수율", "• 첨가제 톤당 3,000원 투자 대비\n• 사료비 절감 및 출하 성적으로\n• 톤당 약 21,600원의 실질 이익 환원", (168, 85, 247))
    ]
    
    cw = 220
    gap = 25
    cx0 = 120
    
    for i, (title, stat, stat_sub, desc, col) in enumerate(card_data):
        x = cx0 + i * (cw + gap)
        y = 160
        h = 410
        draw.rounded_rectangle([(x, y), (x + cw, y + h)], radius=14, fill=(30, 41, 59), outline=col, width=2)
        
        # Header inside card
        draw.rounded_rectangle([(x, y), (x + cw, y + 60)], radius=14, fill=col)
        draw.text((x + 25, y + 18), title, font=get_font(18, bold=True), fill=(255, 255, 255))
        
        # Stat
        draw.text((x + 20, y + 80), stat, font=get_font(34, bold=True), fill=col)
        draw.text((x + 20, y + 130), stat_sub, font=get_font(15, bold=True), fill=(255, 255, 255))
        
        # Divider
        draw.line([(x + 20, y + 165), (x + cw - 20, y + 165)], fill=(51, 65, 85), width=1)
        
        # Desc
        draw.text((x + 20, y + 185), desc, font=get_font(13), fill=(203, 213, 225))

    # Bottom footer
    draw.rounded_rectangle([(120, 600), (1100, 660)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((150, 618), "★ 삼원팜텍 맞춤형 솔루션: 1원 투자 시 농가에 7.2원의 실질 수익을 되돌려드립니다", font=get_font(18, bold=True), fill=(255, 255, 255))

    out_path = os.path.join(out_dir, "chart_livestock_roi.png")
    img.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    make_cost_comparison_chart()
    make_homogeneity_chart()
    make_heat_stability_chart()
    make_livestock_roi_chart()
    print("All Pillow charts rendered successfully!")
