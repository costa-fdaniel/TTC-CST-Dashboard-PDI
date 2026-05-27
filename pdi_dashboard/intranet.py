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
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --ink:#17211e; --muted:#65726e; --line:#dbe3df; --bg:#f3f6f5; --panel:#ffffff;
      --green:#13795b; --blue:#315f9d; --amber:#a76617; --red:#a33b2f; --teal:#0f766e; --soft:#eef5f3;
      --shadow:0 16px 38px rgba(25,38,35,.09);
    }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--ink); font:14px/1.5 Arial, Helvetica, sans-serif; }
    .shell { display:grid; grid-template-columns:270px minmax(0,1fr); min-height:100vh; }
    aside { position:sticky; top:0; height:100vh; padding:18px; border-right:1px solid var(--line); background:linear-gradient(180deg,#fff,#f8fbfa); overflow:auto; }
    main { padding:22px; max-width:1480px; width:100%; }
    .client-area { color:var(--muted); font-weight:800; font-size:12px; text-transform:uppercase; }
    h1 { margin:6px 0 14px; font-size:22px; line-height:1.15; }
    h2 { margin:0; font-size:17px; }
    h3 { margin:0 0 8px; font-size:13px; text-transform:uppercase; color:var(--muted); }
    nav { display:grid; gap:8px; margin-top:14px; }
    nav button { justify-content:flex-start; color:var(--ink); text-decoration:none; padding:10px 11px; border:1px solid var(--line); border-radius:8px; background:#f9fbfa; font-weight:800; transition:.15s ease; }
    nav button:hover, nav button.active { border-color:rgba(15,118,110,.45); background:#eaf5f2; transform:translateX(2px); }
    select, input, textarea, button { font:inherit; }
    select, input, textarea { width:100%; border:1px solid var(--line); border-radius:8px; padding:10px 11px; background:white; color:var(--ink); }
    textarea { min-height:96px; resize:vertical; }
    button, .button { border:1px solid var(--line); border-radius:8px; padding:10px 12px; background:white; color:var(--ink); font-weight:850; cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; justify-content:center; }
    button.primary, .button.primary { background:var(--teal); border-color:var(--teal); color:white; }
    .filters {
      position:sticky; top:0; z-index:5; display:grid; grid-template-columns:1.1fr 1.1fr 1fr 1.2fr auto;
      gap:10px; margin:0 0 18px; padding:12px; border:1px solid var(--line); border-radius:10px;
      background:rgba(255,255,255,.96); box-shadow:var(--shadow);
    }
    .filters label { display:grid; gap:5px; color:var(--muted); font-size:11px; font-weight:850; text-transform:uppercase; }
    section { margin-bottom:22px; scroll-margin-top:84px; }
    .view { display:none; }
    .view.active { display:block; }
    .report-hero { background:linear-gradient(135deg,#fff 0%,#edf7f4 100%); border:1px solid var(--line); border-radius:14px; padding:20px; box-shadow:var(--shadow); margin-bottom:18px; }
    .report-hero .eyebrow { color:var(--muted); font-size:12px; font-weight:850; text-transform:uppercase; }
    .report-hero h2 { font-size:26px; margin:4px 0 8px; }
    .report-hero p { margin:0; color:var(--muted); max-width:980px; }
    .scope-strip { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
    .scope-strip span { border:1px solid var(--line); border-radius:999px; padding:5px 10px; background:#fff; color:var(--muted); font-size:12px; font-weight:850; }
    .section-title { display:flex; align-items:end; justify-content:space-between; gap:12px; margin:0 0 10px; }
    .section-title h2 { font-size:20px; }
    .section-title p { margin:4px 0 0; color:var(--muted); }
    .section-body { display:grid; gap:14px; }
    .panel { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:15px; box-shadow:var(--shadow); }
    .insight { display:grid; gap:10px; }
    .insight-card { border:1px solid var(--line); border-radius:10px; padding:14px; background:linear-gradient(180deg,#fff,#fbfdfc); }
    .insight-card strong { display:block; margin-bottom:5px; font-size:15px; }
    .insight-card p { margin:0; color:var(--muted); }
    .panel-head { display:flex; justify-content:space-between; gap:12px; align-items:start; margin-bottom:12px; }
    .method-note { border-left:4px solid var(--teal); background:#f6fbf9; }
    .method-note p { margin:0 0 8px; color:var(--muted); }
    .method-note .list li { background:#fff; }
    .subtle { color:var(--muted); font-size:12px; }
    .grid-2 { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:14px; }
    .grid-3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }
    .grid-4 { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
    .kpi { border:1px solid var(--line); border-radius:8px; padding:12px; background:#fbfcfc; }
    .kpi span { display:block; color:var(--muted); font-size:11px; font-weight:850; text-transform:uppercase; }
    .kpi b { display:block; margin-top:5px; font-size:20px; }
    .kpi small { display:block; margin-top:4px; color:var(--muted); }
    .score-card { border:1px solid var(--line); border-radius:10px; padding:13px; background:var(--soft); }
    .score-card b { display:block; font-size:24px; }
    .score-card span { color:var(--muted); font-size:12px; font-weight:850; text-transform:uppercase; }
    .mini-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:10px; }
    .mini-value { border:1px solid var(--line); border-radius:8px; padding:11px; background:#fbfcfc; }
    .mini-value span { display:block; color:var(--muted); font-size:11px; font-weight:850; text-transform:uppercase; }
    .mini-value b { display:block; margin-top:5px; font-size:18px; }
    .chart-canvas { display:none; height:292px; position:relative; }
    .chart-canvas canvas { width:100% !important; height:292px !important; }
    .charts-ready .chart-canvas { display:block; }
    .charts-ready .chart-fallback { display:none; }
    .sparkline { width:100%; height:230px; display:block; }
    .sparkline path.line { fill:none; stroke:var(--teal); stroke-width:3; }
    .sparkline circle { fill:var(--teal); }
    .multi-line path.base, .multi-line circle.base { stroke:var(--teal); fill:var(--teal); }
    .multi-line path.rh, .multi-line circle.rh { stroke:var(--blue); fill:var(--blue); }
    .multi-line path.servicos, .multi-line circle.servicos { stroke:var(--amber); fill:var(--amber); }
    .multi-line path.beneficio, .multi-line circle.beneficio { stroke:var(--green); fill:var(--green); }
    .legend-inline { display:flex; gap:10px; flex-wrap:wrap; color:var(--muted); font-size:12px; }
    .legend-inline span::before { content:""; display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:5px; background:var(--c); }
    .donut-wrap { display:grid; grid-template-columns:150px minmax(0,1fr); gap:14px; align-items:center; }
    .donut { width:150px; height:150px; border-radius:50%; background:conic-gradient(var(--green) 0 var(--good), var(--amber) var(--good) var(--warn), var(--red) var(--warn) 100%); position:relative; }
    .donut.financial { background:var(--parts); }
    .donut::after { content:""; position:absolute; inset:30px; border-radius:50%; background:white; border:1px solid var(--line); }
    .matrix { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; }
    .bar { display:grid; grid-template-columns:minmax(130px,260px) 1fr auto; gap:10px; align-items:center; margin:9px 0; }
    .bar label { font-weight:800; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .track { height:12px; background:#e7ece9; border-radius:99px; overflow:hidden; }
    .fill { height:100%; width:var(--w); background:linear-gradient(90deg,var(--teal),#5f9d80); border-radius:99px; }
    .fill.blue { background:linear-gradient(90deg,var(--blue),#7b96bd); }
    .fill.amber { background:linear-gradient(90deg,var(--amber),#d6a45e); }
    .list { margin:0; padding:0; list-style:none; display:grid; gap:8px; }
    .list li { padding:10px; border:1px solid var(--line); border-radius:8px; background:#fbfcfc; }
    .pill { display:inline-flex; border-radius:999px; padding:4px 9px; background:#eef2f1; color:var(--muted); font-weight:850; font-size:12px; }
    .ok { color:var(--green); background:#e5f4ed; }
    .warn { color:var(--amber); background:#fff3dc; }
    .bad { color:var(--red); background:#f8e8e5; }
    .table-wrap { overflow:auto; max-height:440px; border:1px solid var(--line); border-radius:8px; background:white; }
    table { width:100%; border-collapse:collapse; min-width:820px; font-size:12px; }
    th, td { text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
    th { position:sticky; top:0; background:#f0f4f2; z-index:1; font-size:11px; text-transform:uppercase; }
    .messages { min-height:300px; max-height:460px; overflow:auto; display:grid; gap:10px; align-content:start; padding:12px; border:1px solid var(--line); border-radius:8px; background:#fbfcfc; }
    .msg { border:1px solid var(--line); border-radius:8px; padding:10px; background:white; white-space:pre-wrap; }
    .msg.user { margin-left:auto; background:#e7f2f0; border-color:#bfd9d5; }
    .chat-form { display:grid; grid-template-columns:1fr auto; gap:8px; margin-top:10px; }
    .actions { display:flex; gap:8px; flex-wrap:wrap; }
    .toc-note { color:var(--muted); font-size:12px; margin-top:12px; }
    @media (max-width: 1050px) {
      .shell { grid-template-columns:1fr; }
      aside { position:static; height:auto; }
      .filters, .grid-2, .grid-3, .grid-4 { grid-template-columns:1fr; position:static; }
      .bar { grid-template-columns:1fr; }
      .chat-form { grid-template-columns:1fr; }
    }
  </style>
</head>
<body>
  <script id="data" type="application/json">__PAYLOAD__</script>
  <div class="shell">
    <aside>
      <div class="client-area">Área do cliente</div>
      <h1>Relatórios de PD&I</h1>
      <select id="companySelect" onchange="setCompany(this.value)" aria-label="Relatório"></select>
      <nav aria-label="Table of contents">
        <button type="button" data-view="resumo" onclick="setView('resumo')">Resumo</button>
        <button type="button" data-view="lei" onclick="setView('lei')">Lei do Bem</button>
        <button type="button" data-view="tecnoparque" onclick="setView('tecnoparque')">Tecnoparque</button>
        <button type="button" data-view="analiticos" onclick="setView('analiticos')">Dados analíticos</button>
        <button type="button" data-view="avaliacao" onclick="setView('avaliacao')">Avaliação PD&I</button>
        <button type="button" data-view="indice" onclick="setView('indice')">Índice ano a ano</button>
        <button type="button" data-view="agentes" onclick="setView('agentes')">Agentes e suporte</button>
        <button type="button" data-view="downloads" onclick="setView('downloads')">Downloads</button>
      </nav>
      <p class="toc-note">Header corporativo entra acima desta área na intranet.</p>
    </aside>
    <main>
      <div class="filters">
        <label>Ano<select id="yearSelect" onchange="setFilter('year', this.value)" aria-label="Ano"></select></label>
        <label>Projeto<select id="projectSelect" onchange="setFilter('project', this.value)" aria-label="Projeto"></select></label>
        <label>Despesa<select id="expenseSelect" onchange="setFilter('expense', this.value)" aria-label="Tipo de despesa"></select></label>
        <label>Busca<input id="searchInput" oninput="setFilter('q', this.value)" placeholder="Projeto, atividade, evidência ou fornecedor"></label>
        <button type="button" onclick="clearFilters()">Limpar</button>
      </div>
      <div id="app"></div>
    </main>
  </div>
  <script>
    const PORTAL = JSON.parse(document.getElementById('data').textContent);
    const COMPANIES = PORTAL.companies || [];
    const fmtMoney = new Intl.NumberFormat('pt-BR', { style:'currency', currency:'BRL' });
    const fmtNum = new Intl.NumberFormat('pt-BR', { maximumFractionDigits:2 });
    const state = { company:0, year:'all', project:'all', expense:'all', q:'', view:'resumo' };
    const chats = {};
    let chartSeq = 0;
    let chartConfigs = {};
    let chartInstances = [];
    const $ = id => document.getElementById(id);
    const norm = v => String(v || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().trim();
    const esc = v => String(v ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
    const money = v => fmtMoney.format(Number(v || 0));
    const num = v => fmtNum.format(Number(v || 0));
    const short = (v, n=180) => { const t=String(v||'').replace(/\\s+/g,' ').trim(); return t.length>n ? t.slice(0,n-3)+'...' : t; };
    const DATA = () => COMPANIES[state.company] || {};
    function cell(row, names) {
      const wanted = names.map(norm);
      const key = Object.keys(row || {}).find(k => wanted.includes(norm(k)));
      return key ? row[key] : '';
    }
    function numCell(row, names) {
      const raw = String(cell(row, names) || '').replace(/R\\$/g,'').replace(/%/g,'').trim();
      const normalized = raw.includes(',') ? raw.replace(/\\./g,'').replace(',','.') : raw;
      const value = Number(normalized);
      return Number.isFinite(value) ? value : 0;
    }
    function boolCell(row, names) { return ['true','verdadeiro','sim','yes','1'].includes(norm(cell(row,names))); }
    function rows(key) { return (DATA().tables?.[key] || []).filter(row => Object.values(row || {}).some(v => String(v||'').trim())); }
    function years() {
      const set = new Set((DATA().history?.years || []).map(y => String(y.year)).filter(Boolean));
      if (DATA().year) set.add(String(DATA().year));
      return [...set].sort();
    }
    function projectCode(row) {
      return String(cell(row, ['Attach']) || cell(row, ['Projeto']) || '').trim();
    }
    function projects() {
      const current = rows('projetos').map((row, i) => {
        const title = String(cell(row, ['Projeto']) || 'Projeto ' + (i+1)).trim();
        return { id:'c'+state.company+'-p'+i, title, code:projectCode(row), row, source:'Atual', year:DATA().year || '' };
      });
      const history = (DATA().history?.projects || []).map((item, i) => ({
        id:'c'+state.company+'-h'+i,
        title:item.name || item.summary || 'Projeto histórico ' + (i+1),
        code:'',
        row:{ Projeto:item.name || '', Descrição:item.summary || '', Incentivado:item.status || '' },
        source:'Histórico',
        year:item.year || '',
        history:item
      }));
      const seen = new Set();
      return [...current, ...history].filter(p => {
        const key = norm((p.code || '') + '|' + p.title + '|' + p.year);
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }
    function selectedProject() {
      return state.project === 'all' ? null : projects().find(p => p.id === state.project);
    }
    function rowYear(row) {
      const explicit = cell(row, ['Ano', 'Year']);
      if (explicit) {
        const match = String(explicit).match(/20\\d{2}/);
        return match ? match[0] : String(explicit);
      }
      const text = Object.values(row || {}).join(' ');
      const match = text.match(/20\\d{2}/);
      return match ? match[0] : '';
    }
    function matchYear(row) {
      if (state.year === 'all') return true;
      const y = rowYear(row);
      if (y) return String(y) === String(state.year);
      return String(DATA().year || '') === String(state.year);
    }
    function matchProject(row, p = selectedProject()) {
      if (!p) return true;
      const text = norm(JSON.stringify(row || {}));
      const code = norm(p.code);
      const title = norm(p.title);
      return (code && text.includes(code)) || (title.length > 10 && text.includes(title.slice(0,80)));
    }
    function matchQuery(row) {
      return !state.q || norm(JSON.stringify(row || {})).includes(norm(state.q));
    }
    function filteredProjects() {
      const q = norm(state.q);
      return projects().filter(p => {
        if (state.year !== 'all' && p.year && String(p.year) !== String(state.year)) return false;
        if (state.project !== 'all' && p.id !== state.project) return false;
        if (q && !norm([p.title, p.code, cell(p.row,['Descrição'])].join(' ')).includes(q)) return false;
        return true;
      });
    }
    function availableProjectsForControl() {
      return projects().filter(p => state.year === 'all' || !p.year || String(p.year) === String(state.year));
    }
    function activeProject() { return filteredProjects()[0] || projects()[0]; }
    function projectRows(key, p=activeProject()) {
      const selected = state.project === 'all' ? null : p;
      return rows(key).filter(row => matchYear(row) && matchQuery(row) && matchProject(row, selected));
    }
    function expenses() {
      const set = new Set(['all']);
      ['RH', 'Materiais', 'Serviços/terceiros'].forEach(v => set.add(v));
      rows('investimentos').forEach(row => { const v = cell(row, ['Natureza', 'Tipo de despesa']); if (v) set.add(v); });
      return [...set];
    }
    function filteredInvestments() {
      return projectRows('investimentos').filter(row => state.expense === 'all' || norm(cell(row, ['Natureza', 'Tipo de despesa'])) === norm(state.expense));
    }
    function filteredHistoryYears() {
      return (DATA().history?.years || []).filter(row => state.year === 'all' || String(row.year) === String(state.year));
    }
    function filteredHistoryProjects() {
      const p = selectedProject();
      return (DATA().history?.projects || []).filter(item => {
        const row = { Ano:item.year, Projeto:item.name, Descrição:item.summary, Atividades:(item.activities || []).join(' ') };
        return matchYear(row) && matchQuery(row) && matchProject(row, p);
      });
    }
    function filteredContext() {
      const work = projectRows('trabalho');
      const people = projectRows('pessoal');
      const inv = filteredInvestments();
      const histYears = filteredHistoryYears();
      const histProjects = filteredHistoryProjects();
      const accepted = work.filter(row => boolCell(row, ['Projeto incentivado?']) && boolCell(row, ['Atividade incentivada?']));
      return { work, people, inv, histYears, histProjects, accepted, p:selectedProject() };
    }
    function sum(rows, names) { return rows.reduce((acc,row)=>acc+numCell(row,names),0); }
    function group(rows, keyNames, valueNames, limit=10) {
      const map = new Map();
      rows.forEach(row => {
        const key = String(cell(row,keyNames) || 'Não informado').trim() || 'Não informado';
        const value = valueNames ? numCell(row,valueNames) : 1;
        if (value) map.set(key, (map.get(key)||0)+value);
      });
      return [...map.entries()].sort((a,b)=>b[1]-a[1]).slice(0,limit).map(([name,value]) => ({name,value}));
    }
    function chartColor(tone) {
      return tone === 'blue' ? '#315f9d' : tone === 'amber' ? '#a76617' : tone === 'green' ? '#13795b' : '#0f766e';
    }
    function seriesColor(item) {
      return item.className === 'rh' ? '#315f9d' : item.className === 'servicos' ? '#a76617' : item.className === 'beneficio' ? '#13795b' : '#0f766e';
    }
    function chartPanel(title, config, fallback, pill='') {
      const id = 'chart_' + (++chartSeq);
      chartConfigs[id] = config;
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2>'+(pill ? '<span class="pill">'+esc(pill)+'</span>' : '')+'</div><div class="chart-canvas"><canvas id="'+id+'"></canvas></div><div class="chart-fallback">'+fallback+'</div></div>';
    }
    function renderChartCanvases() {
      chartInstances.forEach(chart => chart.destroy());
      chartInstances = [];
      if (!window.Chart) return;
      document.body.classList.add('charts-ready');
      Object.entries(chartConfigs).forEach(([id, config]) => {
        const canvas = $(id);
        if (!canvas || !canvas.offsetParent) return;
        chartInstances.push(new Chart(canvas, config));
      });
    }
    function chart(title, items, kind='number', tone='') {
      const clean = (items||[]).filter(item => Number(item.value||0)>0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem dados suficientes.</p></div>';
      const max = Math.max(...clean.map(i=>Number(i.value||0)),1);
      const fallback = clean.map(item => {
        const value = kind === 'money' ? money(item.value) : num(item.value);
        return '<div class="bar"><label title="'+esc(item.name)+'">'+esc(item.name)+'</label><div class="track"><div class="fill '+tone+'" style="--w:'+Math.max(4, item.value/max*100)+'%"></div></div><b>'+value+'</b></div>';
      }).join('');
      const config = {
        type:'bar',
        data:{ labels:clean.map(item => item.name), datasets:[{ label:title, data:clean.map(item => Number(item.value || 0)), backgroundColor:chartColor(tone), borderRadius:7 }] },
        options:{ responsive:true, maintainAspectRatio:false, indexAxis:'y', plugins:{ legend:{ display:false }, tooltip:{ callbacks:{ label:ctx => kind === 'money' ? money(ctx.raw) : num(ctx.raw) } } }, scales:{ x:{ grid:{ color:'#edf2ef' }, ticks:{ callback:value => kind === 'money' ? money(value) : num(value) } }, y:{ grid:{ display:false } } } }
      };
      return chartPanel(title, config, fallback, clean.length+' itens');
    }
    function lineChart(title, rows) {
      const clean = (rows || []).filter(r => Number(r.Índice || r.value || 0) > 0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem dados suficientes.</p></div>';
      if (clean.length === 1) {
        const row = clean[0];
        const value = Number(row.Índice || row.value || 0);
        return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+esc(row.Ano || row.name || 'Ano')+'</span></div><div class="mini-grid"><div class="mini-value"><span>Valor do recorte</span><b>'+num(value)+'</b></div></div></div>';
      }
      const vals = clean.map(r => Number(r.Índice || r.value || 0));
      const labels = clean.map(r => String(r.Ano || r.name || ''));
      const max = Math.max(...vals, 100), min = Math.min(...vals, 0);
      const points = vals.map((v,i) => {
        const x = 30 + (i * (520 / Math.max(vals.length - 1, 1)));
        const y = 190 - ((v - min) / Math.max(max - min, 1) * 150);
        return { x, y, v, label: labels[i] };
      });
      const path = points.map((p,i) => (i ? 'L' : 'M') + p.x + ' ' + p.y).join(' ');
      const dots = points.map(p => '<circle cx="'+p.x+'" cy="'+p.y+'" r="4"><title>'+esc(p.label)+': '+num(p.v)+'</title></circle>').join('');
      const axis = points.map(p => '<text x="'+p.x+'" y="215" text-anchor="middle" font-size="11" fill="#65726e">'+esc(p.label)+'</text>').join('');
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+clean.length+' pontos</span></div><svg class="sparkline" viewBox="0 0 590 230" role="img"><line x1="30" y1="190" x2="560" y2="190" stroke="#dbe3df"/><line x1="30" y1="35" x2="30" y2="190" stroke="#dbe3df"/><path class="line" d="'+path+'"/>'+dots+axis+'</svg></div>';
    }
    function multiLineChart(title, rows, series) {
      const clean = (rows || []).filter(row => series.some(s => Number(row[s.key] || 0) > 0));
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem dados financeiros para exibir.</p></div>';
      if (clean.length === 1) {
        const row = clean[0];
        const cards = series.filter(s => Number(row[s.key] || 0) > 0).map(s => '<div class="mini-value"><span>'+esc(s.label)+'</span><b>'+money(row[s.key])+'</b></div>').join('');
        return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+esc(row.Ano || 'Ano selecionado')+'</span></div><div class="mini-grid">'+cards+'</div></div>';
      }
      const values = clean.flatMap(row => series.map(s => Number(row[s.key] || 0)));
      const max = Math.max(...values, 1);
      const xFor = i => 38 + (i * (510 / Math.max(clean.length - 1, 1)));
      const yFor = v => 190 - (Number(v || 0) / max * 150);
      const paths = series.map(s => {
        const points = clean.map((row,i) => ({ x:xFor(i), y:yFor(row[s.key]), v:Number(row[s.key] || 0), ano:row.Ano }));
        const path = points.map((p,i) => (i ? 'L' : 'M') + p.x + ' ' + p.y).join(' ');
        const dots = points.map(p => '<circle class="'+esc(s.className)+'" cx="'+p.x+'" cy="'+p.y+'" r="3"><title>'+esc(s.label)+' '+esc(p.ano)+': '+money(p.v)+'</title></circle>').join('');
        return '<g><path class="line '+esc(s.className)+'" d="'+path+'"/>'+dots+'</g>';
      }).join('');
      const labels = clean.map((row,i) => '<text x="'+xFor(i)+'" y="215" text-anchor="middle" font-size="11" fill="#65726e">'+esc(row.Ano)+'</text>').join('');
      const legend = '<div class="legend-inline">' + series.map(s => '<span style="--c:'+s.color+'">'+esc(s.label)+'</span>').join('') + '</div>';
      const fallback = legend+'<svg class="sparkline" viewBox="0 0 590 230" role="img"><line x1="38" y1="190" x2="548" y2="190" stroke="#dbe3df"/><line x1="38" y1="35" x2="38" y2="190" stroke="#dbe3df"/>'+paths+labels+'</svg>';
      const config = {
        type:'line',
        data:{ labels:clean.map(row => String(row.Ano)), datasets:series.map(s => ({ label:s.label, data:clean.map(row => Number(row[s.key] || 0)), borderColor:seriesColor(s), backgroundColor:seriesColor(s), tension:.32, pointRadius:4, borderWidth:3 })) },
        options:{ responsive:true, maintainAspectRatio:false, interaction:{ mode:'index', intersect:false }, plugins:{ legend:{ position:'bottom' }, tooltip:{ callbacks:{ label:ctx => ctx.dataset.label + ': ' + money(ctx.raw) } } }, scales:{ y:{ grid:{ color:'#edf2ef' }, ticks:{ callback:value => money(value) } }, x:{ grid:{ display:false } } } }
      };
      return chartPanel(title, config, fallback, clean.length+' anos');
    }
    function stackedBarChart(title, rows) {
      const clean = (rows || []).filter(row => Number(row.RH_val || 0) || Number(row.Material_val || 0) || Number(row.Servicos_val || 0));
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem composição de dispêndios para exibir.</p></div>';
      const max = Math.max(...clean.map(r => Number(r.RH_val||0)+Number(r.Material_val||0)+Number(r.Servicos_val||0)), 1);
      const body = clean.map(r => {
        const rh = Number(r.RH_val||0), mat = Number(r.Material_val||0), serv = Number(r.Servicos_val||0);
        const total = rh + mat + serv || 1;
        return '<div class="bar"><label>'+esc(r.Ano)+'</label><div class="track" style="display:flex;height:16px"><i style="width:'+(rh/total*100)+'%;background:var(--blue)"></i><i style="width:'+(mat/total*100)+'%;background:var(--teal)"></i><i style="width:'+(serv/total*100)+'%;background:var(--amber)"></i></div><strong>'+money(total)+'</strong></div>';
      }).join('');
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+clean.length+' anos</span></div><div class="legend-inline"><span style="--c:var(--blue)">RH</span><span style="--c:var(--teal)">Materiais</span><span style="--c:var(--amber)">Serviços/terceiros</span></div>'+body+'</div>';
    }
    function donutChart(title, quality) {
      const total = Math.max(quality.length, 1);
      const good = quality.filter(r => r.Índice >= 78).length / total * 100;
      const warn = good + quality.filter(r => r.Índice >= 58 && r.Índice < 78).length / total * 100;
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+quality.length+' projetos</span></div><div class="donut-wrap"><div class="donut" style="--good:'+good+'%;--warn:'+warn+'%"></div><ul class="list"><li><b>Fortes:</b> '+num(quality.filter(r=>r.Índice>=78).length)+'</li><li><b>Com ressalvas:</b> '+num(quality.filter(r=>r.Índice>=58 && r.Índice<78).length)+'</li><li><b>Frágeis/críticos:</b> '+num(quality.filter(r=>r.Índice<58).length)+'</li></ul></div></div>';
    }
    function compositionDonut(title, parts) {
      const clean = (parts || []).filter(part => Number(part.value || 0) > 0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem valores positivos para compor o gráfico.</p></div>';
      const total = clean.reduce((acc, part) => acc + Number(part.value || 0), 0);
      let cursor = 0;
      const stops = clean.map(part => {
        const start = cursor;
        cursor += Number(part.value || 0) / total * 100;
        return part.color + ' ' + start.toFixed(2) + '% ' + cursor.toFixed(2) + '%';
      }).join(', ');
      const legend = clean.map(part => '<li><b>'+esc(part.name)+':</b> '+money(part.value)+' <small>('+num(Number(part.value || 0) / total * 100)+'%)</small></li>').join('');
      const fallback = '<div class="donut-wrap"><div class="donut financial" style="--parts:conic-gradient('+stops+')"></div><ul class="list">'+legend+'</ul></div>';
      const config = {
        type:'doughnut',
        data:{ labels:clean.map(part => part.name), datasets:[{ data:clean.map(part => Number(part.value || 0)), backgroundColor:['#315f9d','#0f766e','#a76617','#13795b','#a33b2f'], borderWidth:0 }] },
        options:{ responsive:true, maintainAspectRatio:false, cutout:'62%', plugins:{ legend:{ position:'right' }, tooltip:{ callbacks:{ label:ctx => ctx.label + ': ' + money(ctx.raw) } } } }
      };
      return chartPanel(title, config, fallback, money(total));
    }
    function kpi(label, value, sub='') { return '<div class="kpi"><span>'+esc(label)+'</span><b>'+value+'</b><small>'+esc(sub)+'</small></div>'; }
    function programScoreForYear(row) {
      let score = 20;
      if (Number(row.base_total||0)>0) score += 18;
      if (Number(row.rh_total||0)>0) score += 12;
      if (Number(row.material_total||0)>0 || Number(row.third_party_total||0)>0) score += 12;
      if (Number(row.eligible_hours_partial||0)>0 || Number(row.eligible_hours_exclusive||0)>0) score += 14;
      if (Number(row.estimated_savings||0)>0) score += 10;
      const evidence = (DATA().history?.evidence || []).filter(e => String(e.source||'').includes(String(row.year))).length;
      if (evidence) score += Math.min(14, evidence*4);
      return Math.min(100, score);
    }
    function scoreBand(score) { return score >= 82 ? 'Programa maduro' : score >= 65 ? 'Bom, com oportunidades' : score >= 45 ? 'Em estruturação' : 'Requer plano de ação'; }
    function projectHistoryMatches(p) {
      if (!p) return [];
      const title = norm(p.title);
      const code = norm(p.code);
      const tokens = title.split(' ').filter(t => t.length > 3 && !['projeto','desenvolvimento','linha'].includes(t));
      return (DATA().history?.projects || []).filter(item => {
        const text = norm([item.name, item.summary, item.status, ...(item.activities || [])].join(' '));
        const overlap = tokens.filter(t => text.includes(t)).length;
        return (code && text.includes(code)) || (title.length > 10 && text.includes(title.slice(0,80))) || overlap >= Math.min(3, tokens.length);
      });
    }
    function projectQuality(p) {
      const work = projectRows('trabalho', p);
      const inv = filteredInvestments().filter(row => matchProject(row, p));
      const accepted = work.filter(row => boolCell(row, ['Projeto incentivado?']) && boolCell(row, ['Atividade incentivada?']));
      const desc = cell(p?.row || {}, ['Descrição']);
      const element = cell(p?.row || {}, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']);
      const barrier = cell(p?.row || {}, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']);
      const hist = projectHistoryMatches(p);
      let score = 0;
      if (desc) score += 14;
      if (element) score += 20;
      if (barrier) score += 20;
      if (accepted.length) score += 18;
      if (sum(accepted, ['Horas decimais','Horas']) > 40) score += 10;
      if (sum(inv, ['Valor Incentivado','Valor']) > 0) score += 10;
      if (hist.length) score += Math.min(8, hist.length * 2);
      const status = score >= 78 ? 'Projeto forte' : score >= 58 ? 'Bom, mas exige reforço' : score >= 38 ? 'Frágil para defesa' : 'Crítico';
      const risk = score >= 78 ? 'baixo' : score >= 58 ? 'moderado' : 'alto';
      return { score:Math.min(score,100), status, risk, accepted, inv, hist, desc, element, barrier };
    }
    function projectQualityRows() {
      return filteredProjects().map(p => {
        const q = projectQuality(p);
        return {
          Projeto:p.title,
          Código:p.code,
          Origem:p.source,
          Ano:p.year || '',
          Índice:q.score,
          Diagnóstico:q.status,
          Risco:q.risk,
          Evidência: q.element || q.barrier || q.desc || 'Sem narrativa técnica suficiente'
        };
      }).sort((a,b)=>b.Índice-a.Índice);
    }
    function historyProjectCountForYear(year) {
      const seen = new Set();
      (DATA().history?.projects || []).forEach(item => {
        if (String(item.year || '') !== String(year || '')) return;
        const key = norm(item.name || item.summary || '');
        if (key) seen.add(key);
      });
      return seen.size;
    }
    function historyIncentivizedCountForYear(year) {
      const seen = new Set();
      (DATA().history?.projects || []).forEach(item => {
        if (String(item.year || '') !== String(year || '')) return;
        const text = norm([item.status, item.summary, item.name].join(' '));
        if (!text.includes('incent')) return;
        const key = norm(item.name || item.summary || '');
        if (key) seen.add(key);
      });
      return seen.size;
    }
    function annualProjectValue(row, p) {
      if (!p) return 0;
      const code = norm(p.code);
      const title = norm(p.title);
      const tokens = title.split(' ').filter(t => t.length > 3 && !['projeto','desenvolvimento','linha'].includes(t));
      const matches = (row.top_projects || []).filter(item => {
        const name = norm(item.name || '');
        const overlap = tokens.filter(t => name.includes(t)).length;
        return (code && name.includes(code)) || (title && name.includes(title.slice(0,80))) || overlap >= Math.min(3, tokens.length);
      });
      return matches.reduce((acc,item)=>acc+Number(item.value || 0),0);
    }
    function annualHasProject(row, p) {
      if (!p) return true;
      if (annualProjectValue(row, p) > 0) return true;
      return projectHistoryMatches(p).some(item => String(item.year || '') === String(row.year || DATA().year || ''));
    }
    function annualMatchesQuery(row) {
      if (!state.q) return true;
      const q = norm(state.q);
      const top = (row.top_projects || []).map(item => item.name).join(' ');
      const refs = (row.source_refs || []).join(' ');
      const hist = (DATA().history?.projects || [])
        .filter(item => String(item.year || '') === String(row.year || ''))
        .map(item => [item.name, item.summary, item.status, ...(item.activities || [])].join(' '))
        .join(' ');
      return norm([row.year, top, refs, hist].join(' ')).includes(q);
    }
    function applyExpenseFilter(values, row) {
      if (state.expense === 'all') return values;
      const selected = norm(state.expense);
      const baseTotal = Number(row.base_total || 0) || values.base || 1;
      const only = { rh:0, material:0, servicos:0, investimento:0, base:0, beneficio:0 };
      if (selected.includes('rh') || selected.includes('pessoal') || selected.includes('folha') || selected.includes('salario')) {
        only.rh = values.rh;
        only.base = values.rh;
      } else if (selected.includes('serv') || selected.includes('terc') || selected.includes('fornecedor') || selected.includes('laborat') || selected.includes('analise')) {
        only.servicos = values.servicos;
        only.investimento = values.servicos;
        only.base = values.servicos;
      } else if (selected.includes('mat') || selected.includes('insumo') || selected.includes('consumo') || selected.includes('equip')) {
        only.material = values.material;
        only.investimento = values.material;
        only.base = values.material;
      } else {
        only.investimento = values.investimento;
        only.base = values.investimento;
      }
      const share = Math.min(1, Math.max(0, only.base / baseTotal));
      only.beneficio = values.beneficio * share;
      return only;
    }
    function annualRows() {
      const p = selectedProject();
      const historyYears = filteredHistoryYears();
      const source = historyYears.filter(row => annualHasProject(row, p) && annualMatchesQuery(row));
      const fallback = [{ year:DATA().year, base_total:DATA().metrics?.base_total, estimated_savings:DATA().metrics?.estimated_savings, rh_total:DATA().metrics?.people_pdi_total, material_total:DATA().metrics?.investment_incentivized }];
      const rows = (source.length ? source : (historyYears.length ? [] : fallback))
        .slice()
        .sort((a,b) => Number(a.year || 0) - Number(b.year || 0));
      const scopedRows = rows.map(row => {
        let values = {
          rh:Number(row.rh_total || 0),
          material:Number(row.material_total || 0),
          servicos:Number(row.third_party_total || 0),
          investimento:Number(row.investment_total || 0) || Number(row.material_total || 0) + Number(row.third_party_total || 0),
          base:Number(row.base_total || 0),
          beneficio:Number(row.estimated_savings || 0)
        };
        const projectValue = annualProjectValue(row, p);
        if (p) {
          const baseTotal = Number(row.base_total || 0) || values.base || 1;
          const share = projectValue > 0 ? Math.min(1, Math.max(0, projectValue / baseTotal)) : 0;
          values = {
            rh:values.rh * share,
            material:values.material * share,
            servicos:values.servicos * share,
            investimento:values.investimento * share,
            base:projectValue || values.base * share,
            beneficio:values.beneficio * share
          };
        }
        values = applyExpenseFilter(values, row);
        const rh = values.rh;
        const material = values.material;
        const servicos = values.servicos;
        const investimento = values.investimento || material + servicos;
        const base = values.base;
        const beneficio = values.beneficio;
        const topProjects = (row.top_projects || []).filter(item => norm(item.name || '')).length;
        const positiveTopProjects = (row.top_projects || []).filter(item => Number(item.value || 0) > 0).length;
        const histProjects = historyProjectCountForYear(row.year);
        const histIncentivized = historyIncentivizedCountForYear(row.year);
        const projetos = p ? 1 : (Number(row.projects_total || 0) || topProjects || histProjects);
        const incentivados = p ? (projectValue > 0 ? 1 : 0) : (Number(row.projects_incentivized || 0) || positiveTopProjects || histIncentivized);
        return { ...row, rh_total:rh, material_total:material, third_party_total:servicos, investment_total:investimento, base_total:base, estimated_savings:beneficio, projects_total:projetos, projects_incentivized:incentivados, _projectValue:projectValue };
      });
      return scopedRows.map((row, idx) => {
        const score = programScoreForYear(row);
        const prev = idx ? programScoreForYear(scopedRows[idx-1]) : null;
        const delta = prev == null ? 0 : score - prev;
        const trend = delta > 6 ? 'ganhou força' : delta < -6 ? 'perdeu força' : 'estável';
        const rh = Number(row.rh_total || 0);
        const material = Number(row.material_total || 0);
        const servicos = Number(row.third_party_total || 0);
        const investimento = Number(row.investment_total || 0) || material + servicos;
        const base = Number(row.base_total || 0);
        const beneficio = Number(row.estimated_savings || 0);
        const projetos = Number(row.projects_total || 0);
        const incentivados = Number(row.projects_incentivized || 0);
        const recommendation = score >= 82
          ? 'Manter governança e transformar maturidade em agenda de suporte, com revisão preventiva de evidências.'
          : score >= 65
            ? 'Reforçar rastreabilidade de testes, resultados e valores para reduzir risco em fiscalização.'
            : score >= 45
              ? 'Implantar plano de ação: timesheet técnico, memória por projeto, conciliação mensal e comitê de evidências.'
              : 'Priorizar reconstrução documental e revisão de elegibilidade antes de defender benefício fiscal.';
        return {
          Ano:row.year || DATA().year || 'Atual',
          Índice:score,
          Tendência:trend,
          Variação:delta ? (delta > 0 ? '+' : '') + num(delta) : 'base',
          Diagnóstico:scoreBand(score),
          Base:money(base),
          Base_val:base,
          RH:money(rh),
          RH_val:rh,
          Materiais:money(material),
          Material_val:material,
          'Serviços/terceiros':money(servicos),
          Servicos_val:servicos,
          Investimentos:money(investimento),
          Investimentos_val:investimento,
          Benefício:money(beneficio),
          Beneficio_val:beneficio,
          Projetos:projetos,
          Incentivados:incentivados,
          Recomendação:recommendation
        };
      });
    }
    function annualExpenseItems(annual = annualRows()) {
      const totals = annual.reduce((acc,row) => {
        acc.rh += Number(row.RH_val || 0);
        acc.material += Number(row.Material_val || 0);
        acc.servicos += Number(row.Servicos_val || 0);
        acc.beneficio += Number(row.Beneficio_val || 0);
        return acc;
      }, { rh:0, material:0, servicos:0, beneficio:0 });
      return [
        { name:'RH', value:totals.rh },
        { name:'Materiais', value:totals.material },
        { name:'Serviços/terceiros', value:totals.servicos },
        { name:'Benefício estimado', value:totals.beneficio }
      ];
    }
    function annualActivityItems(annual = annualRows()) {
      const hist = filteredHistoryProjects();
      const map = new Map();
      hist.forEach(item => {
        const key = item.name || item.summary || 'Projeto histórico';
        map.set(key, (map.get(key) || 0) + 1);
      });
      if (map.size) return [...map.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10).map(([name,value]) => ({ name, value }));
      return annual.map(row => ({ name:'Projetos em ' + row.Ano, value:Number(row.Projetos || 0) })).filter(item => item.value > 0);
    }
    function evidenceRows() {
      return (DATA().history?.evidence || []).filter(row => state.year === 'all' || !row.year || String(row.year) === String(state.year));
    }
    function methodPanel() {
      const evidence = evidenceRows();
      const sourceKind = (DATA().history?.years || []).some(row => row.method) ? 'histórico estruturado' : 'base atual';
      const rows = evidence.map(row => ({
        Ano:row.year || 'Todos',
        Fonte:short(row.source || DATA().source || '', 90),
        Tipo:row.kind || sourceKind,
        Confiança:row.confidence || 'não informada',
        Nota:short(row.notes || row.extracted_from || 'Sem nota metodológica.', 180)
      }));
      const intro = '<div class="panel method-note"><div class="panel-head"><h2>Fonte, método e confiança</h2><span class="pill">'+esc(sourceKind)+'</span></div><p>Inspirado no HTML da BIGCORE, este bloco explicita de onde vieram os dados do recorte e como eles devem ser lidos antes da decisão comercial ou fiscal.</p><ul class="list"><li><b>Valores:</b> priorizam dados históricos estruturados quando há ano selecionado; quando não há detalhe analítico, usam agregados anuais.</li><li><b>Projetos e fornecedores:</b> aparecem como drilldown para explicar o valor, sem remover a base original.</li><li><b>Risco:</b> aumenta quando falta vínculo entre descrição técnica, atividade executada e despesa.</li></ul></div>';
      return intro + table('Evidências do recorte', rows, ['Ano','Fonte','Tipo','Confiança','Nota']);
    }
    function topSpendRows() {
      const out = [];
      filteredHistoryYears().forEach(row => {
        (row.top_projects || []).forEach(item => {
          const value = Number(item.value || 0);
          if (value > 0) out.push({ Ano:row.year || '', Item:item.name || 'Não informado', Valor:money(value), Valor_num:value, Origem:'histórico anual' });
        });
      });
      if (!out.length) {
        filteredInvestments().forEach(row => {
          const value = numCell(row, ['Valor Incentivado','Valor']);
          if (value > 0) out.push({ Ano:rowYear(row) || state.year || '', Item:cell(row, ['Fornecedor','Projeto','Natureza']) || 'Não informado', Valor:money(value), Valor_num:value, Origem:'investimentos analíticos' });
        });
      }
      return out.sort((a,b)=>b.Valor_num-a.Valor_num).slice(0,20).map(row => ({ Ano:row.Ano, Item:row.Item, Valor:row.Valor, Origem:row.Origem }));
    }
    function quarterlyRows() {
      const rows = [];
      filteredHistoryYears().forEach(yearRow => {
        (yearRow.quarterly || []).forEach(item => rows.push({
          Ano:yearRow.year || '',
          Trimestre:item.name || item.quarter || '',
          Base:Number(item.base || item.total || 0),
          Investimentos:Number(item.investment || 0),
          RH:Number(item.rh || 0),
          Exclusão:Number(item.exclusion || 0),
          Benefício:Number(item.savings || item.benefit || 0)
        }));
      });
      if (!rows.length && (DATA().metrics?.quarterly || []).length && (state.year === 'all' || String(DATA().year || '') === String(state.year))) {
        (DATA().metrics.quarterly || []).forEach(item => rows.push({
          Ano:DATA().year || '',
          Trimestre:item.name || '',
          Base:Number(item.base || 0),
          Investimentos:Number(item.investment || 0),
          RH:Number(item.rh || 0),
          Exclusão:Number(item.exclusion || 0),
          Benefício:Number(item.savings || 0)
        }));
      }
      return rows.filter(row => row.Base || row.Investimentos || row.RH || row.Benefício);
    }
    function quarterlyPanel() {
      const rows = quarterlyRows();
      if (!rows.length) return '<div class="panel"><div class="panel-head"><h2>Leitura trimestral</h2></div><p class="subtle">Sem abertura trimestral estruturada para o recorte atual.</p></div>';
      const labels = rows.map(row => String(row.Ano) + ' ' + row.Trimestre);
      const fallback = '<div class="mini-grid">' + rows.map(row => '<div class="mini-value"><span>'+esc(row.Ano+' '+row.Trimestre)+'</span><b>'+money(row.Base)+'</b><small class="subtle">Benefício: '+money(row.Benefício)+'</small></div>').join('') + '</div>';
      const config = {
        type:'bar',
        data:{ labels, datasets:[
          { label:'Base PD&I', data:rows.map(row=>row.Base), backgroundColor:'#0f766e', borderRadius:6 },
          { label:'Benefício', data:rows.map(row=>row.Benefício), backgroundColor:'#13795b', borderRadius:6 }
        ] },
        options:{ responsive:true, maintainAspectRatio:false, plugins:{ legend:{ position:'bottom' }, tooltip:{ callbacks:{ label:ctx => ctx.dataset.label + ': ' + money(ctx.raw) } } }, scales:{ y:{ ticks:{ callback:value => money(value) }, grid:{ color:'#edf2ef' } }, x:{ grid:{ display:false } } } }
      };
      return chartPanel('Leitura trimestral: base e benefício', config, fallback, rows.length+' períodos');
    }
    function portfolioNarrative() {
      const ctx = filteredContext();
      const qRows = projectQualityRows();
      const p = selectedProject();
      const avg = qRows.length ? qRows.reduce((a,r)=>a+r.Índice,0)/qRows.length : 0;
      const strong = qRows.filter(r => r.Índice >= 78).length;
      const weak = qRows.filter(r => r.Índice < 58).length;
      const annual = annualRows();
      const base = annual.reduce((a,r)=>a+Number(r.Base_val||0),0);
      const benefit = annual.reduce((a,r)=>a+Number(r.Beneficio_val||0),0);
      const projectsCount = annual.reduce((a,r)=>a+Number(r.Projetos||0),0);
      const losing = annual.filter(r => r.Tendência === 'perdeu força').map(r => r.Ano);
      const top = qRows[0];
      const low = qRows[qRows.length - 1];
      return [
        { title:'Leitura executiva', text:'No recorte selecionado' + (p ? ' para o projeto ' + p.title : '') + ', a base PD&I soma ' + money(base) + ', com benefício estimado de ' + money(benefit) + ' e ' + num(projectsCount || filteredProjects().length) + ' projeto(s)/ocorrência(s) analisados no período.' },
        { title:'Qualidade técnica', text:'O recorte atual tem índice médio de qualidade de ' + num(avg) + '/100, com ' + strong + ' projeto(s) forte(s) e ' + weak + ' projeto(s) que exigem reforço documental ou técnico.' },
        { title:'Força dos projetos', text: top ? 'Projeto mais forte: ' + top.Projeto + ' (' + num(top.Índice) + '/100). Projeto em maior atenção: ' + low.Projeto + ' (' + num(low.Índice) + '/100). A recomendação é usar essa leitura para priorizar revisões mensais e memoriais técnicos.' : 'Sem projetos suficientes no recorte para ranquear força técnica.' },
        { title:'Tração histórica', text: losing.length ? 'O programa perdeu força em ' + losing.join(', ') + ', indicando necessidade de recuperar evidências, resultados e vínculo financeiro.' : 'Não identifiquei perda relevante de força no recorte anual; a oportunidade é estruturar governança para manter consistência.' },
        { title:'Potencial comercial', text:'As lacunas encontradas não devem aparecer só como risco: elas podem ser convertidas em escopo de suporte, revisão de projetos, treinamento de timesheet, conciliação de despesas e preparação preventiva para fiscalização.' }
      ];
    }
    function scopeSummary() {
      const p = selectedProject();
      const parts = [
        'Empresa: ' + (DATA().company || 'Não informada'),
        'Ano: ' + (state.year === 'all' ? 'Todos' : state.year),
        'Projeto: ' + (p ? short(p.title, 90) : 'Todos'),
        'Despesa: ' + (state.expense === 'all' ? 'Todas' : state.expense)
      ];
      if (state.q) parts.push('Busca: ' + short(state.q, 80));
      return '<div class="scope-strip">' + parts.map(item => '<span>'+esc(item)+'</span>').join('') + '</div>';
    }
    function strengths() {
      const m = DATA().metrics || {};
      const ctx = filteredContext();
      const out = [];
      if (Number(m.base_total||0)>0) out.push('Base econômica de PD&I quantificada e pronta para narrativa executiva.');
      if (filteredProjects().some(p => boolCell(p.row, ['Incentivado?']))) out.push('Carteira filtrada com projetos incentivados identificados.');
      if (ctx.accepted.length) out.push('Timesheet técnico filtrado com horas elegíveis para sustentar execução.');
      if (ctx.histYears.length || ctx.histProjects.length) out.push('Memória histórica filtrada disponível para demonstrar evolução e continuidade.');
      return out.length ? out : ['Há dados carregados para iniciar estruturação do programa de PD&I.'];
    }
    function improvements() {
      const m = DATA().metrics || {};
      const ctx = filteredContext();
      const out = [];
      if (!ctx.accepted.length) out.push('Padronizar timesheet técnico com atividade, etapa, evidência e critério de incentivo para o recorte filtrado.');
      if (!ctx.inv.length) out.push('Reconciliar investimentos por projeto, natureza, fornecedor e justificativa técnica.');
      if (!ctx.histProjects.length) out.push('Criar memória anual de projetos com objetivo, incerteza, testes, resultados e valores.');
      out.push('Usar rotina mensal de revisão para reduzir risco de glosa e vender suporte técnico recorrente.');
      return out;
    }
    function agentAssessment() {
      const p = activeProject();
      const q = projectQuality(p);
      const annual = annualRows();
      const base = annual.reduce((a,r)=>a+Number(r.Base_val||0),0);
      const benefit = annual.reduce((a,r)=>a+Number(r.Beneficio_val||0),0);
      const expenses = annualExpenseItems(annual).filter(item => item.value > 0).map(item => item.name + ': ' + money(item.value)).join('; ') || 'sem valores positivos no recorte';
      const status = q.status;
      return '<div class="panel"><div class="panel-head"><h2>Agente de avaliação PD&I</h2><span class="pill '+(status.includes('ressalvas')?'warn':status.includes('Precisa')?'bad':'ok')+'">'+esc(status)+'</span></div>' +
        '<ul class="list"><li><b>Escopo:</b> '+esc(DATA().company || '')+' · '+esc(state.year === 'all' ? 'todos os anos' : state.year)+' · '+esc(selectedProject()?.title || 'todos os projetos')+'</li><li><b>Índice técnico:</b> '+num(q.score)+'/100, risco '+esc(q.risk)+'.</li><li><b>Tese técnica:</b> '+esc(short(q.desc || q.element || 'Sem tese técnica suficiente na base filtrada.', 380))+'</li><li><b>Incerteza/barreira:</b> '+esc(short(q.barrier || 'Não localizada de forma explícita.', 300))+'</li><li><b>Valores do recorte:</b> base '+money(base)+', benefício '+money(benefit)+'. Composição: '+esc(expenses)+'.</li><li><b>Execução analítica:</b> '+num(sum(q.accepted, ['Horas decimais','Horas']))+' horas aceitas em '+num(q.accepted.length)+' linhas.</li><li><b>Histórico:</b> '+num(q.hist.length)+' narrativa(s) conectada(s).</li></ul></div>';
    }
    function table(title, data, cols) {
      const isZeroLike = value => {
        const text = String(value ?? '').trim().toLowerCase();
        if (!text || ['nan','undefined','null','-'].includes(text)) return true;
        const numeric = text.replace(/r[$]/g,'').replace(/%/g,'').replace(/\\s/g,'').replace(/[.]/g,'').replace(',','.');
        return /^-?0+([.]0+)?$/.test(numeric);
      };
      const hasMaterialText = row => ['Fornecedor','Natureza','Descrição','Projeto','Código','Evidência','Diagnóstico','Recomendação','Atividade','Fonte','Confiança','Nota','Item','Ano'].some(key => {
        const value = String(row[key] ?? '').trim();
        return value && !isZeroLike(value);
      });
      const hasPositiveNumber = row => cols.some(c => {
        const value = String(row[c] ?? '').replace(/R[$]/g,'').replace(/%/g,'').trim();
        const normalized = value.includes(',') ? value.replace(/[.]/g,'').replace(',','.') : value;
        const number = Number(normalized);
        return Number.isFinite(number) && Math.abs(number) > 0;
      });
      const visible = (data || []).filter(row => (hasMaterialText(row) || hasPositiveNumber(row)) && cols.some(c => {
        const value = String(row[c] ?? '').trim();
        return value && !['nan','undefined','null'].includes(value.toLowerCase());
      }));
      if (!visible.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem linhas relevantes para exibir no recorte atual.</p></div>';
      const body = visible.slice(0,500).map(row => '<tr>'+cols.map(c => '<td>'+esc(row[c] ?? '')+'</td>').join('')+'</tr>').join('');
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+num(visible.length)+' linhas</span></div><div class="table-wrap"><table><thead><tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr></thead><tbody>'+body+'</tbody></table></div></div>';
    }
    function summary() {
      const m = DATA().metrics || {};
      const ctx = filteredContext();
      const annual = annualRows();
      const annualBase = annual.reduce((a,row)=>a+Number(row.Base_val||0),0);
      const annualBenefit = annual.reduce((a,row)=>a+Number(row.Beneficio_val||0),0);
      const annualInvest = annual.reduce((a,row)=>a+Number(row.Investimentos_val||0),0);
      const annualRh = annual.reduce((a,row)=>a+Number(row.RH_val||0),0);
      const base = annualBase || (state.year === 'all' ? (m.base_total || (m.people_pdi_total||0)+(m.investment_incentivized||0)) : (sum(ctx.people, ['Total PD&I','Total PDI']) + sum(ctx.inv, ['Valor Incentivado','Valor'])));
      const financialSeries = [
        { key:'Base_val', label:'Base PD&I', className:'base', color:'var(--teal)' },
        { key:'RH_val', label:'RH', className:'rh', color:'var(--blue)' },
        { key:'Servicos_val', label:'Serviços/terceiros', className:'servicos', color:'var(--amber)' },
        { key:'Beneficio_val', label:'Benefício', className:'beneficio', color:'var(--green)' }
      ];
      const expenseParts = [
        { name:'RH', value:annual.reduce((a,r)=>a+Number(r.RH_val||0),0), color:'var(--blue)' },
        { name:'Materiais', value:annual.reduce((a,r)=>a+Number(r.Material_val||0),0), color:'var(--teal)' },
        { name:'Serviços/terceiros', value:annual.reduce((a,r)=>a+Number(r.Servicos_val||0),0), color:'var(--amber)' }
      ];
      const narrative = portfolioNarrative();
      return '<section id="resumo" class="view">' +
        '<div class="report-hero"><div class="eyebrow">'+esc(DATA().company || '')+' · '+(state.year === 'all' ? 'Todos os anos' : esc(state.year))+'</div><h2>Relatório de PD&I para renovação e suporte</h2><p>Visão executiva com os filtros aplicados em todas as seções: projeto, ano, despesa e busca textual alimentam o mesmo recorte de dados.</p>'+scopeSummary()+'</div>' +
        '<div class="grid-3">' +
        kpi('Base PD&I', money(base), 'Recorte filtrado') +
        kpi('Economia estimada', money(annualBenefit || (state.year === 'all' ? (m.estimated_savings || 0) : ctx.histYears.reduce((a,row)=>a+Number(row.estimated_savings||0),0))), 'Lei do Bem') +
        kpi('Anos no recorte', num(annual.length), 'Memória filtrada') +
        kpi('Projetos filtrados', num(filteredProjects().length), 'Seleção atual') +
        kpi('Investimentos', money(annualInvest || sum(ctx.inv, ['Valor Incentivado','Valor'])), state.expense === 'all' ? 'Todas as despesas' : state.expense) +
        kpi('RH filtrado', money(annualRh || sum(ctx.people, ['Total PD&I','Total PDI'])), 'Projeto/ano atual') +
      '</div><div class="grid-2" style="margin-top:14px">' +
        '<div class="panel insight"><div class="panel-head"><h2>Resumo consultivo da IA</h2><span class="pill">recorte atual</span></div>' + narrative.map(item => '<div class="insight-card"><strong>'+esc(item.title)+'</strong><p>'+esc(item.text)+'</p></div>').join('') + '</div>' +
        multiLineChart('Evolução financeira anual', annual, financialSeries) +
        stackedBarChart('Composição anual dos dispêndios', annual) +
        compositionDonut('Composição acumulada dos dispêndios', expenseParts) +
        chart('Quantidade de projetos por ano', annual.map(r => ({ name:String(r.Ano), value:r.Projetos })), 'number', 'blue') +
        table('Principais itens que explicam o valor', topSpendRows(), ['Ano','Item','Valor','Origem']) +
        methodPanel() +
        donutChart('Distribuição de qualidade', projectQualityRows()) +
        chart('Força técnica dos projetos', projectQualityRows().slice(0,8).map(r => ({ name:r.Projeto, value:r.Índice })), 'number', 'blue') +
      '</div></section>';
    }
    function leiDoBem() {
      const m = DATA().metrics || {};
      return '<section id="lei" class="view"><div class="section-title"><div><h2>Lei do Bem</h2><p>Leitura fiscal e técnica do recorte selecionado.</p></div><span class="pill">Governança fiscal</span></div><div class="grid-2"><div class="panel"><div class="panel-head"><h2>Resumo fiscal</h2></div><ul class="list"><li>Base PD&I conciliada: <b>'+money(m.base_total || 0)+'</b></li><li>Exclusão adicional: <b>'+money(m.exclusion_total || 0)+'</b></li><li>Economia fiscal: <b>'+money(m.estimated_savings || 0)+'</b></li><li>Risco central: manter vínculo entre incerteza tecnológica, execução e valor.</li></ul></div>'+agentAssessment()+quarterlyPanel()+methodPanel()+'</div></section>';
    }
    function tecnoparque() {
      return '<section id="tecnoparque" class="view"><div class="section-title"><div><h2>Tecnoparque</h2><p>Oportunidades comerciais e de melhoria do programa.</p></div><span class="pill warn">Suporte recorrente</span></div><div class="panel"><p>Área para consolidar oportunidades de parceria, infraestrutura, ecossistema de inovação, ICTs, laboratórios, projetos de continuidade e suporte técnico recorrente.</p><ul class="list"><li>Mapear projetos com potencial de laboratório, validação, prototipagem ou ensaio.</li><li>Relacionar maturidade técnica com necessidade de suporte mensal.</li><li>Transformar lacunas documentais em plano de horas e renovação contratual.</li></ul></div></section>';
    }
    function analytics() {
      const ctx = filteredContext();
      const quality = projectQualityRows();
      const annual = annualRows();
      const activityItems = group(ctx.work, ['Atividade realizada','Atividade'], ['Horas decimais','Horas'], 10);
      const expenseItems = group(ctx.inv, ['Natureza','Tipo de despesa'], ['Valor Incentivado','Valor'], 10);
      const financialSeries = [
        { key:'Base_val', label:'Base PD&I', className:'base', color:'var(--teal)' },
        { key:'RH_val', label:'RH', className:'rh', color:'var(--blue)' },
        { key:'Servicos_val', label:'Serviços/terceiros', className:'servicos', color:'var(--amber)' },
        { key:'Beneficio_val', label:'Benefício', className:'beneficio', color:'var(--green)' }
      ];
      return '<section id="analiticos" class="view"><div class="section-title"><div><h2>Dados analíticos</h2><p>Tabelas, gráficos e estatísticas abaixo usam exatamente os filtros do topo.</p></div><span class="pill">'+num(ctx.work.length + ctx.inv.length + ctx.people.length)+' registros</span></div><div class="grid-4">' +
        '<div class="score-card"><span>Índice médio dos projetos</span><b>'+num(quality.length ? quality.reduce((a,r)=>a+r.Índice,0)/quality.length : 0)+'</b></div>' +
        '<div class="score-card"><span>Projetos fortes</span><b>'+num(quality.filter(r=>r.Índice>=78).length)+'</b></div>' +
        '<div class="score-card"><span>Projetos em atenção</span><b>'+num(quality.filter(r=>r.Índice<58).length)+'</b></div>' +
        '<div class="score-card"><span>Horas aceitas</span><b>'+num(sum(ctx.accepted, ['Horas decimais','Horas']))+'</b></div>' +
      '</div><div class="section-body grid-2" style="margin-top:14px">' +
        multiLineChart('Base, RH, serviços e benefício por ano', annual, financialSeries) +
        stackedBarChart('RH, materiais e serviços por ano', annual) +
        chart('Benefício fiscal por ano', annual.map(r => ({ name:String(r.Ano), value:r.Beneficio_val })), 'money', 'blue') +
        chart('Serviços/terceiros por ano', annual.map(r => ({ name:String(r.Ano), value:r.Servicos_val })), 'money', 'amber') +
        quarterlyPanel() +
        table('Top fornecedores/projetos por valor', topSpendRows(), ['Ano','Item','Valor','Origem']) +
        donutChart('Qualidade da carteira filtrada', quality) +
        chart(activityItems.length ? 'Atividades por horas' : 'Atividades/projetos históricos do ano', activityItems.length ? activityItems : annualActivityItems(annual), 'number', 'blue') +
        chart(expenseItems.length ? 'Despesas por natureza' : 'Composição financeira do ano', expenseItems.length ? expenseItems : annualExpenseItems(annual), 'money', 'amber') +
        table('Ranking técnico dos projetos', quality.map(r => ({ Projeto:r.Projeto, Índice:num(r.Índice), Diagnóstico:r.Diagnóstico, Risco:r.Risco, Evidência:short(r.Evidência, 260) })), ['Projeto','Índice','Diagnóstico','Risco','Evidência']) +
        table('Projetos filtrados', filteredProjects().map(p => ({ Projeto:p.title, Código:p.code, Origem:p.source, Ano:p.year || '', Status: boolCell(p.row,['Incentivado?']) ? 'Incentivado' : 'Revisar', Descrição: short(cell(p.row,['Descrição']), 220) })), ['Projeto','Código','Origem','Ano','Status','Descrição']) +
        table('Investimentos filtrados', ctx.inv.map(row => ({ Fornecedor:cell(row,['Fornecedor']), Natureza:cell(row,['Natureza']), Valor:money(numCell(row,['Valor Incentivado','Valor'])), Valor_num:numCell(row,['Valor Incentivado','Valor']), Descrição:short(cell(row,['Descrição','Objetivo do gasto']), 180) })).filter(row => row.Valor_num > 0 || row.Fornecedor || row.Natureza || row.Descrição).map(row => ({ Fornecedor:row.Fornecedor, Natureza:row.Natureza, Valor:row.Valor, Descrição:row.Descrição })), ['Fornecedor','Natureza','Valor','Descrição']) +
      '</div></section>';
    }
    function evaluation() {
      const narrative = portfolioNarrative();
      return '<section id="avaliacao" class="view"><div class="section-title"><div><h2>Nossa avaliação do programa</h2><p>Diagnóstico comercial e técnico para renovar contrato e orientar suporte.</p></div></div><div class="panel insight" style="margin-bottom:14px"><div class="panel-head"><h2>Parecer da IA sobre o programa</h2><span class="pill">consultivo</span></div>' + narrative.map(item => '<div class="insight-card"><strong>'+esc(item.title)+'</strong><p>'+esc(item.text)+'</p></div>').join('') + '</div><div class="grid-2">' +
        '<div class="panel"><div class="panel-head"><h2>Pontos fortes</h2></div><ul class="list">'+strengths().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
        '<div class="panel"><div class="panel-head"><h2>Melhorias recomendadas</h2></div><ul class="list">'+improvements().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
      '</div></section>';
    }
    function indexSection() {
      const rows = annualRows();
      const current = rows.length ? rows : [{ Ano:DATA().year || 'Atual', Índice:programScoreForYear({base_total:DATA().metrics?.base_total, estimated_savings:DATA().metrics?.estimated_savings}), Tendência:'base', Variação:'base', Diagnóstico:'Ano corrente', Base:money(DATA().metrics?.base_total || 0), Base_val:Number(DATA().metrics?.base_total||0), RH:money(DATA().metrics?.people_pdi_total || 0), RH_val:Number(DATA().metrics?.people_pdi_total||0), Materiais:money(DATA().metrics?.investment_incentivized || 0), Material_val:Number(DATA().metrics?.investment_incentivized||0), 'Serviços/terceiros':money(0), Servicos_val:0, Investimentos:money(DATA().metrics?.investment_incentivized || 0), Investimentos_val:Number(DATA().metrics?.investment_incentivized||0), Benefício:money(DATA().metrics?.estimated_savings || 0), Beneficio_val:Number(DATA().metrics?.estimated_savings||0), Projetos:filteredProjects().length, Incentivados:filteredProjects().filter(p=>boolCell(p.row,['Incentivado?'])).length, Recomendação:'Consolidar governança' }];
      const financialSeries = [
        { key:'Base_val', label:'Base PD&I', className:'base', color:'var(--teal)' },
        { key:'RH_val', label:'RH', className:'rh', color:'var(--blue)' },
        { key:'Servicos_val', label:'Serviços/terceiros', className:'servicos', color:'var(--amber)' },
        { key:'Beneficio_val', label:'Benefício', className:'beneficio', color:'var(--green)' }
      ];
      const expenseParts = [
        { name:'RH', value:current.reduce((a,r)=>a+Number(r.RH_val||0),0), color:'var(--blue)' },
        { name:'Materiais', value:current.reduce((a,r)=>a+Number(r.Material_val||0),0), color:'var(--teal)' },
        { name:'Serviços/terceiros', value:current.reduce((a,r)=>a+Number(r.Servicos_val||0),0), color:'var(--amber)' }
      ];
      return '<section id="indice" class="view"><div class="section-title"><div><h2>Evolução anual, valores e índice PD&I</h2><p>O índice é um diagnóstico técnico; os gráficos abaixo mostram os valores reais de RH, serviços, materiais, base, benefício e quantidade de projetos.</p></div></div><div class="section-body grid-2">' +
        multiLineChart('Evolução dos valores anuais', current, financialSeries) +
        stackedBarChart('Composição anual dos dispêndios', current) +
        compositionDonut('Composição acumulada dos dispêndios', expenseParts) +
        chart('Projetos por ano', current.map(r => ({ name:String(r.Ano), value:r.Projetos })), 'number', 'blue') +
        chart('Projetos incentivados por ano', current.map(r => ({ name:String(r.Ano), value:r.Incentivados })), 'number') +
        lineChart('Índice de maturidade PD&I', current) +
        table('Valores, benefício e recomendação anual', current, ['Ano','Projetos','Incentivados','Base','RH','Materiais','Serviços/terceiros','Investimentos','Benefício','Índice','Tendência','Variação','Diagnóstico','Recomendação']) +
      '</div></section>';
    }
    function agentDossier() {
      const annual = annualRows();
      const qRows = projectQualityRows();
      const avg = qRows.length ? qRows.reduce((a,r)=>a+r.Índice,0)/qRows.length : 0;
      const base = annual.reduce((a,r)=>a+Number(r.Base_val||0),0);
      const benefit = annual.reduce((a,r)=>a+Number(r.Beneficio_val||0),0);
      const p = selectedProject();
      return '<div class="panel"><div class="panel-head"><h2>Dossiê do recorte</h2><span class="pill">'+num(annual.length)+' ano(s)</span></div><div class="mini-grid">' +
        '<div class="mini-value"><span>Empresa</span><b>'+esc(DATA().company || '')+'</b></div>' +
        '<div class="mini-value"><span>Ano</span><b>'+esc(state.year === 'all' ? 'Todos' : state.year)+'</b></div>' +
        '<div class="mini-value"><span>Projeto</span><b>'+esc(p ? short(p.title, 42) : 'Todos')+'</b></div>' +
        '<div class="mini-value"><span>Base PD&I</span><b>'+money(base)+'</b></div>' +
        '<div class="mini-value"><span>Benefício</span><b>'+money(benefit)+'</b></div>' +
        '<div class="mini-value"><span>Índice médio</span><b>'+num(avg)+'/100</b></div>' +
      '</div><div class="actions" style="margin-top:12px"><button type="button" onclick="quickAsk(\\'Por que é incentivado?\\')">Por que é incentivado?</button><button type="button" onclick="quickAsk(\\'Quais riscos e faltas do ano?\\')">Riscos do ano</button><button type="button" onclick="quickAsk(\\'Explique os valores usados\\')">Valores usados</button><button type="button" onclick="quickAsk(\\'O projeto perdeu força?\\')">Maturidade</button></div></div>';
    }
    function agents() {
      const endpoint = PORTAL.support_endpoint ? 'Envio automático configurado' : 'Endpoint de envio não configurado';
      return '<section id="agentes" class="view"><div class="section-title"><div><h2>Agentes e suporte</h2><p>Agente local limitado ao recorte filtrado e canal humano para abrir demanda.</p></div></div><div class="grid-2">'+agentDossier()+'<div class="panel"><div class="panel-head"><h2>Falar com especialista</h2><span class="pill '+(PORTAL.support_endpoint?'ok':'warn')+'">'+endpoint+'</span></div><form onsubmit="openTicket(event)"><input id="ticketSubject" placeholder="Assunto da ordem de serviço"><textarea id="ticketBody" placeholder="Descreva a dúvida, projeto, ano e urgência"></textarea><div class="actions"><button class="primary">Enviar solicitação</button></div><p id="ticketStatus" class="toc-note">Para envio sem abrir e-mail, configure um endpoint interno que encaminhe para inovacao@taticcaconsulting.com.</p></form></div></div><div class="panel" style="margin-top:14px"><div class="panel-head"><h2>Chatbot técnico de projetos</h2><span class="pill">Escopo filtrado</span></div><div class="messages" id="botMessages"></div><form class="chat-form" onsubmit="askBot(event)"><input id="botInput" placeholder="Pergunte sobre projetos, anos, descrição, valores, riscos ou maturidade"><button class="primary">Enviar</button></form></div></section>';
    }
    function downloads() {
      const sheets = PORTAL.sheets_url ? '<a class="button" target="_blank" rel="noopener" href="'+esc(PORTAL.sheets_url)+'">Abrir Google Sheets</a>' : '<span class="pill warn">Google Sheets restrito: informar URL no gerador</span>';
      return '<section id="downloads" class="view"><div class="panel"><div class="panel-head"><h2>Downloads e congelamento</h2></div><div class="actions"><button onclick="window.print()">Baixar PDF / imprimir</button><button onclick="downloadFrozenHtml()">Baixar HTML congelado</button>'+sheets+'</div><p class="toc-note">O HTML congelado baixa uma cópia com os dados embutidos neste momento, útil para evidência de versão.</p></div></section>';
    }
    function renderControls() {
      if (!COMPANIES[state.company]) state.company = 0;
      $('companySelect').innerHTML = COMPANIES.map((c,i)=>'<option value="'+i+'">'+esc(c.company)+'</option>').join('');
      $('companySelect').value = String(state.company);
      const ys = years();
      if (state.year !== 'all' && !ys.includes(String(state.year))) state.year = 'all';
      $('yearSelect').innerHTML = '<option value="all">Todos os anos</option>' + ys.map(y=>'<option value="'+esc(y)+'">'+esc(y)+'</option>').join('');
      $('yearSelect').value = state.year;
      const ps = availableProjectsForControl();
      $('projectSelect').innerHTML = '<option value="all">Todos os projetos</option>' + ps.map(p=>'<option value="'+esc(p.id)+'">'+esc((p.code || 'Projeto')+' · '+short(p.title,80))+'</option>').join('');
      $('projectSelect').value = ps.some(p=>p.id===state.project) ? state.project : 'all';
      state.project = $('projectSelect').value;
      $('expenseSelect').innerHTML = expenses().map(v=>'<option value="'+esc(v)+'">'+esc(v === 'all' ? 'Todas as despesas' : v)+'</option>').join('');
      $('expenseSelect').value = expenses().includes(state.expense) ? state.expense : 'all';
      state.expense = $('expenseSelect').value;
      $('searchInput').value = state.q;
    }
    function render() {
      chartSeq = 0;
      chartConfigs = {};
      renderControls();
      $('app').innerHTML = summary() + leiDoBem() + tecnoparque() + analytics() + evaluation() + indexSection() + agents() + downloads();
      activateView();
      renderBot();
      requestAnimationFrame(renderChartCanvases);
    }
    function setCompany(value) {
      const next = Number(value || 0);
      state.company = COMPANIES[next] ? next : 0;
      state.year='all';
      state.project='all';
      state.expense='all';
      state.q='';
      render();
    }
    function setFilter(key, value) {
      state[key] = key === 'q' ? (value || '') : (value || 'all');
      if (key === 'year') state.project = 'all';
      render();
    }
    function setView(view) { state.view = view || 'resumo'; activateView(); }
    function activateView() {
      document.querySelectorAll('.view').forEach(el => el.classList.toggle('active', el.id === state.view));
      document.querySelectorAll('nav button').forEach(btn => btn.classList.toggle('active', btn.dataset.view === state.view));
      requestAnimationFrame(renderChartCanvases);
    }
    function clearFilters() { state.year='all'; state.project='all'; state.expense='all'; state.q=''; render(); }
    function recorteFacts() {
      const p = selectedProject();
      const annual = annualRows();
      const qRows = projectQualityRows();
      const quality = p ? projectQuality(p) : null;
      const base = annual.reduce((a,r)=>a+Number(r.Base_val||0),0);
      const rh = annual.reduce((a,r)=>a+Number(r.RH_val||0),0);
      const material = annual.reduce((a,r)=>a+Number(r.Material_val||0),0);
      const servicos = annual.reduce((a,r)=>a+Number(r.Servicos_val||0),0);
      const beneficio = annual.reduce((a,r)=>a+Number(r.Beneficio_val||0),0);
      const projetos = annual.reduce((a,r)=>a+Number(r.Projetos||0),0) || filteredProjects().length;
      const incentivados = annual.reduce((a,r)=>a+Number(r.Incentivados||0),0);
      const avg = qRows.length ? qRows.reduce((a,r)=>a+r.Índice,0)/qRows.length : 0;
      return { p, annual, qRows, quality, base, rh, material, servicos, beneficio, projetos, incentivados, avg };
    }
    function formatAgentAnswer(title, lines) {
      return '<b>'+esc(title)+'</b>\\n' + lines.map(line => '• ' + esc(line)).join('\\n');
    }
    function botAnswer(q) {
      const facts = recorteFacts();
      const p = facts.p || activeProject();
      const ql = facts.quality || projectQuality(p);
      const question = norm(q);
      const scope = (DATA().company || '') + ' · ' + (state.year === 'all' ? 'todos os anos' : state.year) + ' · ' + (facts.p ? facts.p.title : 'todos os projetos');
      if (question.includes('valor') || question.includes('despesa') || question.includes('usado') || question.includes('base')) {
        return formatAgentAnswer('Valores do recorte', [
          'Escopo: ' + scope,
          'Base PD&I: ' + money(facts.base) + '; RH: ' + money(facts.rh) + '; materiais: ' + money(facts.material) + '; serviços/terceiros: ' + money(facts.servicos) + '.',
          'Benefício estimado: ' + money(facts.beneficio) + '.',
          'Quando o ano é histórico e não há tabela analítica aberta, uso os agregados anuais importados da memória histórica.'
        ]);
      }
      if (question.includes('incent') || question.includes('porque') || question.includes('por que')) {
        return formatAgentAnswer('Critério técnico de incentivo', [
          'Escopo: ' + scope,
          'O projeto tende a ser defendável quando há incerteza tecnológica, elemento inovador, atividades técnicas e vínculo financeiro rastreável.',
          'Neste recorte: elemento inovador ' + (ql.element ? 'localizado' : 'não localizado de forma explícita') + '; barreira tecnológica ' + (ql.barrier ? 'localizada' : 'não localizada de forma explícita') + '; execução aceita em ' + num(ql.accepted.length) + ' linha(s).',
          'Índice técnico: ' + num(ql.score) + '/100 (' + ql.status + ', risco ' + ql.risk + ').'
        ]);
      }
      if (question.includes('risco') || question.includes('falta') || question.includes('melhoria')) {
        return formatAgentAnswer('Riscos e faltas do recorte', [
          'Risco técnico atual: ' + ql.risk + '.',
          ql.barrier ? 'A barreira tecnológica foi localizada: ' + short(ql.barrier, 220) : 'Falta explicitar barreira/incerteza tecnológica com linguagem defensável.',
          ql.element ? 'O elemento inovador foi localizado: ' + short(ql.element, 220) : 'Falta explicitar o elemento novo/inovador frente ao estado da técnica.',
          facts.servicos || facts.material || facts.rh ? 'Há valores vinculados ao recorte; a prioridade é amarrar despesa, atividade e evidência.' : 'Não localizei valores positivos no recorte filtrado.'
        ]);
      }
      if (question.includes('ano') || question.includes('hist') || question.includes('forca') || question.includes('força') || question.includes('matur')) {
        const years = facts.annual.map(row => row.Ano + ': base ' + money(row.Base_val) + ', benefício ' + money(row.Beneficio_val) + ', índice ' + num(row.Índice)).join('; ');
        return formatAgentAnswer('Maturidade e evolução', [
          'Escopo: ' + scope,
          years || 'Sem série anual positiva para o recorte.',
          'Projetos/ocorrências no período: ' + num(facts.projetos) + '; incentivados/positivos: ' + num(facts.incentivados) + '.',
          'Histórico textual conectado: ' + (ql.hist.slice(0,4).map(item => (item.year||'') + ' ' + short(item.name||item.summary,90)).join('; ') || 'não localizado para o projeto selecionado')
        ]);
      }
      return formatAgentAnswer('Resposta técnica do agente', [
        'Escopo: ' + scope,
        'Base PD&I: ' + money(facts.base) + '; benefício estimado: ' + money(facts.beneficio) + '; índice médio da carteira: ' + num(facts.avg) + '/100.',
        'Projeto de referência: ' + (p?.title || 'carteira completa') + '.',
        'Descrição/tese disponível: ' + short(ql.desc || ql.element || cell(p?.row || {}, ['Descrição']) || 'não localizada na base filtrada', 320)
      ]);
    }
    function renderBot() {
      const box = $('botMessages');
      if (!box) return;
      const key = DATA().company + '|' + state.project;
      chats[key] = chats[key] || [{ role:'bot', text:'Pergunte sobre o projeto selecionado. Meu escopo está limitado à descrição, histórico e valores carregados neste relatório.' }];
      box.innerHTML = chats[key].map(m => '<div class="msg '+m.role+'">'+m.text+'</div>').join('');
      box.scrollTop = box.scrollHeight;
    }
    function askBot(ev) {
      ev.preventDefault();
      const input = $('botInput');
      const q = (input.value || '').trim();
      if (!q) return;
      const key = DATA().company + '|' + state.project;
      chats[key] = chats[key] || [];
      chats[key].push({ role:'user', text:esc(q) });
      chats[key].push({ role:'bot', text:botAnswer(q) });
      input.value = '';
      renderBot();
    }
    function quickAsk(text) {
      const input = $('botInput');
      if (input) input.value = text;
      askBot({ preventDefault(){} });
    }
    async function openTicket(ev) {
      ev.preventDefault();
      const status = $('ticketStatus');
      const payload = {
        to:'inovacao@taticcaconsulting.com',
        subject:$('ticketSubject').value || 'Ordem de serviço PD&I',
        message:$('ticketBody').value || '',
        company:DATA().company,
        project:activeProject()?.title || 'Todos',
        year:state.year,
        expense:state.expense,
        page:location.href
      };
      if (!PORTAL.support_endpoint) {
        status.textContent = 'Envio direto exige um endpoint interno/API. Configure support_endpoint no gerador para enviar automaticamente para inovacao@taticcaconsulting.com.';
        status.className = 'toc-note bad';
        return;
      }
      status.textContent = 'Enviando solicitação...';
      try {
        const res = await fetch(PORTAL.support_endpoint, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        status.textContent = 'Solicitação enviada para inovacao@taticcaconsulting.com.';
        status.className = 'toc-note ok';
        $('ticketSubject').value = '';
        $('ticketBody').value = '';
      } catch (err) {
        status.textContent = 'Não foi possível enviar automaticamente. Verifique o endpoint interno de suporte.';
        status.className = 'toc-note bad';
      }
    }
    function downloadFrozenHtml() {
      const blob = new Blob([document.documentElement.outerHTML], { type:'text/html;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'relatorio-pdi-congelado-' + norm(DATA().company || 'cliente').replace(/[^a-z0-9]+/g,'-') + '.html';
      a.click();
      URL.revokeObjectURL(a.href);
    }
    window.setCompany=setCompany; window.setFilter=setFilter; window.setView=setView; window.clearFilters=clearFilters; window.askBot=askBot; window.quickAsk=quickAsk; window.openTicket=openTicket; window.downloadFrozenHtml=downloadFrozenHtml;
    render();
  </script>
</body>
</html>"""
    return html.replace("__TITLE__", escape(title)).replace("__PAYLOAD__", payload)
