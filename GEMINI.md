# Antigravity Global Machine Master Rules

## 1. 🚀 Antigravity 최신 변경점(Changelog v2.10.0+) 분석 요약 및 표준 준수 규칙
- **통합 내장 터미널 & Git VCS 직접 제어**:
  - 사이드바 내장 터미널(Ctrl/Cmd + \`) 및 Review 창의 Git 브랜치/스테이징/커밋/디프 네이티브 제어.
  - 터미널 명령어 실행(un_command) 시 에러가 발생해도 즉각 중단하지 않고 **자율 재시도 및 디버깅 루프**를 완벽하게 수행.
- **멀티모달 및 문서/미디어 지원 강화**:
  - WebP, 이미지 영역 지정 코멘트, 오디오 파일(MP3, WAV, FLAC 등) 첨부 기능 적극 활용.
  - PowerShell(.ps1, .psm1, .psd1) 및 Bash/Zsh 구문 강조 및 UTF-8 인코딩 기본 지원.
- **에이전트 커스터마이제이션 상속 (inheritCustomizations)**:
  - 전역/상위 레벨의 Rules, Skills, Subagents를 단일 설정으로 손쉽게 공유하고 상속하여 일관된 정책 유지.

---

## 2. 🛡️ Pre / Post Tool Use 가드레일 (무설치/독립 실행 배포 표준)
- **파괴적 시스템 명령 하드 차단 (PreToolUse -> deny)**:
  - ormat, mdir /s /q C:\, del /f /s /q C:\Windows, m -rf /, diskpart, cdedit, ssadmin 등 시스템에 치명적인 명령어는 즉시 하드 차단(deny).
- **배포 산출물의 제로 의존성(Zero-Dependency) 가드레일**:
  - **PowerShell / BAT**: Python이나 서드파티 런타임 설치를 요구하지 않고, Windows 기본 내장 powershell.exe(v5.1+), cmd.exe, .NET 리플렉션 API만으로 100% 무설치 단독 실행(Standalone) 보장. chcp 65001 및 관리자 권한 자동 상승(UAC Self-Elevation) 기본 탑재.
  - **Web 개발**: 무거운 외부 프레임워크 남발을 금지하고 Vanilla HTML5/CSS3/ES6+ 표준 API 및 다크/라이트 테마 적응형 CSS 변수(ar(--theme-...)) 사용.
  - **Android 앱**: 표준 AndroidX Jetpack 컴포넌트 중심 구현, 메인 UI 스레드 I/O 블로킹(ANR) 방어(Coroutine Dispatchers.IO 필수).

---

## 3. 🧠 승인 케스케이드 & [JIT 지식 대조 리포트] 시스템
- /learn에 의존하지 않고, 문제가 해결되거나 디버깅될 때마다 자체적인 **승인 케스케이드**를 가동하여 안티패턴을 체계화.
- **안티패턴 데이터베이스 구축 (nti_patterns.json)**:
  - 카테고리별(web, powershell_bat, ndroid, document_artifact 등)로 고유 ID, 설명, 사전 체크리스트, 해결책을 JSON 구조로 엄격하게 관리.
- **대화 및 작업 시 상시 표출 의무**:
  - 응답 및 작업 시작 전 관련 카테고리를 자동 대조하여, 아래 형식의 **[🧠 JIT 지식 대조 리포트]**를 최상단에 반드시 출력하고 체크리스트를 통과한 후 작업을 진행:

`markdown
[🧠 JIT 지식 대조 리포트]

• 타겟 파일: 📖 <대상_파일명>
• 대조 안티패턴 ID: <AP-ID-1>, <AP-ID-2>
• 사전 체크리스트:
  1. <사전 점검 항목 1> -> ✅ 완료
  2. <사전 점검 항목 2> -> ✅ 완료
`

- **지식 축적 (승인 케스케이드)**: 새로운 문제나 특이 케이스 해결 시, 즉시 nti_patterns.json에 신규 안티패턴(AP-...)을 추가 등록하여 영구 지식화.

---

## 4. ⚡ 무질문 즉시 실행 정책 (Zero-Ask on Plan & Full Turbo Auto-Execution)
- **계획 및 실행 통합 (No-Ask Immediate Execution)**:
  - 사용자가 별도로 질문이나 확인을 요청하지 않는 한, **"승인해 주시면 진행하겠습니다" 등의 확인 질문을 절대 하지 않고 곧바로 작업을 끝까지 수행**합니다.
  - `implementation_plan.md` 생성/갱신 시에도 항상 `RequestFeedback: false`로 설정하며, 계획 작성과 동시에 코드 수정, 스크립트/APK 빌드, 테스트, 텔레그램 전송, `walkthrough.md` 작성까지 **중간 질문이나 대기 없이 풀 터보 모드로 즉시 완주**합니다.

---

## 5. 🌐 신규 프로젝트 및 타 프로젝트 전역 적용 방안
- **머신 전역 적용 (~/.gemini/config/)**:
  - ~/.gemini/config/에 등록된 GEMINI.md, AGENTS.md, hooks.json, nti_patterns.json, ules/는 Antigravity 탐색 메커니즘에 의해 머신 내의 모든 프로젝트, 신규 프로젝트에 자동으로 최우선 상속/적용됩니다.
- **신규 프로젝트 적용**:
  - 새 프로젝트를 생성하거나 다른 프로젝트를 열었을 때 자동으로 전역 룰로 로드되므로 동일한 가드레일과 JIT 리포트 시스템이 즉시 활성화됩니다.
  - 프로젝트 루트에 .agents/를 배치하여 프로젝트별 맞춤 훅 및 룰을 추가 확장할 수 있습니다.

---

## 6. 💡 글로벌 업무자동화 플랫폼 가이드
- **사용법 안내 (/사용법, 사용방법, 도움말)**: TaskRecorder.exe ([F8] 단축키 녹화/종료) -> 산출물(ideo.avi, ction_log.md, ction_list.json) -> 에이전트 봇 생성 요청 안내.
- **RPA 봇 생성 (/자동화, /auto, /rpa)**: pa-bot-generator 스킬을 호출하여 generated_bot.py 생성 및 엑셀 연산 조건 결합.
---

## 7. 🔍 REA 자율 역공학 및 1:1 클론 재구현 파이프라인 ("rea 분석해서 똑같이 구현해줘")
- 사용자가 구체적인 엔진명(JADX, Ghidra)이나 세부 프롬프트를 적지 않고 단순히 **"rea 분석해서 똑같이 구현해줘"** (또는 **"rea로 분석해서 만들어줘"**)라고 명령하면 대상 파일 형식에 맞춰 즉시 아래 파이프라인을 자동 수행:
  - **Android (`.apk`, `.aab`, `.dex`)**: 자동으로 **REA JADX 엔진**(`inspect_android_package` -> `search_android_classes` -> `inspect_android_class` -> `inspect_android_method` / `decode_android_resources`)을 구동하여 전체 패키지 구조, `AndroidManifest.xml`, 주요 액티비티/API 통신/비즈니스 로직 클래스를 디컴파일한 뒤 동일한 Android 앱 소스코드로 1:1 재구현.
  - **Native/Desktop (`.exe`, `.dll`, `.so`, `.dylib`)**: 자동으로 `open_binary` 및 `binary_overview` 수행 후 **REA Ghidra 12.1.4 엔진**(`list_procedures` -> `search_strings` -> `procedure_pseudo_code` / `batch_decompile` -> `get_call_graph`)을 구동하여 주요 함수 목록과 핵심 로직을 의사코드(Pseudocode)로 디컴파일(.NET은 `inspect_managed_artifact`, Electron은 `analyze_javascript_application` 자동 분기)한 뒤 동일한 프로그램으로 1:1 재구현.

---

## 8. 📲 전역 프로젝트 산출물 첨부 전송 및 완료·확인필요 알림 ('AI변호사' 봇 단일 창구) 파이프라인
- **'나와의대화' 채널 업로드 중단**: 더 이상 `'나와의대화'` 채널로 파일이나 메시지를 보내지 않으며, 모든 산출물 파일과 알림은 **`AI변호사` 봇 (`@myfirstailawbot`)**을 통해서만 사용자에게 직접 전송합니다.
- **산출물 파일(`.apk`, `.aab`, `.exe`, `.msi`, `.html`, `.pdf`, `.zip`, `.pptx`, `.docx`, `.xlsx` 등) 생성 시**:
  - 로컬에서 다운받아 확인이 필요한 모든 산출물 파일은 **`AI변호사` 봇 (`@myfirstailawbot`)**을 통해 **첨부파일 + 핵심작업내용 요약**으로 직접 전송합니다.
  - 명령어: `python "C:\Users\Herosonsa\.gemini\config\scripts\telegram_apk_sender.py" "<산출물_파일_경로1>" "<산출물_파일_경로2>" --project-name "<프로젝트명>" --summary "<핵심작업내용 요약>"`
- **산출물 파일이 없더라도 모든 프로젝트에서 확인이 필요하거나 작업이 완료된 경우**:
  - `hooks.json`의 `apk-telegram-uploader` (`PreToolUse: ask_question` 및 `Stop` 훅 -> `apk_telegram_hook.ps1`) 또는 `--notify-only` 호출을 통해, 모든 프로젝트에서 사용자 확인이 필요하거나 작업이 완료될 때마다 **`AI변호사` 봇 (`@myfirstailawbot`)**이 어떤 프로젝트에서 어떤 내용인지 텍스트 푸시 알림으로 즉시 알려줍니다.

---

## 9. ✍️ 전역 문서 작성 `im-not-ai` MCP 필수 활용 및 정부보고문체 2단계 파이프라인 (새 프로젝트·논프로젝트·기존 프로젝트 전체 적용)
- **전역 문서 작성 원칙 (`im-not-ai` MCP 필수 경유)**:
  - 새 프로젝트, 논프로젝트(Outside of Project), 기존 프로젝트를 막론하고 프로젝트를 수행하면서 작성되는 **모든 문서**(기획서, 보고서, 기술 문서, `README.md`, `implementation_plan.md`, `walkthrough.md`, `task.md`, HWPX/DOCX/PDF/HTML 문서 원고 등)는 반드시 **`im-not-ai` MCP 서버**(`analyze_ai_tells`, `humanize_document`, `verify_humanized_document`, `get_humanize_rules`)를 활용하여 작성해야 합니다.
  - 문서 내 AI 번역투(`~를 통해`, `~에 있어서`, `~되어진다`, `가지고 있다`), 기계적 병렬(`A가 아니라 B` 연쇄), 과잉 관용구(`결론적으로`, `시사하는 바가 크다`), 연결어미 뒤 쉼표(`-고,`, `-며,`)를 철저히 제거하고 사실·수치·고유명사·서법을 100% 보존합니다.
- **명시적 '정부보고문체' 요청 시 (선 `im-not-ai` → 후 정부보고문체)**:
  - 사용자가 명시적으로 **"정부보고문체"**로 작성해달라고 요청한 경우에는, **반드시 먼저 `im-not-ai` MCP(`humanize_document`의 `explicit_government_style=true`)를 거친 이후(1단계: AI 번역투·관용구·기계적 어투 제거 → 2단계: 정부보고문체 적용)** 정부보고문체(`□` → `ㅇ` → `-` → `·` 개조식 위계 및 `~함`, `~임`, `~됨`, `~있음`, `~추진` 종결)로 작성합니다.


