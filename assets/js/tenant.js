/**
 * Tenant Portal Renderer & Interactive Triage
 * hospital.html?hospital=seoul-central  또는  hospital.html?hospitalId=xxx
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
    if (hid && /^[a-z0-9-]{3,32}$/.test(hid)) {
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
    setText('tenantAddressShort', (c.city || '') + ' · ' + (c.phone || ''));
    setText('posterName', hName);
    setText('posterSpecialty', c.specialty || '');
    setText('posterAddress', c.address || c.city || '');
    setText('posterPhone', c.phone || '');
    setText('tenantAddress', c.address || c.city || '');
    setText('tenantHours', c.businessHours || '평일 09:30 ~ 19:00 / 주말 진료');

    document.title = hName + ' | 24시 AI 사전 문진 및 안심 케어';
    var tTitle = document.getElementById('tenantTitle');
    if (tTitle) tTitle.textContent = hName + ' | 24시 AI 사전 문진 및 안심 케어';

    var tel = (c.phone || '').replace(/[^0-9]/g,'');
    setHref('posterPhone', 'tel:' + tel);
    setHref('tenantTelLink', 'tel:' + tel);
    setHref('btnCallHospital', 'tel:' + tel);
    if (c.naverPlaceUrl) setHref('tenantNaverLink', c.naverPlaceUrl);

    var portalUrl = 'https://vet-animal-hospital.net/hospital.html?hospital=' + encodeURIComponent(c.hospitalId || 'seoul-central');
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
      var isRed = (triageState.stool === '물설사(수양성)' || triageState.stool === '혈변/점액변') && (triageState.vomit === '3회 이상 반복' || triageState.activity === '완전폐식/무기력');
      var isOrange = (triageState.stool !== '정상변' || triageState.vomit !== '구토 없음' || triageState.activity !== '정상');

      var badge = document.getElementById('resultBadge');
      var title = document.getElementById('resultTitle');
      var text = document.getElementById('resultText');

      if (isRed) {
        badge.style.background = '#ef4444';
        badge.style.color = '#ffffff';
        badge.textContent = 'RED : 긴급 대면 진료 권고 (골든타임 주의)';
        title.textContent = '급성 탈수 및 출혈성 장염 의심 — 즉시 대면 진료';
        text.textContent = '지속적인 수분 손실로 급성 탈수가 진행될 위험이 높습니다. 즉시 진료실로 입장하여 수액 및 지사 처치를 받으세요.';
      } else if (isOrange) {
        badge.style.background = '#f59e0b';
        badge.style.color = '#000000';
        badge.textContent = 'ORANGE : 당일 정밀 진료 및 처방 상담';
        title.textContent = '소화기 점막 손상 및 설사 의심 — 처방 상담 권고';
        text.textContent = '장내 독소 흡착 및 설사 완화를 위한 수의 처방제(몬스멕타 등) 복약 상담이 즉시 권고됩니다.';
      } else {
        badge.style.background = '#10b981';
        badge.style.color = '#ffffff';
        badge.textContent = 'GREEN : 초기 경증 관찰 가능';
        title.textContent = '단순 소화 불량 의심 — 12시간 관찰 요망';
        text.textContent = '일시적인 식이 변화일 수 있습니다. 충분한 음수를 제공하고 증상 지속 시 내원하세요.';
      }

      var summaryList = document.getElementById('summaryList');
      if (summaryList) {
        summaryList.innerHTML = [
          '<li><strong>환자:</strong> ' + petName + ' (' + petSpecies + ', ' + petAge + ', ' + petWeight + 'kg)</li>',
          '<li><strong>보호자:</strong> ' + ownerContact + '</li>',
          '<li><strong>증상:</strong> 배변(' + triageState.stool + ') / 구토(' + triageState.vomit + ') / 활력(' + triageState.activity + ')</li>',
          '<li><strong>지속 기간:</strong> ' + duration + '</li>',
          '<li style="color:#5eead4;"><strong>처방 고려:</strong> 장관 내 독소·세균 흡착 지사제 [몬스멕타(Monsmecta)] 투여 여부 수의사 상담</li>'
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
      var nowStr = new Date().toLocaleDateString('ko-KR', { year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' });

      var w = window.open('', '_blank');
      if (!w) return;
      var html = '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">' +
        '<title>진료실 차트 요약서 - ' + petName + '</title>' +
        '<style>' +
        '@page { size: A4 portrait; margin: 15mm; }' +
        'body { font-family: "Malgun Gothic", "Pretendard", sans-serif; color: #0f172a; padding: 20px; line-height: 1.5; }' +
        '.header { border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }' +
        '.title { font-size: 22px; font-weight: 900; color: #0f172a; margin: 0; }' +
        '.sub { font-size: 13px; color: #64748b; margin-top: 4px; }' +
        'table { width: 100%; border-collapse: collapse; margin-top: 14px; margin-bottom: 18px; }' +
        'th, td { border: 1px solid #cbd5e1; padding: 10px 12px; font-size: 13px; text-align: left; }' +
        'th { background: #f1f5f9; font-weight: 700; width: 22%; color: #334155; }' +
        '.alert-box { background: #f8fafc; border-left: 4px solid #0d9488; padding: 12px 16px; margin: 16px 0; border-radius: 4px; }' +
        '.alert-title { font-weight: 800; font-size: 14px; color: #0f766e; }' +
        '.alert-desc { font-size: 12.5px; color: #334155; margin-top: 4px; }' +
        '.sign-area { margin-top: 40px; border-top: 1px dashed #cbd5e1; padding-top: 20px; display: flex; justify-content: space-between; font-size: 13px; }' +
        '.footer-note { font-size: 11px; color: #94a3b8; margin-top: 30px; text-align: center; }' +
        '</style></head><body>' +
        '<div class="header">' +
        '  <div>' +
        '    <h1 class="title">' + (cfg.name || '동물병원') + ' 진료실 사전 문진 요약서</h1>' +
        '    <div class="sub">접수일시: ' + nowStr + ' | 몬스멕타 처방 DX 포털 연동</div>' +
        '  </div>' +
        '  <div style="text-align:right; font-size:12px; color:#64748b;">' + (cfg.phone || '') + '<br/>' + (cfg.city || '') + '</div>' +
        '</div>' +
        '<table>' +
        '  <tr><th>환자명 (축종)</th><td>' + petName + ' (' + petSpecies + ')</td><th>나이 / 체중</th><td>' + petAge + ' / ' + petWeight + ' kg</td></tr>' +
        '  <tr><th>보호자 연락처</th><td colspan="3">' + ownerContact + '</td></tr>' +
        '  <tr><th>배변 (설사) 양상</th><td><b>' + triageState.stool + '</b></td><th>구토 여부</th><td>' + triageState.vomit + '</td></tr>' +
        '  <tr><th>식욕 및 활력</th><td>' + triageState.activity + '</td><th>증상 지속 기간</th><td>' + duration + '</td></tr>' +
        '</table>' +
        '<div class="alert-box">' +
        '  <div class="alert-title">💊 원내 처방 고려 안내 (소화기 점막 보호 & 흡착성 지사제)</div>' +
        '  <div class="alert-desc">본 환자는 소화기 증상(' + triageState.stool + ')이 확인되었으므로, 탈수 방지 수액 처치와 함께 <b>몬스멕타(Monsmecta)</b> 복약 처방이 적극 권장됩니다. (천연 디옥타헤드랄 스멕타이트 성분으로 장내 독소 및 바이러스 흡착 배출)</div>' +
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
    var portalUrl = 'https://vet-animal-hospital.net/hospital.html?hospital=' + encodeURIComponent(cfg.hospitalId || 'seoul-central');
    QRCode.toDataURL(portalUrl, { width: 450, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function(qrDataUrl) {
      var w = window.open('', '_blank');
      if (!w) return;
      var html = '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">' +
        '<title>원내 카운터 A4 알림판 - ' + hName + '</title>' +
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
        '<h1 class="h1">' + hName + '</h1>' +
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
        '  <strong>' + hName + '</strong> | ' + (cfg.phone || '') + '<br/>' +
        '  <span style="font-size:12px;">' + (cfg.address || cfg.city || '') + ' · 몬스멕타 공식 파트너 병원</span>' +
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
