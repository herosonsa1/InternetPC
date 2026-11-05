# 다중 프로젝트 및 전역 적용 규칙 (Global & Multi-Project Integration)

## 1. Antigravity 커스터마이제이션 우선순위 및 상속 구조
Antigravity는 다음 우선순위에 따라 룰과 훅을 로드합니다:
1. **현재 작업 공간(Workspace)**: `.agents/`, `GEMINI.md`, `AGENTS.md`
2. **명시적 설정(Declared Configs)**: `skills.json`, `plugins.json`
3. **머신 전역 설정(Global Discovery)**: `~/.gemini/config/` (또는 전역 Rules/Plugins)

## 2. 신규 프로젝트 및 타 프로젝트 전역 적용 방법
- **상속 설정 (`inheritCustomizations`)**: 커스텀 에이전트 선언 시 `inheritCustomizations: true`를 지정하여 상위 및 전역 스킬, 룰, 훅을 자동 상속합니다.
- **공통 템플릿 복제 또는 심볼릭 링크**:
  - 신규 프로젝트 생성 시 `.agents/` 디렉토리를 프로젝트 루트에 배치하면 프로젝트별 가드레일과 안티패턴 DB가 즉시 독립적으로 활성화됩니다.
  - 전역 설정을 통해 모든 워크스페이스에서 `GEMINI.md`와 `anti_patterns.json` 기반의 [JIT 지식 대조 리포트] 및 승인 케스케이드가 항시 작동합니다.

## 3. 프로젝트별 맞춤 Tool Use 및 Hook 활용 전략
- **웹 프로젝트**: PreToolUse에서 무거운 번들러/의존성 감지, PostToolUse에서 번들 크기 및 CSS 테마 적응도 점검.
- **Windows 스크립트 프로젝트 (ps1, bat)**: PreToolUse에서 외부 Python/의존성 설치 시도 감지 시 무설치 내장형 전환 유도, UTF-8 인코딩 및 관리자 권한 검사.
- **안드로이드 프로젝트**: PreToolUse에서 Jetpack 표준 준수 점검, PostToolUse에서 비동기 I/O Coroutine 사용 여부 점검.
