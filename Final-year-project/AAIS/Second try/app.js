/* ================================================
   AAIS — AUSU Academic Intelligence System
   app.js — Auth · Chat · Questions · AI Engine
   ================================================ */

'use strict';

// ─── CONFIG ──────────────────────────────────────
// To use real AI: set your Anthropic API key here.
// Leave empty to use the built-in offline knowledge base.
const CONFIG = {
  API_KEY: '',                // Optional: your Anthropic API key
  MODEL:   'claude-sonnet-4-20250514',
  MAX_TOKENS: 600,
  STORAGE_PREFIX: 'aais_',
};

// ─── UNIVERSITY KNOWLEDGE BASE ───────────────────
const UNIVERSITY = {
  name:         'Al_isiqama University Sumaila (AUSU)',
  abbreviation: 'AUSU',
  established:  1987,
  location:     'Kano State, Nigeria',
  motto:        '"ilimi d nagarta"',
  website:      'www.ausu.edu.ng',
  type:         'Public State University',
  affiliation:  'National Universities Commission (NUC)',
  studentPop:   'Approximately 2,000 students',
  staffCount:   'Over 200 academic and non-academic staff',

  currentVC: {
    name:   'Professor bashir saleh kumurya',
    title:  'Vice Chancellor',
    tenure: '2025 – Present',
    bg:     'Professor of  med lab scince',
  },

  currentDVC: {
    name:   'Professor Fatima Lawal Suleiman',
    title:  'Deputy Vice Chancellor (Academics)',
    tenure: '2022 – Present',
  },

  registrar: {
    name:  'hasan sumaial',
    title: 'University Registrar',
  },

  bursar: {
    name:  'Mallam Sani Umar Kofar-Ruwa',
    title: 'University Bursar',
  },

  librarian: {
    name:  'Dr. Hauwa Dantata Musa',
    title: 'University Librarian',
  },

  pastVCs: [
    { name: 'Prof. Garba Inuwa Abdullahi',  tenure: '1987 – 1993', note: 'Founding Vice Chancellor' },
    { name: 'Prof. Maryam Zakari Hassan',    tenure: '1993 – 1999' },
    { name: 'Prof. Aliyu Danladi Bello',    tenure: '1999 – 2006' },
    { name: 'Prof. Umar Shehu Ringim',      tenure: '2006 – 2012' },
    { name: 'Prof. Aisha Baba Muhammed',    tenure: '2012 – 2016' },
    { name: 'Prof. Sa\'ad Nuhu Katsina',    tenure: '2016 – 2021' },
  ],

  history: [
    'AUSU was established in 1987 by the Kano State Government under the Kano State University Law No. 7 of 1987.',
    'The university was named after Alhaji Ahmadu Usman, a distinguished statesman and educationalist who advocated for tertiary education in Northern Nigeria.',
    'The institution began with three faculties: Arts, Science, and Education, and an initial student enrolment of 643 students.',
    'In 1992, AUSU received full accreditation from the National Universities Commission (NUC).',
    'The Faculty of Engineering and Technology was established in 1995, marking a pivotal shift toward STEM education.',
    'A landmark research centre, the Centre for Digital Innovation (CDI), was established in 2019 in partnership with global technology firms.',
    'AUSU has consistently ranked among the top 10 state universities in Nigeria by the NUC performance index.',
  ],

  faculties: [
    {
      name: 'Faculty of Arts and Humanities',
      dean: 'Prof. Aminu Sa\'idu Kiru',
      departments: ['English Language & Literature', 'History & Archaeology', 'Islamic Studies', 'Philosophy', 'Linguistics & Nigerian Languages', 'French & International Studies'],
    },
    {
      name: 'Faculty of Science',
      dean: 'Prof. Rahila Musa Tanko',
      departments: ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Biochemistry', 'Statistics', 'Microbiology', 'Geology'],
    },
    {
      name: 'Faculty of Engineering & Technology',
      dean: 'Prof. Kabir Yusuf Dakata',
      departments: ['Civil Engineering', 'Electrical & Electronics Engineering', 'Mechanical Engineering', 'Computer Engineering', 'Chemical Engineering', 'Agricultural Engineering'],
    },
    {
      name: 'Faculty of Computing & Information Technology',
      dean: 'Prof. Zainab Murtala Dankoli',
      departments: ['Computer Science', 'Information Technology', 'Cyber Security', 'Software Engineering', 'Data Science & AI', 'Information Systems'],
    },
    {
      name: 'Faculty of Education',
      dean: 'Prof. Hassan Danlami Rimi',
      departments: ['Educational Administration', 'Curriculum Studies', 'Early Childhood Education', 'Special Education', 'Science Education', 'Social Studies Education'],
    },
    {
      name: 'Faculty of Social Sciences',
      dean: 'Prof. Ramatu Aliyu Sokoto',
      departments: ['Economics', 'Political Science', 'Sociology', 'Psychology', 'Geography', 'Mass Communication & Media Studies'],
    },
    {
      name: 'Faculty of Law',
      dean: 'Prof. Bala Muhammed Gwale',
      departments: ['Private & Business Law', 'Public Law & Jurisprudence', 'Islamic Law', 'International & Comparative Law', 'Commercial Law'],
    },
    {
      name: 'Faculty of Medicine & Health Sciences',
      dean: 'Prof. Nafisa Ibrahim Dutse',
      departments: ['Medicine & Surgery', 'Nursing Science', 'Pharmacy', 'Medical Laboratory Science', 'Physiology', 'Anatomy', 'Public Health'],
    },
    {
      name: 'Faculty of Agriculture',
      dean: 'Prof. Usman Garba Funtua',
      departments: ['Crop Science', 'Animal Science', 'Soil Science', 'Agricultural Economics', 'Food Science & Technology', 'Agricultural Extension'],
    },
    {
      name: 'Faculty of Business Administration',
      dean: 'Prof. Sadiya Inuwa Kano',
      departments: ['Accounting', 'Business Administration', 'Banking & Finance', 'Marketing', 'Entrepreneurship', 'Human Resource Management'],
    },
  ],

  postgraduate: {
    body:     'School of Postgraduate Studies (SPGS)',
    director: 'Prof. Yahaya Musa Kiyawa',
    programs: ['MBA', 'MSc Computer Science', 'MSc Engineering', 'MA Islamic Studies', 'PhD (various disciplines)', 'Postgraduate Diploma programs'],
  },

  campuses: [
    { name: 'Main Campus',         location: 'Mariri, Kano',          area: '620 hectares' },
    { name: 'Medical Campus',      location: 'Sharada, Kano',         area: '85 hectares' },
    { name: 'Agricultural Campus', location: 'Dawakin Tofa, Kano',   area: '1,200 hectares' },
  ],

  facilities: [
    'Central Library (over 180,000 volumes + digital resources)',
    'Centre for Digital Innovation (CDI)',
    'University Teaching Hospital (UTH)',
    'Sports Complex (400-metre track, football pitch, courts)',
    'Student Union Building',
    'Multipurpose Lecture Halls (capacity 2,000+)',
    'University Guesthouse',
    'ICT Centre with 24-hour internet access',
    'Entrepreneurship & Skills Development Centre',
  ],

  admission: {
    utme:     'Minimum of 200 UTME score (varies by faculty)',
    oLevel:   '5 credit passes including English and Mathematics in WAEC/NECO (max 2 sittings)',
    direct:   'National Diploma (Upper Credit) for Direct Entry',
    form:     'Applications via JAMB portal and AUSU admissions office',
    deadline: 'As published annually by JAMB and NUC',
  },

  notableAlumni: [
    'Alhaji Musa Kwankwaso — Politician & former governor',
    'Dr. Zainab Aliyu — Prominent medical researcher',
    'Engr. Sadiq Bello — Telecommunications pioneer',
    'Prof. Hadiza Umar — NUC board member',
    'Ibrahim Al-Amin — Award-winning author',
  ],

  studentUnion: {
    name:      'AUSU Students Union Government (SUG)',
    president: 'Comrade Tijjani Abdullahi Kura',
    vp:        'Comrade Aisha Sani Rimi',
  },

  academicCalendar: {
    semesters: 'Two semesters per academic year',
    firstSem:  'October – February',
    secondSem: 'March – July',
    exams:     'January/February (1st Sem) & June/July (2nd Sem)',
    result:    'Published via AUSU Student Portal within 6 weeks of exams',
  },

  fees: {
    tuition:    'Varies by faculty; ₦45,000 – ₦180,000 per session',
    acceptance: '₦25,000 (new students)',
    note:       'Fee schedule published on AUSU portal each session',
  },

  portal: 'portal.ausu.edu.ng',
  email:  'info@ausu.edu.ng',
  phone:  '+234-064-XXX-XXXX',
};

// ─── KNOWLEDGE ENGINE ────────────────────────────

function searchKnowledge(query) {
  const q = query.toLowerCase();

  // Vice Chancellor
  if (/\b(vc|vice chancellor|vice-chancellor|chancellor|head|rector)\b/.test(q) && !/past|former|previous|history|list/.test(q)) {
    const vc = UNIVERSITY.currentVC;
    return `The current Vice Chancellor of ${UNIVERSITY.name} is **${vc.name}**.\n\n**Tenure:** ${vc.tenure}\n**Background:** ${vc.bg}\n\nFor official communications, contact the VC's office through the university's main contact channels.`;
  }

  // Past VCs
  if (/past|former|previous/.test(q) && /vc|vice chancellor|chancellor/.test(q)) {
    let resp = `**Past Vice Chancellors of ${UNIVERSITY.abbreviation}:**\n\n`;
    UNIVERSITY.pastVCs.forEach((v, i) => {
      resp += `${i + 1}. **${v.name}** (${v.tenure})${v.note ? ' — ' + v.note : ''}\n`;
    });
    resp += `\nThe current VC is **${UNIVERSITY.currentVC.name}** (${UNIVERSITY.currentVC.tenure}).`;
    return resp;
  }

  // Established / Founded
  if (/\b(established|founded|founded|when|year|start|began|creation|history)\b/.test(q) && !/faculty|department|course/.test(q)) {
    let resp = `**${UNIVERSITY.name}** was established in **${UNIVERSITY.established}** by the Kano State Government.\n\n`;
    resp += `**Key milestones:**\n`;
    UNIVERSITY.history.slice(0, 5).forEach((h, i) => { resp += `${i + 1}. ${h}\n`; });
    return resp;
  }

  // History
  if (/\b(history|background|origin|story|chronicle)\b/.test(q)) {
    let resp = `**History of ${UNIVERSITY.name}:**\n\n`;
    UNIVERSITY.history.forEach((h, i) => { resp += `${i + 1}. ${h}\n`; });
    return resp;
  }

  // Faculties list
  if (/\b(facult|school|college)\b/.test(q) && !/department|course|programme/.test(q)) {
    let resp = `**${UNIVERSITY.abbreviation} has ${UNIVERSITY.faculties.length} Faculties:**\n\n`;
    UNIVERSITY.faculties.forEach((f, i) => {
      resp += `${i + 1}. **${f.name}**\n   Dean: ${f.dean}\n`;
    });
    resp += `\nAsk me about any specific faculty for more details on its departments.`;
    return resp;
  }

  // Specific faculty or department search
  for (const fac of UNIVERSITY.faculties) {
    const facWords = fac.name.toLowerCase().split(/\s+/);
    const shortName = fac.name.replace('Faculty of ', '').toLowerCase();
    if (q.includes(shortName) || facWords.some(w => w.length > 4 && q.includes(w))) {
      let resp = `**${fac.name}**\n`;
      resp += `**Dean:** ${fac.dean}\n\n`;
      resp += `**Departments:**\n`;
      fac.departments.forEach((d, i) => { resp += `${i + 1}. ${d}\n`; });
      return resp;
    }
  }

  // Computer Science specifically
  if (/computer science|compsci|cs department/.test(q)) {
    const fac = UNIVERSITY.faculties.find(f => f.name.includes('Computing'));
    if (fac) {
      let resp = `**${fac.name}**\n**Dean:** ${fac.dean}\n\n**Departments:**\n`;
      fac.departments.forEach((d, i) => { resp += `${i + 1}. ${d}\n`; });
      resp += `\n**Programmes offered include:** B.Sc. Computer Science (4 years), B.Sc. Software Engineering (4 years), B.Sc. Data Science & AI (4 years). Entry via JAMB UTME or Direct Entry.`;
      return resp;
    }
  }

  // Departments
  if (/\b(department|dept)\b/.test(q)) {
    if (/all|list|every/.test(q)) {
      let resp = `**All Departments at ${UNIVERSITY.abbreviation}:**\n\n`;
      UNIVERSITY.faculties.forEach(f => {
        resp += `**${f.name}**\n`;
        f.departments.forEach(d => { resp += `  • ${d}\n`; });
        resp += '\n';
      });
      return resp;
    }
    return `${UNIVERSITY.abbreviation} has departments across ${UNIVERSITY.faculties.length} faculties. Ask me about a specific faculty (e.g., "departments in Engineering" or "Computing faculty departments") for a detailed list.`;
  }

  // Location / Address
  if (/\b(location|where|address|situated|campus|kano)\b/.test(q) && !/main|medical|agric/.test(q)) {
    let resp = `**${UNIVERSITY.name}** is located in **${UNIVERSITY.location}**.\n\n**Campuses:**\n`;
    UNIVERSITY.campuses.forEach(c => {
      resp += `• **${c.name}** — ${c.location} (${c.area})\n`;
    });
    return resp;
  }

  // Admission
  if (/\b(admission|apply|application|requirement|jamb|utme|waec|cut.?off|entry)\b/.test(q)) {
    const a = UNIVERSITY.admission;
    return `**Admission Requirements for ${UNIVERSITY.abbreviation}:**\n\n` +
      `**UTME:** ${a.utme}\n` +
      `**O'Level:** ${a.oLevel}\n` +
      `**Direct Entry:** ${a.direct}\n` +
      `**How to Apply:** ${a.form}\n` +
      `**Deadline:** ${a.deadline}\n\n` +
      `For more information, visit the AUSU Admissions Office or the university portal at **${UNIVERSITY.portal}**.`;
  }

  // Fees
  if (/\b(fee|fees|tuition|school fees|payment|cost)\b/.test(q)) {
    return `**Fees at ${UNIVERSITY.abbreviation}:**\n\n` +
      `**Tuition:** ${UNIVERSITY.fees.tuition}\n` +
      `**Acceptance Fee:** ${UNIVERSITY.fees.acceptance}\n\n` +
      `*${UNIVERSITY.fees.note}*\n\nVisit **${UNIVERSITY.portal}** for the full fee schedule.`;
  }

  // Registrar
  if (/registrar/.test(q)) {
    return `The University Registrar of ${UNIVERSITY.abbreviation} is **${UNIVERSITY.registrar.name}** (${UNIVERSITY.registrar.title}).`;
  }

  // Bursar
  if (/bursar|bursary|financial officer/.test(q)) {
    return `The University Bursar of ${UNIVERSITY.abbreviation} is **${UNIVERSITY.bursar.name}** (${UNIVERSITY.bursar.title}).`;
  }

  // Librarian
  if (/librarian|library/.test(q)) {
    return `The University Librarian of ${UNIVERSITY.abbreviation} is **${UNIVERSITY.librarian.name}** (${UNIVERSITY.librarian.title}).\n\nThe Central Library holds over 180,000 volumes and has access to digital research databases.`;
  }

  // DVC
  if (/deputy|dvc/.test(q)) {
    const dvc = UNIVERSITY.currentDVC;
    return `The Deputy Vice Chancellor (Academics) of ${UNIVERSITY.abbreviation} is **${dvc.name}** — serving since ${dvc.tenure}.`;
  }

  // Student union
  if (/student union|sug|students union|president|comrade/.test(q)) {
    const su = UNIVERSITY.studentUnion;
    return `**${su.name}**\n\n**SUG President:** ${su.president}\n**VP:** ${su.vp}\n\nThe Students Union Government advocates for student welfare and organises campus activities at AUSU.`;
  }

  // Motto
  if (/motto|slogan|mission|vision/.test(q)) {
    return `The official motto of ${UNIVERSITY.name} is **${UNIVERSITY.motto}**.\n\nThe university is committed to producing graduates of excellence who serve their communities with integrity and knowledge.`;
  }

  // Notable alumni
  if (/alumni|graduate|notable|famous|celebrity/.test(q)) {
    let resp = `**Notable Alumni of ${UNIVERSITY.abbreviation}:**\n\n`;
    UNIVERSITY.notableAlumni.forEach((a, i) => { resp += `${i + 1}. ${a}\n`; });
    return resp;
  }

  // Academic calendar
  if (/calendar|semester|session|exam|result|academic year/.test(q)) {
    const ac = UNIVERSITY.academicCalendar;
    return `**${UNIVERSITY.abbreviation} Academic Calendar:**\n\n` +
      `**Structure:** ${ac.semesters}\n` +
      `**1st Semester:** ${ac.firstSem}\n` +
      `**2nd Semester:** ${ac.secondSem}\n` +
      `**Examinations:** ${ac.exams}\n` +
      `**Results:** ${ac.result}`;
  }

  // Facilities
  if (/facilit|infrastructure|building|library|hospital|sport|hostel|ict/.test(q)) {
    let resp = `**Facilities at ${UNIVERSITY.abbreviation}:**\n\n`;
    UNIVERSITY.facilities.forEach((f, i) => { resp += `${i + 1}. ${f}\n`; });
    return resp;
  }

  // Postgraduate
  if (/postgraduate|masters|phd|doctorate|mba|msc|spgs/.test(q)) {
    const pg = UNIVERSITY.postgraduate;
    let resp = `**${pg.body}**\n**Director:** ${pg.director}\n\n**Postgraduate Programmes:**\n`;
    pg.programs.forEach((p, i) => { resp += `${i + 1}. ${p}\n`; });
    resp += `\nContact the SPGS office or visit **${UNIVERSITY.portal}** for admission details.`;
    return resp;
  }

  // Contact / portal
  if (/contact|portal|email|phone|website|online/.test(q)) {
    return `**Contact ${UNIVERSITY.abbreviation}:**\n\n` +
      `**Student Portal:** ${UNIVERSITY.portal}\n` +
      `**Email:** ${UNIVERSITY.email}\n` +
      `**Phone:** ${UNIVERSITY.phone}\n` +
      `**Website:** ${UNIVERSITY.website}`;
  }

  // General info
  if (/about|overview|information|general|tell me|what is|who is/.test(q)) {
    return `**${UNIVERSITY.name} (${UNIVERSITY.abbreviation})**\n\n` +
      `📍 **Location:** ${UNIVERSITY.location}\n` +
      `📅 **Established:** ${UNIVERSITY.established}\n` +
      `🎓 **Type:** ${UNIVERSITY.type}\n` +
      `👤 **Vice Chancellor:** ${UNIVERSITY.currentVC.name}\n` +
      `🏛️ **Faculties:** ${UNIVERSITY.faculties.length}\n` +
      `👥 **Students:** ${UNIVERSITY.studentPop}\n` +
      `⚖️ **Motto:** ${UNIVERSITY.motto}\n` +
      `🌐 **Portal:** ${UNIVERSITY.portal}`;
  }

  return null; // No match found
}

function getAIResponse(query) {
  const match = searchKnowledge(query);
  if (match) return Promise.resolve(match);

  // Fallback response for unrecognized queries
  return Promise.resolve(
    `I'm AAIS, specialized in answering questions about **${UNIVERSITY.name}**. ` +
    `I couldn't find specific information for your query.\n\n` +
    `Try asking about:\n` +
    `• The Vice Chancellor or university administration\n` +
    `• Faculties and departments\n` +
    `• University history and establishment\n` +
    `• Admission requirements\n` +
    `• Campuses and facilities\n\n` +
    `You can also click any of the suggested questions below the input field for guidance.`
  );
}

async function callAnthropicAPI(messages) {
  const systemPrompt = `You are AAIS (AUSU Academic Intelligence System), an intelligent AI assistant for ${UNIVERSITY.name} (${UNIVERSITY.abbreviation}) in ${UNIVERSITY.location}.

You have the following verified data:
${JSON.stringify(UNIVERSITY, null, 2)}

Rules:
1. ONLY answer questions about ${UNIVERSITY.abbreviation} and its academic affairs
2. Always be accurate using the data provided above
3. Format answers clearly using bullet points or numbered lists when listing items
4. If asked something unrelated to the university, politely redirect to university topics
5. Keep responses concise and professional
6. Use bold text for important names and facts`;

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type':         'application/json',
      'x-api-key':            CONFIG.API_KEY,
      'anthropic-version':    '2023-06-01',
    },
    body: JSON.stringify({
      model:      CONFIG.MODEL,
      max_tokens: CONFIG.MAX_TOKENS,
      system:     systemPrompt,
      messages,
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const data = await response.json();
  return data.content[0].text;
}

// ─── QUESTION POOL ─────────────────
const QUESTION_POOL = [
  // Administration
  'Who is the current Vice Chancellor of AUSU?',
  'Who is the Deputy Vice Chancellor?',
  'Who is the University Registrar?',
  'Who is the University Bursar?',
  'Who is the University Librarian?',
  'Who is the SUG President?',
  'List all past Vice Chancellors of AUSU',
  'Who was the founding Vice Chancellor?',
  // History
  'When was AUSU established?',
  'What is the history of AUSU?',
  'How was AUSU founded?',
  'What is the motto of AUSU?',
  'Where is AUSU located?',
  'What type of university is AUSU?',
  'How many students does AUSU have?',
  // Faculties
  'List all faculties in AUSU',
  'What faculties does AUSU have?',
  'How many faculties are in AUSU?',
  'Who is the Dean of the Faculty of Computing?',
  'Who is the Dean of the Faculty of Engineering?',
  'Who is the Dean of the Faculty of Medicine?',
  'Who is the Dean of the Faculty of Law?',
  'Who is the Dean of the Faculty of Education?',
  // Departments
  'What departments are in Computer Science?',
  'What departments are in Engineering?',
  'What departments are in Medicine?',
  'What departments are in Law?',
  'What departments are in Social Sciences?',
  'What departments are in the Faculty of Arts?',
  'What courses are in the Faculty of Computing?',
  'List all departments in AUSU',
  // Academics
  'What are the admission requirements for AUSU?',
  'What is the UTME cutoff score for AUSU?',
  'How do I apply to AUSU?',
  'What is the academic calendar for AUSU?',
  'When does the first semester begin?',
  'When does the second semester begin?',
  'How are AUSU exam results released?',
  'Does AUSU offer postgraduate programs?',
  'What postgraduate programmes does AUSU offer?',
  // Facilities
  'What facilities does AUSU have?',
  'Does AUSU have a teaching hospital?',
  'What campuses does AUSU operate?',
  'Where is the AUSU main campus?',
  'Does AUSU have an agricultural campus?',
  'Does AUSU have an ICT centre?',
  // Fees & Contact
  'What are the school fees at AUSU?',
  'How much is the AUSU acceptance fee?',
  'What is the AUSU student portal address?',
  'How do I contact AUSU?',
  'What is the AUSU email address?',
  // Alumni & Research
  'Who are notable AUSU alumni?',
  'What is the Centre for Digital Innovation?',
  'What research centres does AUSU have?',
  'Is AUSU accredited by NUC?',
  // Fun / General
  'Give me a brief overview of AUSU',
  'Tell me about AUSU',
  'What makes AUSU unique?',
  'What is the AUSU student population?',
  'What degree programmes does AUSU offer?',
];

// ─── AUTH MODULE ─────────────────────────────────
const Auth = {
  KEY: CONFIG.STORAGE_PREFIX + 'users',
  SESSION: CONFIG.STORAGE_PREFIX + 'session',

  getUsers() {
    try { return JSON.parse(localStorage.getItem(this.KEY)) || {}; }
    catch { return {}; }
  },

  saveUsers(users) {
    localStorage.setItem(this.KEY, JSON.stringify(users));
  },

  getSession() {
    try { return JSON.parse(sessionStorage.getItem(this.SESSION)); }
    catch { return null; }
  },

  setSession(user) {
    sessionStorage.setItem(this.SESSION, JSON.stringify(user));
  },

  clearSession() {
    sessionStorage.removeItem(this.SESSION);
  },

  isLoggedIn() {
    return !!this.getSession();
  },

  login(regNum) {
    const users = this.getUsers();
    const user = users[regNum.toUpperCase()];
    if (!user) return { ok: false, msg: 'Registration number not found. Please sign up first.' };
    this.setSession(user);
    return { ok: true, user };
  },

  signup(fullName, regNum) {
    if (!fullName.trim() || !regNum.trim()) {
      return { ok: false, msg: 'All fields are required.' };
    }
    const rn = regNum.toUpperCase();
    const users = this.getUsers();
    if (users[rn]) return { ok: false, msg: 'This registration number already exists. Please login instead.' };
    const user = { name: fullName.trim(), regNum: rn, joinedAt: Date.now() };
    users[rn] = user;
    this.saveUsers(users);
    return { ok: true, user };
  },

  logout() {
    this.clearSession();
    window.location.href = 'index.html';
  },

  guard() {
    if (!this.isLoggedIn()) window.location.href = 'index.html';
  },

  redirectIfLoggedIn() {
    if (this.isLoggedIn()) window.location.href = 'chat.html';
  },
};

// ─── CHAT MODULE ─────────────────────────────────
const Chat = {
  messages: [],    // { role: 'user'|'assistant', content, time }
  isThinking: false,

  init() {
    Auth.guard();

    const session = Auth.getSession();
    const avatarEl = document.getElementById('userAvatar');
    const regnumEl = document.getElementById('userRegNum');
    if (avatarEl) avatarEl.textContent = session.name.charAt(0).toUpperCase();
    if (regnumEl) regnumEl.textContent = session.regNum;

    Questions.init();
    this.bindEvents();
  },

  bindEvents() {
    const input   = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => Auth.logout());
    }

    if (input) {
      input.addEventListener('input', () => {
        // Auto-resize
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 160) + 'px';
        sendBtn.disabled = !input.value.trim();
      });

      input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.send();
        }
      });
    }

    if (sendBtn) {
      sendBtn.addEventListener('click', () => this.send());
      sendBtn.disabled = true;
    }
  },

  async send(text) {
    const input = document.getElementById('chatInput');
    const query = (text || input?.value || '').trim();
    if (!query || this.isThinking) return;

    if (input) {
      input.value = '';
      input.style.height = 'auto';
    }
    document.getElementById('sendBtn').disabled = true;

    // Hide welcome, show chat
    const welcome = document.getElementById('welcomeScreen');
    const msgList = document.getElementById('messagesList');
    if (welcome) welcome.style.display = 'none';
    if (msgList) msgList.style.display = 'flex';

    // Add user message
    this.messages.push({ role: 'user', content: query, time: this.timestamp() });
    this.renderMessage('user', query);

    // Show thinking
    this.isThinking = true;
    this.showThinking();
    this.scrollToBottom();

    try {
      let reply;
      if (CONFIG.API_KEY) {
        // Use real Anthropic API
        const apiMessages = this.messages
          .filter(m => m.role !== 'thinking')
          .map(m => ({ role: m.role, content: m.content }));
        reply = await callAnthropicAPI(apiMessages);
      } else {
        // Use local knowledge base (with simulated delay for UX)
        await this.delay(900 + Math.random() * 600);
        reply = await getAIResponse(query);
      }

      this.hideThinking();
      this.messages.push({ role: 'assistant', content: reply, time: this.timestamp() });
      this.renderMessage('ai', reply);

      // Show compact questions after first exchange
      Questions.showCompact();
    } catch (err) {
      this.hideThinking();
      const errMsg = 'Sorry, I encountered an issue processing your request. Please try again.';
      this.renderMessage('ai', errMsg);
    }

    this.isThinking = false;
    this.scrollToBottom();
    document.getElementById('sendBtn').disabled = false;
  },

  renderMessage(role, text) {
    const list = document.getElementById('messagesList');
    if (!list) return;

    const session = Auth.getSession();
    const initials = session?.name?.charAt(0).toUpperCase() || 'U';
    const time = this.timestamp();
    const isUser = role === 'user';

    const group = document.createElement('div');
    group.className = 'msg-group';

    const row = document.createElement('div');
    row.className = `msg-row ${isUser ? 'user' : ''}`;

    const avatar = document.createElement('div');
    avatar.className = `msg-avatar ${isUser ? 'user-av' : 'ai'}`;
    avatar.textContent = isUser ? initials : 'AI';

    const bubble = document.createElement('div');
    bubble.className = `bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`;
    bubble.innerHTML = this.formatText(text);

    row.appendChild(avatar);
    row.appendChild(bubble);

    const timeEl = document.createElement('div');
    timeEl.className = 'msg-time';
    timeEl.textContent = time;

    group.appendChild(row);
    group.appendChild(timeEl);

    // Insert before spacer
    const spacer = document.getElementById('scrollSpacer');
    list.insertBefore(group, spacer);

    this.scrollToBottom();
  },

  formatText(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n•\s/g, '\n• ')
      .replace(/\n/g, '<br>')
      .replace(/(\d+)\.\s(.*?)(<br>|$)/g, '<span style="display:block;margin:2px 0"><strong style="color:var(--accent)">$1.</strong> $2</span>');
  },

  showThinking() {
    const list = document.getElementById('messagesList');
    const spacer = document.getElementById('scrollSpacer');
    if (!list) return;

    const row = document.createElement('div');
    row.className = 'thinking-row';
    row.id = 'thinkingRow';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar ai';
    avatar.textContent = 'AI';

    const bubble = document.createElement('div');
    bubble.className = 'thinking-bubble';
    bubble.innerHTML = `
      <span class="thinking-text">Thinking</span>
      <div class="thinking-dots">
        <span></span><span></span><span></span>
      </div>`;

    row.appendChild(avatar);
    row.appendChild(bubble);
    list.insertBefore(row, spacer);
  },

  hideThinking() {
    const row = document.getElementById('thinkingRow');
    if (row) row.remove();
  },

  scrollToBottom() {
    const body = document.getElementById('chatBody');
    if (body) setTimeout(() => { body.scrollTop = body.scrollHeight; }, 50);
  },

  timestamp() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  },

  delay(ms) {
    return new Promise(res => setTimeout(res, ms));
  },
};

// ─── QUESTIONS MODULE ────────────────────────────
const Questions = {
  pool: QUESTION_POOL,
  shown: [],
  GRID_SIZE: 12,
  COMPACT_SIZE: 4,

  init() {
    this.render();
    const refreshBtn = document.getElementById('refreshQuestions');
    if (refreshBtn) refreshBtn.addEventListener('click', () => this.refresh());
  },

  sample(n) {
    const shuffled = [...this.pool].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, n);
  },

  render() {
    const grid = document.getElementById('questionsGrid');
    if (!grid) return;
    grid.innerHTML = '';
    this.shown = this.sample(this.GRID_SIZE);
    this.shown.forEach(q => {
      const pill = this.makePill(q);
      grid.appendChild(pill);
    });
  },

  refresh() {
    const grid = document.getElementById('questionsGrid');
    if (!grid) return;
    grid.style.opacity = '0';
    setTimeout(() => {
      this.render();
      grid.style.opacity = '1';
    }, 200);
  },

  showCompact() {
    const area = document.getElementById('compactQuestions');
    if (!area || area.children.length > 0) return;
    const questions = this.sample(this.COMPACT_SIZE);
    questions.forEach(q => {
      const chip = document.createElement('button');
      chip.className = 'compact-q';
      chip.textContent = q;
      chip.title = q;
      chip.addEventListener('click', () => Chat.send(q));
      area.appendChild(chip);
    });
    area.style.display = 'flex';
  },

  makePill(question) {
    const pill = document.createElement('button');
    pill.className = 'question-pill';
    pill.innerHTML = `
      <svg class="q-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
      <span>${question}</span>`;
    pill.addEventListener('click', () => {
      const input = document.getElementById('chatInput');
      if (input) {
        input.value = question;
        input.focus();
        input.dispatchEvent(new Event('input'));
      }
      Chat.send(question);
    });
    return pill;
  },
};

// ─── LOGIN PAGE ──────────────────────────────────
function initLogin() {
  Auth.redirectIfLoggedIn();

  const form    = document.getElementById('loginForm');
  const regInput = document.getElementById('regNum');
  const errEl   = document.getElementById('loginError');
  const btn     = document.getElementById('loginBtn');

  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const regNum = regInput.value.trim();

    errEl.classList.remove('show');
    regInput.classList.remove('error');

    if (!regNum) {
      showError(errEl, regInput, 'Please enter your registration number.');
      return;
    }

    btn.classList.add('loading');
    btn.disabled = true;

    await delay(600);

    const result = Auth.login(regNum);

    if (result.ok) {
      btn.innerHTML = `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <span class="btn-text">Welcome back!</span>`;
      setTimeout(() => { window.location.href = 'chat.html'; }, 500);
    } else {
      btn.classList.remove('loading');
      btn.disabled = false;
      showError(errEl, regInput, result.msg);
    }
  });
}

// ─── SIGNUP PAGE ─────────────────────────────────
function initSignup() {
  Auth.redirectIfLoggedIn();

  const form      = document.getElementById('signupForm');
  const nameInput = document.getElementById('fullName');
  const regInput  = document.getElementById('regNum');
  const errEl     = document.getElementById('signupError');
  const successEl = document.getElementById('signupSuccess');
  const btn       = document.getElementById('signupBtn');

  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();

    errEl.classList.remove('show');
    successEl.classList.remove('show');
    nameInput.classList.remove('error');
    regInput.classList.remove('error');

    const name   = nameInput.value.trim();
    const regNum = regInput.value.trim();

    if (!name) { showError(errEl, nameInput, 'Full name is required.'); return; }
    if (!regNum) { showError(errEl, regInput, 'Registration number is required.'); return; }

    btn.classList.add('loading');
    btn.disabled = true;

    await delay(700);

    const result = Auth.signup(name, regNum);

    if (result.ok) {
      btn.classList.remove('loading');
      successEl.textContent = '✓ Account created! Redirecting to login…';
      successEl.classList.add('show');
      setTimeout(() => { window.location.href = 'index.html'; }, 1500);
    } else {
      btn.classList.remove('loading');
      btn.disabled = false;
      const targetInput = result.msg.includes('registration') ? regInput : nameInput;
      showError(errEl, targetInput, result.msg);
    }
  });
}

// ─── HELPERS ─────────────────────────────────────
function showError(errEl, inputEl, msg) {
  if (errEl) {
    const span = errEl.querySelector('span');
    if (span) span.textContent = msg;
    else errEl.textContent = msg;
    errEl.classList.add('show');
  }
  if (inputEl) { inputEl.classList.add('error'); inputEl.focus(); }
}

function delay(ms) { return new Promise(res => setTimeout(res, ms)); }

// ─── ROUTER ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;

  if (page === 'login')  initLogin();
  if (page === 'signup') initSignup();
  if (page === 'chat')   Chat.init();
});
