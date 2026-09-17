/**
 * VetLink AI Core Interactive Engine v2.5
 * - Live Template Customizer & Real-time Dynamic Hospital Portal Bridge
 * - AI Triage Simulator (정규화 + 동의어 + XSS 방지)
 * - Counter A4 Poster & Branded QR Generation
 * - Partner Apply Form with Instant Portal Preview Link
 * - Disclaimer Modal (a11y)
 */
import QRCode from "qrcode";

document.addEventListener('DOMContentLoaded', () => {
  initHospitalConfigBridge();
  initCustomizer();
  initTriageSimulator();
  initDisclaimerModal();
  initMobileNav();
  initPartnerApplyForm();
});

function escapeHtml(value) {
  return String(value || '').replace(/[&<>"']/g, function (char) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
  });
}

// 0. hospital-config → UI 브리지 (P0-1) + 비동기 fetch 대응
function initHospitalConfigBridge() {
  var cfg = window.__VETLINK_CONFIG__;
  if (!cfg) return;
  function apply(cfgData) {
    var nameInput = document.getElementById('inputHospitalName');
    var cityInput = document.getElementById('inputCity');
    var specialtyInput = document.getElementById('inputSpecialty');
    var phoneInput = document.getElementById('inputPhone');

    if (nameInput && cfgData.name) nameInput.value = cfgData.name;
    if (cityInput && cfgData.city) cityInput.value = cfgData.city;
    if (specialtyInput && cfgData.specialty) specialtyInput.value = cfgData.specialty;
    if (phoneInput && cfgData.phone) phoneInput.value = cfgData.phone;

    if (nameInput) nameInput.dispatchEvent(new Event('input'));
    if (cityInput) cityInput.dispatchEvent(new Event('input'));
    if (specialtyInput) specialtyInput.dispatchEvent(new Event('input'));
    if (phoneInput) phoneInput.dispatchEvent(new Event('input'));

    var btn = document.querySelector('.theme-pill-btn[data-theme="' + cfgData.theme + '"]');
    if (btn) btn.click();

    if (cfgData.phone) {
      var telClean = cfgData.phone.replace(/[^0-9]/g, '');
      document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
        if (!a.getAttribute('data-keep-tel')) {
          a.href = 'tel:' + telClean;
        }
      });
    }
  }
  // 초기 동기 적용
  setTimeout(function () { apply(cfg); }, 0);
  // 비동기 fetch 후 갱신 대응
  window.addEventListener('vetlink:config-ready', function (e) {
    apply(e.detail || window.__VETLINK_CONFIG__);
  });
}

// 동적 병원 포털 쿼리 생성기 (전국 5,000개 병원 실시간 대응)
function buildCustomHospitalQuery() {
  var nameInput = document.getElementById('inputHospitalName');
  var cityInput = document.getElementById('inputCity');
  var specialtyInput = document.getElementById('inputSpecialty');
  var phoneInput = document.getElementById('inputPhone');
  var activeThemeBtn = document.querySelector('.theme-pill-btn.active');

  var name = (nameInput && nameInput.value.trim()) || '행복한 동물병원';
  var city = (cityInput && cityInput.value.trim()) || '서울 강남구 역삼동';
  var specialty = (specialtyInput && specialtyInput.value.trim()) || '외과 수술 & 소화기 정밀 내과';
  var phone = (phoneInput && phoneInput.value.trim()) || '02-1234-5678';
  var theme = (activeThemeBtn && activeThemeBtn.getAttribute('data-theme')) || 'teal';

  var params = new URLSearchParams();
  params.set('name', name);
  params.set('city', city);
  params.set('phone', phone);
  params.set('specialty', specialty);
  params.set('theme', theme);
  return params.toString();
}

// 1. Live Template Customizer Engine
function initCustomizer() {
  var nameInput = document.getElementById('inputHospitalName');
  var cityInput = document.getElementById('inputCity');
  var specialtyInput = document.getElementById('inputSpecialty');
  var phoneInput = document.getElementById('inputPhone');
  var themeButtons = document.querySelectorAll('.theme-pill-btn');

  var previewName = document.getElementById('previewName');
  var previewSpecialty = document.getElementById('previewSpecialty');
  var previewCity = document.getElementById('previewCity');
  var previewHeroTitle = document.getElementById('previewHeroTitle');
  var previewNavbar = document.getElementById('previewNavbar');
  var previewBadge = document.getElementById('previewBadge');
  var btnTenant = document.getElementById('btnOpenTenant');

  function safeText(v, fallback) {
    var s = (v || '').toString().trim().slice(0, 60);
    return s || fallback;
  }

  function refreshTenantLink() {
    if (btnTenant) {
      btnTenant.href = './hospital.html?' + buildCustomHospitalQuery();
    }
  }

  if (nameInput) {
    nameInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '우리동물병원');
      if (previewName) previewName.textContent = val;
      if (previewHeroTitle) previewHeroTitle.textContent = val + ' 스마트 케어';
      refreshTenantLink();
    });
  }
  if (cityInput) {
    cityInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '서울 강남구');
      if (previewCity) previewCity.textContent = val;
      refreshTenantLink();
    });
  }
  if (specialtyInput) {
    specialtyInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '외과·내과·건강검진 전문');
      if (previewSpecialty) previewSpecialty.textContent = val;
      refreshTenantLink();
    });
  }
  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      refreshTenantLink();
    });
  }

  themeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      themeButtons.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed','false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed','true');
      var theme = btn.getAttribute('data-theme');
      applyThemeToPreview(theme, previewNavbar, previewBadge);
      refreshTenantLink();
    });
  });

  refreshTenantLink();
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

// 2. Triage - 정규화 & 동의어 (중복 제거, 공백 유지 매칭)
var TRIAGE_RED = ['혈변','피똥','피 섞인','혈뇨','호흡곤란','숨가쁨','가쁜숨','호흡 곤란','경련','발작','전신 떨림','허탈','의식저하','복부팽만','토혈','개구호흡'];
var TRIAGE_ORANGE = ['구토','토함','거품토','설사','묽은변','무른변','식욕부진','밥 안 먹','기력저하','침흘림','기침','콧물','혈액','점액변'];

function normalizeInput(text) {
  return (text || '').toLowerCase().replace(/[.,!?;:'"()\[\]{}]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 500);
}
function containsAny(normalized, keywords) {
  return keywords.some(function (kw) {
    var k = kw.toLowerCase().trim();
    return normalized.includes(k) || normalized.replace(/\s+/g, '').includes(k.replace(/\s+/g, ''));
  });
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
    var errorEl = document.getElementById('simError');
    if (!raw) {
      if (errorEl) {
        errorEl.textContent = '증상을 입력하거나 아래 예시 칩을 눌러보세요.';
        errorEl.style.display = 'block';
        simInput.focus();
      } else {
        simInput.setAttribute('aria-invalid', 'true');
        simInput.placeholder = '증상을 입력해 주세요 (예: 묽은 변 2회, 식욕 저하)';
      }
      return;
    }
    if (errorEl) errorEl.style.display = 'none';
    simInput.removeAttribute('aria-invalid');
    if (raw.length > 500) raw = raw.slice(0,500);
    var text = normalizeInput(raw);
    simOutput.style.display = 'block';
    simOutput.setAttribute('aria-live', 'polite');

    if (containsAny(text, TRIAGE_RED)) {
      simBadge.style.background = '#ef4444';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'RED : 긴급 대면 내원 요망';
      simTitle.textContent = '응급 신호 관련 표현이 확인되었습니다';
      simAction.textContent = '호흡곤란·경련·출혈 등 응급 증상이 있다면 즉시 가까운 동물병원에 연락하고 내원하세요. 단순 키워드 안내로 증상의 유무나 원인을 판단할 수 없습니다.';
    } else if (containsAny(text, TRIAGE_ORANGE)) {
      simBadge.style.background = '#f59e0b';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = 'ORANGE : 당일 정밀 진료 권고';
      simTitle.textContent = '소화기/염증 증상 관련 표현이 확인되었습니다';
      simAction.textContent = '탈수 위험이 있으므로 당일 대면 진료 및 수의사 처방(몬스멕타 복약 등) 상담을 권고합니다. 작성된 사전 문진표는 원장님 차트로 전달됩니다.';
    } else {
      simBadge.style.background = '#475569';
      simBadge.style.color = '#ffffff';
      simBadge.textContent = '확인 필요 : 자동 판단 불가';
      simTitle.textContent = '입력 내용만으로 응급도를 판단할 수 없습니다';
      simAction.textContent = '일치하는 키워드가 없다고 안전한 것은 아닙니다. 증상이 있거나 걱정된다면 수의사에게 상담하세요. 호흡곤란·경련·의식 저하 등 응급 증상이 있으면 즉시 내원하세요.';
    }
    simOutput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  simBtn.addEventListener('click', analyze);
  simInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) analyze();
  });

  document.querySelectorAll('[data-chip]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.getAttribute('data-chip') || '';
      simInput.value = t;
      analyze();
    });
  });
}

function setSimChip(text) {
  var input = document.getElementById('simSymptomInput');
  if (input) { input.value = text; document.getElementById('simAnalyzeBtn').click(); }
}
window.setSimChip = setSimChip;

// 3. Studio → Tenant & Dynamic Poster bridge
(function initStudioExtras(){
  var btnPoster = document.getElementById('btnStudioPoster');
  var nameInput = document.getElementById('inputHospitalName');
  var cityInput = document.getElementById('inputCity');
  var phoneInput = document.getElementById('inputPhone');

  if (btnPoster) {
    btnPoster.addEventListener('click', function(){
      var name = (nameInput && nameInput.value.trim()) || '행복한 동물병원';
      var city = (cityInput && cityInput.value.trim()) || '서울 강남구 역삼동';
      var phone = (phoneInput && phoneInput.value.trim()) || '02-1234-5678';

      // 현재 도메인 및 경로 기준 완벽한 URL 생성
      var basePath = window.location.pathname.replace(/\/[^\/]*$/, '/');
      var portalUrl = window.location.origin + basePath + 'hospital.html?' + buildCustomHospitalQuery();

      QRCode.toDataURL(portalUrl, { width: 320, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function (qrDataUrl) {
        var w = window.open('', '_blank');
        if (!w) return;
        w.document.write('<!doctype html><html lang=ko><head><meta charset=utf-8><title>원내 카운터 A4 알림판 - ' + escapeHtml(name) + '</title><style>@page{size:A4 portrait;margin:15mm}body{font-family:"Malgun Gothic","Pretendard",sans-serif;padding:30px 20px;color:#0f172a;text-align:center;line-height:1.5}.badge{display:inline-block;background:#0f172a;color:#2dd4bf;font-size:14px;font-weight:800;padding:6px 16px;border-radius:999px;margin-bottom:16px}.h1{font-size:30px;font-weight:900;margin:0 0 10px}.sub{font-size:16px;color:#475569;margin-bottom:24px;font-weight:600}.qr-wrapper{width:240px;height:240px;margin:20px auto;border:2px solid #0f172a;padding:12px;border-radius:18px;box-shadow:0 8px 20px rgba(0,0,0,0.06)}.qr-wrapper img{width:100%;height:100%;display:block}.steps{background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:18px;max-width:460px;margin:20px auto;text-align:left;font-size:14px;color:#334155}.step-item{font-weight:700;margin-bottom:6px}.step-desc{font-size:12px;color:#64748b;margin-left:22px;margin-bottom:10px}.foot{margin-top:24px;font-size:12px;color:#64748b;border-top:1px solid #e2e8f0;padding-top:14px}</style></head><body><div><div class=badge>🏥 스마트 원내 사전 접수처</div><h1 class=h1>' + escapeHtml(name) + '</h1><div class=sub>대기실에서 스마트폰 카메라로 QR을 스캔하여 1초 만에 문진을 작성해 주세요</div><div class=qr-wrapper><img src=\"' + qrDataUrl + '\" alt=\"QR\"/></div><div class=steps><div class=step-item>1️⃣ 기본 카메라로 위 QR코드를 비춥니다.</div><div class=step-desc>별도 앱 설치 없이 병원 전용 스마트 문진창으로 즉시 연결됩니다.</div><div class=step-item>2️⃣ 아이의 주요 증상을 간편하게 체크합니다.</div><div class=step-desc>작성 즉시 진료실 차트로 전달되어 대기 시간이 대폭 단축됩니다.</div></div><div class=foot><strong>' + escapeHtml(name) + '</strong> | ' + escapeHtml(phone) + ' (' + escapeHtml(city) + ')<br/>몬스멕타 공식 처방 파트너 · VetLink AI</div></div><script>window.onload=function(){window.print();};<\/script></body></html>');
        w.document.close();
      }).catch(function (err) {
        console.error('QR 생성 실패', err);
        var toast = document.getElementById('simError');
        if (toast) { toast.textContent = 'QR 생성에 실패했습니다. 팝업 차단을 확인해 주세요.'; toast.style.display = 'block'; }
      });
    });
  }
})();

// 4. Disclaimer Modal (focus trap, inert)
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

// 5. 파트너 동물병원 간편 신청 및 실시간 포털 생성
function initPartnerApplyForm() {
  var form = document.getElementById('partnerApplyForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var hName = document.getElementById('applyHospitalName')?.value.trim();
    var docName = document.getElementById('applyDoctorName')?.value.trim();
    var phone = document.getElementById('applyPhone')?.value.trim();
    var region = document.getElementById('applyRegion')?.value.trim();

    if (!hName || !docName || !phone) return;

    var customPortalUrl = './hospital.html?name=' + encodeURIComponent(hName) +
                          '&phone=' + encodeURIComponent(phone) +
                          '&city=' + encodeURIComponent(region || '대한민국') +
                          '&theme=teal';

    var successMsg = document.getElementById('applySuccessMsg');
    var successText = document.getElementById('applySuccessText');
    var linkBox = document.getElementById('applyPortalLinkBox');

    if (successMsg && successText) {
      successMsg.style.display = 'block';
      successText.innerHTML = '🎉 <strong>' + escapeHtml(hName) + ' (' + escapeHtml(docName) + ' 원장님)</strong> 무상 키트 세팅 신청이 완료되었습니다!';
      if (linkBox) {
        linkBox.innerHTML = '<a href="' + customPortalUrl + '" target="_blank" class="btn-hero-primary" style="display:inline-flex; align-items:center; gap:6px; margin-top:8px; padding:10px 18px; font-size:13px; font-weight:800; text-decoration:none; box-shadow: 0 4px 14px rgba(20,184,166,0.35);">' +
                            '🏥 생성된 ' + escapeHtml(hName) + ' 스마트 포털 바로 열기 &rarr;</a>';
      }
      successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    try {
      var leads = JSON.parse(localStorage.getItem('vetlink_partner_leads') || '[]');
      leads.push({
        hospitalName: hName,
        doctorName: docName,
        phone: phone,
        region: region,
        portalUrl: customPortalUrl,
        createdAt: new Date().toISOString()
      });
      localStorage.setItem('vetlink_partner_leads', JSON.stringify(leads));
    } catch(err){}
  });
}
