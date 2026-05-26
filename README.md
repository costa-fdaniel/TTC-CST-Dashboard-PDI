# PDI Dashboard Generator

Gerador de HTML interativo para bases de beneficio fiscal de PD&I.

O projeto foi desenhado para ler uma pasta de CSVs exportados ou um arquivo `.xlsx`
com varias abas, normalizar os dados principais e gerar um dashboard HTML estatico.
Ele nao depende de servidor para abrir o resultado.

## Uso rapido

Mais simples no Windows: arraste um arquivo `.xlsx` exportado para cima de
`gerar_dashboard.bat`, ou execute:

```powershell
.\gerar_dashboard.ps1 -InputPath "caminho\arquivo.xlsx" -OutputPath "dist\prodiet.html" -Company "PRODIET" -Year 2026
```

Sem parametros, o script gera um HTML usando a base minima de exemplo.
Em toda geracao, o sistema tambem salva um CSV bruto por aba em
`exports\csv\<nome_da_base>\`, alem de um `_manifest.csv` com linhas e colunas.

## Painel multiempresa

Edite `empresas_pdi_2026.json` para adicionar ou trocar empresas e rode:

```powershell
.\gerar_portfolio.ps1
```

O resultado padrao e `dist\painel_pdi_2026.html`, com seletor de empresa,
comparativo executivo, graficos e tabelas filtraveis.

## Historico legado

Fontes antigas ficam organizadas em `data_sources\raw\<empresa>\`. Os dados
normalizados ficam em `data_sources\extracted\` e a trilha de origem em
`data_sources\evidence\manifest.csv`.

Para importar o HTML legado da NDB:

```powershell
python scripts\import_ndb_history.py --input "data_sources\raw\ndb\NETZSCH_LeiDoBem_2011_2025_v3.html"
```

Para importar os lotes legados/modernos ja baixados:

```powershell
python scripts\import_prodiet_history.py
python scripts\import_modern_history.py --company prodiet
python scripts\import_modern_history.py --company nem
```

Depois gere o painel com:

```powershell
python -m pdi_dashboard portfolio --config empresas_pdi_2026.json --output "dist\painel_pdi_2026_historico.html"
```

O painel inclui uma aba `Historico` quando houver anos normalizados para a
empresa selecionada.

```powershell
python -m pdi_dashboard build --input "caminho\arquivo.xlsx" --output "dist\prodiet.html" --company "PRODIET" --year 2026
```

Tambem funciona com uma pasta contendo um CSV por aba:

```powershell
python -m pdi_dashboard build --input "caminho\csvs" --output "dist\empresa.html" --company "EMPRESA" --year 2026
```

## Sobre arquivos `.gsheet`

Arquivos `.gsheet` do Google Drive sao atalhos, nao planilhas com dados. Exporte a
planilha como `.xlsx` pelo Google Sheets/Drive e use o arquivo exportado como entrada.

## Abas esperadas

O gerador reconhece, quando existirem:

- `RESUMO`
- `Projetos`
- `Trabalho`
- `Pessoal` ou `Pessoal (2)`
- `Investimentos`
- `Dias uteis e Feriados`
- `# Encargos folha`
- `# Salarios`
- `#verificacao RH`

As proximas empresas podem usar o mesmo comando, trocando apenas entrada, saida,
empresa e ano.
