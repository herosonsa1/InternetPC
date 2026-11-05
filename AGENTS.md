# AGENTS.md - Antigravity Global Autonomous Agent Directives

## 1. 🚀 최신 Changelog 요약 및 엔지니어링 표준 (v2.10.0+)
- 내장 터미널 & Git VCS 제어 시 자율 재시도 및 디버깅 루프 수행.
- 멀티모달(WebP, 오디오, 영역 코멘트) 및 PowerShell/Bash UTF-8 기본 지원.
- Windows 배치 및 파워쉘 스크립트 작성 시 외부 런타임(Python) 없이 100% 무설치 단독 실행(Standalone) 보장.
- Web 개발 시 Vanilla JS/CSS 표준 준수 및 Generative UI 테마 완벽 적응.
- Android 개발 시 Jetpack 표준 컴포넌트 활용 및 UI 스레드 블로킹(ANR) 방지.

## 2. 🛡️ 훅 및 가드레일 (Hooks & Guardrails)
- hooks.json 및 guardrail.ps1의 PreToolUse 가드레일을 통해 위험 파괴 명령(deny) 및 환경 오염 방지.

## 3. 🧠 승인 케스케이드 및 JIT 지식 대조 리포트
- 모든 응답 및 작업 시작 전 상단에 [🧠 JIT 지식 대조 리포트] 표출 의무.
- 문제 해결 시 nti_patterns.json에 안티패턴 자동 추가(승인 케스케이드) 및 영구 지식화.

## 4. ⚡ 무질문 즉시 실행 & 풀 터보 완주 (Zero-Ask Full Turbo Auto-Execution)
- 모든 작업에서 사용자에게 계획 승인이나 진행 여부를 묻지 않고(`RequestFeedback: false`), 계획 수립 즉시 코드 수정·빌드·검증·텔레그램 전송·walkthrough.md까지 논스톱 자율 완주.

## 5. 🌐 전역 상속 및 신규 프로젝트 연동
- inheritCustomizations 설정을 통해 머신 전역의 모든 프로젝트에 동일한 룰, 스킬, 가드레일이 자동 상속 적용.

---

## 💡 글로벌 업무자동화 플랫폼 가이드
- **/사용법 / 도움말**: TaskRecorder(F8) 녹화 -> 산출물 확보 -> /자동화 요청 가이드 제공.
- **/자동화 / /auto / /rpa**: pa-bot-generator 스킬 구동, ction_list.json 분석 후 pa_platform/core 기반 generated_bot.py 자동 생성.
- **"rea 분석해서 똑같이 구현해줘" / /rea**: 타겟 파일 확장자를 자동 감지하여 `.apk`는 JADX 엔진(`inspect_android_package` -> `search_android_classes` -> `inspect_android_class`/`method`), `.exe`/`.dll`/`.so`는 Ghidra 엔진(`open_binary` -> `binary_overview` -> `list_procedures` -> `procedure_pseudo_code`/`batch_decompile`)으로 전체 구조와 핵심 로직을 자동 디컴파일한 후 동일한 앱/프로그램으로 즉시 재구현.
- **전역 프로젝트 산출물 첨부 전송 및 완료·확인필요 알림 ('AI변호사' 봇 단일 창구)**:
  1. 산출물 파일(`.apk`, `.exe`, `.html`, `.pdf`, `.zip` 등 로컬 확인이 필요한 모든 파일) 생성 시: `python "C:\Users\Herosonsa\.gemini\config\scripts\telegram_apk_sender.py" "<산출물_파일_경로>" --project-name "<프로젝트명>" --summary "<핵심작업내용 요약>"`을 실행하여 **`AI변호사` 봇(`@myfirstailawbot`)**을 통해 첨부파일과 핵심작업내용 요약을 사용자에게 직접 전송함 (`'나와의대화'` 채널 전송 중단).
  2. 일반 작업 완료 또는 사용자 확인이 필요한 경우: 모든 프로젝트에서 `Stop` 훅 및 `PreToolUse(ask_question)` 훅(`apk_telegram_hook.ps1`) 또는 `--notify-only` 호출을 통해 **`AI변호사` 봇(`@myfirstailawbot`)**이 어떤 내용인지 텍스트 요약 알림을 자동 발송함.
- **전역 문서 작성 `im-not-ai` MCP 필수 활용 및 정부보고문체 2단계 원칙 (새 프로젝트·논프로젝트·기존 프로젝트 공통)**:
  1. 모든 프로젝트 및 논프로젝트에서 작성되는 모든 문서(기획서, 보고서, README, 가이드, `implementation_plan.md`, `walkthrough.md`, HWPX/DOCX/PDF/HTML 원고 등)는 반드시 **`im-not-ai` MCP**(`analyze_ai_tells`, `humanize_document`, `verify_humanized_document`, `get_humanize_rules`)를 활용하여 AI 번역투·관용구·기계적 병렬·연결어미 뒤 쉼표를 제거한 자연스러운 한국어로 작성함.
  2. 사용자가 명시적으로 **"정부보고문체"**로 해달라고 요청한 경우에는 반드시 **`im-not-ai` MCP(`explicit_government_style=true`)를 먼저 거친 이후** 정부보고문체(`□` → `ㅇ` → `-` → `·` 계층 기호 및 `~함/~임/~됨` 개조식 종결)로 작성함.


