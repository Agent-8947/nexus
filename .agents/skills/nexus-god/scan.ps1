# NEXUS GOD — Live Environment Scanner
# Генерирует inventory.json с полной картиной среды
# Вызывается автоматически при активации /nexus

$ErrorActionPreference = "SilentlyContinue"
$root = "e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS"
$currentDir = Get-Location

# ── Scan Skills ──────────────────────────────────────────────
$skillsDir = Join-Path $root ".agents\skills"
$skills = @()
if (Test-Path $skillsDir) {
    Get-ChildItem -Path $skillsDir -Directory | ForEach-Object {
        $skillMd = Join-Path $_.FullName "SKILL.md"
        $desc = ""
        if (Test-Path $skillMd) {
            $firstLines = Get-Content $skillMd -TotalCount 5 -ErrorAction SilentlyContinue
            foreach ($line in $firstLines) {
                if ($line -match "^Description:\s*(.+)") {
                    $desc = $Matches[1].Trim()
                    break
                }
                if ($line -match "^#\s+(.+)") {
                    $desc = $Matches[1].Trim()
                }
            }
        }
        $skills += @{
            name = $_.Name
            has_skill_md = (Test-Path $skillMd)
            description = $desc
        }
    }
}

# ── Scan Workflows ───────────────────────────────────────────
$workflowsDir = Join-Path $root ".agents\workflows"
$workflows = @()
if (Test-Path $workflowsDir) {
    Get-ChildItem -Path $workflowsDir -Filter "*.md" | ForEach-Object {
        $desc = ""
        $content = Get-Content $_.FullName -TotalCount 10 -ErrorAction SilentlyContinue
        foreach ($line in $content) {
            if ($line -match "^description:\s*(.+)") {
                $desc = $Matches[1].Trim()
                break
            }
        }
        $workflows += @{
            name = $_.BaseName
            command = "/" + $_.BaseName
            description = $desc
        }
    }
}

# ── Scan Projects & Local Context ────────────────────────────
$projectDir = Join-Path $root "PROJECT"
$projects = @()

# Add current directory as local context if outside Hub
if ($currentDir.Path -notlike "$root*") {
    $projects += @{
        name = "LOCAL_CONTEXT: " + $currentDir.Leaf
        path = $currentDir.Path
        has_memory = Test-Path (Join-Path $currentDir.Path "memory.json")
        has_docker = (Test-Path (Join-Path $currentDir.Path "docker-compose.yaml")) -or (Test-Path (Join-Path $currentDir.Path "docker-compose.yml"))
        is_local_focus = $true
    }
}

if (Test-Path $projectDir) {
    Get-ChildItem -Path $projectDir -Directory | ForEach-Object {
        $hasMemory = Test-Path (Join-Path $_.FullName "memory.json")
        $hasDocker = (Test-Path (Join-Path $_.FullName "docker-compose.yaml")) -or (Test-Path (Join-Path $_.FullName "docker-compose.yml"))
        $hasPython = Test-Path (Join-Path $_.FullName "*.py")
        $projects += @{
            name = $_.Name
            has_memory = $hasMemory
            has_docker = $hasDocker
            has_python = $hasPython
            is_local_focus = $false
        }
    }
}

# ── System Status ────────────────────────────────────────────
$dockerRunning = $false
try {
    $job = Start-Job -ScriptBlock { docker ps 2>&1; return $LASTEXITCODE } -ErrorAction SilentlyContinue
    $completed = Wait-Job $job -Timeout 3
    if ($completed -and $completed.State -eq "Completed") {
        $exitCode = Receive-Job $job -ErrorAction SilentlyContinue
        if ($exitCode -eq 0) { $dockerRunning = $true }
    }
    Remove-Job $job -Force -ErrorAction SilentlyContinue
} catch {}

$pythonVersion = ""
try {
    $pythonVersion = (python --version 2>&1).ToString().Trim()
} catch {}

$diskFree = ""
try {
    $drive = Get-PSDrive C -ErrorAction SilentlyContinue
    if ($drive) {
        $freeGB = [math]::Round($drive.Free / 1GB, 1)
        $diskFree = "${freeGB} GB"
    }
} catch {}

# ── Assemble Inventory ───────────────────────────────────────
$inventory = @{
    generated_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssK")
    system = @{
        docker_running = $dockerRunning
        python_version = $pythonVersion
        disk_free = $diskFree
        workspace = $root
    }
    skills = @{
        count = $skills.Count
        items = $skills
    }
    workflows = @{
        count = $workflows.Count
        items = $workflows
    }
    projects = @{
        count = $projects.Count
        items = $projects
    }
}

# ── Write Output ─────────────────────────────────────────────
$outPath = Join-Path $root ".agents\skills\nexus-god\inventory.json"
$inventory | ConvertTo-Json -Depth 5 | Set-Content -Path $outPath -Encoding UTF8

Write-Host "NEXUS GOD: Inventory generated at $outPath"
Write-Host "  Skills:    $($skills.Count)"
Write-Host "  Workflows: $($workflows.Count)"
Write-Host "  Projects:  $($projects.Count)"
Write-Host "  Docker:    $(if($dockerRunning){'ONLINE'}else{'OFFLINE'})"
Write-Host "  Python:    $pythonVersion"
Write-Host "  Disk Free: $diskFree"
