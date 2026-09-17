/**
 * VetLink AI Core Interactive Engine v2.5
 * - Live Template Customizer & Real-time Dynamic Hospital Portal Bridge
 * - Interactive Live QR Code preview, download & KakaoTalk sharing link copy
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

// 스마트폰 카메라 스캔 및 카카오톡 전달을 위한 공용 배포 URL 반환
function getPublicPortalUrl() {
  var query = buildCustomHospitalQuery();
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'https://vet-animal-hospital.pages.dev/hospital?' + query;
  }
  var basePath = window.location.pathname.replace(/\/[^\/]*$/, '/');
  return window.location.origin + basePath + 'hospital?' + query;
}

// 1. Live Template Customizer Engine & Studio QR
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
  var studioQrImg = document.getElementById('studioPreviewQr');

  function safeText(v, fallback) {
    var s = (v || '').toString().trim().slice(0, 60);
    return s || fallback;
  }

  function refreshTenantLinkAndQr() {
    var query = buildCustomHospitalQuery();
    if (btnTenant) {
      btnTenant.href = './hospital.html?' + query;
    }
    if (studioQrImg) {
      var publicUrl = getPublicPortalUrl();
      QRCode.toDataURL(publicUrl, { width: 320, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } })
        .then(function (url) {
          studioQrImg.src = url;
        })
        .catch(function (err) { console.error('Studio QR Error', err); });
    }
  }

  if (nameInput) {
    nameInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '우리동물병원');
      if (previewName) previewName.textContent = val;
      if (previewHeroTitle) previewHeroTitle.textContent = val + ' 스마트 케어';
      refreshTenantLinkAndQr();
    });
  }
  if (cityInput) {
    cityInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '서울 강남구');
      if (previewCity) previewCity.textContent = val;
      refreshTenantLinkAndQr();
    });
  }
  if (specialtyInput) {
    specialtyInput.addEventListener('input', function (e) {
      var val = safeText(e.target.value, '외과·내과·건강검진 전문');
      if (previewSpecialty) previewSpecialty.textContent = val;
      refreshTenantLinkAndQr();
    });
  }
  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      refreshTenantLinkAndQr();
    });
  }

  themeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      themeButtons.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed','false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed','true');
      var theme = btn.getAttribute('data-theme');
      applyThemeToPreview(theme, previewNavbar, previewBadge);
      refreshTenantLinkAndQr();
    });
  });

  // [QR 다운로드]
  var btnDownloadStudioQr = document.getElementById('btnDownloadStudioQr');
  if (btnDownloadStudioQr) {
    btnDownloadStudioQr.addEventListener('click', function () {
      if (!studioQrImg || !studioQrImg.src) return;
      var hName = safeText(nameInput && nameInput.value, '동물병원');
      var a = document.createElement('a');
      a.href = studioQrImg.src;
      a.download = hName + '_스마트문진_QR코드.png';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  }

  // [카톡 전달용 링크 복사 & 모바일 네이티브 공유]
  var btnCopyStudioLink = document.getElementById('btnCopyStudioLink');
  var studioCopyToast = document.getElementById('studioCopyToast');
  if (btnCopyStudioLink) {
    btnCopyStudioLink.addEventListener('click', function () {
      var publicUrl = getPublicPortalUrl();
      var hName = safeText(nameInput && nameInput.value, '동물병원');

      if (navigator.share && /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent)) {
        navigator.share({
          title: hName + ' 24시 스마트 케어 포털',
          text: '[' + hName + '] 대기시간 단축 및 1초 사전 문진 모바일 안내 링크입니다.',
          url: publicUrl
        }).catch(function () {
          fallbackCopy(publicUrl);
        });
      } else {
        fallbackCopy(publicUrl);
      }

      function fallbackCopy(textToCopy) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(textToCopy).then(showToast);
        } else {
          var ta = document.createElement('textarea');
          ta.value = textToCopy;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          showToast();
        }
      }

      function showToast() {
        if (studioCopyToast) {
          studioCopyToast.style.display = 'block';
          setTimeout(function () { studioCopyToast.style.display = 'none'; }, 3500);
        }
      }
    });
  }

  // [원내 카운터 A4 알림판 인쇄 팝업]
  var btnStudioPoster = document.getElementById('btnStudioPoster');
  if (btnStudioPoster) {
    btnStudioPoster.addEventListener('click', function () {
      var hName = safeText(nameInput && nameInput.value, '동물병원');
      var city = safeText(cityInput && cityInput.value, '서울 강남구 역삼동');
      var phone = safeText(phoneInput && phoneInput.value, '02-1234-5678');
      var publicUrl = getPublicPortalUrl();

      QRCode.toDataURL(publicUrl, { width: 450, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function (qrDataUrl) {
        var w = window.open('', '_blank');
        if (!w) return;
        var html = '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">' +
          '<title>원내 카운터 A4 알림판 - ' + escapeHtml(hName) + '</title>' +
          '<style>' +
          '@page { size: A4 portrait; margin: 15mm; }' +
          'body { font-family: "Malgun Gothic", "Pretendard", -apple-system, sans-serif; color: #0f172a; text-align: center; padding: 30px 20px; line-height: 1.5; }' +
          '.badge { display: inline-block; background: #0f172a; color: #2dd4bf; padding: 8px 18px; border-radius: 999px; font-size: 15px; font-weight: 800; margin-bottom: 20px; }' +
          '.h1 { font-size: 32px; font-weight: 900; margin: 0 0 10px; color: #0f172a; }' +
          '.sub { font-size: 18px; color: #475569; margin-bottom: 30px; font-weight: 600; }' +
          '.qr-wrapper { border: 3px solid #0f172a; border-radius: 24px; padding: 24px; width: 280px; margin: 0 auto 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }' +
          '.qr-img { width: 100%; height: auto; display: block; }' +
          '.step-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; max-width: 480px; margin: 0 auto 30px; text-align: left; }' +
          '.step-item { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }' +
          '.step-desc { font-size: 13px; color: #64748b; margin-left: 24px; margin-bottom: 12px; }' +
          '.footer { font-size: 14px; color: #64748b; border-top: 1px solid #cbd5e1; padding-top: 20px; max-width: 500px; margin: 0 auto; }' +
          '</style></head><body>' +
          '<div class="badge">🏥 스마트 원내 사전 접수처</div>' +
          '<h1 class="h1">' + escapeHtml(hName) + '</h1>' +
          '<div class="sub">대기실에서 스마트폰으로 1초 만에 사전 문진을 작성해 주세요</div>' +
          '<div class="qr-wrapper">' +
          '  <img class="qr-img" src="' + qrDataUrl + '" alt="QR" />' +
          '</div>' +
          '<div class="step-box">' +
          '  <div class="step-item">1️⃣ 스마트폰 기본 카메라로 위 QR코드를 비춥니다.</div>' +
          '  <div class="step-desc">별도의 앱 설치 없이 1초 만에 병원 전용 문진창이 열립니다.</div>' +
          '  <div class="step-item">2️⃣ 아이의 증상(구토, 설사 등)을 간편하게 체크합니다.</div>' +
          '  <div class="step-desc">작성 즉시 진료실 원장님 차트로 전달되어 진료 대기 시간이 단축됩니다.</div>' +
          '</div>' +
          '<div class="footer">' +
          '  <strong>' + escapeHtml(hName) + '</strong>' + (phone ? ' | ' + escapeHtml(phone) : '') + '<br/>' +
          '  <span style="font-size:12px;">' + escapeHtml(city) + ' · 몬스멕타 공식 파트너 병원</span>' +
          '</div>' +
          '<script>window.onload = function(){ window.print(); };<\/script>' +
          '</body></html>';
        w.document.write(html);
        w.document.close();
      });
    });
  }

  refreshTenantLinkAndQr();
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

// 4. Disclaimer Modal (focus trap, inert) & Top Banner Dismiss
function initDisclaimerModal() {
  var modal = document.getElementById('disclaimerModal');
  var openBtn = document.getElementById('openDisclaimer');
  var closeBtn = document.getElementById('closeDisclaimer');
  var dismissBannerBtn = document.getElementById('dismissDisclaimer');
  var disclaimerBar = document.getElementById('disclaimerBar');

  if (dismissBannerBtn && disclaimerBar) {
    try {
      if (sessionStorage.getItem('vetlink_disclaimer_dismissed') === '1') {
        disclaimerBar.classList.add('dismissed');
      }
    } catch (e) {}

    dismissBannerBtn.addEventListener('click', function () {
      disclaimerBar.classList.add('dismissed');
      try {
        sessionStorage.setItem('vetlink_disclaimer_dismissed', '1');
      } catch (e) {}
    });
  }

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
        var publicShareUrl = customPortalUrl;
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
          publicShareUrl = 'https://vet-animal-hospital.pages.dev/hospital.html?name=' + encodeURIComponent(hName) +
                           '&phone=' + encodeURIComponent(phone) +
                           '&city=' + encodeURIComponent(region || '대한민국') +
                           '&theme=teal';
        }

        QRCode.toDataURL(publicShareUrl, { width: 320, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } })
          .then(function (qrDataUrl) {
            linkBox.innerHTML =
              '<div style="margin-top:12px; background:#ffffff; border-radius:12px; padding:16px; text-align:center; color:#0f172a;">' +
              '  <div style="font-size:13px; font-weight:800; margin-bottom:8px;">📱 스마트폰 카메라로 비추면 바로 열립니다</div>' +
              '  <img src="' + qrDataUrl + '" alt="' + escapeHtml(hName) + ' QR 코드" style="width:140px; height:140px; display:inline-block; border:2px solid #0f172a; border-radius:12px; padding:6px; background:#fff;" />' +
              '  <div style="margin-top:12px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">' +
              '    <a href="' + customPortalUrl + '" target="_blank" class="btn-hero-primary" style="padding:8px 14px; font-size:12px; text-decoration:none;">🏥 포털 열기 &rarr;</a>' +
              '    <button type="button" id="btnDownloadApplyQr" class="btn-hero-secondary" style="padding:8px 14px; font-size:12px;">📥 QR 다운로드</button>' +
              '    <button type="button" id="btnCopyApplyLink" class="btn-hero-secondary" style="padding:8px 14px; font-size:12px;">🔗 카톡 링크 복사</button>' +
              '  </div>' +
              '  <div id="applyCopyToast" style="display:none; margin-top:8px; font-size:12px; color:#0d9488; font-weight:800;">✅ 카카오톡에 전달할 수 있는 링크가 복사되었습니다!</div>' +
              '</div>';

            var btnDown = document.getElementById('btnDownloadApplyQr');
            if (btnDown) {
              btnDown.addEventListener('click', function () {
                var a = document.createElement('a');
                a.href = qrDataUrl;
                a.download = hName + '_스마트문진_QR코드.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
              });
            }

            var btnCopy = document.getElementById('btnCopyApplyLink');
            if (btnCopy) {
              btnCopy.addEventListener('click', function () {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                  navigator.clipboard.writeText(publicShareUrl).then(showToast);
                } else {
                  showToast();
                }
                function showToast() {
                  var t = document.getElementById('applyCopyToast');
                  if (t) { t.style.display = 'block'; setTimeout(function () { t.style.display = 'none'; }, 3500); }
                }
              });
            }
          })
          .catch(function (err) {
            console.error('Apply QR generate error', err);
            linkBox.innerHTML = '<a href="' + customPortalUrl + '" target="_blank" class="btn-hero-primary" style="display:inline-flex; align-items:center; gap:6px; margin-top:8px; padding:10px 18px; font-size:13px; font-weight:800; text-decoration:none;">' +
                                '🏥 생성된 ' + escapeHtml(hName) + ' 스마트 포털 바로 열기 &rarr;</a>';
          });
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
