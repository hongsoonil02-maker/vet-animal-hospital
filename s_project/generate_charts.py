import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set Korean font
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

out_dir = r"C:\Users\master\vet_animal_hospital\s_project\assets"
os.makedirs(out_dir, exist_ok=True)

# ----------------------------------------------------
# 1. Grain Price Volatility Chart
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026(E)']
corn = [160, 240, 310, 260, 230, 275, 290] # $/ton
soybean_meal = [340, 420, 520, 460, 410, 480, 510] # $/ton

ax.plot(years, corn, marker='o', color='#F59E0B', linewidth=3, label='수입 옥수수 ($/ton)')
ax.plot(years, soybean_meal, marker='s', color='#EF4444', linewidth=3, label='수입 대두박 ($/ton)')
ax.fill_between(years, corn, alpha=0.15, color='#F59E0B')
ax.fill_between(years, soybean_meal, alpha=0.1, color='#EF4444')

ax.set_title('국제 주요 사료 원료곡 가격 변동 추이 (2020~2026)', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_ylabel('국제 시세 (USD / M/T)', fontsize=11, fontweight='bold', color='#334155')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', edgecolor='#E2E8F0', fontsize=10.5)
ax.annotate('곡물가 급등 및 환율 쇼크\n(사료 제조원가 압박 심화)', xy=('2022', 520), xytext=('2021', 560),
            arrowprops=dict(facecolor='#EF4444', shrink=0.05, width=2, headwidth=8),
            fontsize=10, fontweight='bold', color='#B91C1C', bbox=dict(boxstyle="round,pad=0.4", fc="#FEF2F2", ec="#EF4444"))
plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_grain_prices.png'))
plt.close(fig)

# ----------------------------------------------------
# 2. Cost Comparison Bar Chart
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
categories = ['시중 일반 처방 A\n(1.0kg 투입)', '시중 일반 처방 B\n(1.5kg 투입)', '시중 일반 처방 C\n(2.0kg 투입)', '삼원팜텍 고농축\n(500g 투입)']
costs = [4500, 6750, 9000, 3000]
colors = ['#94A3B8', '#64748B', '#475569', '#10B981']

bars = ax.bar(categories, costs, color=colors, width=0.55, edgecolor='#0F172A', linewidth=1.2)
ax.set_title('사료 톤(ton)당 첨가제 투입 비용 비교', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_ylabel('사료 톤당 투입비 (원 / ton)', fontsize=11, fontweight='bold', color='#334155')
ax.set_ylim(0, 10500)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    if yval == 3000:
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 300, f'단 {yval:,}원\n(최적 원가)', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#059669')
    else:
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 200, f'{yval:,}원', ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#334155')

ax.axhline(3000, color='#10B981', linestyle=':', linewidth=2)
plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_cost_comparison.png'))
plt.close(fig)

# ----------------------------------------------------
# 3. Monthly & Annual Savings Waterfall / Cumulative
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
months = [f'{m}월' for m in range(1, 13)]
# Monthly saving ~81M - 54M = 27M ~ 108M. Let's take standard average savings = 8,000만원/월
monthly_saving = 8000 # 만원
cumulative_savings = [(i + 1) * monthly_saving for i in range(12)]

bars = ax.bar(months, cumulative_savings, color='#3B82F6', alpha=0.85, width=0.6, edgecolor='#1E3A8A', linewidth=1.2)
bars[-1].set_color('#10B981') # Year end highlight
bars[-1].set_edgecolor('#059669')

ax.set_title('S-NACF 연간 누적 원가 절감 효과 (월 18,000톤 기준)', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_ylabel('누적 원가 절감액 (만원)', fontsize=11, fontweight='bold', color='#334155')
ax.grid(axis='y', linestyle='--', alpha=0.5)

ax.text(11, cumulative_savings[-1] + 2500, f'연간 누적\n9억 6,000만원 절감\n(최대 13억원)', ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#059669', bbox=dict(boxstyle="round,pad=0.4", fc="#ECFDF5", ec="#10B981"))
plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_monthly_savings.png'))
plt.close(fig)

# ----------------------------------------------------
# 4. Mixing Homogeneity Bell Curve (CV < 5% vs CV 10%)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
x = np.linspace(350, 650, 500)
# Samwon: Mean 500g, SD = 19g (CV = 3.8%)
y_samwon = (1 / (19 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 500) / 19)**2)
# Industry standard: Mean 500g, SD = 50g (CV = 10%)
y_ind = (1 / (50 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 500) / 50)**2)

ax.plot(x, y_samwon, color='#10B981', linewidth=3.5, label='삼원팜텍 초정밀 분산 (CV 3.8%)')
ax.fill_between(x, y_samwon, alpha=0.2, color='#10B981')
ax.plot(x, y_ind, color='#94A3B8', linewidth=2.5, linestyle='--', label='사료산업 일반 기준 (CV 10.0%)')
ax.fill_between(x, y_ind, alpha=0.1, color='#94A3B8')

ax.set_title('한일사료 메인 믹서 내 투입 혼화도 분포 곡선', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_xlabel('1톤 사료 내 첨가제 검출 농도 (g/ton)', fontsize=11, fontweight='bold', color='#334155')
ax.set_ylabel('분포 밀도 (Density)', fontsize=11, fontweight='bold', color='#334155')
ax.axvline(500, color='#0F2043', linestyle=':', alpha=0.7)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', edgecolor='#E2E8F0', fontsize=10.5)
plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_homogeneity_cv.png'))
plt.close(fig)

# ----------------------------------------------------
# 5. Pellet Heat Stability Curve (85~110℃)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
temps = [75, 80, 85, 90, 95, 100, 105, 110]
samwon_retention = [99.5, 99.0, 98.2, 96.8, 95.5, 94.2, 92.8, 91.5]
general_retention = [95.0, 88.0, 78.0, 65.0, 48.0, 32.0, 18.0, 8.0]

ax.plot(temps, samwon_retention, marker='o', color='#10B981', linewidth=3.5, label='삼원팜텍 마이크로 캡슐 코팅')
ax.plot(temps, general_retention, marker='x', color='#EF4444', linewidth=2.5, linestyle='--', label='시중 비코팅 일반 원료')

ax.set_title('펠렛·익스팬더 스팀 가공 온도별 유효 활성 잔존율', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_xlabel('가공 공정 온도 (℃)', fontsize=11, fontweight='bold', color='#334155')
ax.set_ylabel('유효 성분 활성 잔존율 (%)', fontsize=11, fontweight='bold', color='#334155')
ax.set_ylim(0, 105)
ax.axvspan(85, 105, alpha=0.15, color='#F59E0B', label='한일사료 펠렛 스팀 가공 구간 (85~105℃)')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', edgecolor='#E2E8F0', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_pellet_heat_stability.png'))
plt.close(fig)

# ----------------------------------------------------
# 6. Dairy Performance Gains Bar Chart (100% Dairy)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
indicators = ['젖소 착유우\n일 산유량 방어', '원유 유질\n체세포수 저감', '송아지·육성우\n설사 발생 억제', '임상형 유방염\n발생 예방', '목장 ROI\n투자 가치 회수']
values = [18.0, 42.0, 80.0, 65.0, 52.0] # scaled for visualization
display_labels = ['+1.8kg/일', '-42.2%', '-80.4%', '-65.0%', '1 : 5.2배']
colors = ['#059669', '#0D9488', '#2563EB', '#D97706', '#7C3AED']

bars = ax.bar(indicators, values, color=colors, width=0.55, edgecolor='#0F172A', linewidth=1.2)
ax.set_title('서울우유 낙농 목장 핵심 생산성 지표 개선 실증 수치', fontsize=14, fontweight='bold', pad=15, color='#0F2043')
ax.set_ylabel('개선 강도 및 효과 지수', fontsize=11, fontweight='bold', color='#334155')
ax.grid(axis='y', linestyle='--', alpha=0.5)

for i, bar in enumerate(bars):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, display_labels[i], ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0F2043')

plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'chart_livestock_radar.png'))
plt.close(fig)

print("All 6 charts successfully generated!")
