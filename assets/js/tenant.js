/**
 * Tenant Portal Renderer & Interactive Triage
 * hospital.html?hospital=seoul-central  또는  hospital.html?hospitalId=xxx
 * 또는 커스텀: hospital.html?name=...&phone=...&city=...&specialty=...&theme=...
 * 몬스멕타 공식 파트너 병원 전용 DX 키트
 */
import QRCode from "qrcode";
import { HOSPITAL_MAP, fetchHospitalConfig } from "./hospital-data.js";

(function () {
  var cfg = window.__VETLINK_CONFIG__ || {};
  var pendingHid = null;

  try {
    var p = new URLSearchParams(window.location.search);
    var hid = p.get('hospital') || p.get('hospitalId');
    var customName = p.get('name');

    if (customName) {
      cfg.name = customName.trim();
      cfg.hospitalId = hid || 'custom';
      if (p.get('city')) cfg.city = p.get('city').trim();
      if (p.get('address')) cfg.address = p.get('address').trim();
      if (p.get('phone')) cfg.phone = p.get('phone').trim();
      if (p.get('specialty')) cfg.specialty = p.get('specialty').trim();
      if (p.get('theme')) cfg.theme = p.get('theme').trim();
      if (p.get('hours')) cfg.businessHours = p.get('hours').trim();
      window.__VETLINK_CONFIG__ = cfg;
    } else if (hid && /^[a-z0-9-]{3,32}$/.test(hid)) {
      if (HOSPITAL_MAP[hid]) {
        Object.assign(cfg, HOSPITAL_MAP[hid]);
        window.__VETLINK_CONFIG__ = cfg;
      } else {
        pendingHid = hid;
      }
    }
  } catch(e){}

  function setText(id, text) { var el = document.getElementById(id); if (el) el.textContent = text; }
  function setHref(id, href) { var el = document.getElementById(id); if (el) el.href = href; }
  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, function (char) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
    });
  }

  // 현재 입력된 문진 상태
  var triageState = {
    stool: "묽은변/무른변",
    vomit: "구토 없음",
    activity: "정상"
  };

  function setupChipGrid(gridId, stateKey) {
    var grid = document.getElementById(gridId);
    if (!grid) return;
    grid.addEventListener('click', function(e) {
      var btn = e.target.closest('.chip-btn');
      if (!btn) return;
      var buttons = grid.querySelectorAll('.chip-btn');
      buttons.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      triageState[stateKey] = btn.getAttribute('data-val');
    });
  }

  function render(c) {
    var hName = c.name || '동물병원';
    setText('tenantNavName', hName);
    setText('tenantH1', hName + ' 스마트 케어');
    setText('tenantSpecialty', c.specialty || '소화기 내과 · 외과 수술 전문');
    setText('tenantAddressShort', (c.city || '') + (c.phone ? ' · ' + c.phone : ''));
    setText('posterName', hName);
    setText('posterSpecialty', c.specialty || '');
    setText('posterAddress', c.address || c.city || '');
    setText('posterPhone', c.phone || '');
    setText('tenantAddress', c.address || c.city || '');
    setText('tenantHours', c.businessHours || '평일 09:30 ~ 19:00 / 주말 진료');

    // 테마 동적 색상 매핑
    var themeMap = {
      teal: { primary: '#14b8a6', gradient: 'linear-gradient(135deg, #0d9488 0%, #14b8a6 100%)', badgeBg: 'rgba(20,184,166,0.15)', badgeBorder: 'rgba(20,184,166,0.4)', badgeText: '#2dd4bf' },
      navy: { primary: '#3b82f6', gradient: 'linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%)', badgeBg: 'rgba(59,130,246,0.15)', badgeBorder: 'rgba(59,130,246,0.4)', badgeText: '#60a5fa' },
      emerald: { primary: '#10b981', gradient: 'linear-gradient(135deg, #047857 0%, #10b981 100%)', badgeBg: 'rgba(16,185,129,0.15)', badgeBorder: 'rgba(16,185,129,0.4)', badgeText: '#34d399' }
    };
    var tTheme = themeMap[c.theme] || themeMap.teal;
    document.documentElement.style.setProperty('--portal-primary', tTheme.primary);
    var pBadge = document.getElementById('partnerBadge');
    if (pBadge) {
      pBadge.style.background = tTheme.badgeBg;
      pBadge.style.borderColor = tTheme.badgeBorder;
      pBadge.style.color = tTheme.badgeText;
    }
    var submitBtn = document.getElementById('btnSubmitTriage');
    if (submitBtn) {
      submitBtn.style.background = tTheme.gradient;
    }

    document.title = hName + ' | 24시 AI 사전 문진 및 안심 케어';
    var tTitle = document.getElementById('tenantTitle');
    if (tTitle) tTitle.textContent = hName + ' | 24시 AI 사전 문진 및 안심 케어';

    var tel = (c.phone || '').replace(/[^0-9]/g,'');
    setHref('posterPhone', 'tel:' + tel);
    setHref('tenantTelLink', 'tel:' + tel);
    setHref('btnCallHospital', 'tel:' + tel);
    if (c.naverPlaceUrl) setHref('tenantNaverLink', c.naverPlaceUrl);

    // 현재 창의 URL(동적 쿼리 포함)을 그대로 QR 및 메타데이터에 연동
    var portalUrl = window.location.href;
    var qrImg = document.getElementById('qrImg');
    if (qrImg) {
      qrImg.alt = hName + ' QR 코드';
      QRCode.toDataURL(portalUrl, { width: 320, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function (url) {
        qrImg.src = url;
      }).catch(function () { qrImg.alt = portalUrl; });
    }

    var canonical = document.getElementById('tenantCanonical');
    if (canonical) canonical.href = portalUrl;
    var ogUrl = document.getElementById('tenantOgUrl');
    if (ogUrl) ogUrl.content = portalUrl;
    var desc = document.getElementById('tenantDesc');
    if (desc) desc.content = hName + ' - 24시 AI 사전 문진 및 소화기 처방 케어';
  }

  // 초기 칩 그리드 바인딩
  setupChipGrid('stoolGrid', 'stool');
  setupChipGrid('vomitGrid', 'vomit');
  setupChipGrid('activityGrid', 'activity');

  // 문진 제출 처리
  var btnSubmit = document.getElementById('btnSubmitTriage');
  if (btnSubmit) {
    btnSubmit.addEventListener('click', function() {
      var petName = document.getElementById('petName')?.value.trim() || '환견/환묘';
      var petSpecies = document.getElementById('petSpecies')?.value || '반려견';
      var petAge = document.getElementById('petAge')?.value.trim() || '미상';
      var petWeight = document.getElementById('petWeight')?.value.trim() || '-';
      var duration = document.getElementById('durationSelect')?.value || '12시간 이내';
      var ownerContact = document.getElementById('ownerContact')?.value.trim() || '보호자';

      // 위험도 평가
      var isRed = triageState.stool === '혈변/점액변' || triageState.vomit === '3회 이상 반복' || triageState.activity === '완전폐식/무기력';
      var isOrange = (triageState.stool !== '정상변' || triageState.vomit !== '구토 없음' || triageState.activity !== '정상');

      var badge = document.getElementById('resultBadge');
      var title = document.getElementById('resultTitle');
      var text = document.getElementById('resultText');

      if (isRed) {
        badge.style.background = '#ef4444';
        badge.style.color = '#ffffff';
        badge.textContent = 'RED : 긴급 대면 진료 권고 (골든타임 주의)';
        title.textContent = '빠른 수의사 확인이 필요한 증상이 선택되었습니다';
        text.textContent = '병원에 즉시 연락해 증상을 알리고 내원을 안내받으세요. 이 문진은 진단이나 처방을 결정하지 않습니다.';
      } else if (isOrange) {
        badge.style.background = '#f59e0b';
        badge.style.color = '#000000';
        badge.textContent = 'ORANGE : 당일 정밀 진료 및 처방 상담';
        title.textContent = '선택한 증상을 수의사에게 알려 주세요';
        text.textContent = '증상의 원인과 치료 필요성은 이 문진으로 판단할 수 없습니다. 병원에 연락해 진료 시점을 상담하세요.';
      } else {
        badge.style.background = '#475569';
        badge.style.color = '#ffffff';
        badge.textContent = '확인 필요 : 자동 판단 불가';
        title.textContent = '선택한 항목만으로 건강 상태를 판단할 수 없습니다';
        text.textContent = '정상 항목을 선택해도 응급 상황을 배제할 수 없습니다. 호흡곤란·경련·의식 저하 등 응급 증상이 있다면 즉시 내원하고, 그 외 증상도 수의사에게 알려 주세요.';
      }

      var summaryList = document.getElementById('summaryList');
      if (summaryList) {
        summaryList.innerHTML = [
          '<li><strong>환자:</strong> ' + escapeHtml(petName) + ' (' + escapeHtml(petSpecies) + ', ' + escapeHtml(petAge) + ', ' + escapeHtml(petWeight) + 'kg)</li>',
          '<li><strong>보호자:</strong> ' + escapeHtml(ownerContact) + '</li>',
          '<li><strong>증상:</strong> 배변(' + escapeHtml(triageState.stool) + ') / 구토(' + escapeHtml(triageState.vomit) + ') / 활력(' + escapeHtml(triageState.activity) + ')</li>',
          '<li><strong>지속 기간:</strong> ' + escapeHtml(duration) + '</li>',
          '<li style="color:#5eead4;"><strong>진료 연계:</strong> 수의사 대면 진료 시 위 사전 문진 데이터가 참고되며, 소화기 치료 및 처방 지사제(몬스멕타 등) 복약 상담이 진행됩니다.</li>'
        ].join('');
      }

      var resultBox = document.getElementById('triageResultBox');
      if (resultBox) {
        resultBox.style.display = 'block';
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  }

  // 진료실 차트용 A4 요약서 즉시 인쇄
  var btnPrintDoc = document.getElementById('btnPrintDoctorSummary');
  if (btnPrintDoc) {
    btnPrintDoc.addEventListener('click', function() {
      var petName = document.getElementById('petName')?.value.trim() || '환견/환묘';
      var petSpecies = document.getElementById('petSpecies')?.value || '반려동물';
      var petAge = document.getElementById('petAge')?.value.trim() || '미상';
      var petWeight = document.getElementById('petWeight')?.value.trim() || '-';
      var duration = document.getElementById('durationSelect')?.value || '12시간 이내';
      var ownerContact = document.getElementById('ownerContact')?.value.trim() || '보호자';
      petName = escapeHtml(petName);
      petSpecies = escapeHtml(petSpecies);
      petAge = escapeHtml(petAge);
      petWeight = escapeHtml(petWeight);
      ownerContact = escapeHtml(ownerContact);
      var nowStr = new Date().toLocaleDateString('ko-KR', { year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' });

      var w = window.open('', '_blank');
      if (!w) return;
      var html = '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">' +
        '<title>진료실 차트 요약서 - ' + petName + '</title>' +
        '<style>' +
        '@page { size: A4 portrait; margin: 15mm; }' +
        'body { font-family: "Malgun Gothic", "Pretendard", sans-serif; color: #0f172a; padding: 20px; line-height: 1.5; }' +
        '.header { display: flex; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; }' +
        '.title { font-size: 22px; font-weight: 800; margin: 0; color: #0f172a; }' +
        '.sub { font-size: 12px; color: #64748b; margin-top: 4px; }' +
        'table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }' +
        'th, td { border: 1px solid #cbd5e1; padding: 10px 14px; font-size: 13px; }' +
        'th { background: #f8fafc; font-weight: 700; width: 22%; color: #334155; }' +
        '.alert-box { background: #f0fdfa; border: 1px solid #14b8a6; border-radius: 8px; padding: 16px; margin-bottom: 20px; }' +
        '.alert-title { font-weight: 800; font-size: 14px; color: #0f766e; margin-bottom: 6px; }' +
        '.alert-desc { font-size: 12.5px; color: #134e4a; line-height: 1.6; }' +
        '.sign-area { margin-top: 40px; border-top: 1px dashed #cbd5e1; padding-top: 20px; display: flex; justify-content: space-between; font-size: 13px; }' +
        '.footer-note { font-size: 11px; color: #94a3b8; margin-top: 30px; text-align: center; }' +
        '</style></head><body>' +
        '<div class="header">' +
        '  <div>' +
        '    <h1 class="title">' + escapeHtml(cfg.name || '동물병원') + ' 진료실 사전 문진 요약서</h1>' +
        '    <div class="sub">접수일시: ' + nowStr + ' | 몬스멕타 처방 DX 포털 연동</div>' +
        '  </div>' +
        '  <div style="text-align:right; font-size:12px; color:#64748b;">' + escapeHtml(cfg.phone || '') + '<br/>' + escapeHtml(cfg.city || '') + '</div>' +
        '</div>' +
        '<table>' +
        '  <tr><th>환자명 (축종)</th><td>' + petName + ' (' + petSpecies + ')</td><th>나이 / 체중</th><td>' + petAge + ' / ' + petWeight + ' kg</td></tr>' +
        '  <tr><th>보호자 연락처</th><td colspan="3">' + ownerContact + '</td></tr>' +
        '  <tr><th>배변 (설사) 양상</th><td><b>' + escapeHtml(triageState.stool) + '</b></td><th>구토 여부</th><td>' + escapeHtml(triageState.vomit) + '</td></tr>' +
        '  <tr><th>식욕 및 활력</th><td>' + escapeHtml(triageState.activity) + '</td><th>증상 지속 기간</th><td>' + escapeHtml(duration) + '</td></tr>' +
        '</table>' +
        '<div class="alert-box">' +
        '  <div class="alert-title">💊 원내 임상 참고 사항 (소화기 증상 및 처방 지침)</div>' +
        '  <div class="alert-desc">본 환자는 보호자 문진상 소화기 증상(' + escapeHtml(triageState.stool) + ', ' + escapeHtml(triageState.vomit) + ')이 접수되었습니다. 대면 검진 후 탈수 교정 수액 요법 및 장관 내 독소·병원체 흡착을 위한 <b>몬스멕타(천연 디옥타헤드랄 스멕타이트 지사제)</b> 등 원내 처방을 수의사 판단에 따라 검토하시기 바랍니다.</div>' +
        '</div>' +
        '<div class="sign-area">' +
        '  <div>담당 수의사 소견: [ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ]</div>' +
        '  <div>처방 확인 및 서명: ____________________ (인)</div>' +
        '</div>' +
        '<div class="footer-note">본 문진표는 보호자가 사전 입력한 데이터를 진료 참고용으로 요약한 것이며 최종 진단과 처방은 수의사의 대면 진료로 확정됩니다.</div>' +
        '<script>window.onload = function(){ window.print(); };<\/script>' +
        '</body></html>';
      w.document.write(html);
      w.document.close();
    });
  }

  // 카운터 A4 알림판 인쇄
  function printPoster() {
    var hName = cfg.name || '동물병원';
    var portalUrl = window.location.href;
    QRCode.toDataURL(portalUrl, { width: 450, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function(qrDataUrl) {
      var w = window.open('', '_blank');
      if (!w) return;
      var html = '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">' +
        '<title>원내 카운터 A4 알림판 - ' + escapeHtml(hName) + '</title>' +
        '<style>' +
        '@page { size: A4 portrait; margin: 15mm; }' +
        'body { font-family: "Malgun Gothic", "Pretendard", sans-serif; color: #0f172a; text-align: center; padding: 30px 20px; line-height: 1.5; }' +
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
        '  <strong>' + escapeHtml(hName) + '</strong>' + (cfg.phone ? ' | ' + escapeHtml(cfg.phone) : '') + '<br/>' +
        '  <span style="font-size:12px;">' + escapeHtml(cfg.address || cfg.city || '') + ' · 몬스멕타 공식 파트너 병원</span>' +
        '</div>' +
        '<script>window.onload = function(){ window.print(); };<\/script>' +
        '</body></html>';
      w.document.write(html);
      w.document.close();
    });
  }

  var btnPoster1 = document.getElementById('btnPosterPrint');
  if (btnPoster1) btnPoster1.addEventListener('click', printPoster);
  var btnPoster2 = document.getElementById('btnPosterPrintDirect');
  if (btnPoster2) btnPoster2.addEventListener('click', printPoster);

  render(cfg);

  if (pendingHid) {
    fetchHospitalConfig(pendingHid).then(function (data) {
      if (data) {
        Object.assign(cfg, data);
        window.__VETLINK_CONFIG__ = cfg;
        render(cfg);
      }
    });
  }
})();
