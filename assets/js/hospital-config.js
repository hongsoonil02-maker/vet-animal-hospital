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
 * 단일 소스: hospital-data.js + fetch fallback
 */
import { HOSPITAL_MAP, fetchHospitalConfig } from "./hospital-data.js";
(function applyQueryOverride() {
  try {
    var params = new URLSearchParams(window.location.search);
    var hid = params.get("hospital");
    if (!hid) return;
    if (!/^[a-z0-9-]{3,32}$/.test(hid)) return;
    if (HOSPITAL_MAP[hid]) {
      Object.assign(window.__VETLINK_CONFIG__, HOSPITAL_MAP[hid], { hospitalId: hid });
      window.dispatchEvent(new CustomEvent("vetlink:config-ready", { detail: window.__VETLINK_CONFIG__ }));
      return;
    }
    // 비등록 ID는 fetch 시도 (비동기)
    fetchHospitalConfig(hid).then(function (data) {
      if (data) {
        Object.assign(window.__VETLINK_CONFIG__, data, { hospitalId: hid });
        window.dispatchEvent(new CustomEvent("vetlink:config-ready", { detail: window.__VETLINK_CONFIG__ }));
      }
    });
  } catch (e) { /* ignore */ }
})();
