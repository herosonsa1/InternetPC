# 전역 가드레일 및 무설치/독립 배포 규칙

## 1. Web 개발 표준
- 외부 무거운 프레임워크나 패키지 관리자 종속 없이 동작 가능한 Vanilla HTML5/CSS3/JavaScript를 최우선 고려.
- Antigravity Generative UI 및 시스템 테마(다크/라이트)에 완전 적응하는 CSS 변수 사용.

## 2. Windows Batch 및 PowerShell 스크립트 표준
- **Python 등 외부 런타임 미설치 PC에서도 100% 독립 실행**:
  - Python이 설치되지 않은 환경을 기본 전제로 하여, Windows 기본 내장 cmd.exe 및 powershell.exe v5.1+ 명령과 .NET 프레임워크 내장 클래스를 직접 활용.
- **인코딩 및 한글 출력**:
  - 배치: 상단에 `chcp 65001 >nul` 삽입.
  - 파워쉘: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` 명시.
- **관리자 권한 자동 상승(Self-Elevation)**:
  - 시스템/네트워크 설정 변경이 필요한 경우 UAC 권한 검사 및 자동 상승 스크립트 필수 탑재.

## 3. Android 앱 개발 표준
- 표준 AndroidX Jetpack 컴포넌트 활용, 대용량 상용 SDK 의존성 배제.
- UI 스레드 I/O 블로킹 방지 (Kotlin Coroutines Dispatchers.IO 필수 적용).
- 별도 환경 구성 없이 표준 Gradle 빌드 및 APK/AAB 독립 배포 가능하도록 구성.

## 4. PreToolUse 가드레일
- 파괴적 시스템 명령어(`format`, `rmdir /s /q c:\`, `rm -rf /` 등)는 자동 차단(`deny`).
