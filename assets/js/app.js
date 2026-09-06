/**
 * VetLink AI Core Interactive Engine v2.4
 * - Live Template Customizer (hospital-config.js 연동)
 * - AI Triage Simulator (정규화 + 동의어 + XSS 방지)
 * - Disclaimer Modal (a11y)
 */
document.addEventListener('DOMContentLoaded', () => {
  initHospitalConfigBridge();
  initCustomizer();
  initTriageSimulator();
  initDisclaimerModal();
  initMobileNav();
});

// 0. hospital-config → UI 브리지 (P0-1)
function initHospitalConfigBridge() {
  var cfg = window.__VETLINK_CONFIG__;
  if (!cfg) return;
  var nameInput = document.getElementById('inputHospitalName');
  var cityInput = document.getElementById('inputCity');
  var specialtyInput = document.getElementById('inputSpecialty');
  if (nameInput && cfg.name) nameInput.value = cfg.name;
  if (cityInput && cfg.city) cityInput.value = cfg.city;
  if (specialtyInput && cfg.specialty) specialtyInput.value = cfg.specialty;
  // 초기 프리뷰 반영
  setTimeout(function () {
    if (nameInput) nameInput.dispatchEvent(new Event('input'));
    if (cityInput) cityInput.dispatchEvent(new Event('input'));
    if (specialtyInput) specialtyInput.dispatchEvent(new Event('input'));
    // theme
    var btn = document.querySelector('.theme-pill-btn[data-theme="' + cfg.theme + '"]');
    if (btn) btn.click();
    // 전화번호 치환 (footer/CTA)
    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      if (cfg.phone) a.href = 'tel:' + cfg.phone.replace(/[^0-9]/g, '');
    });
  }, 0);
}

// 1. Live Template Customizer Engine
function initCustomizer() {
  var nameInput = document.getElementById('inputHospitalName');
  var cityInput = document.getElementById('inputCity');
  var specialtyInput = document.getElementById('inputSpecialty');
  var themeButtons = document.querySelectorAll('.theme-pill-btn');

  var previewName = document.getElementById('previewName');
  var previewSpecialty = document.getElementById('previewSpecialty');
  var previewCity = document.getElementById('previewCity');
  var previewHeroTitle = document.getElementById('previewHeroTitle');
  var previewNavbar = document.getElementById('previewNavbar');
  var previewBadge = document.getElementById('previewBadge');

  function safeText(v, fallback) {
    var s = (v || '').toString().trim().slice(0, 60);
    // XSS 방지: textContent만 사용
    return s || fallback;
  }

  if (nameInput) {
    nameInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '우리동물병원');
      if (previewName) previewName.textContent = val;
      if (previewHeroTitle) previewHeroTitle.textContent = val + ' 스마트 케어';
    });
  }
  if (cityInput) {
    cityInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '서울 강남구');
      if (previewCity) previewCity.textContent = val;
    });
  }
  if (specialtyInput) {
    specialtyInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '외과·내과·건강검진 전문');
      if (previewSpecialty) previewSpecialty.textContent = val;
    });
  }
  themeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      themeButtons.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed','false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed','true');
      var theme = btn.getAttribute('data-theme');
      applyThemeToPreview(theme, previewNavbar, previewBadge);
    });
  });
}

function applyThemeToPreview(theme, nav, badge) {
  if (!nav || !badge) return;
  var map = {
    teal: { bg: '#14b8a6', border: '#14b8a6' },
    navy: { bg: '#1e3a8a', border: '#1e3a8a' },
    emerald: { bg: '#059669', border: '#059669' }
  };
  var c = map[theme] || map.teal;
  badge.style.background = c.bg;
  badge.style.color = '#ffffff';
  nav.style.borderBottomColor = c.border;
}

// 2. Triage - 정규화 & 동의어
var TRIAGE_RED = ['혈변','피똥','피 섞인','혈뇨','호흡곤란','숨가쁨','가쁜숨','호흡 곤란','경련','발작','떨림','허탈','의식저하','복부팽만','토혈','개구호흡'];
var TRIAGE_ORANGE = ['구토','토함','거품토','설사','묽은변','무른변','설사','식욕부진','밥 안 먹','안 먹','기력저하','침흘림','기침','콧물','혈액','점액변'];

function normalizeInput(text) {
  return (text || '').toLowerCase().replace(/\s+/g,'').slice(0, 500);
}
function containsAny(normalized, keywords) {
  return keywords.some(function (kw) { return normalized.includes(kw.replace(/\s+/g,'').toLowerCase()); });
}

function initTriageSimulator() {
  var simInput = document.getElementById('simSymptomInput');
  var simBtn = document.getElementById('simAnalyzeBtn');
  var simOutput = document.getElementById('simOutputCard');
  var simBadge = document.getElementById('simBadge');
  var simTitle = document.getElementById('simTitle');
  var simAction = document.getElementById('simAction');

  if (!simBtn || !simInput) return;

  function analyze() {
    var raw = simInput.value.trim();
    if (!raw) {
      alert('증상을 입력하거나 아래 예시 칩을 눌러보세요.');
      return;
    }
    if (raw.length > 500) raw = raw.slice(0,500);
    var text = normalizeInput(raw);
    simOutput.style.display = 'block';
    simOutput.setAttribute('aria-live', 'polite');

    if (containsAny(text, TRIAGE_RED)) {
      simBadge.style.background = '#ef4444';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'RED : 긴급 대면 내원 요망';
      simTitle.textContent = '응급 중증도 - 지체 없이 내원';
      simAction.textContent = '호흡·출혈·신경 증상은 골든타임이 중요합니다. 즉시 내원하여 수액 및 정밀 검사를 받으세요. (본 결과는 참고용이며 진단을 대체하지 않습니다)';
    } else if (containsAny(text, TRIAGE_ORANGE)) {
      simBadge.style.background = '#f59e0b';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'ORANGE : 당일 정밀 진료 권고';
      simTitle.textContent = '소화기/전신 염증 의심 - 당일 진료 권고';
      simAction.textContent = '탈수 위험이 있어 당일 진료와 진단키트 검사를 권고합니다. 보호자 요약서가 진료실로 자동 전달됩니다. (수의사 상담 필요)';
    } else {
      simBadge.style.background = '#10b981';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'GREEN : 안정 및 초기 관찰';
      simTitle.textContent = '경증 - 가정 관찰 가능';
      simAction.textContent = '일시적 컨디션 저하일 수 있습니다. 음수·체온·배변을 12시간 관찰하고 악화 시 내원하세요.';
    }
    simOutput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  simBtn.addEventListener('click', analyze);
  simInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) analyze();
  });

  // chip buttons (data-chip)
  document.querySelectorAll('[data-chip]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.getAttribute('data-chip') || '';
      simInput.value = t;
      analyze();
    });
  });
}

// legacy global for backwards compat (inline onclick 제거 후에도 동작)
function setSimChip(text) {
  var input = document.getElementById('simSymptomInput');
  if (input) { input.value = text; document.getElementById('simAnalyzeBtn').click(); }
}
window.setSimChip = setSimChip;

// 4. Studio → Tenant & Poster bridge
(function initStudioExtras(){
  var btnTenant = document.getElementById('btnOpenTenant');
  var btnPoster = document.getElementById('btnStudioPoster');
  var nameInput = document.getElementById('inputHospitalName');
  function currentId() {
    var v = (nameInput && nameInput.value.trim()) || (window.__VETLINK_CONFIG__ && window.__VETLINK_CONFIG__.hospitalId) || 'happy-animal';
    // slugify: 한글은 happy로 fallback, 영문이면 slug
    var slug = v.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    if (!slug || /[^a-z0-9-]/.test(v) || slug.length < 3) {
      // 한글 병원명은 쿼리로 매핑된 예시 사용, 그 외는 happy
      var cfg = window.__VETLINK_CONFIG__ || {};
      return cfg.hospitalId || 'happy-animal';
    }
    return slug;
  }
  if (btnTenant) {
    // input 시 href 동적 갱신
    var updateTenantHref = function(){
      var id = currentId();
      // 알려진 예시는 그대로
      var known = ['happy-animal','seoul-central','busan-pet'];
      if (!known.includes(id)) id = (window.__VETLINK_CONFIG__ && window.__VETLINK_CONFIG__.hospitalId) || 'happy-animal';
      btnTenant.href = './hospital.html?hospital=' + encodeURIComponent(id);
    };
    if (nameInput) nameInput.addEventListener('input', updateTenantHref);
    updateTenantHref();
  }
  if (btnPoster) {
    btnPoster.addEventListener('click', function(){
      var cfg = window.__VETLINK_CONFIG__ || {};
      var name = (nameInput && nameInput.value.trim()) || cfg.name || '행복한 동물병원';
      var cityEl = document.getElementById('inputCity');
      var city = (cityEl && cityEl.value.trim()) || cfg.city || '';
      var phone = cfg.phone || '02-1234-5678';
      var portalUrl = 'https://vet-animal-hospital.net/hospital.html?hospital=' + encodeURIComponent(cfg.hospitalId || 'happy-animal');
      var qr = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + encodeURIComponent(portalUrl);
      var w = window.open('', '_blank');
      if (!w) return;
      w.document.write('<!doctype html><html lang=ko><head><meta charset=utf-8><title>A4 알림판 - ' + name + '</title><style>@page{size:A4;margin:18mm}body{font-family:sans-serif;padding:24px;color:#0f172a}h1{font-size:28px;margin:0}.badge{display:inline-block;background:#14b8a6;color:#fff;font-size:12px;font-weight:800;padding:4px 10px;border-radius:999px;margin:12px 0}.qr{width:180px;height:180px;margin:18px auto;border:1px solid #e2e8f0;padding:8px;border-radius:12px}.qr img{width:100%;height:100%}.foot{margin-top:20px;font-size:11px;color:#64748b;text-align:center;border-top:1px solid #e2e8f0;padding-top:12px}</style></head><body><div style=text-align:center><h1>' + name + '</h1><div style=color:#475569>' + city + ' · ' + phone + '</div><div class=badge>24시 AI 사전 트리아지 공식 운영처</div><div class=qr><img src=\"' + qr + '\" alt=\"QR\"/></div><p style=font-size:14px;color:#334155>스마트폰 카메라로 QR을 스캔하면<br/><strong>병원 전용 스마트 포털</strong>로 바로 연결됩니다.</p><div class=foot>본 알림판은 정보 제공용이며, 호흡곤란·경련·혈변 등 응급 시 즉시 내원하세요. · vet-animal-hospital.net</div></div><script>window.print()<\/script></body></html>');
      w.document.close();
    });
  }
})();

// 3. Disclaimer Modal (focus trap, inert)
function initDisclaimerModal() {
  var modal = document.getElementById('disclaimerModal');
  var openBtn = document.getElementById('openDisclaimer');
  var closeBtn = document.getElementById('closeDisclaimer');
  if (!modal) return;
  var lastFocus = null;
  function open() {
    lastFocus = document.activeElement;
    modal.classList.add('open');
    modal.removeAttribute('inert');
    modal.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    if (closeBtn) closeBtn.focus();
  }
  function close() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
    modal.setAttribute('inert','');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
    else if (openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', function (e) { e.preventDefault(); open(); });
  if (closeBtn) closeBtn.addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
  // focus trap inside modal
  modal.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab' || !modal.classList.contains('open')) return;
    var focusable = modal.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])');
    if (!focusable.length) return;
    var first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
}

function initMobileNav() {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
  });
  nav.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (window.innerWidth <= 768) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
        toggle.setAttribute('aria-label','메뉴 열기');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !toggle.contains(e.target) && nav.classList.contains('open')) {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded','false');
    }
  });
}
