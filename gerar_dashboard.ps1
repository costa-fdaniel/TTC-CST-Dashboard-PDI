param(
    [Parameter(Mandatory = $false)]
    [string]$InputPath = "examples\prodiet_minimal",

    [Parameter(Mandatory = $false)]
    [string]$OutputPath = "dist\dashboard_pdi.html",

    [Parameter(Mandatory = $false)]
    [string]$Company = "PRODIET",

    [Parameter(Mandatory = $false)]
    [int]$Year = 2026,

    [Parameter(Mandatory = $false)]
    [string]$CsvDir = ""
)

$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot

if (-not (Test-Path -LiteralPath $InputPath)) {
    Write-Host ""
    Write-Host "Entrada nao encontrada:" -ForegroundColor Red
    Write-Host "  $InputPath"
    Write-Host ""
    Write-Host "Use um arquivo .xlsx exportado do Google Sheets ou uma pasta com CSVs."
    exit 1
}

if ([System.IO.Path]::GetExtension($InputPath).ToLowerInvariant() -eq ".gsheet") {
    Write-Host ""
    Write-Host "O arquivo informado e .gsheet, que e apenas um atalho do Google Drive." -ForegroundColor Yellow
    Write-Host "Abra a planilha no Google Sheets e exporte como .xlsx:"
    Write-Host "  Arquivo > Fazer download > Microsoft Excel (.xlsx)"
    Write-Host ""
    Write-Host "Depois rode este script apontando para o .xlsx exportado."
    exit 1
}

if ([string]::IsNullOrWhiteSpace($CsvDir)) {
    python -m pdi_dashboard build --input $InputPath --output $OutputPath --company $Company --year $Year
} else {
    python -m pdi_dashboard build --input $InputPath --output $OutputPath --company $Company --year $Year --csv-dir $CsvDir
}

Write-Host ""
Write-Host "Pronto. Abra este arquivo no navegador:" -ForegroundColor Green
Write-Host "  $((Resolve-Path -LiteralPath $OutputPath).Path)"
