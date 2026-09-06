/**
 * VetLink Master Config - 단일 파일 제어
 * 실제 배포 시: /config/examples/{hospitalId}.json 을 fetch 하거나
 * 빌드타임에 이 파일을 병원별로 치환하여 배포한다.
 * 
 * 로컬 데모/스캐폴드 기본값: happy-animal
 */
window.__VETLINK_CONFIG__ = {
  hospitalId: "happy-animal",
  name: "행복한 동물병원",
  city: "서울 강남구 역삼동",
  address: "서울 강남구 테헤란로 123",
  phone: "02-1234-5678",
  theme: "teal",
  specialty: "외과 수술 & 소화기 정밀 내과",
  businessHours: "평일 09:30 ~ 18:30 / 토 09:30 ~ 15:00",
  monsmectaPartner: false,
  features: { triage: true, summaryPdf: true, counterPoster: true, qrPortal: true }
};

/**
 * Optional: URL ?hospital=seoul-central 로 테넌트 프리뷰
 * 예: index.html?hospital=seoul-central
 */
(function applyQueryOverride() {
  try {
    var params = new URLSearchParams(window.location.search);
    var hid = params.get("hospital");
    if (!hid) return;
    // config/examples 매핑 (빌드 시엔 fetch로 교체)
    var map = {
      "seoul-central": { name: "서울센트럴동물병원", city: "서울 서초구 반포동", phone: "02-5407-5708", theme: "navy", specialty: "정형외과 · CT 정밀진단 · 고양이 특화", monsmectaPartner: true },
      "busan-pet": { name: "부산펫메디컬센터", city: "부산 해운대구 우동", phone: "051-123-4567", theme: "emerald", specialty: "내과·건강검진·노령견 케어", monsmectaPartner: true },
      "happy-animal": { name: "행복한 동물병원", city: "서울 강남구 역삼동", phone: "02-1234-5678", theme: "teal", specialty: "외과 수술 & 소화기 정밀 내과", monsmectaPartner: false }
    };
    if (map[hid]) {
      Object.assign(window.__VETLINK_CONFIG__, map[hid], { hospitalId: hid });
    }
  } catch (e) { /* ignore */ }
})();
