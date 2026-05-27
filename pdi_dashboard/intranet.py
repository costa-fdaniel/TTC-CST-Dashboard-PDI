from __future__ import annotations

import json
from html import escape

from .html import slim_analysis


def render_intranet_site(
    analyses: list[dict],
    *,
    title: str = "Intranet PD&I",
    sheets_url: str = "",
    support_endpoint: str = "",
) -> str:
    payload = json.dumps(
        {
            "companies": [slim_analysis(item) for item in analyses],
            "sheets_url": sheets_url,
            "support_endpoint": support_endpoint,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    html = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/2.0.0/css/dataTables.dataTables.min.css">
  <script src="https://cdn.datatables.net/2.0.0/js/dataTables.min.js"></script>
  <style>
    :root {
      --bg: #f8fafc; /* Mais claro */
      --panel: #ffffff;
      --panel-2: #fefefe; /* Quase branco */
      --ink: #1e293b; /* Azul escuro */
      --muted: #64748b; /* Cinza azulado */
      --line: #e2e8f0; /* Cinza claro */
      --teal: #0f766e;
      --blue: #3867a6;
      --amber: #c47b2b;
      --red: #b84c3d;
      --green: #16805b;
      --shadow: 0 18px 42px rgba(25, 38, 35, .08);
    }
    * { box-sizing: border-box; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    body {
      margin: 0;
      background:
        linear-gradient(180deg, #f0f4f8 0, #f8fafc 320px), /* Gradiente mais suave */
        var(--bg);
      color: var(--ink);
      font-family: 'Inter', sans-serif; /* Preferência por Inter */
      font-size: 14px;
      line-height: 1.35;
    }
    button, input, select { font: inherit; }
    button { cursor: pointer; }
    .shell {
      display: grid;
      grid-template-columns: 232px minmax(0, 1fr);
      min-height: 100vh;
    }
    aside {
      position: -webkit-sticky; /* For Safari */
      position: sticky; /* Fixa a sidebar */
      top: 0;
      height: 100vh;
      padding: 22px 16px;
      color: white;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .brand {
      padding: 4px 8px 16px;
      border-bottom: 1px solid rgba(255,255,255,.15); /* Borda mais visível */
    }
    .brand h1 {
      margin: 0;
      font-size: 18px;
      letter-spacing: 0;
    }
    .brand small {
      display: block;
      margin-top: 4px;
      color: rgba(255,255,255,.62);
    }
    nav {
      display: grid;
      gap: 6px;
    }
    nav button {
      border: 0;
      border-radius: 8px;
      padding: 11px 12px;
      text-align: left; /* Alinhamento à esquerda */
      color: rgba(255,255,255,.76);
      background: transparent;
      font-weight: 750;
    }
    nav button.active {
      color: white;
      background: rgba(255,255,255,.18); /* Fundo mais escuro para ativo */
      box-shadow: inset 3px 0 0 var(--amber);
    }
    .side-note {
      margin-top: auto;
      padding: 12px;
      border-radius: 8px;
      background: rgba(255,255,255,.08);
      color: rgba(255,255,255,.7);
      font-size: 12px;
    }
    main {
      min-width: 0;
      padding: 20px 24px 38px;
      background: var(--bg); /* Garante que o main tenha o fundo correto */
    }
    .topbar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); /* Mais flexível */
      gap: 12px;
      align-items: center;
      margin-bottom: 20px;
    }
    select, input {
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
      color: var(--ink);
      padding: 9px 12px;
      outline: none;
    }
    select:focus, input:focus, textarea:focus { /* Adicionado textarea */
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(15,118,110,.14);
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(320px, .7fr); /* Ajuste de proporção */
      gap: 16px;
      margin-bottom: 16px;
    }
    .hero-main, .panel, details.panel {
      background: rgba(255,255,255,.92);
      border: 1px solid var(--line); /* Borda mais suave */
      border-radius: 12px;
      box-shadow: var(--shadow);
    }
    .hero-main {
      padding: 24px;
      min-height: 230px;
      display: grid;
      align-content: space-between;
      background: linear-gradient(135deg, var(--panel) 0%, #f0f4f8 100%); /* Gradiente sutil */
    }
    .hero-main .eyebrow {
      color: var(--blue); /* Cor mais distinta */
      font-size: 13px; /* Um pouco maior */
      letter-spacing: .05em;
    }
    .eyebrow {
      color: var(--teal);
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 850;
      letter-spacing: .04em;
    }
    .hero-title {
      margin: 8px 0 6px;
      font-size: clamp(26px, 3vw, 42px); /* Título maior */
      line-height: 1.02;
      letter-spacing: 0;
    }
    .source {
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
      max-width: 940px;
    }
    .metric-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-top: 22px;
    }
    .metric {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
      padding: 12px;
      min-height: 86px;
    }
    .metric span {
      color: var(--muted);
      font-size: 11px;
      font-weight: 700; /* Menos negrito */
      text-transform: uppercase;
    }
    .metric b {
      display: block;
      margin-top: 7px;
      font-size: 18px;
      overflow-wrap: anywhere;
    }
    .metric small {
      display: block;
      margin-top: 3px;
      color: var(--muted);
    }
    .panel, details.panel {
      padding: 16px;
      margin-bottom: 16px;
    }
    .panel h2, details.panel summary {
      margin: 0;
      font-size: 16px;
      letter-spacing: 0;
      font-weight: 850;
    }
    .panel-head {
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 16px; /* Margem maior */
    }
    .hint {
      color: var(--muted);
      font-size: 12px;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(360px, .8fr); /* Ajuste de proporção */
      gap: 16px;
      align-items: start;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }
    .calc-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); /* Mais flexível */
      gap: 10px;
    }
    .calc-card {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
      padding: 12px;
    }
    .calc-card span {
      display: block;
      color: var(--muted);
      font-size: 11px; /* Um pouco maior */
      font-weight: 850;
      text-transform: uppercase;
    }
    .calc-card b {
      display: block;
      margin-top: 6px;
      font-size: 16px;
    }
    .calc-card small {
      display: block;
      color: var(--muted);
      margin-top: 4px;
    }
    .sim-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); /* Mais flexível */
      gap: 10px;
      margin-top: 12px;
    }
    .sim-result {
      margin-top: 12px;
      padding: 12px;
      border-radius: 10px;
      background: #e7f2f0;
      border: 1px solid #bfdbd7; /* Borda mais suave */
      font-weight: 700; /* Menos negrito */
    }
    .stack {
      height: 18px;
      display: flex;
      overflow: hidden;
      border-radius: 99px;
      background: #e9eeed;
      margin: 14px 0 12px;
    }
    .stack i { display: block; width: var(--w); background: var(--c); }
    .legend {
      display: grid;
      gap: 10px;
      padding: 0;
      margin: 0;
      list-style: none;
    }
    .legend li, .summary li {
      display: flex; /* Flexbox para alinhamento */
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 9px;
      border-bottom: 1px solid var(--line);
    }
    .legend em {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 3px;
      margin-right: 7px;
      background: var(--c);
      vertical-align: middle;
    }
    .chart {
      display: grid;
      gap: 12px; /* Espaçamento maior */
    }
    .history-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .history-year {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2); /* Fundo mais claro */
      padding: 12px;
    }
    .history-year h3 {
      margin: 0 0 10px;
      font-size: 15px;
    }
    .bar {
      display: grid;
      grid-template-columns: minmax(120px, 260px) 1fr auto; /* Ajuste de largura */
      align-items: center;
      gap: 10px;
      font-size: 13px;
    }
    .bar label {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-weight: 750;
    }
    .track {
      height: 12px;
      border-radius: 99px;
      background: var(--line); /* Cor de fundo da trilha */
      overflow: hidden;
    }
    .fill {
      width: var(--w);
      height: 100%;
      border-radius: 99px;
      background: linear-gradient(90deg, var(--teal), #2e9d8f);
    } /* Cores de gradiente mais suaves */
    .fill.blue { background: linear-gradient(90deg, #5c85d6, #3867a6); }
    .fill.amber { background: linear-gradient(90deg, #e0a35b, #c47b2b); }
    .pill {
      display: inline-flex; /* Flexbox para alinhamento */
      align-items: center;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      font-weight: 850;
      background: #eef2f1;
      color: var(--muted);
      white-space: nowrap;
    }
    .pill.ok { color: var(--green); background: #dcfce7; } /* Fundo mais claro */
    .pill.no { color: var(--red); background: #fee2e2; } /* Fundo mais claro */
    .project-list { /* Espaçamento maior */
      display: grid;
      gap: 10px;
    }
    .project-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: 12px;
      padding: 16px; /* Padding maior */
      transition: border-color .14s ease, transform .14s ease, box-shadow .14s ease;
    }
    .project-card:hover {
      border-color: var(--teal); /* Borda teal no hover */
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(25, 38, 35, .06); /* Sombra mais suave */
    }
    .project-card.selected {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(15,118,110,.18); /* Sombra mais forte para selecionado */
    }
    .project-card button {
      all: unset;
      cursor: pointer;
      display: block;
      width: 100%;
    }
    .project-top {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 14px; /* Espaçamento maior */
      margin-bottom: 8px;
    }
    .project-top strong {
      display: block;
      font-size: 15px;
    }
    .project-desc {
      color: var(--muted);
      font-size: 13px;
      min-height: 35px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .mini-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); /* Mais flexível */
      gap: 8px;
      margin-top: 12px;
    }
    .mini {
      background: var(--panel-2);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px;
    }
    .mini span {
      display: block;
      font-size: 10px;
      color: var(--muted); /* Cor mais suave */
      text-transform: uppercase;
      font-weight: 850;
    }
    .mini b {
      display: block;
      margin-top: 4px;
      font-size: 13px;
    }
    .text-panels {
      display: grid;
      gap: 10px;
    }
    .text-panels article {
      background: var(--panel-2);
      border: 1px solid var(--line); /* Borda mais suave */
      border-radius: 10px;
      padding: 12px;
    }
    .text-panels h3 {
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }
    .text-panels p {
      margin: 0;
      font-size: 13px;
    }
    section { display: none; min-height: 50vh; } /* Adicionado min-height */
    section.active { display: block; }
    details.panel summary {
      cursor: pointer;
      list-style: none;
    }
    details.panel summary::-webkit-details-marker { display: none; }
    details.panel summary::after {
      content: "+";
      float: right;
      color: var(--blue); /* Cor diferente para o ícone */
      font-size: 22px;
    }
    details.panel[open] summary {
      margin-bottom: 14px;
    }
    details.panel[open] summary::after { content: "-"; }
    .table-tools {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    .table-tools input { max-width: 340px; }
    .table-wrap {
      max-height: 58vh; /* Altura máxima ajustada */
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: white;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 800px; /* Largura mínima maior */
      font-size: 12px;
    }
    th, td {
      padding: 9px 10px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      max-width: 380px;
    }
    th {
      position: sticky;
      top: 0;
      background: #eef2f6; /* Fundo mais claro */
      color: #34403d;
      font-size: 11px;
      text-transform: uppercase;
      z-index: 1;
    }
    .empty {
      color: var(--muted);
      padding: 16px 0;
    }
    .chat-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px; /* Largura maior para o painel lateral */
      gap: 16px;
    }
    .chat-box {
      background: white;
      border: 1px solid var(--line);
      border-radius: 12px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .messages {
      min-height: 400px; /* Altura mínima ajustada */
      max-height: 62vh;
      overflow: auto;
      padding: 16px;
      display: grid;
      gap: 12px;
      align-content: start;
    }
    .msg {
      max-width: 900px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 11px 12px;
      background: var(--panel-2); /* Fundo mais claro */
      white-space: pre-wrap;
    }
    .msg.user {
      margin-left: auto;
      background: #e0f2f7; /* Fundo azul claro para usuário */
      border-color: #bfdbd7;
    }
    .msg ul { margin: 8px 0 0; padding-left: 18px; }
    .chat-form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      padding: 12px;
      border-top: 1px solid var(--line);
      background: var(--panel-2); /* Fundo mais claro */
    }
    .primary {
      border: 0;
      border-radius: 8px;
      padding: 0 16px;
      background: var(--teal);
      color: white;
      font-weight: 700; /* Menos negrito */
    }
    .quick {
      display: grid;
      gap: 8px;
    }
    .quick button {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
      text-align: left; /* Alinhamento à esquerda */
      background: white;
      color: var(--ink);
      font-weight: 750;
    }
    .agent-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 12px;
    }
    .agent-actions a, .agent-actions button {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px 11px;
      background: var(--panel-2); /* Fundo mais claro */
      color: var(--ink);
      font-weight: 850;
      text-decoration: none;
      cursor: pointer;
    }
    @media (max-width: 1120px) {
      .shell { grid-template-columns: 1fr; }
      aside {
        position: static;
        height: auto;
        padding: 16px; /* Padding ajustado */
      }
      nav {
        display: flex;
        overflow-x: auto;
      }
      .side-note { display: none; }
      main { padding: 18px 16px 36px; }
      .topbar { grid-template-columns: 1fr 1fr; }
      .hero, .grid-2, .chat-layout { grid-template-columns: 1fr; }
    }
    @media (max-width: 768px) { /* Breakpoint ajustado */
      .topbar, .metric-strip, .grid-3, .mini-grid, .calc-grid, .sim-grid { grid-template-columns: 1fr; }
      .bar { grid-template-columns: 1fr; }
      .hero-main { padding: 18px; }
      table { min-width: 620px; }
      .chat-form { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="brand">
        <h1>__TITLE__</h1>
        <small>Relatórios de PD&I e Lei do Bem</small>
      </div>
      <nav id="tabs"></nav>
      <div class="side-note">Use os filtros para cruzar projeto, status, atividades, RH e investimentos. As bases ficam recolhidas na aba Auditoria.</div>
    </aside>
    <main>
      <div class="topbar">
        <select id="companySelect" aria-label="Empresa" onchange="setCompany(this.value)"></select>
        <select id="yearFilterSelect" aria-label="Ano" onchange="setYearFilter(this.value)">
          <option value="all">Todos os anos</option>
          <!-- Opções preenchidas via JS -->
        </select>
        <select id="projectSelect" aria-label="Projeto" onchange="setProject(this.value)"></select>
        <select id="departmentSelect" aria-label="Departamento" onchange="setDepartment(this.value)"></select>
        <select id="statusSelect" aria-label="Status" onchange="setStatus(this.value)">
          <option value="all">Todos os status</option>
          <option value="ok">Incentivados</option>
          <option value="no">Não incentivados</option>
        </select>
        <input id="searchInput" placeholder="Buscar projeto, atividade, fornecedor, colaborador" oninput="setSearch(this.value)">
      </div>
      <div id="app"></div>
    </main>
  </div>
  <script id="data" type="application/json">__PAYLOAD__</script>
  <script>
    const PORTFOLIO = JSON.parse(document.getElementById('data').textContent);
    const COMPANIES = PORTFOLIO.companies || [];
    const fmtMoney = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    const fmtNum = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2, minimumFractionDigits: 0 });
    const state = { company: 0, project: 'all', status: 'all', q: '', department: 'all', tab: 'overview', impact: 'all', yearFilter: 'all' }; // Novos estados
    const chatState = {};
    let searchTimer = null;
    let DATA = COMPANIES[0] || {};
    window.TABLES = {};
    const PIE_COLORS = ['#0f766e', '#3867a6', '#c47b2b', '#b84c3d', '#16805b', '#66726f', '#a63867', '#2b8c8c', '#8c2b8c', '#8c8c2b'];
    window.CHART_CONFIGS = {};
    const tabs = [
      ['overview', 'Resumo'],
      ['projects', 'Projetos'],
      ['activities', 'Atividades'],
      ['finance', 'Valores'],
      ['people', 'Pessoas'],
      ['history', 'Histórico'],
      ['avaliacao', 'Avaliação PD&I'], // Renamed from 'risks'
      ['risks_opportunities', 'Riscos e Oportunidades'], // Nova aba
      ['tecnoparque', 'Tecnoparque'], // Nova aba Tecnoparque
      ['chat', 'Chatbot'],
      ['audit', 'Auditoria']
    ];

    const $ = id => document.getElementById(id); // Helper function
    const norm = v => String(v || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase().trim();
    const money = v => fmtMoney.format(Number(v || 0));
    const num = v => fmtNum.format(Number(v || 0));
    const esc = v => String(v ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
    const short = (v, n = 140) => {
      const text = String(v || '').replace(/\\s+/g, ' ').trim();
      return text.length > n ? text.slice(0, n - 3) + '...' : text;
    };
    function cell(row, names) {
      const wanted = names.map(norm);
      const key = Object.keys(row || {}).find(k => wanted.includes(norm(k)));
      return key ? row[key] : '';
    }
    function numCell(row, names) {
      const raw = String(cell(row, names) || '').replace(/R\\$/g, '').replace(/%/g, '').trim();
      if (!raw || raw === '-') return 0;
      const normalized = raw.includes(',') ? raw.replace(/\\./g, '').replace(',', '.') : raw;
      const value = Number(normalized);
      return Number.isFinite(value) ? value : 0;
    }
    function boolCell(row, names) {
      return ['true', 'verdadeiro', 'sim', 'yes', '1', 'x'].includes(norm(cell(row, names))); // Adicionado 'x' para booleanos
    }
    function codeKey(v) {
      const match = String(v || '').toUpperCase().match(/(INOV|NRD)0*(\\d{1,7})/);
      return match ? match[1] + String(Number(match[2])) : '';
    }
    function codeLabel(v) {
      const match = String(v || '').toUpperCase().match(/(INOV|NRD)0*(\\d{1,7})/);
      return match ? match[1] + String(Number(match[2])).padStart(5, '0') : '';
    }
    function codeFrom(v) {
      return codeLabel(v);
    }
    function cleanRows(rows) {
      return (rows || []).filter(row => Object.values(row || {}).some(v => String(v || '').trim()));
    }
    function departmentValue(row) {
      return String(cell(row, ['Departamento', 'Setor', 'Area', 'Área']) || '').trim();
    }
    function matchDepartment(row) {
      return state.department === 'all' || norm(departmentValue(row)) === norm(state.department);
    }
    function allDepartments() {
      const seen = new Map();
      cleanRows(DATA.tables?.pessoal || []).forEach(row => {
        const value = departmentValue(row);
        if (value && !seen.has(norm(value))) seen.set(norm(value), value);
      });
      return [...seen.values()].sort((a, b) => a.localeCompare(b, 'pt-BR'));
    }
    function departmentProjectRefs() {
      if (state.department === 'all') return null;
      const refs = new Set();
      cleanRows(DATA.tables?.pessoal || []).filter(matchDepartment).forEach(row => {
        const project = String(cell(row, ['Projeto', 'Attach']) || '').trim();
        const code = codeKey(project);
        if (code) refs.add(code);
        if (project) refs.add(norm(project));
      });
      return refs;
    }
    function matchCode(row, code) {
      if (!code || code === 'all') return true;
      const target = codeKey(code);
      if (target && Object.keys(row || {}).some(k => codeKey(k) === target && numCell(row, [k]) > 0)) return true;
      if (numCell(row, [code]) > 0) return true;
      const text = Object.values(row || {}).join(' ').toUpperCase();
      if (text.includes(code)) return true;
      const found = text.match(/(INOV|NRD)0*(\\d{1,7})/g) || [];
      return !!target && found.some(item => codeKey(item) === target);
    }
    function rowProjectText(row) {
      return String(cell(row, ['Projeto', 'Attach', 'Projeto e eventual info de rateio', 'Projeto vinculado', 'Código', 'Codigo']) || '').trim();
    }
    function projectUid(row, index) {
      const title = String(cell(row, ['Projeto']) || '').trim();
      const attach = String(cell(row, ['Attach']) || '').trim();
      const code = codeFrom(title) || codeFrom(attach);
      const token = code || attach || title || ('projeto-' + index);
      return 'p' + index + '-' + norm(token).replace(/[^a-z0-9]+/g, '-').slice(0, 80);
    }
    function matchProject(row, project) {
      if (!project || state.project === 'all') return true;
      const projectCode = codeKey(project.code || project.attach || project.title);
      if (projectCode && matchCode(row, project.code || project.attach || project.title)) return true;
      const rowProject = rowProjectText(row);
      const rowNorm = norm(rowProject);
      const attachNorm = norm(project.attach);
      const titleNorm = norm(project.title);
      if (attachNorm && rowNorm && rowNorm === attachNorm) return true;
      if (titleNorm && rowNorm && (rowNorm === titleNorm || rowNorm.includes(titleNorm) || titleNorm.includes(rowNorm))) return true;
      const textNorm = norm(Object.values(row || {}).join(' '));
      if (attachNorm && attachNorm.length >= 3 && textNorm.includes(attachNorm)) return true;
      if (titleNorm && titleNorm.length >= 12 && textNorm.includes(titleNorm.slice(0, 80))) return true;
      return false;
    }
    function matchSearch(row) {
      return !state.q || norm(Object.values(row || {}).join(' ')).includes(norm(state.q));
    }
    function matchImpact(row) {
      return state.impact === 'all' || norm(cell(row, ['Impacto'])) === norm(state.impact);
    }
    function matchYearFilter(row) {
      return state.yearFilter === 'all' || norm(cell(row, ['Ano', 'Year'])) === norm(state.yearFilter);
    }
    function sum(rows, names) {
      return rows.reduce((acc, row) => acc + numCell(row, names), 0);
    }
    function projectInvestmentValue(row, code) {
      const target = codeKey(code);
      if (target) {
        const key = Object.keys(row || {}).find(k => codeKey(k) === target && numCell(row, [k]) > 0);
        if (key) return numCell(row, [key]);
      }
      return numCell(row, ['Valor Incentivado', 'Valor']);
    }
    function sumInvestments(rows, code = 'all') {
      return rows.reduce((acc, row) => acc + projectInvestmentValue(row, code), 0);
    }
    function group(rows, keyNames, valueNames, limit = 12) {
      const map = new Map();
      cleanRows(rows).filter(matchSearch).forEach(row => {
        const key = String(cell(row, keyNames) || 'Não informado').trim() || 'Não informado';
        const value = numCell(row, valueNames);
        if (value) map.set(key, (map.get(key) || 0) + value);
      });
      return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(([name, value]) => ({ name, value }));
    }
    function countBy(rows, keyNames, limit = 12) {
      const map = new Map();
      cleanRows(rows).filter(matchSearch).forEach(row => {
        const key = String(cell(row, keyNames) || 'Não informado').trim() || 'Não informado';
        map.set(key, (map.get(key) || 0) + 1);
      });
      return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(([name, value]) => ({ name, value }));
    }
    function groupInvestments(rows, keyNames, code = 'all', limit = 12) {
      const map = new Map();
      cleanRows(rows).filter(matchSearch).forEach(row => {
        const key = String(cell(row, keyNames) || 'Não informado').trim() || 'Não informado';
        const value = projectInvestmentValue(row, code);
        if (value) map.set(key, (map.get(key) || 0) + value);
      });
      return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(([name, value]) => ({ name, value }));
    }
    function allProjects() {
      const refs = departmentProjectRefs();
      return cleanRows(DATA.tables?.projetos || []).filter(row => {
        if (!refs) return true;
        const title = String(cell(row, ['Projeto']) || '').trim();
        const attach = String(cell(row, ['Attach']) || '').trim();
        const code = codeKey(title) || codeKey(attach);
        return (code && refs.has(code)) || refs.has(norm(title)) || refs.has(norm(attach));
      }).map((row, index) => {
        const title = String(cell(row, ['Projeto']) || '').trim();
        const attach = String(cell(row, ['Attach']) || '').trim();
        const code = codeFrom(title) || codeFrom(attach) || attach || title.split(' ')[0];
        const project = { uid: projectUid(row, index), code, attach, title: title || code || 'Projeto' };
        const work = cleanRows(DATA.tables?.trabalho || []).filter(r => matchProject(r, project));
        const people = cleanRows(DATA.tables?.pessoal || []).filter(r => matchProject(r, project)).filter(matchDepartment);
        const inv = cleanRows(DATA.tables?.investimentos || []).filter(r => matchProject(r, project));
        const accepted = work.filter(r => boolCell(r, ['Projeto incentivado?']) && boolCell(r, ['Atividade incentivada?']));
        const rejected = work.filter(r => !boolCell(r, ['Projeto incentivado?']) || !boolCell(r, ['Atividade incentivada?']));
        const rh = numCell(row, ['Total Help Desk']) || sum(people, ['Total PD&I', 'Total PDI']);
        const investment = numCell(row, ['Total investido']) || sumInvestments(inv, code);
        const ok = boolCell(row, ['Incentivado?', 'Lei do Bem?', 'Projeto incentivado?']);
        return {
          uid: project.uid,
          code,
          attach,
          row,
          work,
          people,
          inv,
          accepted,
          rejected,
          ok,
          rh,
          investment,
          base: rh + investment,
          hours: sum(accepted, ['Horas decimais', 'Horas']),
          title: title || code || 'Projeto',
          nature: cell(row, ['Natureza']) || 'Não informada',
          desc: cell(row, ['Descrição']) || ''
        };
      }).filter(p => p.uid || p.code || p.title);
    }
    function visibleProjects() {
      return allProjects().filter(p => {
        if (state.project !== 'all' && p.uid !== state.project) return false;
        if (state.status === 'ok' && !p.ok) return false;
        if (state.status === 'no' && p.ok) return false;
        if (state.q && !norm([p.code, p.attach, p.title, p.nature, p.desc].join(' ')).includes(norm(state.q))) return false;
        return true;
      });
    }
    function activeProject() {
      const list = visibleProjects();
      return state.project !== 'all' ? list[0] : list.sort((a, b) => b.base - a.base)[0];
    }
    function activeRows(key) {
      const selected = state.project === 'all' ? null : allProjects().find(p => p.uid === state.project);
      let rows = cleanRows(DATA.tables?.[key] || []).filter(row => matchProject(row, selected)).filter(matchSearch);
      if (key === 'pessoal' || key === 'trabalho' || key === 'investimentos' || key === 'riscos_oportunidades') rows = rows.filter(matchDepartment).filter(matchYearFilter); // Aplica filtro de ano e departamento
      return rows;
    }
    function kpi(label, value, sub = '') {
      return '<div class="metric"><span>' + esc(label) + '</span><b>' + value + '</b><small>' + esc(sub) + '</small></div>';
    }
    function composition(parts) {
      const total = parts.reduce((a, p) => a + Number(p.value || 0), 0) || 1;
      const stack = parts.map(p => '<i style="--w:' + Math.max(0, Number(p.value || 0) / total * 100) + '%;--c:' + p.color + '"></i>').join('');
      const legend = parts.map(p => '<li><span><em style="--c:' + p.color + '"></em>' + esc(p.label) + '</span><b>' + money(p.value) + '</b></li>').join('');
      return '<div class="stack">' + stack + '</div><ul class="legend">' + legend + '</ul>';
    }
    function chart(title, rows, kind = 'number', tone = '', chartType = 'bar') { // Adiciona chartType
      const chartId = 'chart-' + Math.random().toString(36).substr(2, 9);
      const clean = (rows || []).filter(r => Number(r.value || 0) > 0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>' + esc(title) + '</h2></div><div class="empty">Sem dados suficientes para exibir.</div></div>';

      const labels = clean.map(r => r.name);
      const values = clean.map(r => r.value);

      let backgroundColor;
      if (chartType === 'pie') {
        backgroundColor = labels.map((_, i) => PIE_COLORS[i % PIE_COLORS.length]);
      } else { // Cores para gráfico de barras
        backgroundColor = {
    return html.replace("__TITLE__", escape(title)).replace("__PAYLOAD__", payload)
