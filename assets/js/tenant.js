/**
 * Tenant Portal Renderer
 * hospital.html?hospital=seoul-central  또는  hospital.html?hospitalId=xxx
 * hospital-config.js의 window.__VETLINK_CONFIG__를 기반으로 렌더링
 */
import QRCode from "qrcode";
import { HOSPITAL_MAP, fetchHospitalConfig } from "./hospital-data.js";
(function () {
  var cfg = window.__VETLINK_CONFIG__ || {};
  // URL override (hospital.html에서도 ?hospital= 지원) - 단일 소스 + fetch
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

  function render(c) {
    setText('tenantNavName', c.name || '동물병원');
    setText('tenantH1', (c.name || '동물병원') + ' 스마트 케어');
    setText('tenantSpecialty', c.specialty || '');
    setText('tenantCity', c.city || '');
    setText('posterName', c.name || '');
    setText('posterCity', c.city || '');
    setText('posterPhone', c.phone || '');
    setText('tenantAddress', c.address || c.city || '');
    setText('tenantHours', c.businessHours || '');
    document.title = (c.name || '동물병원') + ' | 24시 AI 트리아지 공식 운영처';
    var tTitle = document.getElementById('tenantTitle');
    if (tTitle) tTitle.textContent = (c.name || '동물병원') + ' | 24시 AI 트리아지 공식 운영처';
    var tel = (c.phone || '').replace(/[^0-9]/g,'');
    setHref('posterPhone', 'tel:' + tel);
    setHref('tenantTelLink', 'tel:' + tel);
    if (c.naverPlaceUrl) setHref('tenantNaverLink', c.naverPlaceUrl);
    var badge = document.getElementById('tenantThemeBadge');
    var themeColor = { teal:'#14b8a6', navy:'#1e3a8a', emerald:'#059669' }[c.theme] || '#14b8a6';
    if (badge) badge.style.background = themeColor;
    var portalUrl = 'https://vet-animal-hospital.net/hospital.html?hospital=' + encodeURIComponent(c.hospitalId || 'happy-animal');
    var qrImg = document.getElementById('qrImg');
    if (qrImg) {
      qrImg.alt = (c.name || '') + ' QR 코드';
      QRCode.toDataURL(portalUrl, { width: 300, margin: 1, color: { dark: '#0f172a', light: '#ffffff' } }).then(function (url) {
        qrImg.src = url;
      }).catch(function () { qrImg.alt = portalUrl; });
    }
    var canonical = document.getElementById('tenantCanonical');
    if (canonical) canonical.href = portalUrl;
    var ogUrl = document.getElementById('tenantOgUrl');
    if (ogUrl) ogUrl.content = portalUrl;
    var desc = document.getElementById('tenantDesc');
    if (desc) desc.content = (c.name || '') + ' - ' + (c.specialty || '') + ' | ' + (c.city || '') + ' 24시 AI 사전 트리아지';
    // SEO og tags update if present
    var ogTitle = document.getElementById('tenantOgTitle') || document.querySelector('meta[property=\"og:title\"]');
    if (ogTitle) ogTitle.content = (c.name || '동물병원') + ' | 24시 AI 트리아지 공식 운영처';
    var ogDesc = document.getElementById('tenantOgDesc') || document.querySelector('meta[property=\"og:description\"]');
    if (ogDesc) ogDesc.content = (c.name || '') + ' - ' + (c.specialty || '') + ' | ' + (c.city || '') + ' 24시 AI 사전 트리아지';
    var twTitle = document.getElementById('tenantTwTitle');
    if (twTitle) twTitle.content = (c.name || '동물병원') + ' | 24시 AI 트리아지';
    var twDesc = document.getElementById('tenantTwDesc');
    if (twDesc) twDesc.content = (c.specialty || '') + ' | ' + (c.city || '') + ' 공식 운영처';
    var jsonLd = document.getElementById('tenantJsonLd');
    if (jsonLd) {
      try {
        var ld = JSON.parse(jsonLd.textContent);
        ld.name = c.name || ld.name;
        ld.url = portalUrl;
        if (c.address) ld.address = { "@type": "PostalAddress", "streetAddress": c.address, "addressLocality": c.city, "addressCountry": "KR" };
        jsonLd.textContent = JSON.stringify(ld);
      } catch {}
    }
  }

  render(cfg);

  // 비등록 ID면 fetch로 재시도 → 렌더 갱신
  if (pendingHid) {
    fetchHospitalConfig(pendingHid).then(function (data) {
      if (data) {
        Object.assign(cfg, data);
        window.__VETLINK_CONFIG__ = cfg;
        render(cfg);
      } else {
        // 404 처리: 제목에 안내
        setText('tenantH1', '병원을 찾을 수 없습니다');
        setText('tenantSpecialty', 'hospitalId \"' + pendingHid + '\" 에 해당하는 병원 정보가 없습니다. 관리자에게 문의하세요.');
      }
    });
  }

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
