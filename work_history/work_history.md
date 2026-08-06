# 📋 Hyper-V 인터넷망 네트워크 자동 복구 프로젝트 작업 이력 (Work History)

## 📌 1. 프로젝트 개요 및 추진 배경
* **프로젝트명**: Hyper-V 인터넷망 가상스위치 자동 복구 툴
* **환경**: 폐쇄망 PC (3개 이상의 물리 랜포트 보유, Hyper-V 기반 인터넷 PC 운용 환경, Python 미설치 환경 대응)
* **발생 문제**: PC 부팅 시마다 랜카드의 물리 이더넷 식별 번호가 무작위로 변경되면서, Hyper-V 가상스위치('인터넷망')에 연결된 어댑터 바인딩이 풀려 `vEthernet(인터넷망)` 네트워크가 **언플러그(Unplugged)** 상태로 빠지고 인터넷이 끊기는 현상 발생.
* **목적**: 매번 수동으로 제어판 및 Hyper-V 관리자에서 조치하던 과정을 무설치 원클릭(1-Click)으로 자동 탐지, 가상스위치 바인딩 변경, 가상 어댑터 갱신 및 가상 PC(VM) 재부팅까지 완수하는 자동화 프로그램 개발.

---

## 🛠️ 2. 주요 개발 산출물 구성

| 산출물 파일 | 유형 | 설명 |
|:---|:---|:---|
| `HyperV_Network_Fixer.exe` (및 `v2.exe`) | 독립 실행형 EXE | Python Tkinter 기반 무설치 단일 실행 파일 (PyInstaller 빌드) |
| `HyperV_인터넷망_자동복구.bat` | 콘솔 무설치 배치 | Windows 내장 PowerShell 기반 4단계 무인 자동 복구 콘솔 스크립트 |
| `HyperV_인터넷망_GUI복구(무설치).bat` | GUI 무설치 배치 | PowerShell WinForms 기반 무설치 GUI 배치 스크립트 (Base64 인코딩) |
| `hyperv_network_fixer.py` | Python 원본 소스 | GUI 및 자동화 핵심 로직 Python 소스 코드 |
| `build_encoded_bat.py` / `build_encoded_console_bat.py` | 빌드 헬퍼 | 배치 파일용 Base64 유니코드 인코더 스크립트 |

---

## ⚙️ 3. 세부 기능 구현 및 기술적 특징

1. **"식별되지 않은 네트워크" 최우선순위(Priority 1등) 자동 탐지 알고리즘**
   - Windows 네트워크 연결(`ncpa.cpl`)상에서 실제 케이블이 연결되어 외부 신호가 유입되는 랜카드가 **`식별되지 않은 네트워크 (Unidentified Network)`** 프로필을 가진다는 점에 착안.
   - `Get-NetConnectionProfile` 기반 1순위 정렬 알고리즘을 도입하여, 여러 개의 활성 랜카드 중 외부 인터넷 랜카드(`#14 이더넷` 등)를 1등 기본값으로 자동 선택.

2. **드롭다운 및 로그 상태 직관적 명시**
   - 물리 어댑터 목록에 `[이더넷 14] Realtek PCIe GbE Family Controller #14 - (식별되지 않은 네트워크)` 와 같이 제어판 네트워크 프로필 상태 명칭을 또렷하게 표시.

3. **원스톱(One-stop) 4단계 풀 프로세스 자동화**
   - **1단계**: 외부 인터넷 물리 랜카드 자동 탐지 (`Status: Up` & `식별되지 않은 네트워크`)
   - **2단계**: Hyper-V 가상스위치 어댑터 바인딩 자동 변경 (`Set-VMSwitch`)
   - **3단계**: `vEthernet(인터넷망)` 가상 네트워크 어댑터 리셋 및 상태 갱신
   - **4단계**: 타겟 가상 PC(VM) 자동 탐지 및 원스톱 재부팅 명령 전달 (`Restart-VM -Force`)

4. **폐쇄망 / Python 미설치 환경 100% 호환성 확보**
   - 외부 라이브러리 의존성을 제거하고 Windows 내장 PowerShell 표준 Cmdlet만 활용.
   - 배치 파일 파싱 에러 및 한글 깨짐 방지를 위한 Base64 유니코드 인코딩(`powershell -EncodedCommand`) 구조 적용.
   - 관리자 권한 자동 승격(`RunAs`) 처리 포함.

---

## 🐛 4. 주요 트러블슈팅 및 결함 조치 내역

1. **`Set-VMSwitch` 매개변수 오류 수정 (`NamedParameterNotFound` / `Force` / `NetAdapterName`)**
   - `Set-VMSwitch` Cmdlet에는 `-NetAdapterName` 및 `-Force` 매개변수가 존재하지 않고, 오직 **`-NetAdapterInterfaceDescription`**만 표준 지원함을 확인하여 구문 정밀 수정.

2. **파이썬-PowerShell 간 한글 가상스위치명 파싱 왜곡 해결 (`T_s` / `ObjectNotFound`)**
   - Python subprocess 실행 시 한글('인터넷망') 유니코드 왜곡 문제를 해결하고, PowerShell 스크립트 내부에서 '인터넷망' 키워드 및 외부(External) 가상스위치를 2중으로 자동 추적하는 **스마트 세이프가드(Fallback)** 로직 구현.

3. **Tkinter GUI 폰트 크기 예외 수정 (`expected integer but got "9.5"`)**
   - `scrolledtext` 폰트 인자를 소수점 실수(`9.5`)에서 정수(`10`)로 교체하여 실행 즉시 튕기던 크래시 문제 해결.

4. **GUI 레이아웃 및 텍스트 잘림 개선**
   - 기본 창 크기를 `860x680`으로 확대하고 오른쪽 우측 버튼 정렬을 가변 그리드 가중치(`columnconfigure weight=1`)로 정돈.

---

## 🚀 5. 향후 유지보수 및 폐쇄망 배포 가이드
* 폐쇄망 PC에는 `HyperV_Network_Fixer_v2.exe`, `HyperV_인터넷망_자동복구.bat`, `HyperV_인터넷망_GUI복구(무설치).bat` 중 사용자가 선호하는 **단 1개의 파일만 복사**하여 실행해도 100% 독립 동작함.
