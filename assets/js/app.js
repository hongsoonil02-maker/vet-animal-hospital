/**
 * VetLink AI Core Interactive Engine
 * Controls: Live Template Customizer, AI Triage Simulator, Pricing Calculator
 */

document.addEventListener('DOMContentLoaded', () => {
  initCustomizer();
  initTriageSimulator();
});

// 1. Live Template Customizer Engine
function initCustomizer() {
  const nameInput = document.getElementById('inputHospitalName');
  const cityInput = document.getElementById('inputCity');
  const specialtyInput = document.getElementById('inputSpecialty');
  const themeButtons = document.querySelectorAll('.theme-pill-btn');

  const previewName = document.getElementById('previewName');
  const previewSpecialty = document.getElementById('previewSpecialty');
  const previewCity = document.getElementById('previewCity');
  const previewHeroTitle = document.getElementById('previewHeroTitle');
  const previewNavbar = document.getElementById('previewNavbar');
  const previewBadge = document.getElementById('previewBadge');

  if (nameInput) {
    nameInput.addEventListener('input', (e) => {
      const val = e.target.value.trim() || '우리동물병원';
      if (previewName) previewName.textContent = val;
      if (previewHeroTitle) previewHeroTitle.textContent = `${val} 스마트 케어`;
    });
  }

  if (cityInput) {
    cityInput.addEventListener('input', (e) => {
      const val = e.target.value.trim() || '서울 강남구';
      if (previewCity) previewCity.textContent = val;
    });
  }

  if (specialtyInput) {
    specialtyInput.addEventListener('input', (e) => {
      const val = e.target.value.trim() || '외과·내과·건강검진 전문';
      if (previewSpecialty) previewSpecialty.textContent = val;
    });
  }

  themeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      themeButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const theme = btn.getAttribute('data-theme');
      applyThemeToPreview(theme, previewNavbar, previewBadge);
    });
  });
}

function applyThemeToPreview(theme, nav, badge) {
  if (!nav || !badge) return;
  if (theme === 'teal') {
    badge.style.background = '#14b8a6';
    badge.style.color = '#ffffff';
    nav.style.borderBottomColor = '#14b8a6';
  } else if (theme === 'navy') {
    badge.style.background = '#1e3a8a';
    badge.style.color = '#ffffff';
    nav.style.borderBottomColor = '#1e3a8a';
  } else if (theme === 'emerald') {
    badge.style.background = '#059669';
    badge.style.color = '#ffffff';
    nav.style.borderBottomColor = '#059669';
  }
}

// 2. Interactive AI Triage Simulator for Director Demo
function initTriageSimulator() {
  const simInput = document.getElementById('simSymptomInput');
  const simBtn = document.getElementById('simAnalyzeBtn');
  const simOutput = document.getElementById('simOutputCard');
  const simBadge = document.getElementById('simBadge');
  const simTitle = document.getElementById('simTitle');
  const simAction = document.getElementById('simAction');

  if (!simBtn || !simInput) return;

  simBtn.addEventListener('click', () => {
    const text = simInput.value.trim();
    if (!text) {
      alert('증상을 입력하거나 아래 예시 키워드를 눌러보세요.');
      return;
    }

    simOutput.style.display = 'block';

    if (text.includes('혈변') || text.includes('경련') || text.includes('호흡곤란')) {
      simBadge.style.background = '#ef4444';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'RED : 긴급 대면 내원 요망';
      simTitle.textContent = '위급성 응급 중증도 판정 (지체 없이 원내 방문)';
      simAction.textContent = '수액 및 바이러스/혈액 정밀 검사를 위한 신속 내원 안내 SMS가 보호자에게 자동 발송됩니다.';
    } else if (text.includes('구토') || text.includes('설사') || text.includes('식욕부진')) {
      simBadge.style.background = '#f59e0b';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'ORANGE : 당일 정밀 진료 권고';
      simTitle.textContent = '탈수 및 급성 소화기 염증 의심';
      simAction.textContent = '몬스멕타(Monsmecta) 등 점막보호제 처방 및 진단키트 검사 준비를 위한 사전 요약서가 생성됩니다.';
    } else {
      simBadge.style.background = '#10b981';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'GREEN : 안정 및 초기 관찰';
      simTitle.textContent = '일시적 컨디션 저하 또는 경증';
      simAction.textContent = '자가 체온 체크 및 음수량 관리 요령 안내문이 보호자에게 자동 전달됩니다.';
    }
  });
}

function setSimChip(text) {
  const input = document.getElementById('simSymptomInput');
  if (input) {
    input.value = text;
    document.getElementById('simAnalyzeBtn').click();
  }
}
