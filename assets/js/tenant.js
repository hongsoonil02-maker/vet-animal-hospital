/**
 * Tenant Portal Renderer
 * hospital.html?hospital=seoul-central  또는  hospital.html?hospitalId=xxx
 * hospital-config.js의 window.__VETLINK_CONFIG__를 기반으로 렌더링
 */
(function () {
  var cfg = window.__VETLINK_CONFIG__ || {};
  // URL override (hospital.html에서도 ?hospital= 지원)
  try {
    var p = new URLSearchParams(window.location.search);
    var hid = p.get('hospital') || p.get('hospitalId');
    if (hid) {
      var map = {
        'seoul-central': { hospitalId:'seoul-central', name:'서울센트럴동물병원', city:'서울 서초구 반포동', address:'서울 서초구 신반포로 45', phone:'02-5407-5708', theme:'navy', specialty:'정형외과 · CT 정밀진단 · 고양이 특화', businessHours:'평일 10:00 ~ 19:00 / 주말 10:00 ~ 17:00', naverPlaceUrl:'https://naver.me/seoul-central' },
        'busan-pet': { hospitalId:'busan-pet', name:'부산펫메디컬센터', city:'부산 해운대구 우동', address:'부산 해운대구 해운대로 200', phone:'051-123-4567', theme:'emerald', specialty:'내과·건강검진·노령견 케어', businessHours:'연중무휴 09:00 ~ 21:00', naverPlaceUrl:'' },
        'happy-animal': { hospitalId:'happy-animal', name:'행복한 동물병원', city:'서울 강남구 역삼동', address:'서울 강남구 테헤란로 123', phone:'02-1234-5678', theme:'teal', specialty:'외과 수술 & 소화기 정밀 내과', businessHours:'평일 09:30 ~ 18:30 / 토 09:30 ~ 15:00', naverPlaceUrl:'' }
      };
      if (map[hid]) Object.assign(cfg, map[hid]);
    }
  } catch(e){}

  function setText(id, text) { var el = document.getElementById(id); if (el) el.textContent = text; }
  function setHref(id, href) { var el = document.getElementById(id); if (el) el.href = href; }

  setText('tenantNavName', cfg.name || '동물병원');
  setText('tenantH1', (cfg.name || '동물병원') + ' 스마트 케어');
  setText('tenantSpecialty', cfg.specialty || '');
  setText('tenantCity', cfg.city || '');
  setText('posterName', cfg.name || '');
  setText('posterCity', cfg.city || '');
  setText('posterPhone', cfg.phone || '');
  setText('tenantAddress', cfg.address || cfg.city || '');
  setText('tenantHours', cfg.businessHours || '');
  setText('tenantTitle', (cfg.name || '동물병원') + ' | 24시 AI 트리아지 공식 운영처');
  var tel = (cfg.phone || '').replace(/[^0-9]/g,'');
  setHref('posterPhone', 'tel:' + tel);
  setHref('tenantTelLink', 'tel:' + tel);
  if (cfg.naverPlaceUrl) setHref('tenantNaverLink', cfg.naverPlaceUrl);

  // theme badge
  var badge = document.getElementById('tenantThemeBadge');
  var themeColor = { teal:'#14b8a6', navy:'#1e3a8a', emerald:'#059669' }[cfg.theme] || '#14b8a6';
  if (badge) badge.style.background = themeColor;

  // QR: 병원 전용 URL → QR 이미지 (무료 API, 프로덕션은 자체 생성기로 교체)
  var portalUrl = 'https://vet-animal-hospital.net/hospital.html?hospital=' + encodeURIComponent(cfg.hospitalId || 'happy-animal');
  var qrImg = document.getElementById('qrImg');
  if (qrImg) {
    qrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=' + encodeURIComponent(portalUrl);
    qrImg.alt = (cfg.name || '') + ' QR 코드';
  }
  var canonical = document.getElementById('tenantCanonical');
  if (canonical) canonical.href = portalUrl;

  // SEO desc
  var desc = document.getElementById('tenantDesc');
  if (desc) desc.content = (cfg.name || '') + ' - ' + (cfg.specialty || '') + ' | ' + (cfg.city || '') + ' 24시 AI 사전 트리아지';

  // Print handlers
  var btnPoster = document.getElementById('btnPosterPrint');
  if (btnPoster) btnPoster.addEventListener('click', function(){ window.print(); });
  var btnSummary = document.getElementById('btnSummaryPrint');
  if (btnSummary) btnSummary.addEventListener('click', function(){
    var w = window.open('', '_blank');
    if (!w) return;
    w.document.write('<!doctype html><html lang=ko><head><meta charset=utf-8><title>진료실 1장 요약서 샘플 - ' + (cfg.name||'') + '</title><style>body{font-family:sans-serif;padding:32px}h1{font-size:20px}table{width:100%;border-collapse:collapse;margin-top:16px}th,td{border:1px solid #cbd5e1;padding:8px;text-align:left;font-size:13px} .warn{margin-top:16px;font-size:11px;color:#64748b}</style></head><body><h1>' + (cfg.name||'') + ' - 진료실 1장 요약서 (샘플)</h1><p style=color:#64748b;font-size:13px>' + (cfg.city||'') + ' · ' + (cfg.phone||'') + '</p><table><tr><th>보호자</th><td>홍길동 / 010-****-1234</td><th>반려동물</th><td>초코 (말티즈, 3세)</td></tr><tr><th>증상</th><td colspan=3>어제 저녁부터 묽은 변 2회, 식욕 저하 (AI 트리아지: ORANGE)</td></tr><tr><th>메모</th><td colspan=3>몬스멕타 등 처방 여부는 수의사 대면 진료 후 결정</td></tr></table><p class=warn>본 요약서는 보호자 작성 사전 문진을 진료 참고용으로 정리한 것입니다. 진단·처방은 대면 진료한 수의사가 결정합니다. 응급 시 즉시 내원하세요.</p><script>window.print()<\/script></body></html>');
    w.document.close();
  });
})();
