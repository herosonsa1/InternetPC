param()

# Read stdin (JSON payload from Antigravity)
$inputJson = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($inputJson)) {
    Write-Output "{}"
    exit 0
}

try {
    $data = $inputJson | ConvertFrom-Json
} catch {
    Write-Output "{}"
    exit 0
}

# Determine event context
$toolCall = $data.toolCall

if ($toolCall) {
    # PreToolUse Event
    $toolName = $toolCall.name
    $args = $toolCall.args

    if ($toolName -eq "run_command" -and $args.CommandLine) {
        $cmd = $args.CommandLine.ToLower()

        # Hard Guardrail: Destructive Commands
        $dangerousPatterns = @(
            "format\s+[a-z]:",
            "rmdir\s+.*[a-z]:\\",
            "del\s+.*[a-z]:\\windows",
            "del\s+.*[a-z]:\\system32",
            "remove-item\s+.*-recurse\s+.*[a-z]:\\",
            "rm\s+-rf\s+/[^a-z]?",
            "diskpart",
            "bcdedit",
            "vssadmin\s+delete\s+shadows"
        )

        foreach ($p in $dangerousPatterns) {
            if ($cmd -match $p) {
                $response = @{
                    decision = "deny"
                    reason = "가드레일 하드 차단(Deny): 시스템에 치명적인 손상을 초래할 수 있는 위험 명령어가 감지되었습니다 ($p)."
                }
                $response | ConvertTo-Json -Compress
                exit 0
            }
        }

        # Guardrail for Portable / Zero-Dependency Deployment (Warning / Notice for Heavy Global Packages)
        if ($cmd -match "pip\s+install" -or $cmd -match "npm\s+install\s+-g") {
            $response = @{
                decision = "allow"
                reason = "가드레일 알림: 배포 산출물은 외부 패키지 설치 없이 독립 실행(Standalone/Zero-Dependency) 가능한 구조를 유지해야 합니다."
            }
            $response | ConvertTo-Json -Compress
            exit 0
        }
    }

    # Default Allow for PreToolUse
    $response = @{
        decision = "allow"
    }
    $response | ConvertTo-Json -Compress
    exit 0
}

# Default output for other hooks
Write-Output "{}"
