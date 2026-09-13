/**
 * VetLink Hospital Registry - Single Source of Truth
 * config/examples/*.json 과 동기화 유지. 빌드 시 스키마 검증됨.
 */
export const HOSPITAL_MAP = {
  "seoul-central": { hospitalId: "seoul-central", name: "서울센트럴동물병원", city: "서울 서초구 반포동", address: "서울 서초구 신반포로 45", phone: "02-5407-5708", theme: "navy", specialty: "정형외과 · CT 정밀진단 · 고양이 특화", businessHours: "평일 10:00 ~ 19:00 / 주말 10:00 ~ 17:00", naverPlaceUrl: "https://naver.me/seoul-central", monsmectaPartner: true },
  "busan-pet": { hospitalId: "busan-pet", name: "부산펫메디컬센터", city: "부산 해운대구 우동", address: "부산 해운대구 해운대로 200", phone: "051-123-4567", theme: "emerald", specialty: "내과·건강검진·노령견 케어", businessHours: "연중무휴 09:00 ~ 21:00", naverPlaceUrl: "", monsmectaPartner: true },
  "happy-animal": { hospitalId: "happy-animal", name: "행복한 동물병원", city: "서울 강남구 역삼동", address: "서울 강남구 테헤란로 123", phone: "02-1234-5678", theme: "teal", specialty: "외과 수술 & 소화기 정밀 내과", businessHours: "평일 09:30 ~ 18:30 / 토 09:30 ~ 15:00", naverPlaceUrl: "", monsmectaPartner: false }
};

export async function fetchHospitalConfig(hospitalId) {
  if (HOSPITAL_MAP[hospitalId]) return HOSPITAL_MAP[hospitalId];
  try {
    const res = await fetch(`/config/examples/${encodeURIComponent(hospitalId)}.json`, { cache: "no-store" });
    if (!res.ok) return null;
    const data = await res.json();
    // 최소 검증: hospitalId 패턴
    if (!data.hospitalId || !/^[a-z0-9-]{3,32}$/.test(data.hospitalId)) return null;
    return data;
  } catch {
    return null;
  }
}
