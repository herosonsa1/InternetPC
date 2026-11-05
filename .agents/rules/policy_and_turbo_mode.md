# 승인 정책(Policy) 및 Turbo Mode 동작 규칙

## 1. Planning Mode 승인 정책 (Always Ask on Plan)
- 복잡한 작업, 아키텍처 변경, 신규 기능 구현 시 `implementation_plan.md`를 생성하고 `RequestFeedback: true`로 설정하여 사용자 승인을 요청합니다.
- 불명확한 요구사항이나 중요한 설계 결정은 구현 계획서 내부의 `Open Questions` 및 `User Review Required`에 명시합니다.

## 2. Execution 단계 Turbo Mode (Auto-Execution)
- 사용자가 구현 계획을 승인(`Proceed` 또는 대화로 확인)한 후에는 **일체의 중간 도구 승인 질문 없이 터보 모드로 완전 자동 완주**합니다.
- 코드 작성 -> 빌드/실행 -> 에러 발생 시 자율 디버깅 -> 최종 `walkthrough.md` 생성까지 중단 없이 자율 수행합니다.
- 가드레일(`hooks.json`)이 위반되지 않는 한 도구 실행은 자동으로 허용(`allow`) 처리됩니다.
