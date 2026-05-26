from __future__ import annotations

import json
from html import escape


def render_dashboard(analysis: dict) -> str:
    return render_portfolio([analysis], title=f"Dashboard PD&I - {analysis.get('company', 'Empresa')}")


def render_portfolio(analyses: list[dict], title: str = "Painel Executivo PD&I") -> str:
    payload = json.dumps({"title": title, "companies": [slim_analysis(item) for item in analyses]}, ensure_ascii=False, separators=(",", ":"))
    html = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #f5f7f7;
      --panel: #ffffff;
      --panel-2: #fbfcfc;
      --ink: #17201f;
      --muted: #66726f;
      --line: #dfe5e3;
      --teal: #0f766e;
      --blue: #3867a6;
      --amber: #c47b2b;
      --red: #b84c3d;
      --green: #16805b;
      --shadow: 0 18px 42px rgba(25, 38, 35, .08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background:
        linear-gradient(180deg, #eef4f3 0, #f5f7f7 320px),
        var(--bg);
      color: var(--ink);
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
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
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 22px 16px;
      background: #17201f;
      color: white;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .brand {
      padding: 4px 8px 16px;
      border-bottom: 1px solid rgba(255,255,255,.12);
    }
    .brand h1 {
      margin: 0;
      font-size: 18px;
      letter-spacing: 0;
    }
    .brand small {
      display: block;
      margin-top: 6px;
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
      text-align: left;
      color: rgba(255,255,255,.76);
      background: transparent;
      font-weight: 750;
    }
    nav button.active {
      color: white;
      background: rgba(255,255,255,.12);
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
    }
    .topbar {
      display: grid;
      grid-template-columns: minmax(180px, 280px) minmax(150px, 240px) minmax(120px, 180px) minmax(120px, 180px) minmax(220px, 1fr);
      gap: 10px;
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
    select:focus, input:focus {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(15,118,110,.14);
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(320px, .8fr);
      gap: 16px;
      margin-bottom: 16px;
    }
    .hero-main, .panel, details.panel {
      background: rgba(255,255,255,.92);
      border: 1px solid var(--line);
      border-radius: 12px;
      box-shadow: var(--shadow);
    }
    .hero-main {
      padding: 24px;
      min-height: 230px;
      display: grid;
      align-content: space-between;
      overflow: hidden;
      position: relative;
    }
    .hero-main::after {
      content: "";
      position: absolute;
      right: -120px;
      top: -120px;
      width: 310px;
      height: 310px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(15,118,110,.18), rgba(15,118,110,0) 67%);
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
      font-size: clamp(24px, 3vw, 38px);
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
      font-weight: 850;
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
      margin-bottom: 14px;
    }
    .hint {
      color: var(--muted);
      font-size: 12px;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(330px, .72fr);
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
      grid-template-columns: repeat(4, minmax(0, 1fr));
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
      font-size: 10px;
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
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 12px;
    }
    .sim-result {
      margin-top: 12px;
      padding: 12px;
      border-radius: 10px;
      background: #e7f2f0;
      border: 1px solid #bfdbd7;
      font-weight: 850;
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
      display: flex;
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
      gap: 10px;
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
      background: white;
      padding: 12px;
    }
    .history-year h3 {
      margin: 0 0 10px;
      font-size: 15px;
    }
    .bar {
      display: grid;
      grid-template-columns: minmax(110px, 230px) 1fr auto;
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
      background: #e9eeed;
      overflow: hidden;
    }
    .fill {
      width: var(--w);
      height: 100%;
      border-radius: 99px;
      background: linear-gradient(90deg, var(--teal), #2e9d8f);
    }
    .fill.blue { background: linear-gradient(90deg, var(--blue), #6d91c3); }
    .fill.amber { background: linear-gradient(90deg, var(--amber), #d69a55); }
    .pill {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      font-weight: 850;
      background: #eef2f1;
      color: var(--muted);
      white-space: nowrap;
    }
    .pill.ok { color: var(--green); background: #e6f4ee; }
    .pill.no { color: var(--red); background: #f8e9e6; }
    .project-list {
      display: grid;
      gap: 10px;
    }
    .project-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: 12px;
      padding: 14px;
      transition: border-color .14s ease, transform .14s ease, box-shadow .14s ease;
    }
    .project-card:hover {
      border-color: rgba(15,118,110,.42);
      transform: translateY(-1px);
      box-shadow: 0 12px 28px rgba(25, 38, 35, .08);
    }
    .project-card.selected {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(15,118,110,.12);
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
      gap: 12px;
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
      grid-template-columns: repeat(3, 1fr);
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
      color: var(--muted);
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
      border: 1px solid var(--line);
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
    section { display: none; }
    section.active { display: block; }
    details.panel summary {
      cursor: pointer;
      list-style: none;
    }
    details.panel summary::-webkit-details-marker { display: none; }
    details.panel summary::after {
      content: "+";
      float: right;
      color: var(--teal);
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
      max-height: 58vh;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: white;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 760px;
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
      background: #f2f5f4;
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
      grid-template-columns: minmax(0, 1fr) 320px;
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
      min-height: 430px;
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
      background: var(--panel-2);
      white-space: pre-wrap;
    }
    .msg.user {
      margin-left: auto;
      background: #e7f2f0;
      border-color: #bfdbd7;
    }
    .msg ul { margin: 8px 0 0; padding-left: 18px; }
    .chat-form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      padding: 12px;
      border-top: 1px solid var(--line);
      background: var(--panel-2);
    }
    .primary {
      border: 0;
      border-radius: 8px;
      padding: 0 16px;
      background: var(--teal);
      color: white;
      font-weight: 850;
    }
    .quick {
      display: grid;
      gap: 8px;
    }
    .quick button {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
      text-align: left;
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
      background: white;
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
        padding: 14px 16px;
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
    @media (max-width: 720px) {
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
        <small>Dashboard interativo de PD&I e Lei do Bem</small>
      </div>
      <nav id="tabs"></nav>
      <div class="side-note">Use os filtros para cruzar projeto, status, atividades, RH e investimentos. As bases ficam recolhidas na aba Auditoria.</div>
    </aside>
    <main>
      <div class="topbar">
        <select id="companySelect" aria-label="Empresa" onchange="setCompany(this.value)"></select>
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
    const fmtNum = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 });
    const state = { company: 0, project: 'all', status: 'all', q: '', department: 'all', tab: 'overview' };
    const chatState = {};
    let searchTimer = 0;
    let DATA = COMPANIES[0] || {};
    window.TABLES = {};

    const tabs = [
      ['overview', 'Resumo'],
      ['projects', 'Projetos'],
      ['activities', 'Atividades'],
      ['finance', 'Valores'],
      ['people', 'Pessoas'],
      ['history', 'Histórico'],
      ['risks', 'Riscos'],
      ['chat', 'Chatbot'],
      ['audit', 'Auditoria']
    ];

    const $ = id => document.getElementById(id);
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
      return ['true', 'verdadeiro', 'sim', 'yes', '1'].includes(norm(cell(row, names)));
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
    function matchSearch(row) {
      return !state.q || norm(Object.values(row || {}).join(' ')).includes(norm(state.q));
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
      }).map(row => {
        const code = codeFrom(cell(row, ['Projeto'])) || codeFrom(cell(row, ['Attach'])) || String(cell(row, ['Projeto']) || '').split(' ')[0];
        const work = cleanRows(DATA.tables?.trabalho || []).filter(r => matchCode(r, code));
        const people = cleanRows(DATA.tables?.pessoal || []).filter(r => matchCode(r, code)).filter(matchDepartment);
        const inv = cleanRows(DATA.tables?.investimentos || []).filter(r => matchCode(r, code));
        const accepted = work.filter(r => boolCell(r, ['Projeto incentivado?']) && boolCell(r, ['Atividade incentivada?']));
        const rejected = work.filter(r => !boolCell(r, ['Projeto incentivado?']) || !boolCell(r, ['Atividade incentivada?']));
        const rh = numCell(row, ['Total Help Desk']) || sum(people, ['Total PD&I', 'Total PDI']);
        const investment = numCell(row, ['Total investido']) || sumInvestments(inv, code);
        const ok = boolCell(row, ['Incentivado?', 'Lei do Bem?', 'Projeto incentivado?']);
        return {
          code,
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
          title: cell(row, ['Projeto']) || code || 'Projeto',
          nature: cell(row, ['Natureza']) || 'Não informada',
          desc: cell(row, ['Descrição']) || ''
        };
      }).filter(p => p.code || p.title);
    }
    function visibleProjects() {
      return allProjects().filter(p => {
        if (state.project !== 'all' && p.code !== state.project) return false;
        if (state.status === 'ok' && !p.ok) return false;
        if (state.status === 'no' && p.ok) return false;
        if (state.q && !norm([p.code, p.title, p.nature, p.desc].join(' ')).includes(norm(state.q))) return false;
        return true;
      });
    }
    function activeProject() {
      const list = visibleProjects();
      return state.project !== 'all' ? list[0] : list.sort((a, b) => b.base - a.base)[0];
    }
    function activeRows(key) {
      let rows = cleanRows(DATA.tables?.[key] || []).filter(row => matchCode(row, state.project)).filter(matchSearch);
      if (key === 'pessoal') rows = rows.filter(matchDepartment);
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
    function chart(title, rows, kind = 'number', tone = '') {
      const clean = (rows || []).filter(r => Number(r.value || 0) > 0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>' + esc(title) + '</h2></div><div class="empty">Sem dados suficientes para exibir.</div></div>';
      const max = Math.max(...clean.map(r => Number(r.value || 0)), 1);
      const body = clean.map(r => {
        const width = Math.max(3, Number(r.value || 0) / max * 100);
        const value = kind === 'money' ? money(r.value) : num(r.value);
        return '<div class="bar"><label title="' + esc(r.name) + '">' + esc(r.name) + '</label><div class="track"><div class="fill ' + tone + '" style="--w:' + width + '%"></div></div><strong>' + value + '</strong></div>';
      }).join('');
      return '<div class="panel"><div class="panel-head"><h2>' + esc(title) + '</h2><span class="hint">' + clean.length + ' itens</span></div><div class="chart">' + body + '</div></div>';
    }
    function quarterRows() {
      return (DATA.metrics?.quarterly || []).filter(q => ['base', 'investment', 'rh', 'exclusion', 'savings', 'commission'].some(k => Number(q[k] || 0)));
    }
    function fiscalSummaryPanel() {
      const m = DATA.metrics || {};
      const base = Number(m.base_total || 0) || Number(m.people_pdi_total || 0) + Number(m.investment_incentivized || 0);
      const exclusion = Number(m.exclusion_total || 0) || base * .6;
      const savings = Number(m.estimated_savings || 0) || exclusion * .34;
      const commission = Number(m.commission || 0);
      const net = savings - commission;
      const rate = base ? savings / base * 100 : 0;
      return '<div class="panel"><div class="panel-head"><h2>Aproveitamento estimado</h2><span class="hint">Base x exclusão x IRPJ/CSLL</span></div><div class="calc-grid">' +
        calcCard('Base PD&I', money(base), 'RH e investimentos elegíveis') +
        calcCard('Exclusão adicional', money(exclusion), 'Parcela dedutível estimada') +
        calcCard('Economia fiscal', money(savings), num(rate) + '% da base PD&I') +
        calcCard('Líquido após comissão', money(net), 'Economia menos comissão') +
      '</div></div>';
    }
    function calcCard(label, value, sub) {
      return '<div class="calc-card"><span>' + esc(label) + '</span><b>' + value + '</b><small>' + esc(sub || '') + '</small></div>';
    }
    function quarterPanel() {
      const rows = quarterRows();
      if (!rows.length) return chart('Aproveitamento por trimestre', [], 'money');
      const totalSavings = rows.reduce((acc, q) => acc + Number(q.savings || 0), 0);
      const list = rows.map(q => '<li><span>' + esc(q.name) + ' · base ' + money(q.base || 0) + '</span><b>' + money(q.savings || 0) + '</b></li>').join('');
      return '<div class="panel"><div class="panel-head"><h2>Aproveitamento por trimestre</h2><span class="hint">Total: ' + money(totalSavings) + '</span></div>' +
        chart('Economia estimada trimestral', rows.map(q => ({ name: q.name, value: q.savings || 0 })), 'money', 'blue').replace('<div class="panel">', '<div>') +
        '<ul class="legend" style="margin-top:12px">' + list + '</ul></div>';
    }
    function simulatorPanel() {
      const base = Number(DATA.metrics?.base_total || 0) || Number(DATA.metrics?.people_pdi_total || 0) + Number(DATA.metrics?.investment_incentivized || 0);
      return '<div class="panel"><div class="panel-head"><h2>Simulador rápido</h2><span class="hint">Ajuste as premissas</span></div><div class="sim-grid">' +
        '<label class="hint">Percentual de exclusão<input id="simExclusion" type="number" min="0" max="100" step="1" value="60" oninput="updateSimulator()"></label>' +
        '<label class="hint">Alíquota IRPJ/CSLL<input id="simTax" type="number" min="0" max="100" step="1" value="34" oninput="updateSimulator()"></label>' +
        '</div><div id="simResult" class="sim-result" data-base="' + base + '"></div></div>';
    }
    function updateSimulator() {
      const target = $('simResult');
      if (!target) return;
      const base = Number(target.dataset.base || 0);
      const exclusionRate = Number($('simExclusion')?.value || 0) / 100;
      const taxRate = Number($('simTax')?.value || 0) / 100;
      const exclusion = base * exclusionRate;
      const savings = exclusion * taxRate;
      target.innerHTML = 'Com essas premissas: exclusão de ' + money(exclusion) + ' e economia de ' + money(savings) + '.';
    }
    function tablePanel(title, rows, columns, open = false) {
      const id = norm(title).replace(/[^a-z0-9]+/g, '-');
      const filtered = cleanRows(rows).filter(matchSearch);
      window.TABLES[id] = { rows: filtered, columns };
      setTimeout(() => drawTable(id), 0);
      return '<details class="panel" ' + (open ? 'open' : '') + '><summary>' + esc(title) + ' <span class="hint">' + num(filtered.length) + ' linhas</span></summary><div class="table-tools"><input placeholder="Filtrar tabela" oninput="drawTable(\\'' + id + '\\', this.value)"><span class="hint">HTML otimizado: bases completas ficam nos CSVs exportados.</span></div><div class="table-wrap" id="table-' + id + '"></div></details>';
    }
    function drawTable(id, filter = '') {
      const target = $('table-' + id);
      const cfg = window.TABLES[id] || {};
      const rows = cfg.rows || [];
      if (!target) return;
      if (!rows.length) {
        target.innerHTML = '<div class="empty">Sem linhas para exibir.</div>';
        return;
      }
      const q = norm(filter);
      const filtered = q ? rows.filter(row => norm(JSON.stringify(row)).includes(q)) : rows;
      const cols = (cfg.columns?.length ? cfg.columns : Object.keys(filtered[0] || rows[0])).filter(c => filtered.some(row => String(row[c] || '').trim())).slice(0, 12);
      const body = filtered.slice(0, 500).map(row => '<tr>' + cols.map(c => '<td>' + esc(row[c] ?? '') + '</td>').join('') + '</tr>').join('');
      target.innerHTML = '<table><thead><tr>' + cols.map(c => '<th>' + esc(c) + '</th>').join('') + '</tr></thead><tbody>' + body + '</tbody></table>';
    }
    function hero() {
      const m = DATA.metrics || {};
      const base = Number(m.base_total || 0) || Number(m.people_pdi_total || 0) + Number(m.investment_incentivized || 0);
      const economy = Number(m.estimated_savings || 0) || base * .6 * .34;
      const selected = activeProject();
      return '<div class="hero"><div class="hero-main"><div><div class="eyebrow">' + esc(DATA.year || '') + ' · ' + esc(DATA.company || '') + '</div><div class="hero-title">' + money(base) + '</div><div class="source">Base de PD&I conciliada com o resumo. Fonte: ' + esc(DATA.source || '') + '</div></div><div class="metric-strip">' +
        kpi('Economia estimada', money(economy), 'Benefício calculado') +
        kpi('RH PD&I', money(m.people_pdi_total), 'Equipe técnica') +
        kpi('Investimentos', money(m.investment_incentivized), 'Materiais, serviços e terceiros') +
        kpi('Horas elegíveis', num(m.eligible_hours), 'Atividades aceitas') +
      '</div></div><div class="panel"><div class="panel-head"><h2>Composição da base</h2><span class="hint">RH x investimentos</span></div>' +
        composition([{ label: 'RH PD&I', value: m.people_pdi_total || 0, color: 'var(--teal)' }, { label: 'Investimentos', value: m.investment_incentivized || 0, color: 'var(--amber)' }, { label: 'Outros ajustes', value: Math.max(base - Number(m.people_pdi_total || 0) - Number(m.investment_incentivized || 0), 0), color: 'var(--blue)' }]) +
        '<ul class="legend" style="margin-top:14px"><li><span>Projeto em foco</span><b>' + esc(selected?.code || 'Todos') + '</b></li><li><span>Projetos incentivados</span><b>' + num(m.projects_incentivized || 0) + ' / ' + num(m.projects_total || 0) + '</b></li></ul></div></div>';
    }
    function overview() {
      const m = DATA.metrics || {};
      return '<section id="overview">' + hero() + fiscalSummaryPanel() + '<div class="grid-2"><div>' +
        quarterPanel() +
        chart('Projetos por base identificada', m.top_projects || [], 'money') +
        chart('Atividades elegíveis por horas', m.hours_by_activity || [], 'number', 'blue') +
      '</div><div>' +
        simulatorPanel() +
        chart('Investimentos por natureza', m.investment_by_nature || [], 'money', 'amber') +
        '<div class="panel"><div class="panel-head"><h2>Leitura executiva</h2></div><ul class="legend"><li><span>Exclusão da base</span><b>' + money(m.exclusion_total || 0) + '</b></li><li><span>Comissão</span><b>' + money(m.commission || 0) + '</b></li><li><span>Abas processadas</span><b>' + num(Object.keys(DATA.sheets || {}).length) + '</b></li></ul></div>' +
      '</div></div></section>';
    }
    function projectCard(p) {
      const selected = state.project === p.code || (state.project === 'all' && activeProject()?.code === p.code);
      return '<div class="project-card ' + (selected ? 'selected' : '') + '"><button type="button" onclick="setProject(\\'' + esc(p.code) + '\\')"><div class="project-top"><div><strong>' + esc(short(p.title, 88)) + '</strong><span class="hint">' + esc(p.code || p.nature) + '</span></div><span class="pill ' + (p.ok ? 'ok' : 'no') + '">' + (p.ok ? 'Incentivado' : 'Fora') + '</span></div><div class="project-desc">' + esc(p.desc || p.nature) + '</div><div class="mini-grid"><div class="mini"><span>Base</span><b>' + money(p.base) + '</b></div><div class="mini"><span>Horas</span><b>' + num(p.hours) + '</b></div><div class="mini"><span>Natureza</span><b>' + esc(short(p.nature, 18)) + '</b></div></div></button></div>';
    }
    function projectDetail(p) {
      if (!p) return '<div class="panel"><h2>Projeto em foco</h2><div class="empty">Nenhum projeto encontrado para os filtros atuais.</div></div>';
      const accepted = group(p.accepted, ['Atividade realizada', 'Atividade'], ['Horas decimais', 'Horas'], 6);
      return '<div class="panel"><div class="panel-head"><h2>' + esc(short(p.title, 110)) + '</h2><span class="pill ' + (p.ok ? 'ok' : 'no') + '">' + (p.ok ? 'Incentivado' : 'Não incentivado') + '</span></div><div class="mini-grid"><div class="mini"><span>Base</span><b>' + money(p.base) + '</b></div><div class="mini"><span>RH</span><b>' + money(p.rh) + '</b></div><div class="mini"><span>Invest.</span><b>' + money(p.investment) + '</b></div></div><div class="text-panels" style="margin-top:12px"><article><h3>Descrição</h3><p>' + esc(cell(p.row, ['Descrição']) || 'Sem descrição informada.') + '</p></article><article><h3>Elemento inovador</h3><p>' + esc(cell(p.row, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']) || 'Sem texto informado.') + '</p></article><article><h3>Barreira tecnológica</h3><p>' + esc(cell(p.row, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']) || 'Sem texto informado.') + '</p></article></div></div>' + chart('Atividades aceitas no projeto', accepted, 'number');
    }
    function projects() {
      const list = visibleProjects().sort((a, b) => b.base - a.base);
      const rows = list.map(p => ({ Projeto: p.title, Código: p.code, Status: p.ok ? 'Incentivado' : 'Não incentivado', Natureza: p.nature, Base: money(p.base), RH: money(p.rh), Investimentos: money(p.investment), Horas: num(p.hours) }));
      return '<section id="projects">' + hero() + '<div class="grid-2"><div><div class="panel"><div class="panel-head"><h2>Carteira de projetos</h2><span class="hint">Clique em um card para focar a análise</span></div><div class="project-list">' + (list.map(projectCard).join('') || '<div class="empty">Nenhum projeto encontrado.</div>') + '</div></div>' + tablePanel('Resumo dos projetos', rows, ['Projeto', 'Código', 'Status', 'Natureza', 'Base', 'RH', 'Investimentos', 'Horas']) + '</div><div>' + projectDetail(activeProject()) + '</div></div></section>';
    }
    function activities() {
      const rows = activeRows('trabalho');
      const accepted = rows.filter(r => boolCell(r, ['Projeto incentivado?']) && boolCell(r, ['Atividade incentivada?']));
      const rejected = rows.filter(r => !boolCell(r, ['Projeto incentivado?']) || !boolCell(r, ['Atividade incentivada?']));
      return '<section id="activities">' + hero() + '<div class="grid-3">' + kpi('Horas aceitas', num(sum(accepted, ['Horas decimais', 'Horas'])), 'Elegíveis') + kpi('Horas fora do filtro', num(sum(rejected, ['Horas decimais', 'Horas'])), 'Revisão') + kpi('Linhas no HTML', num(rows.length), 'Amostra otimizada') + '</div><div class="grid-2" style="margin-top:16px"><div>' + chart('Atividades aceitas', group(accepted, ['Atividade realizada', 'Atividade'], ['Horas decimais', 'Horas']), 'number') + chart('Atividades fora do filtro', group(rejected, ['Atividade realizada', 'Atividade'], ['Horas decimais', 'Horas'], 8), 'number', 'amber') + '</div><div>' + tablePanel('Descrições aceitas', accepted, ['Projeto', 'Funcionário', 'Atividade realizada', 'Descrição da atividade', 'Horas decimais'], true) + '</div></div>' + tablePanel('Amostra do timesheet', rows, ['Projeto', 'Funcionário', 'Mês', 'Etapa', 'Atividade realizada', 'Descrição da atividade', 'Horas', 'Horas decimais', 'Projeto incentivado?', 'Atividade incentivada?']) + '</section>';
    }
    function finance() {
      const inv = activeRows('investimentos');
      const totalInv = sumInvestments(inv, state.project);
      const people = activeRows('pessoal');
      const totalRh = sum(people, ['Total PD&I', 'Total PDI']);
      return '<section id="finance">' + hero() + '<div class="grid-3">' + kpi('Investimentos filtrados', money(totalInv), 'Após filtros') + kpi('RH filtrado', money(totalRh), 'Após filtros') + kpi('Fornecedores', num(groupInvestments(inv, ['Fornecedor'], state.project, 500).length), 'Com lançamentos') + '</div><div class="grid-2" style="margin-top:16px"><div>' + chart('Investimentos por fornecedor', groupInvestments(inv, ['Fornecedor'], state.project, 12), 'money') + chart('Investimentos por natureza', groupInvestments(inv, ['Natureza'], state.project, 12), 'money', 'amber') + '</div><div><div class="panel"><div class="panel-head"><h2>Composição filtrada</h2></div>' + composition([{ label: 'RH filtrado', value: totalRh, color: 'var(--teal)' }, { label: 'Investimentos filtrados', value: totalInv, color: 'var(--amber)' }]) + '</div>' + chart('RH por colaborador', group(people, ['Funcionário', 'Funcionario'], ['Total PD&I', 'Total PDI'], 8), 'money', 'blue') + '</div></div>' + tablePanel('Investimentos detalhados', inv, ['Fornecedor', 'CNPJ', 'Descrição', 'NF/ND', 'Valor', 'Valor Incentivado', 'Data', 'Natureza', 'Objetivo do gasto', 'Projeto e eventual info de rateio', 'Inovação?']) + '</section>';
    }
    function people() {
      const rows = activeRows('pessoal');
      return '<section id="people">' + hero() + '<div class="grid-2"><div>' + chart('RH por colaborador', group(rows, ['Funcionário', 'Funcionario'], ['Total PD&I', 'Total PDI'], 15), 'money') + '</div><div>' + chart('RH por projeto', group(rows, ['Projeto'], ['Total PD&I', 'Total PDI'], 12), 'money', 'blue') + '</div></div>' + tablePanel('Base de RH filtrada', rows, ['Projeto', 'Funcionário', 'Departamento', 'Setor', 'Area', 'Cargo', 'Formação', 'Horas efetivas (PD&I)', 'Custo hora (PD&I)', 'Total PD&I', 'Dedicação']) + '</section>';
    }
    function historyRows() {
      return (DATA.history?.years || []).slice().sort((a, b) => Number(a.year || 0) - Number(b.year || 0));
    }
    function history() {
      const rows = historyRows();
      if (!rows.length) {
        return '<section id="history">' + hero() + '<div class="panel"><div class="panel-head"><h2>Histórico</h2></div><div class="empty">Ainda não há histórico extraído para esta empresa.</div></div></section>';
      }
      const totalBase = rows.reduce((acc, row) => acc + Number(row.base_total || 0), 0);
      const totalSavings = rows.reduce((acc, row) => acc + Number(row.estimated_savings || 0), 0);
      const top = rows.slice().sort((a, b) => Number(b.base_total || 0) - Number(a.base_total || 0))[0] || {};
      const cards = rows.map(row => '<article class="history-year"><h3>' + esc(row.year) + '</h3>' +
        '<ul class="legend">' +
        '<li><span>Base total</span><b>' + money(row.base_total || 0) + '</b></li>' +
        '<li><span>RH</span><b>' + money(row.rh_total || 0) + '</b></li>' +
        '<li><span>Material</span><b>' + money(row.material_total || 0) + '</b></li>' +
        '<li><span>Terceiros</span><b>' + money(row.third_party_total || 0) + '</b></li>' +
        '<li><span>Economia</span><b>' + (row.estimated_savings == null ? '—' : money(row.estimated_savings)) + '</b></li>' +
        '</ul></article>').join('');
      const tableRows = rows.map(row => ({
        Ano: row.year,
        Base: money(row.base_total || 0),
        RH: money(row.rh_total || 0),
        Material: money(row.material_total || 0),
        Terceiros: money(row.third_party_total || 0),
        Economia: row.estimated_savings == null ? '' : money(row.estimated_savings),
        Horas_parcial: row.eligible_hours_partial || '',
        Horas_exclusiva: row.eligible_hours_exclusive || '',
        Colab_parcial: row.collaborators_partial || '',
        Colab_exclusivo: row.collaborators_exclusive || ''
      }));
      const evidence = (DATA.history?.evidence || []).map(item => ({
        Fonte: item.source,
        Tipo: item.kind,
        Extracao: item.extracted_from,
        Confianca: item.confidence,
        Observacoes: item.notes
      }));
      const historyProjects = (DATA.history?.projects || []).map(item => ({
        Ano: item.year || '',
        Projeto: item.name || '',
        Status: item.status || '',
        Resumo: item.summary || '',
        Atividades: (item.activities || []).join('; '),
        Fonte: (item.source_refs || []).join('; ')
      }));
      return '<section id="history">' + hero() +
        '<div class="grid-3">' +
        kpi('Base histórica', money(totalBase), rows[0].year + ' a ' + rows[rows.length - 1].year) +
        kpi('Economia informada', money(totalSavings), 'Soma dos anos com benefício') +
        kpi('Maior ano', esc(top.year || '—'), money(top.base_total || 0)) +
        '</div><div class="grid-2" style="margin-top:16px"><div>' +
        chart('Evolução da base histórica', rows.map(row => ({ name: String(row.year), value: row.base_total || 0 })), 'money') +
        chart('Economia estimada histórica', rows.map(row => ({ name: String(row.year), value: row.estimated_savings || 0 })), 'money', 'blue') +
        '</div><div><div class="panel"><div class="panel-head"><h2>Composição acumulada</h2></div>' +
        composition([{ label: 'RH', value: rows.reduce((a, r) => a + Number(r.rh_total || 0), 0), color: 'var(--teal)' }, { label: 'Material', value: rows.reduce((a, r) => a + Number(r.material_total || 0), 0), color: 'var(--amber)' }, { label: 'Terceiros', value: rows.reduce((a, r) => a + Number(r.third_party_total || 0), 0), color: 'var(--blue)' }]) +
        '</div></div></div><div class="history-grid">' + cards + '</div>' +
        tablePanel('Histórico anual normalizado', tableRows, ['Ano', 'Base', 'RH', 'Material', 'Terceiros', 'Economia', 'Horas_parcial', 'Horas_exclusiva', 'Colab_parcial', 'Colab_exclusivo'], true) +
        tablePanel('Projetos e narrativas históricas', historyProjects, ['Ano', 'Projeto', 'Status', 'Resumo', 'Atividades', 'Fonte'], true) +
        tablePanel('Evidências do histórico', evidence, ['Fonte', 'Tipo', 'Extracao', 'Confianca', 'Observacoes']) +
        '</section>';
    }
    function fiscalAnswer() {
      const m = DATA.metrics || {};
      const base = Number(m.base_total || 0) || Number(m.people_pdi_total || 0) + Number(m.investment_incentivized || 0);
      const exclusion = Number(m.exclusion_total || 0) || base * .6;
      const savings = Number(m.estimated_savings || 0) || exclusion * .34;
      const commission = Number(m.commission || 0);
      return '<strong>Aproveitamento estimado de ' + esc(DATA.company) + '</strong><ul><li>Base PD&I conciliada: ' + money(base) + '</li><li>Exclusão adicional estimada: ' + money(exclusion) + '</li><li>Economia fiscal estimada: ' + money(savings) + '</li><li>Comissão: ' + money(commission) + '</li><li>Líquido após comissão: ' + money(savings - commission) + '</li></ul>';
    }
    function quarterAnswer() {
      const rows = quarterRows();
      if (!rows.length) return 'Não encontrei abertura trimestral suficiente na aba RESUMO desta empresa.';
      return '<strong>Aproveitamento por trimestre</strong><ul>' + rows.map(q => '<li>' + esc(q.name) + ': base ' + money(q.base || 0) + ', exclusão ' + money(q.exclusion || 0) + ', economia ' + money(q.savings || 0) + '</li>').join('') + '</ul>';
    }
    function activitiesAnswer() {
      const p = activeProject();
      const rows = p?.accepted?.length ? group(p.accepted, ['Atividade realizada', 'Atividade'], ['Horas decimais', 'Horas'], 8) : (DATA.metrics?.hours_by_activity || []);
      if (!rows.length) return 'Não encontrei atividades aceitas suficientes para listar com os filtros atuais.';
      return '<strong>Atividades aceitas' + (p?.code ? ' no projeto ' + esc(p.code) : '') + '</strong><ul>' + rows.slice(0, 8).map(r => '<li>' + esc(short(r.name, 110)) + ': ' + num(r.value) + ' h</li>').join('') + '</ul>';
    }
    function investmentAnswer() {
      const inv = activeRows('investimentos');
      const bySupplier = groupInvestments(inv, ['Fornecedor'], state.project, 6);
      const byNature = groupInvestments(inv, ['Natureza'], state.project, 6);
      const total = sumInvestments(inv, state.project);
      return '<strong>Investimentos filtrados</strong><ul><li>Total: ' + money(total) + '</li><li>Principais fornecedores: ' + (bySupplier.map(r => esc(short(r.name, 42)) + ' (' + money(r.value) + ')').join('; ') || 'sem dados') + '</li><li>Naturezas: ' + (byNature.map(r => esc(short(r.name, 42)) + ' (' + money(r.value) + ')').join('; ') || 'sem dados') + '</li></ul>';
    }
    function peopleAnswer() {
      const peopleRows = activeRows('pessoal');
      const total = sum(peopleRows, ['Total PD&I', 'Total PDI']);
      const top = group(peopleRows, ['Funcionário', 'Funcionario'], ['Total PD&I', 'Total PDI'], 6);
      return '<strong>RH PD&I filtrado</strong><ul><li>Total: ' + money(total) + '</li><li>Colaboradores principais: ' + (top.map(r => esc(short(r.name, 42)) + ' (' + money(r.value) + ')').join('; ') || 'sem dados') + '</li></ul>';
    }
    function projectAnswer(p) {
      if (!p) return 'Selecione um projeto no filtro superior ou pergunte por um código INOV/NRD específico.';
      const element = cell(p.row, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']) || 'Não informado.';
      const barrier = cell(p.row, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']) || 'Não informado.';
      const decision = eligibilityDecision(p);
      return '<strong>' + esc(p.title) + '</strong><ul><li>Status técnico: ' + esc(decision.status) + '</li><li>Base: ' + money(p.base) + ' | RH: ' + money(p.rh) + ' | Investimentos: ' + money(p.investment) + '</li><li>Horas aceitas: ' + num(p.hours) + '</li><li>Por quê: ' + esc(decision.reason) + '</li><li>Elemento inovador: ' + esc(short(element, 240)) + '</li><li>Barreira tecnológica: ' + esc(short(barrier, 240)) + '</li></ul>';
    }
    function projectHistoryMatches(p) {
      if (!p) return [];
      const code = codeKey(p.code || p.title);
      const title = norm(p.title);
      return (DATA.history?.projects || []).filter(item => {
        const text = [item.name, item.summary, item.status, ...(item.activities || [])].join(' ');
        return (code && codeKey(text) === code) || (title && norm(text).includes(title.slice(0, 28)));
      });
    }
    function maturityProfile(p) {
      const history = projectHistoryMatches(p);
      let score = 0;
      if (p?.desc) score += 12;
      if (cell(p?.row || {}, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador'])) score += 18;
      if (cell(p?.row || {}, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico'])) score += 18;
      if (p?.accepted?.length) score += 18;
      if (Number(p?.hours || 0) > 40) score += 12;
      if (Number(p?.investment || 0) > 0) score += 10;
      if (history.length) score += 12;
      score = Math.min(score, 100);
      const stage = score >= 82 ? 'Maturidade alta' : score >= 62 ? 'Validação avançada' : score >= 42 ? 'Desenvolvimento técnico' : score >= 22 ? 'Estruturação inicial' : 'Evidência insuficiente';
      const next = score >= 82 ? 'Manter trilha de evidências, impactos e memória técnica por ano.' : score >= 62 ? 'Amarrar resultados, testes, gastos e decisões técnicas ao ganho inovador.' : score >= 42 ? 'Reforçar barreira tecnológica, critérios de aceite e documentação de execução.' : 'Consolidar objetivo técnico, incertezas, atividades e vínculo financeiro.';
      return { score, stage, next, history };
    }
    function riskRowsForProject(p) {
      const explicit = cleanRows(DATA.tables?.riscos || []).filter(row => !p?.code || matchCode(row, p.code));
      const profile = maturityProfile(p);
      const rows = explicit.map(row => ({
        Risco: cell(row, ['Risco', 'Descrição', 'Descricao']) || 'Risco informado',
        Categoria: cell(row, ['Categoria', 'Tipo']) || 'Base de riscos',
        Impacto: cell(row, ['Impacto', 'Valor']) || '',
        Probabilidade: cell(row, ['Probabilidade']) || '',
        Mitigação: cell(row, ['Mitigação', 'Mitigacao']) || ''
      }));
      if (!p) return rows;
      if (!p.ok) rows.push({ Risco: 'Projeto não marcado como incentivado na base atual', Categoria: 'Elegibilidade', Impacto: 'Alto', Probabilidade: 'Média', Mitigação: 'Revisar critérios técnicos, justificativas e atividades elegíveis.' });
      if (!cell(p.row, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador'])) rows.push({ Risco: 'Elemento inovador não descrito', Categoria: 'Documental', Impacto: 'Alto', Probabilidade: 'Média', Mitigação: 'Registrar novidade, melhoria técnica ou avanço frente ao estado anterior.' });
      if (!cell(p.row, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico'])) rows.push({ Risco: 'Barreira tecnológica pouco evidente', Categoria: 'Lei do Bem', Impacto: 'Alto', Probabilidade: 'Média', Mitigação: 'Evidenciar incerteza tecnológica, hipóteses, testes e aprendizado.' });
      if (p.rejected?.length) rows.push({ Risco: 'Atividades fora do incentivo no timesheet', Categoria: 'Elegibilidade', Impacto: 'Médio', Probabilidade: 'Alta', Mitigação: 'Separar atividades administrativas das atividades técnicas de PD&I.' });
      if (!Number(p.investment || 0) && !Number(p.rh || 0)) rows.push({ Risco: 'Projeto sem base financeira filtrada', Categoria: 'Conciliação', Impacto: 'Médio', Probabilidade: 'Média', Mitigação: 'Verificar vínculo entre RH, investimentos, projeto e resumo fiscal.' });
      if (profile.score < 42) rows.push({ Risco: 'Baixa maturidade documental', Categoria: 'Maturidade', Impacto: 'Médio', Probabilidade: 'Média', Mitigação: profile.next });
      return rows;
    }
    function eligibilityCriteriaRows(p) {
      if (!p) return [];
      const element = cell(p.row, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']);
      const barrier = cell(p.row, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']);
      const description = cell(p.row, ['Descrição', 'Descricao']);
      const acceptedHours = Number(p.hours || 0);
      const technicalActivities = countBy(p.accepted || [], ['Atividade realizada', 'Atividade'], 5);
      const rejectedHours = sum(p.rejected || [], ['Horas decimais', 'Horas']);
      const hasFinancialBase = Number(p.rh || 0) > 0 || Number(p.investment || 0) > 0;
      const history = projectHistoryMatches(p);
      return [
        {
          Critério: 'Enquadramento na base',
          Status: p.ok ? 'Atendido' : 'Não atendido',
          Evidência: p.ok ? 'Projeto marcado como incentivado na planilha de projetos.' : 'Projeto não está marcado como incentivado na base atual.',
          Leitura: p.ok ? 'O dado estrutural permite compor a análise de Lei do Bem.' : 'Sem marcação de incentivo, o tratamento técnico deve ser de revisão ou exclusão.'
        },
        {
          Critério: 'Elemento inovador',
          Status: element ? 'Atendido' : 'Pendente',
          Evidência: element ? short(element, 220) : 'Campo não localizado ou vazio.',
          Leitura: element ? 'Há narrativa de novidade, melhoria técnica ou avanço de produto/processo.' : 'Falta amarrar qual avanço diferencia o projeto de rotina operacional.'
        },
        {
          Critério: 'Barreira ou incerteza tecnológica',
          Status: barrier ? 'Atendido' : 'Pendente',
          Evidência: barrier ? short(barrier, 220) : 'Campo não localizado ou vazio.',
          Leitura: barrier ? 'A base descreve desafio técnico a superar, ponto central para Lei do Bem.' : 'Sem incerteza técnica, o risco de glosa aumenta.'
        },
        {
          Critério: 'Atividades técnicas executadas',
          Status: acceptedHours > 0 ? 'Atendido' : 'Pendente',
          Evidência: acceptedHours > 0 ? num(acceptedHours) + ' horas aceitas; principais atividades: ' + technicalActivities.map(r => short(r.name, 48)).join('; ') : 'Não há horas aceitas filtradas.',
          Leitura: acceptedHours > 0 ? 'Há execução técnica registrada e mensurável.' : 'Sem execução técnica elegível, o projeto não sustenta base operacional.'
        },
        {
          Critério: 'Segregação de atividades não elegíveis',
          Status: rejectedHours > 0 ? 'Revisar' : 'Atendido',
          Evidência: rejectedHours > 0 ? num(rejectedHours) + ' horas fora do incentivo no filtro.' : 'Não foram identificadas horas rejeitadas no recorte.',
          Leitura: rejectedHours > 0 ? 'Separar rotina, gestão, comercial ou documentação administrativa das atividades de PD&I.' : 'O recorte atual não indica mistura relevante de atividade não elegível.'
        },
        {
          Critério: 'Vínculo financeiro',
          Status: hasFinancialBase ? 'Atendido' : 'Pendente',
          Evidência: 'RH ' + money(p.rh || 0) + '; investimentos ' + money(p.investment || 0) + '.',
          Leitura: hasFinancialBase ? 'Há valor vinculado ao projeto para composição da base.' : 'É preciso reconciliar RH/investimentos ao projeto antes de defender valor.'
        },
        {
          Critério: 'Memória histórica',
          Status: history.length ? 'Atendido' : 'Não localizado',
          Evidência: history.length ? history.length + ' narrativa(s) histórica(s) conectada(s).' : 'Sem vínculo histórico direto encontrado.',
          Leitura: history.length ? 'Ajuda a demonstrar evolução, continuidade e maturidade do projeto.' : 'A defesa fica mais dependente da base do ano corrente.'
        },
        {
          Critério: 'Descrição técnica mínima',
          Status: description ? 'Atendido' : 'Pendente',
          Evidência: description ? short(description, 220) : 'Descrição não localizada ou vazia.',
          Leitura: description ? 'A descrição ajuda a delimitar escopo e objetivo técnico.' : 'Sem descrição, a análise perde rastreabilidade.'
        }
      ];
    }
    function eligibilityDecision(p) {
      if (!p) return { status: 'Sem projeto selecionado', reason: 'Selecione uma empresa e um projeto para o agente ler a base.' };
      const rows = eligibilityCriteriaRows(p);
      const critical = ['Enquadramento na base', 'Elemento inovador', 'Barreira ou incerteza tecnológica', 'Atividades técnicas executadas', 'Vínculo financeiro'];
      const metCritical = rows.filter(row => critical.includes(row.Critério) && row.Status === 'Atendido').length;
      const pending = rows.filter(row => ['Pendente', 'Não atendido'].includes(row.Status)).length;
      if (p.ok && metCritical >= 4) return { status: 'Incentivado com boa sustentação', reason: 'A base marca o projeto como incentivado e contém evidências técnicas, atividades aceitas e valores vinculados suficientes para sustentar o enquadramento.' };
      if (p.ok) return { status: 'Incentivado com ressalvas', reason: 'A base marca o projeto como incentivado, mas faltam evidências críticas ou conciliações para uma defesa técnica robusta.' };
      if (!p.ok && metCritical >= 4) return { status: 'Revisar potencial de incentivo', reason: 'Apesar de não estar marcado como incentivado, há sinais técnicos e financeiros que justificam reavaliação do enquadramento.' };
      return { status: 'Não incentivado pela leitura atual', reason: 'A base não marca o projeto como incentivado e há pendências técnicas/documentais relevantes nos critérios centrais.' + (pending ? ' Pendências: ' + pending + '.' : '') };
    }
    function riskAnswer() {
      const p = activeProject();
      const profile = maturityProfile(p);
      const risks = riskRowsForProject(p).slice(0, 6);
      const decision = eligibilityDecision(p);
      return '<strong>Agente Benner: riscos, maturidade e incentivo' + (p?.code ? ' do projeto ' + esc(p.code) : '') + '</strong><ul><li>Decisão técnica: ' + esc(decision.status) + '</li><li>Fundamento: ' + esc(decision.reason) + '</li><li>Nível de maturidade: ' + esc(profile.stage) + ' (' + num(profile.score) + '/100)</li><li>Próximo passo: ' + esc(profile.next) + '</li><li>Principais riscos: ' + (risks.map(r => esc(r.Categoria + ': ' + r.Risco)).join('; ') || 'sem riscos mapeados na base filtrada') + '</li></ul>';
    }
    function sectorRows() {
      const rows = COMPANIES.map(company => {
        const m = company.metrics || {};
        const base = Number(m.base_total || 0) || Number(m.people_pdi_total || 0) + Number(m.investment_incentivized || 0);
        const projects = Number(m.projects_total || 0);
        const incentivized = Number(m.projects_incentivized || 0);
        return {
          Empresa: company.company || '',
          Base: money(base),
          Projetos: num(projects),
          Incentivados: num(incentivized),
          '% incentivado': projects ? num(incentivized / projects * 100) + '%' : '',
          'Economia estimada': money(m.estimated_savings || 0)
        };
      });
      return rows.sort((a, b) => numCell({'a': b.Base}, ['a']) - numCell({'a': a.Base}, ['a']));
    }
    function sectorAnswer() {
      const rows = sectorRows();
      return '<strong>Comparativo disponível</strong><ul><li>Este HTML compara internamente as empresas carregadas no portfólio.</li><li>Para benchmark externo do setor, é preciso conectar pesquisa web/API com fontes públicas e data de consulta.</li><li>Empresas na base: ' + rows.map(r => esc(r.Empresa)).join('; ') + '</li></ul>';
    }
    function answer(question) {
      const q = norm(question);
      const code = codeFrom(question);
      if (code) {
        const p = allProjects().find(x => x.code === code);
        if (!p) return 'Não encontrei o projeto <strong>' + esc(code) + '</strong> nesta empresa.';
        return projectAnswer(p);
      }
      if (q.includes('trimestre') || q.includes('trimestral') || q.includes('1 tri') || q.includes('2 tri') || q.includes('3 tri') || q.includes('4 tri')) return quarterAnswer();
      if (q.includes('aproveit') || q.includes('beneficio') || q.includes('economia') || q.includes('exclusao') || q.includes('comissao') || q.includes('liquido') || q.includes('valor')) return fiscalAnswer();
      if (q.includes('por que') || q.includes('porque') || q.includes('incentivado') || q.includes('projeto selecionado')) return projectAnswer(activeProject());
      if (q.includes('atividade') || q.includes('aceita') || q.includes('recusada') || q.includes('descricao')) return activitiesAnswer();
      if (q.includes('invest') || q.includes('fornecedor') || q.includes('material') || q.includes('servico') || q.includes('terceiro')) return investmentAnswer();
      if (q.includes('rh') || q.includes('colaborador') || q.includes('pessoa') || q.includes('funcionario')) return peopleAnswer();
      if (q.includes('risco') || q.includes('maturidade') || q.includes('avanco') || q.includes('evolucao')) return riskAnswer();
      if (q.includes('compar') || q.includes('benchmark') || q.includes('setor') || q.includes('mercado')) return sectorAnswer();
      if (q.includes('lei do bem') || q.includes('criterio') || q.includes('elegivel')) return '<strong>Lei do Bem:</strong> em termos práticos, o projeto precisa demonstrar incerteza tecnológica, método técnico, tentativa de superação de desafio e evidências. Neste painel, o enquadramento usa projeto incentivado, atividade incentivada, descritivos aceitos e conciliação financeira da aba RESUMO.';
      return 'Posso responder sobre aproveitamento fiscal, trimestres, projetos INOV/NRD, motivo do enquadramento, atividades aceitas, RH e investimentos.';
    }
    function chat() {
      return '<section id="chat">' + hero() + '<div class="chat-layout"><div class="chat-box"><div class="messages" id="messages"></div><form class="chat-form" onsubmit="askChat(event)"><input id="chatInput" placeholder="Pergunte sobre aproveitamento, riscos, maturidade, projeto, atividades ou Lei do Bem"><button class="primary" type="submit">Enviar</button></form></div><div class="panel"><div class="panel-head"><h2>Perguntas rápidas</h2></div><div class="quick"><button onclick="quick(\\'Quanto será aproveitado e qual o líquido após comissão?\\')">Aproveitamento estimado</button><button onclick="quick(\\'Qual o aproveitamento por trimestre?\\')">Por trimestre</button><button onclick="quick(\\'Por que o projeto selecionado é incentivado?\\')">Projeto selecionado</button><button onclick="quick(\\'Quais riscos e maturidade do projeto selecionado?\\')">Riscos e maturidade</button><button onclick="quick(\\'Quais atividades foram aceitas?\\')">Atividades aceitas</button><button onclick="quick(\\'Compare a empresa com a base interna e o setor\\')">Comparativo</button><button onclick="quick(\\'Explique a Lei do Bem e os critérios\\')">Critérios da Lei do Bem</button></div></div></div></section>';
    }
    function renderChat() {
      const box = $('messages');
      if (!box) return;
      const key = DATA.company || 'empresa'; // Key for chat history
      if (!chatState[key]) chatState[key] = [{ role: 'bot', text: 'Olá! Eu sou o Gemini, seu assistente de PD&I. Estou lendo os dados de ' + DATA.company + '. Pergunte sobre Lei do Bem, valores, projetos, riscos, maturidade, RH ou investimentos.' }];
      box.innerHTML = chatState[key].map(m => '<div class="msg ' + m.role + '">' + m.text + '</div>').join('');
      box.scrollTop = box.scrollHeight;
    }
    function askChat(ev) {
      ev?.preventDefault();
      const input = $('chatInput');
      const question = (input?.value || '').trim();
      if (!question) return;
      const key = DATA.company || 'empresa';
      chatState[key] = chatState[key] || [];
      chatState[key].push({ role: 'user', text: esc(question) });
      chatState[key].push({ role: 'bot', text: answer(question) });
      input.value = '';
      renderChat();
    }
    function quick(question) {
      if (question.includes('selecionado')) {
        const p = activeProject();
        question = p?.code ? 'Fale do projeto ' + p.code : 'Fale do projeto selecionado';
      }
      $('chatInput').value = question;
      askChat();
    }
    function riskAgentAnswer(question) {
      const q = norm(question || '');
      const p = activeProject();
      if (!p) return 'Selecione um projeto para o agente ler a base técnica.';
      if (!q || q.includes('resumo') || q.includes('diagnostico') || q.includes('diagnóstico')) return riskAnswer();
      if (q.includes('criterio') || q.includes('critério') || q.includes('incentivado') || q.includes('glosa')) {
        const rows = eligibilityCriteriaRows(p);
        return '<strong>Matriz técnica de enquadramento</strong><ul>' + rows.map(row => '<li><b>' + esc(row.Critério) + ':</b> ' + esc(row.Status) + ' — ' + esc(short(row.Leitura, 180)) + '</li>').join('') + '</ul>';
      }
      if (q.includes('valor') || q.includes('base') || q.includes('rh') || q.includes('invest')) return investmentAnswer() + peopleAnswer();
      if (q.includes('atividade') || q.includes('inovador') || q.includes('barreira')) return projectAnswer(p) + activitiesAnswer();
      if (q.includes('risco') || q.includes('maturidade') || q.includes('evolucao') || q.includes('evolução')) return riskAnswer();
      if (q.includes('compar') || q.includes('setor') || q.includes('benchmark')) return sectorAnswer();
      return riskAnswer();
    }
    function renderRiskAgent() {
      const box = $('riskAgentMessages');
      if (!box) return;
      const key = (DATA.company || 'empresa') + '|' + (state.project || 'all') + '|' + (state.department || 'all');
      chatState['risk:' + key] = chatState['risk:' + key] || [{ role: 'bot', text: riskAgentAnswer('diagnóstico') }];
      box.innerHTML = chatState['risk:' + key].map(m => '<div class="msg ' + m.role + '">' + m.text + '</div>').join('');
      box.scrollTop = box.scrollHeight;
    }
    function askRiskAgent(ev) {
      ev?.preventDefault();
      const input = $('riskAgentInput');
      const question = (input?.value || '').trim();
      if (!question) return;
      const key = 'risk:' + (DATA.company || 'empresa') + '|' + (state.project || 'all') + '|' + (state.department || 'all');
      chatState[key] = chatState[key] || [];
      chatState[key].push({ role: 'user', text: esc(question) });
      chatState[key].push({ role: 'bot', text: riskAgentAnswer(question) });
      input.value = '';
      renderRiskAgent();
    }
    function quickRisk(question) {
      const input = $('riskAgentInput');
      if (!input) return;
      input.value = question;
      askRiskAgent();
    }
    function audit() {
      const validations = DATA.validations || [];
      const checks = validations.map(v => '<tr><td>' + esc(v.name) + '</td><td><span class="pill ' + (v.status === 'ok' ? 'ok' : 'no') + '">' + esc(v.status) + '</span></td><td>' + esc(v.detail) + '</td></tr>').join('');
      const sheets = Object.entries(DATA.sheets || {}).map(([key, sheet]) => ({ Aba: sheet.original_name, Chave: key, Linhas: sheet.rows_table, Colunas: sheet.cols_table, Colunas_lidas: (sheet.columns || []).join(', ') }));
      return '<section id="audit">' + hero() + '<div class="panel"><div class="panel-head"><h2>Validações</h2></div><div class="table-wrap"><table><thead><tr><th>Item</th><th>Status</th><th>Detalhe</th></tr></thead><tbody>' + checks + '</tbody></table></div></div>' + tablePanel('Abas lidas', sheets, ['Aba', 'Chave', 'Linhas', 'Colunas'], true) + tablePanel('Resumo original', DATA.tables?.resumo || [], ['Natureza', 'Projetos', '1', '2', '3', '4', 'TOTAL', 'Total']) + tablePanel('Amostra de trabalho no HTML', DATA.tables?.trabalho || [], ['Projeto', 'Funcionário', 'Mês', 'Etapa', 'Atividade realizada', 'Descrição da atividade', 'Horas decimais', 'Projeto incentivado?', 'Atividade incentivada?']) + '</section>';
    }
    function risks() {
      const p = activeProject();
      const profile = maturityProfile(p);
      const riskRows = riskRowsForProject(p).filter(row => matchSearch(row));
      const acceptedActivities = p?.accepted?.slice(0, 8).map(row => ({
        Projeto: cell(row, ['Projeto']),
        Funcionário: cell(row, ['Funcionário', 'Funcionario']),
        Atividade: cell(row, ['Atividade realizada', 'Atividade']),
        Descrição: cell(row, ['Descrição da atividade', 'Descricao da atividade']),
        Horas: cell(row, ['Horas decimais', 'Horas'])
      })) || [];
      const history = profile.history.map(item => ({
        Ano: item.year || '',
        Projeto: item.name || '',
        Status: item.status || '',
        Resumo: item.summary || '',
        Atividades: (item.activities || []).join('; ')
      }));
      const criteriaRows = eligibilityCriteriaRows(p);
      const decision = eligibilityDecision(p);
      const maturityRows = [
        { name: 'Descrição técnica', value: p?.desc ? 12 : 0 },
        { name: 'Elemento inovador', value: cell(p?.row || {}, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']) ? 18 : 0 },
        { name: 'Barreira tecnológica', value: cell(p?.row || {}, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']) ? 18 : 0 },
        { name: 'Atividades aceitas', value: p?.accepted?.length ? 18 : 0 },
        { name: 'Horas relevantes', value: Number(p?.hours || 0) > 40 ? 12 : 0 },
        { name: 'Investimentos vinculados', value: Number(p?.investment || 0) > 0 ? 10 : 0 },
        { name: 'Histórico conectado', value: history.length ? 12 : 0 }
      ];
      const agentPanel = '<div class="panel"><div class="panel-head"><h2>Agente Benner integrado</h2><span class="hint">Lê os filtros atuais</span></div><div class="messages" id="riskAgentMessages" style="min-height:260px;max-height:420px"></div><form class="chat-form" onsubmit="askRiskAgent(event)"><input id="riskAgentInput" placeholder="Pergunte por que incentivou, riscos, valores, maturidade ou evidências"><button class="primary" type="submit">Enviar</button></form><div class="agent-actions"><button onclick="quickRisk(\\'Mostre os critérios técnicos de incentivo e risco de glosa\\')">Critérios técnicos</button><button onclick="quickRisk(\\'Explique quais valores sustentam esse projeto\\')">Valores usados</button><button onclick="quickRisk(\\'O que foi inovador e quais atividades provam isso?\\')">Inovação</button><a href="https://chatgpt.com/g/g-By7xjfnhK-benner" target="_blank" rel="noopener">Abrir GPT Benner</a></div></div>';
      const externalNote = '<div class="panel"><div class="panel-head"><h2>Benchmark externo</h2><span class="hint">Pronto para API</span></div><p class="source">O HTML compara internamente as empresas carregadas. Para pesquisa automática de empresas do setor com fontes públicas atuais, conecte um backend/API; não é seguro embutir chave de IA ou pesquisa diretamente neste arquivo.</p></div>';
      return '<section id="risks">' + hero() +
        '<div class="grid-3">' +
        kpi('Decisão técnica', esc(decision.status), p?.code || 'Projeto filtrado') +
        kpi('Maturidade', esc(profile.stage), num(profile.score) + '/100') +
        kpi('Riscos mapeados', num(riskRows.length), p?.code || 'Carteira filtrada') +
        '</div><div class="grid-2" style="margin-top:16px"><div>' +
        chart('Maturidade por evidência', maturityRows, 'number', 'blue') +
        chart('Riscos por categoria', countBy(riskRows, ['Categoria', 'Tipo'], 10), 'number', 'amber') +
        '</div><div>' +
        '<div class="panel"><div class="panel-head"><h2>Leitura do projeto</h2><span class="pill ' + (p?.ok ? 'ok' : 'no') + '">' + esc(decision.status) + '</span></div><div class="text-panels"><article><h3>Por que entrou ou não entrou</h3><p>' + esc(decision.reason) + '</p></article><article><h3>Próximo passo</h3><p>' + esc(profile.next) + '</p></article><article><h3>Elemento inovador</h3><p>' + esc(short(cell(p?.row || {}, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']) || 'Não informado na base filtrada.', 360)) + '</p></article></div></div>' +
        externalNote +
        '</div></div>' +
        agentPanel +
        tablePanel('Critérios técnicos do agente', criteriaRows, ['Critério', 'Status', 'Evidência', 'Leitura'], true) +
        tablePanel('Tabela de Riscos', riskRows, ['Risco', 'Categoria', 'Impacto', 'Probabilidade', 'Mitigação'], true) +
        tablePanel('Atividades que sustentam a análise', acceptedActivities, ['Projeto', 'Funcionário', 'Atividade', 'Descrição', 'Horas'], true) +
        tablePanel('Evolução histórica vinculada', history, ['Ano', 'Projeto', 'Status', 'Resumo', 'Atividades']) +
        tablePanel('Comparativo interno do portfólio', sectorRows(), ['Empresa', 'Base', 'Projetos', 'Incentivados', '% incentivado', 'Economia estimada'], true) +
        '</section>';
    }
    function populateControls() {
      $('companySelect').innerHTML = COMPANIES.map((c, i) => '<option value="' + i + '">' + esc(c.company) + '</option>').join('');
      $('companySelect').value = String(state.company);
      const departments = allDepartments();
      if (state.department !== 'all' && !departments.some(item => norm(item) === norm(state.department))) state.department = 'all';
      $('departmentSelect').innerHTML = '<option value="all">Todos os departamentos</option>' + departments.map(item => '<option value="' + esc(item) + '">' + esc(item) + '</option>').join('');
      $('departmentSelect').value = state.department;
      const projects = allProjects().sort((a, b) => a.code.localeCompare(b.code));
      $('projectSelect').innerHTML = '<option value="all">Todos os projetos</option>' + projects.map(p => '<option value="' + esc(p.code) + '">' + esc((p.code || 'Projeto') + ' · ' + short(p.title, 70)) + '</option>').join('');
      $('projectSelect').value = projects.some(p => p.code === state.project) ? state.project : 'all';
      state.project = $('projectSelect').value;
      $('statusSelect').value = state.status;
      $('searchInput').value = state.q;
    }
    function render() {
      DATA = COMPANIES[state.company] || {};
      populateControls();
      $('app').innerHTML = [overview(), projects(), activities(), finance(), people(), history(), chat(), audit(), risks()].join('');
      activate(state.tab);
      setTimeout(renderChat, 0);
      setTimeout(renderRiskAgent, 0);
      setTimeout(updateSimulator, 0);
    }
    function activate(tab) {
      state.tab = tab;
      document.querySelectorAll('section').forEach(s => s.classList.toggle('active', s.id === tab));
      document.querySelectorAll('nav button').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
      if (tab === 'chat') renderChat();
    }
    function setProject(code) {
      state.project = code || 'all';
      render();
    }
    function setCompany(value) {
      state.company = Number(value || 0);
      state.project = 'all';
      state.department = 'all';
      state.status = 'all';
      state.q = '';
      render();
    }
    function setDepartment(value) {
      state.department = value || 'all';
      state.project = 'all';
      render();
    }
    function setStatus(value) {
      state.status = value || 'all';
      render();
    }
    function setSearch(value) {
      state.q = value || '';
      clearTimeout(searchTimer);
      searchTimer = setTimeout(render, 180);
    }
    window.setCompany = setCompany;
    window.setProject = setProject;
    window.setDepartment = setDepartment;
    window.setStatus = setStatus;
    window.setSearch = setSearch;
    window.activate = activate;
    window.askChat = askChat;
    window.askRiskAgent = askRiskAgent;
    window.quick = quick;
    window.quickRisk = quickRisk;
    window.updateSimulator = updateSimulator;
    $('tabs').innerHTML = tabs.map(([id, label]) => '<button data-tab="' + id + '" onclick="activate(\\'' + id + '\\')" class="' + (id === state.tab ? 'active' : '') + '">' + label + '</button>').join('');
    render();
  </script>
</body>
</html>"""
    return html.replace("__TITLE__", escape(title)).replace("__PAYLOAD__", payload)


def slim_analysis(analysis: dict) -> dict:
    tables = analysis.get("tables") or {}
    sheets = analysis.get("sheets") or {}
    out = {
        "company": analysis.get("company"),
        "year": analysis.get("year"),
        "source": analysis.get("source"),
        "slug": analysis.get("slug"),
        "csv_dir": analysis.get("csv_dir"),
        "metrics": analysis.get("metrics") or {},
        "history": analysis.get("history") or {"years": [], "projects": [], "evidence": []},
        "validations": analysis.get("validations") or [],
        "sheets": {
            key: {
                "original_name": sheet.get("original_name"),
                "rows_table": sheet.get("rows_table"),
                "cols_table": sheet.get("cols_table"),
            }
            for key, sheet in sheets.items()
        },
        "tables": {},
    }
    out["tables"]["resumo"] = project_columns(tables.get("resumo", []), ["Natureza", "Projetos", "1", "2", "3", "4", "TOTAL", "Total"])
    out["tables"]["projetos"] = project_columns(
        tables.get("projetos", []),
        [
            "Projeto",
            "Natureza",
            "Descrição",
            "Elemento tecnologicamente novo ou inovador",
            "Elemento inovador",
            "Barreira ou desafio tecnológico a superar",
            "Risco tecnológico",
            "Attach",
            "Incentivado?",
            "Lei do Bem?",
            "Total investido",
            "Total Help Desk",
        ],
    )
    out["tables"]["trabalho"] = slim_work_rows(tables.get("trabalho", []))
    out["tables"]["pessoal"] = project_columns(
        tables.get("pessoal", []),
        ["Projeto", "Funcionário", "Funcionario", "Cargo", "Formação", "Departamento", "Setor", "Area", "Horas efetivas (PD&I)", "Horas efetivas PDI", "Custo hora (PD&I)", "Total PD&I", "Total PDI", "Dedicação"],
    )
    out["tables"]["investimentos"] = slim_investment_rows(tables.get("investimentos", []))
    out["tables"]["riscos"] = project_columns(tables.get("riscos", []), ["Risco", "Categoria", "Tipo", "Impacto", "Probabilidade", "Mitigação"])
    return out


def project_columns(rows: list[dict], columns: list[str], limit: int | None = None) -> list[dict]:
    selected = []
    for row in rows[: limit or len(rows)]:
        clean = {}
        norm_map = {norm_key(key): key for key in row}
        for column in columns:
            key = norm_map.get(norm_key(column))
            if key is not None and str(row.get(key, "")).strip():
                clean[column] = row.get(key, "")
        if any(str(value).strip() for value in clean.values()):
            selected.append(clean)
    return selected


def slim_work_rows(rows: list[dict], limit: int = 900) -> list[dict]:
    columns = ["Projeto", "Funcionário", "Mês", "Etapa", "Atividade realizada", "Descrição da atividade", "Horas", "Horas decimais", "Projeto incentivado?", "Atividade incentivada?"]
    priority = []
    fallback = []
    for row in rows:
        if is_truthy(get_by_norm(row, "Projeto incentivado?")) and is_truthy(get_by_norm(row, "Atividade incentivada?")):
            priority.append(row)
        elif len(fallback) < 180:
            fallback.append(row)
    return project_columns((priority + fallback)[:limit], columns)


def slim_investment_rows(rows: list[dict]) -> list[dict]:
    base_columns = ["Fornecedor", "CNPJ", "Descrição", "NF/ND", "Valor", "Valor Incentivado", "Data", "Natureza", "Objetivo do gasto", "Projeto e eventual info de rateio", "Inovação?", "Proj Incentivado?"]
    selected = []
    for row in rows:
        clean = {}
        for key, value in row.items():
            if norm_key(key) in {norm_key(column) for column in base_columns} or key.upper().startswith(("INOV", "NRD")):
                if str(value).strip():
                    clean[key] = value
        if any(str(value).strip() for value in clean.values()):
            selected.append(clean)
    return selected


def get_by_norm(row: dict, name: str) -> str:
    wanted = norm_key(name)
    for key, value in row.items():
        if norm_key(key) == wanted:
            return str(value)
    return ""


def is_truthy(value: str) -> bool:
    return norm_key(value) in {"true", "verdadeiro", "sim", "yes", "1"}


def norm_key(value: str) -> str:
    table = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüç", "aaaaaeeeeiiiiooooouuuuc")
    text = str(value or "").lower().strip().translate(table)
    return "".join(ch if ch.isalnum() else " " for ch in text).strip()
