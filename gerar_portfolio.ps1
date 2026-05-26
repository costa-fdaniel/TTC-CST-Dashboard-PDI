param(
    [Parameter(Mandatory = $false)]
    [string]$Config = "empresas_pdi_2026.json",

    [Parameter(Mandatory = $false)]
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

if (-not (Test-Path -LiteralPath $Config)) {
    Write-Host "Config nao encontrada: $Config" -ForegroundColor Red
    exit 1
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    python -m pdi_dashboard portfolio --config $Config
} else {
    python -m pdi_dashboard portfolio --config $Config --output $OutputPath
}
