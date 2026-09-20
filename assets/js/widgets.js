/**
 * =======================================================================
 * VetLink AI (동물병원 홈페이지 구축 서비스)
 * - 장애인 접근 편의 도구 (접근성 툴바)
 * - FAQ 자동응답 챗봇 위젯
 * 0-Server · 순수 순정 JS · 단독 정적 호스팅에서도 동작
 * =======================================================================
 */
(function () {
  'use strict';

  var DOC = document;
  var root = DOC.documentElement;
  var cfg = window.__VETLINK_CONFIG__ || {};
  var PHONE = cfg.phone || '010-5407-5708';
  var HOTLINE = cfg.phone || '010-5407-5708';

  DOC.addEventListener('vetlink:config-ready', function (e) {
    var d = (e && e.detail) || {};
    if (d.phone) { PHONE = d.phone; HOTLINE = d.phone; }
  });

  /* ------------------------------------------------------------------
   * 공통 유틸리티
   * ---------------------------------------------------------------- */
  function $(sel, ctx) { return (ctx || DOC).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || DOC).querySelectorAll(sel)); }

  var toastTimer = null;
  function toast(msg) {
    var el = DOC.createElement('div');
    el.className = 'acc-toast';
    el.setAttribute('role', 'status');
    el.textContent = msg;
    DOC.body.appendChild(el);
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      if (el && el.parentNode) el.parentNode.removeChild(el);
    }, 2600);
  }

  /* ------------------------------------------------------------------
   * 장애인 접근 편의 상태 관리 (localStorage 영속)
   * ---------------------------------------------------------------- */
  var STORE_KEY = 'vetlink_acc_state_v1';
  var DEFAULTS = {
    zoom: 0,          // 0=100%, 1=110%, 2=120%, 3=135%
    contrast: false,
    invert: false,
    gray: false,
    cursor: false,
    letter: false,
    line: false,
    guide: false
  };

  function readState() {
    var s = {};
    try { s = JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch (e) { s = {}; }
    var out = {};
    for (var k in DEFAULTS) {
      if (DEFAULTS.hasOwnProperty(k)) out[k] = (s[k] !== undefined) ? s[k] : DEFAULTS[k];
    }
    return out;
  }
  function saveState(state) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  var state = readState();
  var accPanel = $('#accPanel');
  var accFab = $('#accFab');

  var TOGGLE_KEYS = ['contrast', 'invert', 'gray', 'cursor', 'letter', 'line'];

  function applyState() {
    for (var z = 0; z <= 3; z++) root.classList.toggle('acc-zoom-' + z, state.zoom === z);
    TOGGLE_KEYS.forEach(function (k) { root.classList.toggle('acc-' + k, !!state[k]); });
    renderGuide();
    $all('[data-acc]').forEach(function (btn) {
      var act = btn.getAttribute('data-acc');
      var on = false;
      if (TOGGLE_KEYS.indexOf(act) !== -1) on = !!state[act];
      btn.classList.toggle('on', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  function setZoom(delta) {
    state.zoom = Math.max(0, Math.min(3, (state.zoom || 0) + delta));
    applyState(); saveState(state);
    if (state.zoom === 0) toast('글자 크기 초기화');
    else toast('글자 크기 ' + ['110%', '120%', '135%'][state.zoom - 1] + ' 적용');
  }

  function resetZoom() {
    state.zoom = 0;
    applyState(); saveState(state);
    toast('글자 크기 초기화');
  }

  function toggleFeature(key) {
    state[key] = !state[key];
    applyState(); saveState(state);
    toast(featureName(key) + (state[key] ? ' 켜짐' : ' 꺼짐'));
  }

  function toggleGuide() {
    state.guide = !state.guide;
    applyState(); saveState(state);
    toast('줄 가이드 ' + (state.guide ? '켜짐' : '꺼짐'));
  }

  function featureName(key) {
    var names = {
      contrast: '고대비 모드',
      invert: '색상 반전',
      gray: '흑백 모드',
      cursor: '큰 커서',
      letter: '글자 간격 확대',
      line: '줄 간격 확대'
    };
    return names[key] || key;
  }

  function resetAll() {
    stopReading();
    for (var k in DEFAULTS) state[k] = DEFAULTS[k];
    for (var z = 0; z <= 3; z++) root.classList.remove('acc-zoom-' + z);
    TOGGLE_KEYS.forEach(function (k) { root.classList.remove('acc-' + k); });
    hideGuide();
    applyState(); saveState(state);
    toast('접근 편의 설정 초기화 완료');
  }

  /* ------------------------------------------------------------------
   * 읽기 가이드 (줄 가이드)
   * ---------------------------------------------------------------- */
  var guideEl = $('#accGuide');
  function renderGuide() {
    if (!guideEl) return;
    guideEl.hidden = !state.guide;
    if (state.guide) root.style.setProperty('--acc-gy', '40px');
  }
  function hideGuide() {
    if (guideEl) guideEl.hidden = true;
  }
  if (guideEl) {
    DOC.addEventListener('mousemove', function (e) {
      if (!state.guide) return;
      root.style.setProperty('--acc-gy', (e.clientY - 24) + 'px');
    });
  }

  /* ------------------------------------------------------------------
   * 읽어주기 (TTS 음성 안내)
   * ---------------------------------------------------------------- */
  var synth = ('speechSynthesis' in window) ? window.speechSynthesis : null;
  var reading = { on: false, paused: false, queue: [], idx: 0, current: null };
  var ttsStateEl = $('#accTtsState');

  function textCandidates() {
    var roots = [];
    var main = $('#main-content');
    if (main) roots.push(main);
    var foot = $('footer');
    if (foot) roots.push(foot);

    var parts = [];
    // 음성 엔진이 긴 문장을 잘라내는 브라우저가 있어 240자 단위로 청크 분리
    function chunk(el, txt) {
      while (txt.length > 240) {
        var cut = txt.lastIndexOf(' ', 240);
        var at = cut > 120 ? cut : 240;
        parts.push({ el: el, text: txt.slice(0, at).trim() });
        txt = txt.slice(at).trim();
      }
      if (txt) parts.push({ el: el, text: txt });
    }
    roots.forEach(function (r) {
      $all('h1, h2, h3, h4, h5, p, li, td, th, blockquote, dt, dd, figcaption, label', r).forEach(function (el) {
        if (el.getAttribute('aria-hidden') === 'true') return;
        if (el.closest('[data-acc-skip]')) return;
        var rect = el.getBoundingClientRect();
        if (!rect || (!rect.width && !rect.height)) return;
        var txt = (el.textContent || '').trim();
        if (txt.length < 2) return;
        chunk(el, txt);
      });
    });
    return parts;
  }

  function startReading() {
    if (reading.on) { stopReading(); return; }
    if (!synth) { toast('이 브라우저는 음성 읽기를 지원하지 않습니다.'); return; }

    var parts = textCandidates();
    if (!parts.length) { toast('읽을 내용이 없습니다.'); return; }

    var midY = window.innerHeight * 0.35;
    var start = 0;
    for (var i = 0; i < parts.length; i++) {
      if (parts[i].el.getBoundingClientRect().bottom >= midY) { start = i; break; }
    }

    reading.queue = parts;
    reading.idx = start;
    reading.on = true;
    reading.paused = false;
    if (ttsStateEl) ttsStateEl.hidden = false;
    setStateText('화면 내용을 차례로 읽어드립니다');
    syncTtsBtn(true);
    speakNext();
  }

  function speakNext() {
    if (!reading.on) return;
    if (reading.idx >= reading.queue.length) {
      stopReading(true);
      toast('전체 읽기를 마쳤습니다');
      return;
    }
    var item = reading.queue[reading.idx];
    var el = item.el;
    clearSpeaking();
    el.classList.add('acc-speaking');
    reading.current = el;
    var r = el.getBoundingClientRect();
    if (r.top < 0 || r.bottom > window.innerHeight) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    setStateText(('읽는 중: ' + el.textContent.trim()).slice(0, 40) + '…');

    var u = new SpeechSynthesisUtterance(item.text);
    u.lang = 'ko-KR';
    u.rate = 0.95;
    u.pitch = 1;
    u.onend = function () { reading.idx++; speakNext(); };
    u.onerror = function () { reading.idx++; speakNext(); };
    synth.speak(u);
  }

  function clearSpeaking() {
    if (reading.current) {
      reading.current.classList.remove('acc-speaking');
      reading.current = null;
    }
  }

  function stopReading(quiet) {
    if (synth) synth.cancel();
    clearSpeaking();
    reading.on = false;
    reading.paused = false;
    reading.queue = [];
    reading.idx = 0;
    if (ttsStateEl) ttsStateEl.hidden = true;
    syncTtsBtn(false);
    if (!quiet) toast('읽어주기를 중지했습니다');
  }

  function togglePauseReading() {
    if (!reading.on || !synth) return;
    if (reading.paused) {
      synth.resume();
      reading.paused = false;
      setStateText('계속 읽기');
    } else {
      synth.pause();
      reading.paused = true;
      setStateText('일시정지됨 · 재생 버튼으로 계속');
    }
  }

  function setStateText(txt) {
    var t = $('#accTtsText');
    if (t) t.textContent = txt;
  }

  function syncTtsBtn(on) {
    var b = $('[data-acc="tts"]');
    if (!b) return;
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
  }

  /* ------------------------------------------------------------------
   * 위젯 열기/닫기
   * ---------------------------------------------------------------- */
  function closePanel(panel, fab) {
    panel.hidden = true;
    if (fab) fab.setAttribute('aria-expanded', 'false');
  }
  function openPanel(panel, fab) {
    panel.hidden = false;
    if (fab) fab.setAttribute('aria-expanded', 'true');
  }
  function togglePanel(panel, fab) {
    if (panel.hidden) openPanel(panel, fab); else closePanel(panel, fab);
  }

  /* ------------------------------------------------------------------
   * 챗봇 (FAQ 자동응답)
   * ---------------------------------------------------------------- */
  var KB = [
    {
      id: 'free-kit',
      keys: ['무상', '무료', '가격', '비용', '얼마', '세팅', '신청', '키트', '조건', '공급', '비파트너', '50만', '500000', '도입'],
      answer: '파트너 무상 키트 조건을 안내드릴게요.\n\n' +
        '· 몬스멕타 정기공급 파트너 동물병원에는 홈페이지 + 24시 트리아지 + 요약서 + 카운터 QR 알림판까지 <strong>운영키트 1식을 무상 세팅</strong>해 드립니다.\n' +
        '· 비파트너 병원 제작은 별도 유상(50만원)이며, 현재는 파트너 병원 도입이 우선입니다.\n\n' +
        '신청을 원하시면 아래 구간의 신청 폼을 작성하시거나 전화 <a href="tel:' + PHONE + '">' + PHONE + '</a> 로 문의해 주세요.',
      chips: ['신청 절차 알려주세요', '몬스멕타 파트너 문의', '전화 문의']
    },
    {
      id: 'monsmecta',
      keys: ['몬스멕타', 'mon', '파트너', '정기', '소화', '제약'],
      answer: '몬스멕타 파트너 프로그램을 안내드릴게요.\n\n' +
        '몬스멕타(Monsmecta) 등 검증된 수의 처방 소화기 의약품을 <strong>정기 공급받는 병원</strong>에 한해 VetLink 스마트 포털 운영키트를 무상으로 세팅해 드립니다.\n\n' +
        '· 복약 상담 시스템·치방 길드와 원내 처방 품목 가치를 동시에 높이는 구조입니다.\n' +
        '· 공급 문의: 전화 <a href="tel:' + PHONE + '">' + PHONE + '</a>',
      chips: ['무상 키트 조건', '신청 절차 알려주세요', '전화 문의']
    },
    {
      id: 'portal',
      keys: ['홈페이지', '포털', '도메인', '연결', 'hospital', '제작', '사이트', '주소', '운영키트'],
      answer: '병원 전용 홈페이지(포털) 관련 안내입니다.\n\n' +
        '· 병원명·지역·진료과목·전화번호만 설정하면 병원 전용 모바일 웹 포털이 즉시 생성됩니다.\n' +
        '· 도메인 연결 및 카운터 A4 알림판 세팅까지 지원합니다.\n' +
        '· 파트너 병원은 <strong>무상 세팅</strong>, 약 공급 중단 시에도 홈페이지 소유권은 병원에 그대로 남습니다.\n\n' +
        '실제 모습은 위 「실시간 체험 스튜디오」에서 바로 미리보기하실 수 있습니다.',
      chips: ['무상 키트 조건', 'AI 트리아지 설명', '전화 문의']
    },
    {
      id: 'triage',
      keys: ['문진', '트리아지', 'triage', 'ai', '증상', '사전', '요약서', '차트', 'soap'],
      answer: 'AI 트리아지·사전 문진을 안내드릴게요.\n\n' +
        '밤에 보호자가 증상을 입력하면 수의학 규칙 기반 알고리즘이 <strong>RED/ORANGE/GREEN 4단계 응급도</strong>를 분류하고 대처 가이드를 안내합니다.\n' +
        '다음날 진료실에서는 보호자 입력이 <strong>A4 요약서 1장</strong>으로 자동 정리되어 상담이 3분이면 끝납니다.\n\n' +
        '본 서비스는 수의사 진단을 대체하지 않으며 응급 시 즉시 대면 내원을 안내합니다.',
      chips: ['A4 알림판 & QR 설명', '원장 상담 신청', '무상 키트 조건']
    },
    {
      id: 'poster',
      keys: ['알림판', 'qr', '카운터', '인쇄', '포스터'],
      answer: '카운터 A4 알림판·QR 포털 안내입니다.\n\n' +
        '병원명과 전화번호만 넣으면 <strong>원내 프린터로 바로 인쇄할 수 있는 A4 안내판</strong>과 병원 전용 브랜디드 QR코드를 자동 생성해 드립니다.\n' +
        '보호자가 스마트폰 짐으로 QR을 비추면 병원 맞춤 포털이 1초 만에 열립니다 (앱 설치 불필요).',
      chips: ['AI 트리아지 설명', '무상 키트 조건', '전화 문의']
    },
    {
      id: 'phone',
      keys: ['전화', '번호', '연락', '문의', '상담', '직통', '콜'],
      answer: '상담 연결 번호를 안내드릴게요.\n\n' +
        '· 직통 상담: <a href="tel:' + PHONE + '">' + PHONE + '</a>\n' +
        '· 운영: 평일 09:30 ~ 18:30\n\n' +
        '파트너 신청·세팅 문의는 아래 번호로 편하게 연락 주세요.',
      chips: ['무상 키트 조건', '신청 절차 알려주세요', '상담 시간 안내']
    },
    {
      id: 'hours',
      keys: ['시간', '운영', '평일', '몇시', '몇 시', '주말', '공휴일'],
      answer: '상담·운영 시간을 안내드릴게요.\n\n' +
        '· 직통 상담: 평일 09:30 ~ 18:30 (점심시간 문의는 유선 남겨주시면 순차 연락드립니다.)\n' +
        '· 온라인 미리보기 스튜디오와 AI 트리아지 시뮬레이터는 <strong>24시간 연중무휴</strong> 운영 중입니다.',
      chips: ['전화 문의', '무상 키트 조건']
    },
    {
      id: 'emergency',
      keys: ['긴급', '응급', '경련', '호흡곤란', '호흡 곤란', '숨', '출혈', '쓰러', '위험', '혔변'],
      answer: '⚠️ 반려동물 긴급 상황입니다. 온라인 상담에 의존하지 마시고 즉시 조치해 주세요.\n\n' +
        '호흡곤란·경련·다량 출혈 등 위급 증상은 즉시 <strong>가까운 24시 동물병원</strong>으로 대면 내원해 주십시오.\n\n' +
        '이동 중 병원 안내가 필요하시면 긴급 상담 <a href="tel:' + HOTLINE + '">' + HOTLINE + '</a> 으로 연락해 주세요.',
      chips: ['원장님 상담 신청', '전화 문의']
    },
    {
      id: 'privacy',
      keys: ['개인정보', '약관', '이용약관', '방침', '정책'],
      answer: '개인정보·약관 안내입니다.\n\n' +
        '페이지 하단의 <a href="./privacy.html">개인정보처리방침</a>과 <a href="./terms.html">이용약관 및 의료 면책고지</a>에서 전문을 확인하실 수 있습니다.',
      chips: ['무상 키트 조건', '전화 문의']
    },
    {
      id: 'welcome',
      keys: ['안녕', '반가워', '하이', 'hi', 'hello', '반갑', '고마워'],
      answer: '안녕하세요! 🐾 VetLink AI 파트너 상담 도우미입니다.\n' +
        '동물병원 홈페이지 구축·AI 문진·무상 세팅 관련 궁금하신 점을 편하게 물어봐 주세요.\n' +
        '(예: 무상 키트 조건, 신청 절차, AI 트리아지, A4 알림판)',
      chips: ['무상 키트 조건', '신청 절차 알려주세요', 'AI 트리아지 설명', '전화 문의']
    }
  ];

  var FALLBACK = {
    id: 'fallback',
    answer: '죄송합니다. 자주 묻는 질문에 없는 내용이라 정확한 답변이 어렵습니다. 🙏\n\n' +
      '· 통화 상담: <a href="tel:' + PHONE + '">' + PHONE + '</a>\n' +
      '· 운영: 평일 09:30 ~ 18:30\n\n' +
      '담당자가 빠르게 도와드릴 수 있도록 아래 버튼을 눌러주세요.',
    chips: ['무상 키트 조건', '신청 절차 알려주세요', 'AI 트리아지 설명', '전화 문의']
  };

  var QUICK_START = ['무상 키트 조건', '신청 절차 알려주세요', 'AI 트리아지 설명', 'A4 알림판 & QR', '전화 문의', '반려동물 긴급 증상은?'];

  function normalize(txt) {
    return String(txt || '').toLowerCase().replace(/[\s\u00a0]/g, '').replace(/[.,!?~·\-_+=:;'"()\[\]{}<>/\\@#$%^&*|]/g, '');
  }

  function kbMatch(input) {
    var ni = normalize(input);
    var best = null;
    var bestScore = 0;
    KB.forEach(function (entry) {
      var score = 0;
      entry.keys.forEach(function (kw) {
        var nk = normalize(kw);
        if (nk && ni.indexOf(nk) !== -1) score += nk.length;
      });
      if (score > bestScore) {
        bestScore = score;
        best = entry;
      }
    });
    return bestScore > 0 ? best : null;
  }

  var chatPanel = $('#chatPanel');
  var chatFab = $('#chatFab');
  var chatBody = $('#chatMessages');
  var chatChips = $('#chatChips');
  var chatForm = $('#chatForm');
  var chatInput = $('#chatInput');
  var greeted = false;

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function addMessage(html, who) {
    var wrap = DOC.createElement('div');
    wrap.className = 'chat-msg ' + who;
    wrap.innerHTML = html;
    chatBody.appendChild(wrap);
    chatBody.scrollTop = chatBody.scrollHeight;
    return wrap;
  }

  function renderChips(list) {
    chatChips.innerHTML = '';
    (list || []).forEach(function (chip) {
      var b = DOC.createElement('button');
      b.type = 'button';
      b.className = 'chat-chip';
      b.textContent = chip;
      b.setAttribute('aria-label', '질문: ' + chip);
      b.addEventListener('click', function () { sendChat(chip); });
      chatChips.appendChild(b);
    });
  }

  function sendChat(text) {
    var t = (text || '').trim();
    if (!t) return;
    addMessage(escapeHtml(t), 'user');
    chatInput.value = '';
    renderChips([]);

    var typing = addMessage('답변 입력 중…', 'bot typing');

    setTimeout(function () {
      var target = kbMatch(text);
      typing.classList.remove('typing');
      typing.innerHTML = target ? target.answer : FALLBACK.answer;
      typing.classList.add('bot');
      renderChips(target ? target.chips : FALLBACK.chips);
    }, 520);
  }

  function openChat() {
    chatPanel.hidden = false;
    chatFab.setAttribute('aria-expanded', 'true');
    if (!greeted) {
      greeted = true;
      addMessage('안녕하세요! 🐾 VetLink AI 파트너 상담(Q&A) 도우미입니다.<div class="chat-mute-author">궁금한 점을 입력하거나 아래 버튼을 눌러주세요.</div>', 'bot');
      renderChips(QUICK_START);
    }
    setTimeout(function () { if (chatInput) chatInput.focus(); }, 60);
  }
  function closeChat() {
    chatPanel.hidden = true;
    chatFab.setAttribute('aria-expanded', 'false');
  }

  /* ------------------------------------------------------------------
   * 이벤트 바인딩
   * ---------------------------------------------------------------- */
  function bindAll() {
    if (!accPanel) return;

    accPanel.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-acc]') : null;
      if (!btn) return;
      var act = btn.getAttribute('data-acc');
      switch (act) {
        case 'text-up': setZoom(1); break;
        case 'text-down': setZoom(-1); break;
        case 'text-reset': resetZoom(); break;
        case 'tts': startReading(); break;
        case 'guide': toggleGuide(); break;
        case 'reset-all': resetAll(); break;
        default:
          if (TOGGLE_KEYS.indexOf(act) !== -1) toggleFeature(act);
      }
    });

    var cBtn = $('[data-acc-close]');
    if (cBtn) cBtn.addEventListener('click', function () { closePanel(accPanel, accFab); });

    if (accFab) {
      accFab.addEventListener('click', function () { togglePanel(accPanel, accFab); });
    }
    DOC.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && accPanel && !accPanel.hidden) closePanel(accPanel, accFab);
    });

    var pBtn = $('#accPauseBtn');
    var sBtn = $('#accStopBtn');
    if (pBtn) pBtn.addEventListener('click', togglePauseReading);
    if (sBtn) sBtn.addEventListener('click', function () { stopReading(); });

    if (chatFab) {
      chatFab.addEventListener('click', function () {
        if (chatPanel.hidden) openChat(); else closeChat();
      });
    }
    if (chatForm) {
      chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        sendChat(chatInput.value);
      });
    }
    var cClose = $('[data-chat-close]');
    if (cClose) cClose.addEventListener('click', closeChat);
    if (chatPanel) {
      chatPanel.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.stopPropagation(); closeChat(); }
      });
    }

    DOC.addEventListener('click', function (e) {
      var t = e.target;
      if (accPanel && !accPanel.hidden && accFab && !accPanel.contains(t) && !accFab.contains(t)) {
        closePanel(accPanel, accFab);
      }
      if (chatPanel && !chatPanel.hidden && chatFab && !chatPanel.contains(t) && !chatFab.contains(t)) {
        closeChat();
      }
    });
  }

  applyState();
  bindAll();
})();