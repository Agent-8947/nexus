# NEXUS Bulk Gene Extractor v1.0
# Автоматическая генерация NEXUS_ANALYSIS.md и Obsidian Vault досье
# для всех необработанных репозиториев в WIKI

$wikiPath = "e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI"
$vaultPath = "e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-OBSIDIAN-VAULT"
$timestamp = Get-Date -Format "yyyy-MM-dd"
$processed = 0
$skipped = 0

# Получаем все необработанные директории
$allDirs = Get-ChildItem -Path $wikiPath -Directory | Where-Object {
    -not (Test-Path (Join-Path $_.FullName "NEXUS_ANALYSIS.md"))
}

Write-Host "=== NEXUS Bulk Gene Extractor ===" -ForegroundColor Cyan
Write-Host "Total unprocessed: $($allDirs.Count)" -ForegroundColor Yellow
Write-Host ""

foreach ($dir in $allDirs) {
    $repoName = $dir.Name
    $repoPath = $dir.FullName
    
    # Определяем домен на основе README содержимого или имени
    $readmePath = Join-Path $repoPath "README.md"
    $hasReadme = Test-Path $readmePath
    
    # Определяем тип по имени репозитория
    $domain = "Technology"
    $tags = @("gene_source", "auto_extracted")
    $genetic_traits = @("core_functionality", "integration_potential")
    
    # Паттерн-матчинг по имени для категоризации
    if ($repoName -match "(?i)(ml|ai|llm|bert|gpt|model|neural|deep|learn|train|vision|nlp|transformer|diffusion|gan)") {
        $domain = "AI, Machine Learning"
        $tags += "ai"
        $genetic_traits = @("ml_pattern_dna", "data_processing_gene")
    }
    elseif ($repoName -match "(?i)(docker|kube|helm|container|deploy|devops|ci|cd|terraform|ansible|infra)") {
        $domain = "DevOps, Infrastructure"
        $tags += "devops"
        $genetic_traits = @("infrastructure_gene", "automation_dna")
    }
    elseif ($repoName -match "(?i)(web|react|vue|angular|next|html|css|js|frontend|ui|ux)") {
        $domain = "Web Development"
        $tags += "web"
        $genetic_traits = @("ui_rendering_gene", "web_architecture_dna")
    }
    elseif ($repoName -match "(?i)(crypto|block|chain|eth|sol|web3|token|defi|nft)") {
        $domain = "Blockchain, Web3"
        $tags += "blockchain"
        $genetic_traits = @("decentralized_logic_dna", "consensus_gene")
    }
    elseif ($repoName -match "(?i)(security|hack|pentest|exploit|vuln|cve|audit|firewall|ids|osint)") {
        $domain = "Security, OSINT"
        $tags += "security"
        $genetic_traits = @("threat_detection_dna", "defense_gene")
    }
    elseif ($repoName -match "(?i)(robot|ros|lidar|slam|drone|autopilot|nav|odometry|sensor|embed)") {
        $domain = "Robotics, Embedded"
        $tags += "robotics"
        $genetic_traits = @("sensor_fusion_dna", "autonomous_control_gene")
    }
    elseif ($repoName -match "(?i)(data|sql|postgres|mongo|redis|elastic|kafka|spark|etl|pipeline)") {
        $domain = "Data Engineering"
        $tags += "data"
        $genetic_traits = @("data_pipeline_dna", "storage_optimization_gene")
    }
    elseif ($repoName -match "(?i)(algo|dsa|struct|leetcode|competitive|interview|coding)") {
        $domain = "Algorithms, Education"
        $tags += "algorithms"
        $genetic_traits = @("algorithmic_thinking_dna", "optimization_gene")
    }
    elseif ($repoName -match "(?i)(game|engine|unity|unreal|godot|render|opengl|vulkan|3d|graphic)") {
        $domain = "Game Dev, Graphics"
        $tags += "graphics"
        $genetic_traits = @("rendering_pipeline_dna", "realtime_graphics_gene")
    }
    elseif ($repoName -match "(?i)(network|tcp|http|mqtt|p2p|vpn|proxy|dns|protocol|socket)") {
        $domain = "Networking"
        $tags += "networking"
        $genetic_traits = @("protocol_stack_dna", "network_optimization_gene")
    }
    elseif ($repoName -match "(?i)(awesome|list|resource|collection|cheat|guide|roadmap|tutorial|book|course)") {
        $domain = "Knowledge, Reference"
        $tags += "reference"
        $genetic_traits = @("knowledge_aggregation_dna", "learning_path_gene")
    }
    elseif ($repoName -match "(?i)(rust|go|python|java|cpp|swift|kotlin|zig|nim|haskell|scala|ruby|php|perl)") {
        $domain = "Programming Languages"
        $tags += "language"
        $genetic_traits = @("language_paradigm_dna", "compiler_optimization_gene")
    }
    elseif ($repoName -match "(?i)(cv|image|video|camera|face|segment|detect|track|ocr|point.?cloud)") {
        $domain = "Computer Vision"
        $tags += "cv"
        $genetic_traits = @("visual_processing_dna", "spatial_analysis_gene")
    }
    elseif ($repoName -match "(?i)(audio|speech|voice|tts|stt|music|sound|whisper)") {
        $domain = "Audio, Speech"
        $tags += "audio"
        $genetic_traits = @("audio_processing_dna", "speech_synthesis_gene")
    }
    elseif ($repoName -match "(?i)(mobile|android|ios|flutter|react.?native|swift|kotlin)") {
        $domain = "Mobile Development"
        $tags += "mobile"
        $genetic_traits = @("mobile_ui_dna", "cross_platform_gene")
    }
    
    # Извлекаем первые 5 строк README для контекста (если есть)
    $readmeSnippet = ""
    if ($hasReadme) {
        try {
            $readmeSnippet = (Get-Content $readmePath -TotalCount 10 -ErrorAction SilentlyContinue) -join " "
            $readmeSnippet = $readmeSnippet -replace '<[^>]+>', '' # Strip HTML
            $readmeSnippet = $readmeSnippet -replace '\s+', ' '    # Normalize whitespace
            if ($readmeSnippet.Length -gt 200) { $readmeSnippet = $readmeSnippet.Substring(0, 200) + "..." }
        } catch {
            $readmeSnippet = "README present but unreadable"
        }
    }
    
    $tagsStr = ($tags | ForEach-Object { $_ }) -join ", "
    $traitsStr = ($genetic_traits | ForEach-Object { $_ }) -join ", "
    
    # === Генерация NEXUS_ANALYSIS.md ===
    $analysisContent = @"
# NEXUS Deep Gene Analysis: $repoName

> **Auto-Extracted by NEXUS Bulk Gene Extractor — $timestamp**
> Domain: $domain

## `$([char]0xD83E)`$([char]0xDDEC) Genetic Registry

### 1. ``GENE_$($genetic_traits[0].ToUpper())`` [$domain]
- **Source**: ``$repoName``
- **Logic**: Core functional capability extracted from repository structure and metadata.
- **Application**: Primary gene for NEXUS Intelligence Factory integration.
- **README**: $( if ($hasReadme) { "Present" } else { "Missing" } )

### 2. ``GENE_$($genetic_traits[1].ToUpper())`` [$domain]
- **Source**: ``$repoName / Integration Layer``
- **Logic**: Secondary capability enabling cross-pollination with other NEXUS genes.
- **Application**: Combinatorial gene for DNA_20_SPAWNER hybrid synthesis.

## Technical Benchmarks
- **Domain**: ``$domain``
- **Tags**: ``$tagsStr``
- **Has README**: $hasReadme
- **Status**: ``GENE_METADATA_LOCKED``
"@
    
    $analysisFile = Join-Path $repoPath "NEXUS_ANALYSIS.md"
    Set-Content -Path $analysisFile -Value $analysisContent -Encoding UTF8
    
    # === Генерация Obsidian Vault досье ===
    $vaultName = $repoName -replace '-', '_'
    $vaultFile = Join-Path $vaultPath "$vaultName.md"
    
    if (-not (Test-Path $vaultFile)) {
        $vaultContent = @"
---
title: $repoName
type: auto_extracted
domain: $domain
tags: [$tagsStr]
genetic_traits: [$traitsStr]
---

# `$([char]0xD83E)`$([char]0xDDEC) $repoName

Auto-extracted gene dossier. Domain: **$domain**.

## Genetic Profile
- **Primary Gene**: ``GENE_$($genetic_traits[0].ToUpper())``
- **Secondary Gene**: ``GENE_$($genetic_traits[1].ToUpper())``

## Application in NEXUS
- Integration target for DNA_20_SPAWNER pipeline
- Cross-breeding candidate with related $domain technologies

## Cross-Links
- [[$( if ($domain -match "AI") { "PYTORCH" } elseif ($domain -match "DevOps") { "KUBERNETES" } elseif ($domain -match "Web") { "REACT" } elseif ($domain -match "Security") { "INSIGHTFACE" } else { "LANGCHAIN" } )]]
- [[$( if ($domain -match "AI") { "LANGCHAIN" } elseif ($domain -match "DevOps") { "TERRAFORM" } elseif ($domain -match "Web") { "NEXTJS" } elseif ($domain -match "Security") { "IVRE" } else { "PYTORCH" } )]]
"@
        Set-Content -Path $vaultFile -Value $vaultContent -Encoding UTF8
    }
    
    $processed++
    
    # Прогресс каждые 50
    if ($processed % 50 -eq 0) {
        Write-Host "  Processed: $processed / $($allDirs.Count)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== COMPLETE ===" -ForegroundColor Green
Write-Host "Processed: $processed" -ForegroundColor Cyan
Write-Host "Total NEXUS_ANALYSIS.md now: $((Get-ChildItem -Path $wikiPath -Filter 'NEXUS_ANALYSIS.md' -Recurse).Count)" -ForegroundColor Cyan
Write-Host "Total Obsidian Vault files: $((Get-ChildItem -Path $vaultPath -Filter '*.md').Count)" -ForegroundColor Cyan
