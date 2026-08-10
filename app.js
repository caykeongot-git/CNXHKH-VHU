/* ==========================================================================
   APP.JS - HIGH PERFORMANCE LOGIC & STRICT GRID COLOR SCHEME ENGINE
   CHXHKH - VHU (300 CÂU TRẮC NGHIỆM)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // APP STATE
  const state = {
    allQuestions: [],
    displayedQuestions: [],
    examQuestions: [], // Shuffled questions for Exam Mode
    chapterFilter: 'all', // 'all' | 'c1'..'c7'
    mode: 'practice', // 'practice' | 'exam'
    showAnswers: true,
    autoNext: false,
    filter: 'all', // 'all' | 'unanswered' | 'wrong'
    userAnswers: {}, // { questionId: 'A'|'B'|'C'|'D' }
    wrongQuestions: new Set(),
    activeQuestionId: 1,
    
    // 20-Minute Exam Timer State
    examActive: false,
    examTimeTotal: 20 * 60, // 20 minutes in seconds
    examTimeRemaining: 20 * 60,
    examTimerInterval: null,
    
    // Custom Confirm Handler
    confirmOkCallback: null
  };

  // DOM ELEMENTS
  const els = {
    btnToggleTheme: document.getElementById('btnToggleTheme'),
    themeIcon: document.getElementById('themeIcon'),
    btnToggleMobileGrid: document.getElementById('btnToggleMobileGrid'),
    btnCloseDrawer: document.getElementById('btnCloseDrawer'),
    sidebarSection: document.getElementById('sidebarSection'),
    btnScrollTop: document.getElementById('btnScrollTop'),
    
    btnModePractice: document.getElementById('btnModePractice'),
    btnModeExam: document.getElementById('btnModeExam'),
    chapterSelect: document.getElementById('chapterSelect'),
    
    switchShowAnswersWrapper: document.getElementById('switchShowAnswersWrapper'),
    switchAutoNextWrapper: document.getElementById('switchAutoNextWrapper'),
    chkShowAnswers: document.getElementById('chkShowAnswers'),
    chkAutoNext: document.getElementById('chkAutoNext'),
    filterSelect: document.getElementById('filterSelect'),
    btnResetProgress: document.getElementById('btnResetProgress'),
    
    timerBadge: document.getElementById('timerBadge'),
    timerText: document.getElementById('timerText'),
    btnSubmitExam: document.getElementById('btnSubmitExam'),
    
    progressText: document.getElementById('progressText'),
    progressPercent: document.getElementById('progressPercent'),
    progressBarFill: document.getElementById('progressBarFill'),
    
    questionsContainer: document.getElementById('questionsContainer'),
    questionGrid: document.getElementById('questionGrid'),
    answerKeyGrid: document.getElementById('answerKeyGrid'),
    
    tabGrid: document.getElementById('tabGrid'),
    tabAnswerKey: document.getElementById('tabAnswerKey'),
    gridTabContent: document.getElementById('gridTabContent'),
    answerKeyTabContent: document.getElementById('answerKeyTabContent'),
    
    statTotal: document.getElementById('statTotal'),
    statCorrect: document.getElementById('statCorrect'),
    statWrong: document.getElementById('statWrong'),
    
    // Confirm Modal
    confirmModal: document.getElementById('confirmModal'),
    confirmTitle: document.getElementById('confirmTitle'),
    confirmMsg: document.getElementById('confirmMsg'),
    btnConfirmCancel: document.getElementById('btnConfirmCancel'),
    btnConfirmOk: document.getElementById('btnConfirmOk'),
    
    // Exam Result Modal
    resultModal: document.getElementById('resultModal'),
    btnCloseModal: document.getElementById('btnCloseModal'),
    scorePercent: document.getElementById('scorePercent'),
    scoreFraction: document.getElementById('scoreFraction'),
    resultMsg: document.getElementById('resultMsg'),
    timeSpentText: document.getElementById('timeSpentText'),
    correctCountText: document.getElementById('correctCountText'),
    wrongCountText: document.getElementById('wrongCountText'),
    unansweredCountText: document.getElementById('unansweredCountText'),
    btnReviewExam: document.getElementById('btnReviewExam'),
    btnRestartExam: document.getElementById('btnRestartExam')
  };

  // LOCAL STORAGE KEYS
  const STORAGE_KEY_ANSWERS = 'cnxhkh_vhu_user_answers';
  const STORAGE_KEY_WRONG = 'cnxhkh_vhu_wrong_questions';
  const STORAGE_KEY_THEME = 'cnxhkh_vhu_theme';
  const STORAGE_KEY_MODE = 'cnxhkh_vhu_mode';
  const STORAGE_KEY_CHAPTER = 'cnxhkh_vhu_chapter';
  const STORAGE_KEY_FILTER = 'cnxhkh_vhu_filter';
  const STORAGE_KEY_ACTIVE_Q = 'cnxhkh_vhu_active_q';
  const STORAGE_KEY_SHOW_ANS = 'cnxhkh_vhu_show_ans';
  const STORAGE_KEY_AUTO_NEXT = 'cnxhkh_vhu_auto_next';

  // HELPER: FISHER-YATES SHUFFLE ALGORITHM
  function shuffleArray(arr) {
    const array = [...arr];
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  // 1. INITIALIZATION & DATA LOADING
  async function init() {
    loadTheme();
    loadLocalStorageData();
    setupEventListeners();
    await fetchQuestionData();
  }

  async function fetchQuestionData() {
    try {
      const response = await fetch('data/cnxhkh_vhu.json');
      if (!response.ok) throw new Error('Không thể tải dữ liệu câu hỏi');
      state.allQuestions = data.questions || [];
      
      // Sanitize stored answers and wrong bookmarks if dataset size changed
      const maxId = state.allQuestions.length;
      Object.keys(state.userAnswers).forEach(idKey => {
        if (parseInt(idKey) > maxId) {
          delete state.userAnswers[idKey];
        }
      });
      state.wrongQuestions = new Set(Array.from(state.wrongQuestions).filter(id => id <= maxId));
      saveUserAnswers();
      saveWrongQuestions();
      
      // Sync UI elements with loaded state
      els.chapterSelect.value = state.chapterFilter;
      els.filterSelect.value = state.filter;
      els.chkShowAnswers.checked = state.showAnswers;
      els.chkAutoNext.checked = state.autoNext;

      switchMode(state.mode);
      
      // Auto-scroll to restore exact active question position after load
      setTimeout(() => {
        if (state.activeQuestionId) {
          scrollToQuestion(state.activeQuestionId);
        }
      }, 300);

    } catch (err) {
      console.error('Lỗi nạp dữ liệu:', err);
      els.questionsContainer.innerHTML = `
        <div class="explanation-box" style="border-left-color: var(--wrong-border);">
          <strong><i class="fa-solid fa-triangle-exclamation"></i> Lỗi:</strong> Không thể nạp dữ liệu 300 câu hỏi từ <code>data/cnxhkh_vhu.json</code>.
        </div>
      `;
    }
  }

  function loadLocalStorageData() {
    try {
      const savedAnswers = localStorage.getItem(STORAGE_KEY_ANSWERS);
      if (savedAnswers) state.userAnswers = JSON.parse(savedAnswers);
      
      const savedWrong = localStorage.getItem(STORAGE_KEY_WRONG);
      if (savedWrong) state.wrongQuestions = new Set(JSON.parse(savedWrong));

      const savedMode = localStorage.getItem(STORAGE_KEY_MODE);
      if (savedMode) state.mode = savedMode;

      const savedChapter = localStorage.getItem(STORAGE_KEY_CHAPTER);
      if (savedChapter) state.chapterFilter = savedChapter;

      const savedFilter = localStorage.getItem(STORAGE_KEY_FILTER);
      if (savedFilter) state.filter = savedFilter;

      const savedActiveQ = localStorage.getItem(STORAGE_KEY_ACTIVE_Q);
      if (savedActiveQ) state.activeQuestionId = parseInt(savedActiveQ, 10);

      const savedShowAns = localStorage.getItem(STORAGE_KEY_SHOW_ANS);
      if (savedShowAns !== null) state.showAnswers = savedShowAns === 'true';

      const savedAutoNext = localStorage.getItem(STORAGE_KEY_AUTO_NEXT);
      if (savedAutoNext !== null) state.autoNext = savedAutoNext === 'true';
    } catch (e) {
      console.error('Failed to load local storage:', e);
    }
  }

  function saveLocalStorageData() {
    try {
      localStorage.setItem(STORAGE_KEY_ANSWERS, JSON.stringify(state.userAnswers));
      localStorage.setItem(STORAGE_KEY_WRONG, JSON.stringify(Array.from(state.wrongQuestions)));
      localStorage.setItem(STORAGE_KEY_MODE, state.mode);
      localStorage.setItem(STORAGE_KEY_CHAPTER, state.chapterFilter);
      localStorage.setItem(STORAGE_KEY_FILTER, state.filter);
      localStorage.setItem(STORAGE_KEY_ACTIVE_Q, state.activeQuestionId);
      localStorage.setItem(STORAGE_KEY_SHOW_ANS, state.showAnswers);
      localStorage.setItem(STORAGE_KEY_AUTO_NEXT, state.autoNext);
    } catch (e) {
      console.error('Failed to save local storage:', e);
    }
  }

  // 2. GLACIER DARK ICE BLUE THEME DEFAULT
  function loadTheme() {
    const savedTheme = localStorage.getItem(STORAGE_KEY_THEME);
    if (savedTheme === 'light') {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light-mode');
      els.themeIcon.className = 'fa-solid fa-sun';
    } else {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light-mode');
      els.themeIcon.className = 'fa-solid fa-moon';
      localStorage.setItem(STORAGE_KEY_THEME, 'dark');
    }
  }

  function toggleTheme() {
    const isLight = document.documentElement.classList.toggle('light-mode');
    if (isLight) {
      document.documentElement.classList.remove('dark');
      els.themeIcon.className = 'fa-solid fa-sun';
      localStorage.setItem(STORAGE_KEY_THEME, 'light');
    } else {
      document.documentElement.classList.add('dark');
      els.themeIcon.className = 'fa-solid fa-moon';
      localStorage.setItem(STORAGE_KEY_THEME, 'dark');
    }
  }

  // 3. FILTERING & DYNAMIC CHAPTER RENDERING
  function applyFilter() {
    state.filter = els.filterSelect.value;
    state.chapterFilter = els.chapterSelect.value;
    
    saveLocalStorageData();

    // Step 1: Filter by Chapter
    let list = state.allQuestions;
    if (state.chapterFilter !== 'all') {
      list = list.filter(q => q.chapter_id === state.chapterFilter);
    }
    
    // Step 2: Filter by Status (in Practice mode)
    if (state.mode === 'practice') {
      if (state.filter === 'unanswered') {
        list = list.filter(q => !state.userAnswers[q.id]);
      } else if (state.filter === 'wrong') {
        list = list.filter(q => state.wrongQuestions.has(q.id));
      }
    }

    state.displayedQuestions = list;
    
    if (state.mode === 'exam') {
      generateExamQuestions();
    } else {
      const isStillAvailable = state.displayedQuestions.some(q => q.id === state.activeQuestionId);
      if (!isStillAvailable && state.displayedQuestions.length > 0) {
        state.activeQuestionId = state.displayedQuestions[0].id;
        saveLocalStorageData();
      }
    }

    renderQuestions();
    renderQuestionGrid();
    renderQuickAnswerKey();
    updateStatsAndProgress();
    updateWrongFilterLabel();
  }

  // GENERATE SHUFFLED REALISTIC EXAM QUESTIONS
  function generateExamQuestions() {
    let sourceList = state.allQuestions;
    if (state.chapterFilter !== 'all') {
      sourceList = state.allQuestions.filter(q => q.chapter_id === state.chapterFilter);
    }
    
    // 1. Shuffle question order 100% randomly
    const shuffledList = shuffleArray(sourceList).map((q, idx) => {
      // 2. Shuffle option order
      const keys = Object.keys(q.options);
      const shuffledKeys = shuffleArray(keys);
      const newOpts = {};
      
      const letters = ['A', 'B', 'C', 'D'];
      shuffledKeys.forEach((oldKey, i) => {
        newOpts[letters[i]] = q.options[oldKey];
      });

      const correctVal = q.options[q.correct_answer];
      const newCorrectKey = Object.keys(newOpts).find(k => newOpts[k] === correctVal);

      return {
        ...q,
        examIndex: idx + 1,
        options: newOpts,
        correct_answer: newCorrectKey
      };
    });

    state.examQuestions = shuffledList;
    state.userAnswers = {}; // Fresh answers for new exam
    
    if (state.examQuestions.length > 0) {
      state.activeQuestionId = state.examQuestions[0].id;
      saveLocalStorageData();
    }
  }

  function updateWrongFilterLabel() {
    const wrongCount = state.wrongQuestions.size;
    const wrongOpt = els.filterSelect.querySelector('option[value="wrong"]');
    if (wrongOpt) {
      wrongOpt.textContent = `Sổ tay câu sai (${wrongCount})`;
    }
  }

  function renderQuestions() {
    const listToRender = state.mode === 'exam' ? state.examQuestions : state.displayedQuestions;

    if (listToRender.length === 0) {
      els.questionsContainer.innerHTML = `
        <div class="question-card" style="text-align: center; padding: 40px 20px;">
          <i class="fa-solid fa-folder-open" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 12px;"></i>
          <h3>Không có câu hỏi nào phù hợp với bộ lọc</h3>
          <p class="text-muted" style="margin-top: 6px;">Hãy thử chọn lại Chương hoặc chọn bộ lọc "Tất cả câu".</p>
        </div>
      `;
      return;
    }

    const isPractice = state.mode === 'practice';

    els.questionsContainer.innerHTML = listToRender.map((q, idx) => {
      const userSel = state.userAnswers[q.id];
      const isWrongBookmarked = state.wrongQuestions.has(q.id);
      const isAnswered = !!userSel;
      const isCorrect = userSel === q.correct_answer;
      const isFocused = state.activeQuestionId === q.id;

      const displayNum = state.mode === 'exam' ? `Câu thi ${idx + 1} / ${listToRender.length}` : `Câu ${q.id} / 300`;
      const titleNum = state.mode === 'exam' ? (idx + 1) : q.id;

      return `
        <div class="question-card ${isFocused ? 'active-focused' : ''}" id="qcard-${q.id}" data-id="${q.id}">
          <div class="question-card-header">
            <span class="question-badge">
              <i class="fa-solid fa-circle-question"></i> ${displayNum}
            </span>
            <button class="wrong-bookmark-btn ${isWrongBookmarked ? 'active' : ''}" 
                    onclick="toggleWrongBookmark(${q.id}, event)" 
                    title="${isWrongBookmarked ? 'Bỏ lưu câu sai' : 'Lưu vào sổ tay câu sai'}">
              <i class="fa-${isWrongBookmarked ? 'solid' : 'regular'} fa-bookmark"></i>
            </button>
          </div>

          <div class="question-title">${titleNum}. ${escapeHtml(q.question)}</div>

          <div class="options-list">
            ${Object.entries(q.options).map(([key, val]) => {
              let optClass = 'option-item';
              if (userSel === key) optClass += ' selected';
              
              // In Practice Mode: reveal answers
              if (isPractice) {
                if (state.showAnswers) {
                  if (key === q.correct_answer) {
                    optClass += ' correct';
                  } else if (userSel === key && !isCorrect) {
                    optClass += ' wrong';
                  }
                } else if (isAnswered) {
                  if (key === q.correct_answer) {
                    optClass += ' correct';
                  } else if (userSel === key && !isCorrect) {
                    optClass += ' wrong';
                  }
                }
              }

              return `
                <div class="${optClass}" onclick="selectOption(${q.id}, '${key}')">
                  <span class="option-key">${key}</span>
                  <span class="option-text">${escapeHtml(val)}</span>
                </div>
              `;
            }).join('')}
          </div>

          ${((isAnswered || state.showAnswers) && isPractice && q.explanation) ? `
            <div class="explanation-box">
              <strong><i class="fa-solid fa-lightbulb"></i> Giải thích:</strong> ${escapeHtml(q.explanation)}
            </div>
          ` : ''}
        </div>
      `;
    }).join('');
  }

  // Render Bảng Số Câu Dynamically with Green for Correct and Red for Wrong in Practice Mode
  function renderQuestionGrid() {
    const isPractice = state.mode === 'practice';
    const listToRender = state.mode === 'exam' ? state.examQuestions : (state.displayedQuestions.length > 0 ? state.displayedQuestions : state.allQuestions);
    
    els.questionGrid.innerHTML = listToRender.map((q, idx) => {
      const userSel = state.userAnswers[q.id];
      let gridClass = 'grid-item';
      
      if (userSel) {
        if (isPractice) {
          gridClass += (userSel === q.correct_answer) ? ' correct' : ' wrong';
        } else {
          gridClass += ' answered';
        }
      }

      const gridLabel = state.mode === 'exam' ? (idx + 1) : q.id;

      return `
        <div class="${gridClass}" id="grid-${q.id}" onclick="scrollToQuestion(${q.id})">
          ${gridLabel}
        </div>
      `;
    }).join('');
  }

  // Render Bảng Đáp Án Nhanh Dynamically
  function renderQuickAnswerKey() {
    const listToRender = state.mode === 'exam' ? state.examQuestions : (state.displayedQuestions.length > 0 ? state.displayedQuestions : state.allQuestions);
    
    els.answerKeyGrid.innerHTML = listToRender.map((q, idx) => {
      const label = state.mode === 'exam' ? (idx + 1) : q.id;
      return `
        <div class="answer-key-item" onclick="scrollToQuestion(${q.id})">
          <span class="ak-num">${label}.</span>
          <span class="ak-ans">${q.correct_answer}</span>
        </div>
      `;
    }).join('');
  }

  // Update Stats & Progress Bar dynamically
  function updateStatsAndProgress() {
    const currentList = state.mode === 'exam' ? state.examQuestions : (state.displayedQuestions.length > 0 ? state.displayedQuestions : state.allQuestions);
    const totalCount = currentList.length;
    let answeredCount = 0;
    let correctCount = 0;
    let wrongCount = 0;

    currentList.forEach(q => {
      const userSel = state.userAnswers[q.id];
      if (userSel) {
        answeredCount++;
        if (userSel === q.correct_answer) correctCount++;
        else wrongCount++;
      }
    });

    els.statTotal.textContent = totalCount;
    els.statCorrect.textContent = correctCount;
    els.statWrong.textContent = wrongCount;

    const percent = totalCount > 0 ? Math.round((answeredCount / totalCount) * 100) : 0;
    els.progressText.textContent = `Đã làm: ${answeredCount} / ${totalCount}`;
    els.progressPercent.textContent = `${percent}%`;
    els.progressBarFill.style.width = `${percent}%`;
  }

  // 4. ACTIVE GLOWING BORDER & USER FOCUS
  function setActiveQuestionFocus(qId) {
    if (state.activeQuestionId === qId) return;
    
    const prevCard = document.getElementById(`qcard-${state.activeQuestionId}`);
    if (prevCard) prevCard.classList.remove('active-focused');
    
    state.activeQuestionId = qId;
    saveLocalStorageData();
    
    const curCard = document.getElementById(`qcard-${qId}`);
    if (curCard) curCard.classList.add('active-focused');
  }

  window.selectOption = function(qId, key) {
    state.userAnswers[qId] = key;
    setActiveQuestionFocus(qId);
    
    const currentList = state.mode === 'exam' ? state.examQuestions : state.allQuestions;
    const qObj = currentList.find(q => q.id === qId);
    
    if (qObj && key !== qObj.correct_answer) {
      state.wrongQuestions.add(qId);
    }

    saveLocalStorageData();
    updateWrongFilterLabel();
    updateStatsAndProgress();
    
    updateQuestionCardUI(qId);
    updateGridItemUI(qId);

    // Smooth auto-next logic in practice mode
    if (state.mode === 'practice' && state.autoNext) {
      setTimeout(() => {
        const nextId = qId + 1;
        if (nextId <= state.allQuestions.length) {
          scrollToQuestion(nextId);
        }
      }, 400);
    }
  };

  function updateQuestionCardUI(qId) {
    const qCard = document.getElementById(`qcard-${qId}`);
    if (!qCard) return;
    
    const currentList = state.mode === 'exam' ? state.examQuestions : state.allQuestions;
    const qObj = currentList.find(q => q.id === qId);
    if (!qObj) return;

    const userSel = state.userAnswers[qId];
    const isPractice = state.mode === 'practice';
    const isCorrect = userSel === qObj.correct_answer;

    const optionEls = qCard.querySelectorAll('.option-item');
    optionEls.forEach(optEl => {
      const keySpan = optEl.querySelector('.option-key');
      if (!keySpan) return;
      const key = keySpan.textContent.trim();

      optEl.className = 'option-item';
      if (userSel === key) optEl.classList.add('selected');

      if (isPractice) {
        if (state.showAnswers) {
          if (key === qObj.correct_answer) {
            optEl.classList.add('correct');
          } else if (userSel === key && !isCorrect) {
            optEl.classList.add('wrong');
          }
        } else if (userSel) {
          if (key === qObj.correct_answer) {
            optEl.classList.add('correct');
          } else if (userSel === key && !isCorrect) {
            optEl.classList.add('wrong');
          }
        }
      }
    });
  }

  function updateGridItemUI(qId) {
    const gridItem = document.getElementById(`grid-${qId}`);
    if (!gridItem) return;
    
    const currentList = state.mode === 'exam' ? state.examQuestions : state.allQuestions;
    const qObj = currentList.find(q => q.id === qId);
    if (!qObj) return;

    const userSel = state.userAnswers[qId];
    gridItem.className = 'grid-item';

    if (userSel) {
      if (state.mode === 'practice') {
        gridItem.classList.add(userSel === qObj.correct_answer ? 'correct' : 'wrong');
      } else {
        gridItem.classList.add('answered');
      }
    }
  }

  window.toggleWrongBookmark = function(qId, event) {
    if (event) event.stopPropagation();
    
    if (state.wrongQuestions.has(qId)) {
      state.wrongQuestions.delete(qId);
    } else {
      state.wrongQuestions.add(qId);
    }
    saveLocalStorageData();
    updateWrongFilterLabel();
    
    const qCard = document.getElementById(`qcard-${qId}`);
    if (qCard) {
      const bookmarkBtn = qCard.querySelector('.wrong-bookmark-btn');
      if (bookmarkBtn) {
        const isNowBookmarked = state.wrongQuestions.has(qId);
        bookmarkBtn.className = `wrong-bookmark-btn ${isNowBookmarked ? 'active' : ''}`;
        bookmarkBtn.innerHTML = `<i class="fa-${isNowBookmarked ? 'solid' : 'regular'} fa-bookmark"></i>`;
      }
    }
  };

  window.scrollToQuestion = function(qId) {
    setActiveQuestionFocus(qId);
    
    const currentList = state.mode === 'exam' ? state.examQuestions : state.displayedQuestions;
    const isDisplayed = currentList.some(q => q.id === qId);
    
    if (!isDisplayed) {
      els.chapterSelect.value = 'all';
      els.filterSelect.value = 'all';
      applyFilter();
    }

    const qCard = document.getElementById(`qcard-${qId}`);
    if (qCard) {
      qCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    els.sidebarSection.classList.remove('open');
  };

  // 5. MODE SWITCHING & 20-MIN EXAM TIMER
  function switchMode(newMode) {
    state.mode = newMode;
    saveLocalStorageData();

    if (newMode === 'practice') {
      els.btnModePractice.classList.add('active');
      els.btnModeExam.classList.remove('active');
      
      if (els.switchShowAnswersWrapper) els.switchShowAnswersWrapper.style.display = 'flex';
      if (els.switchAutoNextWrapper) els.switchAutoNextWrapper.style.display = 'flex';
      
      els.timerBadge.classList.add('hidden');
      els.btnSubmitExam.classList.add('hidden');
      els.timerBadge.style.display = 'none';
      els.btnSubmitExam.style.display = 'none';
      
      stopExamTimer();
      applyFilter();
    } else {
      els.btnModePractice.classList.remove('active');
      els.btnModeExam.classList.add('active');
      
      // Hide ALL practice switches during exam
      if (els.switchShowAnswersWrapper) els.switchShowAnswersWrapper.style.display = 'none';
      if (els.switchAutoNextWrapper) els.switchAutoNextWrapper.style.display = 'none';
      
      // Force timer & submit buttons visible on header
      els.timerBadge.classList.remove('hidden');
      els.btnSubmitExam.classList.remove('hidden');
      els.timerBadge.style.display = 'inline-flex';
      els.btnSubmitExam.style.display = 'inline-flex';
      
      startExamMode();
    }
  }

  function startExamMode() {
    state.examActive = true;
    state.examTimeTotal = 20 * 60; // 20 minutes countdown
    state.examTimeRemaining = state.examTimeTotal;
    
    els.timerBadge.classList.remove('hidden');
    els.btnSubmitExam.classList.remove('hidden');
    els.timerBadge.style.display = 'inline-flex';
    els.btnSubmitExam.style.display = 'inline-flex';
    
    // Generate shuffled questions for exam
    generateExamQuestions();
    renderQuestions();
    renderQuestionGrid();
    renderQuickAnswerKey();
    updateStatsAndProgress();
    
    updateTimerDisplay();
    
    if (state.examTimerInterval) clearInterval(state.examTimerInterval);
    state.examTimerInterval = setInterval(() => {
      state.examTimeRemaining--;
      updateTimerDisplay();
      if (state.examTimeRemaining <= 0) {
        stopExamTimer();
        submitExam();
      }
    }, 1000);
  }

  function stopExamTimer() {
    if (state.examTimerInterval) {
      clearInterval(state.examTimerInterval);
      state.examTimerInterval = null;
    }
  }

  function updateTimerDisplay() {
    const mins = Math.floor(state.examTimeRemaining / 60);
    const secs = state.examTimeRemaining % 60;
    els.timerText.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function submitExam() {
    stopExamTimer();
    
    const targetQuestions = state.examQuestions;
    const total = targetQuestions.length;
    let correct = 0;
    let wrong = 0;
    let unanswered = 0;

    targetQuestions.forEach(q => {
      const userSel = state.userAnswers[q.id];
      if (!userSel) {
        unanswered++;
      } else if (userSel === q.correct_answer) {
        correct++;
      } else {
        wrong++;
        state.wrongQuestions.add(q.id);
      }
    });

    saveLocalStorageData();
    updateWrongFilterLabel();

    const percent = total > 0 ? Math.round((correct / total) * 100) : 0;
    const timeSpentSecs = state.examTimeTotal - state.examTimeRemaining;
    const spentMins = Math.floor(timeSpentSecs / 60);
    const spentSecs = timeSpentSecs % 60;

    els.scorePercent.textContent = `${percent}%`;
    els.scoreFraction.textContent = `${correct}/${total} câu đúng`;
    els.correctCountText.textContent = correct;
    els.wrongCountText.textContent = wrong;
    els.unansweredCountText.textContent = unanswered;
    els.timeSpentText.textContent = `${spentMins} phút ${spentSecs} giây`;

    if (percent >= 80) {
      els.resultMsg.textContent = '🎉 Xuất sắc! Bạn đã sẵn sàng đạt điểm A+!';
    } else if (percent >= 50) {
      els.resultMsg.textContent = '👍 Khá tốt! Hãy ôn lại các câu làm sai để đạt kết quả cao hơn.';
    } else {
      els.resultMsg.textContent = '💪 Cố gắng lên! Hãy cày thêm Sổ tay câu sai nhé.';
    }

    els.resultModal.classList.remove('hidden');
  }

  // CUSTOM CONFIRMATION MODAL HANDLER
  function showCustomConfirm(title, msg, onOk) {
    els.confirmTitle.textContent = title;
    els.confirmMsg.textContent = msg;
    state.confirmOkCallback = onOk;
    els.confirmModal.classList.remove('hidden');
  }

  function resetProgress() {
    showCustomConfirm(
      'Xác nhận làm lại bài?',
      'Toàn bộ đáp án đã làm sẽ bị xoá để bạn bắt đầu làm lại từ đầu.',
      () => {
        state.userAnswers = {};
        saveLocalStorageData();
        if (state.mode === 'exam') {
          startExamMode();
        } else {
          applyFilter();
        }
      }
    );
  }

  // 6. EVENT LISTENERS
  function setupEventListeners() {
    els.btnToggleTheme.addEventListener('click', toggleTheme);
    
    els.btnToggleMobileGrid.addEventListener('click', () => {
      els.sidebarSection.classList.toggle('open');
    });
    
    els.btnCloseDrawer.addEventListener('click', () => {
      els.sidebarSection.classList.remove('open');
    });

    // Sidebar Tabs (Grid vs Quick Answer Sheet)
    els.tabGrid.addEventListener('click', () => {
      els.tabGrid.classList.add('active');
      els.tabAnswerKey.classList.remove('active');
      els.gridTabContent.classList.remove('hidden');
      els.answerKeyTabContent.classList.add('hidden');
    });

    els.tabAnswerKey.addEventListener('click', () => {
      els.tabAnswerKey.classList.add('active');
      els.tabGrid.classList.remove('active');
      els.answerKeyTabContent.classList.remove('hidden');
      els.gridTabContent.classList.add('hidden');
    });

    // Scroll-to-top visibility listener
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        els.btnScrollTop.classList.remove('hidden');
      } else {
        els.btnScrollTop.classList.add('hidden');
      }
    }, { passive: true });

    els.btnScrollTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    els.btnModePractice.addEventListener('click', () => switchMode('practice'));
    els.btnModeExam.addEventListener('click', () => switchMode('exam'));

    els.chapterSelect.addEventListener('change', applyFilter);
    els.filterSelect.addEventListener('change', applyFilter);

    els.chkShowAnswers.addEventListener('change', (e) => {
      state.showAnswers = e.target.checked;
      saveLocalStorageData();
      renderQuestions();
      renderQuestionGrid();
    });

    els.chkAutoNext.addEventListener('change', (e) => {
      state.autoNext = e.target.checked;
      saveLocalStorageData();
    });

    els.btnResetProgress.addEventListener('click', resetProgress);
    
    // Custom Confirm Modal buttons
    els.btnConfirmCancel.addEventListener('click', () => els.confirmModal.classList.add('hidden'));
    els.btnConfirmOk.addEventListener('click', () => {
      els.confirmModal.classList.add('hidden');
      if (state.confirmOkCallback) state.confirmOkCallback();
    });

    els.btnSubmitExam.addEventListener('click', () => {
      showCustomConfirm(
        'Xác nhận nộp bài thi?',
        'Bạn có chắc chắn muốn nộp bài thi thử và chấm điểm ngay bây giờ?',
        () => submitExam()
      );
    });

    // Exam Result Modal controls
    els.btnCloseModal.addEventListener('click', () => els.resultModal.classList.add('hidden'));
    els.btnReviewExam.addEventListener('click', () => {
      els.resultModal.classList.add('hidden');
      state.showAnswers = true;
      els.chkShowAnswers.checked = true;
      saveLocalStorageData();
      renderQuestions();
      renderQuestionGrid();
    });
    els.btnRestartExam.addEventListener('click', () => {
      els.resultModal.classList.add('hidden');
      startExamMode();
    });
  }

  // HELPER FUNCTION
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // START APP
  init();
});
