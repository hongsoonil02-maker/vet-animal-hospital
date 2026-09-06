# VetLink AI — vet-animal-hospital.net SaaS 스캐폴드

대한민국 5,000개 동물병원에 1회 세팅으로 배포하는 **스마트 포털 SaaS 스캐폴드**. 24시 AI 트리아지 → A4 요약서 → 카운터 알림판 & QR까지 단일 `hospital-config`로 제어.

## 스택
- Vanilla HTML/CSS/JS + Vite 빌드
- Cloudflare Pages / Workers ( `wrangler.jsonc` )
- 멀티테넌트: `config/examples/{hospitalId}.json` → `assets/js/hospital-config.js`

## 폴더
```
├─ index.html                # 랜딩 + Studio + Simulator
├─ privacy.html / terms.html # 법무 필수
├─ config/
│  ├─ hospital.schema.json   # JSON Schema (필수/패턴 검증)
│  └─ examples/*.json        # happy-animal, seoul-central, busan-pet
├─ assets/
│  ├─ css/style.css
│  ├─ js/app.js
│  └─ js/hospital-config.js  # 마스터 컨피그 (쿼리 ?hospital= 로 프리뷰)
└─ sitemap.xml / robots.txt
```

## 빠른 시작
```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # dist/ 생성
npm run preview
```

## 테넌트 추가 (30초)
1. `config/examples/my-hospital.json` 복사 후 `hospitalId`, `name`, `phone`, `theme` 수정 (스키마 검증)
2. `?hospital=my-hospital` 로 프리뷰 확인
3. 프로덕션: `hospital-config.js` 치환 또는 `fetch('/config/examples/my-hospital.json')` 로 로드
4. 배포: `npm run build && npx wrangler pages deploy dist`

## 테마
`teal | navy | emerald` — `hospital-config.js` → `applyThemeToPreview()` 매핑

## 법무
- AI 트리아지는 **수의사 진단 대체 불가**. 모든 페이지 상단 disclaimer bar + 모달 + footer 면책 문구 포함.
- `privacy.html` / `terms.html` 필수. 보호자 증상 입력은 데모에선 서버 저장 없음.

## 배포
```bash
npx wrangler pages deploy dist --project-name=vet-animal-hospital
# 커스텀 도메인: vet-animal-hospital.net → Cloudflare Pages > Custom domain
```

## 로드맵
- P1: `/h/{hospitalId}` 라우팅, R2 이미지, jsPDF + QRCode 실제 생성
- P2: D1 + KV + Workers AI (진짜 분류 모델)
