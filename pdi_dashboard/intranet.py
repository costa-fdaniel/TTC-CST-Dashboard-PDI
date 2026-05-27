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
    nav a { color:var(--ink); text-decoration:none; padding:10px 11px; border:1px solid var(--line); border-radius:8px; background:#f9fbfa; font-weight:800; transition:.15s ease; }
    nav a:hover { border-color:rgba(15,118,110,.45); transform:translateX(2px); }
    select, input, textarea, button { font:inherit; }
    select, input, textarea { width:100%; border:1px solid var(--line); border-radius:8px; padding:10px 11px; background:white; color:var(--ink); }
    textarea { min-height:96px; resize:vertical; }
    button, .button { border:1px solid var(--line); border-radius:8px; padding:10px 12px; background:white; color:var(--ink); font-weight:850; cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; justify-content:center; }
    button.primary, .button.primary { background:var(--teal); border-color:var(--teal); color:white; }
    .filters {
      position:sticky; top:0; z-index:5; display:grid; grid-template-columns:1.2fr 1fr 1fr 1.2fr;
      gap:10px; margin:0 0 18px; padding:12px; border:1px solid var(--line); border-radius:10px;
      background:rgba(255,255,255,.96); box-shadow:var(--shadow);
    }
    .filters label { display:grid; gap:5px; color:var(--muted); font-size:11px; font-weight:850; text-transform:uppercase; }
    section { margin-bottom:22px; scroll-margin-top:84px; }
    .report-hero { background:linear-gradient(135deg,#fff 0%,#edf7f4 100%); border:1px solid var(--line); border-radius:14px; padding:20px; box-shadow:var(--shadow); margin-bottom:18px; }
    .report-hero .eyebrow { color:var(--muted); font-size:12px; font-weight:850; text-transform:uppercase; }
    .report-hero h2 { font-size:26px; margin:4px 0 8px; }
    .report-hero p { margin:0; color:var(--muted); max-width:980px; }
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
        <a href="#resumo">Resumo</a>
        <a href="#lei">Lei do Bem</a>
        <a href="#tecnoparque">Tecnoparque</a>
        <a href="#analiticos">Dados analíticos</a>
        <a href="#avaliacao">Avaliação PD&I</a>
        <a href="#indice">Índice ano a ano</a>
        <a href="#agentes">Agentes e suporte</a>
        <a href="#downloads">Downloads</a>
      </nav>
      <p class="toc-note">Header corporativo entra acima desta área na intranet.</p>
    </aside>
    <main>
      <div class="filters">
        <label>Ano<select id="yearSelect" onchange="setFilter('year', this.value)" aria-label="Ano"></select></label>
        <label>Projeto<select id="projectSelect" onchange="setFilter('project', this.value)" aria-label="Projeto"></select></label>
        <label>Despesa<select id="expenseSelect" onchange="setFilter('expense', this.value)" aria-label="Tipo de despesa"></select></label>
        <label>Busca<input id="searchInput" oninput="setFilter('q', this.value)" placeholder="Projeto, atividade, evidência ou fornecedor"></label>
      </div>
      <div id="app"></div>
    </main>
  </div>
  <script>
    const PORTAL = JSON.parse(document.getElementById('data').textContent);
    const COMPANIES = PORTAL.companies || [];
    const fmtMoney = new Intl.NumberFormat('pt-BR', { style:'currency', currency:'BRL' });
    const fmtNum = new Intl.NumberFormat('pt-BR', { maximumFractionDigits:2 });
    const state = { company:0, year:'all', project:'all', expense:'all', q:'' };
    const chats = {};
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
        return { id:'p'+i, title, code:projectCode(row), row, source:'Atual', year:DATA().year || '' };
      });
      const history = (DATA().history?.projects || []).map((item, i) => ({
        id:'h'+i,
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
    function chart(title, items, kind='number', tone='') {
      const clean = (items||[]).filter(item => Number(item.value||0)>0);
      if (!clean.length) return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2></div><p>Sem dados suficientes.</p></div>';
      const max = Math.max(...clean.map(i=>Number(i.value||0)),1);
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+clean.length+' itens</span></div>' + clean.map(item => {
        const value = kind === 'money' ? money(item.value) : num(item.value);
        return '<div class="bar"><label title="'+esc(item.name)+'">'+esc(item.name)+'</label><div class="track"><div class="fill '+tone+'" style="--w:'+Math.max(4, item.value/max*100)+'%"></div></div><b>'+value+'</b></div>';
      }).join('') + '</div>';
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
    function annualRows() {
      const source = filteredHistoryYears();
      const rows = source.length ? source : [{ year:DATA().year, base_total:DATA().metrics?.base_total, estimated_savings:DATA().metrics?.estimated_savings, rh_total:DATA().metrics?.people_pdi_total, material_total:DATA().metrics?.investment_incentivized }];
      return rows.map((row, idx) => {
        const score = programScoreForYear(row);
        const prev = idx ? programScoreForYear(rows[idx-1]) : null;
        const delta = prev == null ? 0 : score - prev;
        const trend = delta > 6 ? 'ganhou força' : delta < -6 ? 'perdeu força' : 'estável';
        const recommendation = score >= 82
          ? 'Manter governança e transformar maturidade em agenda de suporte, com revisão preventiva de evidências.'
          : score >= 65
            ? 'Reforçar rastreabilidade de testes, resultados e valores para reduzir risco em fiscalização.'
            : score >= 45
              ? 'Implantar plano de ação: timesheet técnico, memória por projeto, conciliação mensal e comitê de evidências.'
              : 'Priorizar reconstrução documental e revisão de elegibilidade antes de defender benefício fiscal.';
        return { Ano:row.year || DATA().year || 'Atual', Índice:score, Tendência:trend, Variação:delta ? (delta > 0 ? '+' : '') + num(delta) : 'base', Diagnóstico:scoreBand(score), Base:money(row.base_total || 0), Economia:money(row.estimated_savings || 0), Recomendação:recommendation };
      });
    }
    function portfolioNarrative() {
      const ctx = filteredContext();
      const qRows = projectQualityRows();
      const avg = qRows.length ? qRows.reduce((a,r)=>a+r.Índice,0)/qRows.length : 0;
      const strong = qRows.filter(r => r.Índice >= 78).length;
      const weak = qRows.filter(r => r.Índice < 58).length;
      const annual = annualRows();
      const losing = annual.filter(r => r.Tendência === 'perdeu força').map(r => r.Ano);
      const top = qRows[0];
      const low = qRows[qRows.length - 1];
      return [
        { title:'Leitura executiva', text:'O recorte atual tem índice médio de qualidade de ' + num(avg) + '/100, com ' + strong + ' projeto(s) forte(s) e ' + weak + ' projeto(s) que exigem reforço documental ou técnico. Isso ajuda a separar o que já sustenta renovação do contrato do que vira plano de horas de suporte.' },
        { title:'Força dos projetos', text: top ? 'Projeto mais forte: ' + top.Projeto + ' (' + num(top.Índice) + '/100). Projeto em maior atenção: ' + low.Projeto + ' (' + num(low.Índice) + '/100). A recomendação é usar essa leitura para priorizar revisões mensais e memoriais técnicos.' : 'Sem projetos suficientes no recorte para ranquear força técnica.' },
        { title:'Tração histórica', text: losing.length ? 'O programa perdeu força em ' + losing.join(', ') + ', indicando necessidade de recuperar evidências, resultados e vínculo financeiro.' : 'Não identifiquei perda relevante de força no recorte anual; a oportunidade é estruturar governança para manter consistência.' },
        { title:'Potencial comercial', text:'As lacunas encontradas não devem aparecer só como risco: elas podem ser convertidas em escopo de suporte, revisão de projetos, treinamento de timesheet, conciliação de despesas e preparação preventiva para fiscalização.' }
      ];
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
      const status = q.status;
      return '<div class="panel"><div class="panel-head"><h2>Agente de avaliação PD&I</h2><span class="pill '+(status.includes('ressalvas')?'warn':status.includes('Precisa')?'bad':'ok')+'">'+esc(status)+'</span></div>' +
        '<ul class="list"><li><b>Projeto:</b> '+esc(p?.title || 'Carteira')+'</li><li><b>Índice técnico:</b> '+num(q.score)+'/100, risco '+esc(q.risk)+'.</li><li><b>Tese técnica:</b> '+esc(short(q.desc || q.element || 'Sem tese técnica suficiente na base filtrada.', 380))+'</li><li><b>Incerteza/barreira:</b> '+esc(short(q.barrier || 'Não localizada de forma explícita.', 300))+'</li><li><b>Execução:</b> '+num(sum(q.accepted, ['Horas decimais','Horas']))+' horas aceitas em '+num(q.accepted.length)+' linhas.</li><li><b>Valores:</b> '+money(sum(q.inv, ['Valor Incentivado','Valor']))+' em investimentos filtrados.</li><li><b>Histórico:</b> '+num(q.hist.length)+' narrativa(s) conectada(s).</li></ul></div>';
    }
    function table(title, data, cols) {
      const body = (data||[]).slice(0,500).map(row => '<tr>'+cols.map(c => '<td>'+esc(row[c] ?? '')+'</td>').join('')+'</tr>').join('');
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+num((data||[]).length)+' linhas</span></div><div class="table-wrap"><table><thead><tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr></thead><tbody>'+body+'</tbody></table></div></div>';
    }
    function summary() {
      const m = DATA().metrics || {};
      const ctx = filteredContext();
      const histBase = ctx.histYears.reduce((a,row)=>a+Number(row.base_total||0),0);
      const base = state.year === 'all' ? (m.base_total || (m.people_pdi_total||0)+(m.investment_incentivized||0)) : (histBase || sum(ctx.people, ['Total PD&I','Total PDI']) + sum(ctx.inv, ['Valor Incentivado','Valor']));
      const narrative = portfolioNarrative();
      return '<section id="resumo">' +
        '<div class="report-hero"><div class="eyebrow">'+esc(DATA().company || '')+' · '+(state.year === 'all' ? 'Todos os anos' : esc(state.year))+'</div><h2>Relatório de PD&I para renovação e suporte</h2><p>Visão executiva com os filtros aplicados em todas as seções: projeto, ano, despesa e busca textual alimentam o mesmo recorte de dados.</p></div>' +
        '<div class="grid-3">' +
        kpi('Base PD&I', money(base), 'Recorte filtrado') +
        kpi('Economia estimada', money(state.year === 'all' ? (m.estimated_savings || 0) : ctx.histYears.reduce((a,row)=>a+Number(row.estimated_savings||0),0)), 'Lei do Bem') +
        kpi('Anos no recorte', num(ctx.histYears.length || (state.year === 'all' ? (DATA().history?.years || []).length : 1)), 'Memória filtrada') +
        kpi('Projetos filtrados', num(filteredProjects().length), 'Seleção atual') +
        kpi('Investimentos', money(sum(ctx.inv, ['Valor Incentivado','Valor'])), state.expense === 'all' ? 'Todas as despesas' : state.expense) +
        kpi('RH filtrado', money(sum(ctx.people, ['Total PD&I','Total PDI'])), 'Projeto/ano atual') +
      '</div><div class="grid-2" style="margin-top:14px">' +
        '<div class="panel insight"><div class="panel-head"><h2>Resumo consultivo da IA</h2><span class="pill">recorte atual</span></div>' + narrative.map(item => '<div class="insight-card"><strong>'+esc(item.title)+'</strong><p>'+esc(item.text)+'</p></div>').join('') + '</div>' +
        chart('Força técnica dos projetos', projectQualityRows().slice(0,8).map(r => ({ name:r.Projeto, value:r.Índice })), 'number', 'blue') +
      '</div></section>';
    }
    function leiDoBem() {
      const m = DATA().metrics || {};
      return '<section id="lei"><div class="section-title"><div><h2>Lei do Bem</h2><p>Leitura fiscal e técnica do recorte selecionado.</p></div><span class="pill">Governança fiscal</span></div><div class="grid-2"><div class="panel"><div class="panel-head"><h2>Resumo fiscal</h2></div><ul class="list"><li>Base PD&I conciliada: <b>'+money(m.base_total || 0)+'</b></li><li>Exclusão adicional: <b>'+money(m.exclusion_total || 0)+'</b></li><li>Economia fiscal: <b>'+money(m.estimated_savings || 0)+'</b></li><li>Risco central: manter vínculo entre incerteza tecnológica, execução e valor.</li></ul></div>'+agentAssessment()+'</div></section>';
    }
    function tecnoparque() {
      return '<section id="tecnoparque"><div class="section-title"><div><h2>Tecnoparque</h2><p>Oportunidades comerciais e de melhoria do programa.</p></div><span class="pill warn">Suporte recorrente</span></div><div class="panel"><p>Área para consolidar oportunidades de parceria, infraestrutura, ecossistema de inovação, ICTs, laboratórios, projetos de continuidade e suporte técnico recorrente.</p><ul class="list"><li>Mapear projetos com potencial de laboratório, validação, prototipagem ou ensaio.</li><li>Relacionar maturidade técnica com necessidade de suporte mensal.</li><li>Transformar lacunas documentais em plano de horas e renovação contratual.</li></ul></div></section>';
    }
    function analytics() {
      const ctx = filteredContext();
      const quality = projectQualityRows();
      return '<section id="analiticos"><div class="section-title"><div><h2>Dados analíticos</h2><p>Tabelas, gráficos e estatísticas abaixo usam exatamente os filtros do topo.</p></div><span class="pill">'+num(ctx.work.length + ctx.inv.length + ctx.people.length)+' registros</span></div><div class="grid-4">' +
        '<div class="score-card"><span>Índice médio dos projetos</span><b>'+num(quality.length ? quality.reduce((a,r)=>a+r.Índice,0)/quality.length : 0)+'</b></div>' +
        '<div class="score-card"><span>Projetos fortes</span><b>'+num(quality.filter(r=>r.Índice>=78).length)+'</b></div>' +
        '<div class="score-card"><span>Projetos em atenção</span><b>'+num(quality.filter(r=>r.Índice<58).length)+'</b></div>' +
        '<div class="score-card"><span>Horas aceitas</span><b>'+num(sum(ctx.accepted, ['Horas decimais','Horas']))+'</b></div>' +
      '</div><div class="section-body grid-2" style="margin-top:14px">' +
        chart('Atividades por horas', group(ctx.work, ['Atividade realizada','Atividade'], ['Horas decimais','Horas'], 10), 'number', 'blue') +
        chart('Despesas por natureza', group(ctx.inv, ['Natureza','Tipo de despesa'], ['Valor Incentivado','Valor'], 10), 'money', 'amber') +
        table('Ranking técnico dos projetos', quality.map(r => ({ Projeto:r.Projeto, Índice:num(r.Índice), Diagnóstico:r.Diagnóstico, Risco:r.Risco, Evidência:short(r.Evidência, 260) })), ['Projeto','Índice','Diagnóstico','Risco','Evidência']) +
        table('Projetos filtrados', filteredProjects().map(p => ({ Projeto:p.title, Código:p.code, Origem:p.source, Ano:p.year || '', Status: boolCell(p.row,['Incentivado?']) ? 'Incentivado' : 'Revisar', Descrição: short(cell(p.row,['Descrição']), 220) })), ['Projeto','Código','Origem','Ano','Status','Descrição']) +
        table('Investimentos filtrados', ctx.inv.map(row => ({ Fornecedor:cell(row,['Fornecedor']), Natureza:cell(row,['Natureza']), Valor:money(numCell(row,['Valor Incentivado','Valor'])), Descrição:short(cell(row,['Descrição','Objetivo do gasto']), 180) })), ['Fornecedor','Natureza','Valor','Descrição']) +
      '</div></section>';
    }
    function evaluation() {
      const narrative = portfolioNarrative();
      return '<section id="avaliacao"><div class="section-title"><div><h2>Nossa avaliação do programa</h2><p>Diagnóstico comercial e técnico para renovar contrato e orientar suporte.</p></div></div><div class="panel insight" style="margin-bottom:14px"><div class="panel-head"><h2>Parecer da IA sobre o programa</h2><span class="pill">consultivo</span></div>' + narrative.map(item => '<div class="insight-card"><strong>'+esc(item.title)+'</strong><p>'+esc(item.text)+'</p></div>').join('') + '</div><div class="grid-2">' +
        '<div class="panel"><div class="panel-head"><h2>Pontos fortes</h2></div><ul class="list">'+strengths().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
        '<div class="panel"><div class="panel-head"><h2>Melhorias recomendadas</h2></div><ul class="list">'+improvements().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
      '</div></section>';
    }
    function indexSection() {
      const rows = annualRows();
      const current = rows.length ? rows : [{ Ano:DATA().year || 'Atual', Índice:programScoreForYear({base_total:DATA().metrics?.base_total, estimated_savings:DATA().metrics?.estimated_savings}), Diagnóstico:'Ano corrente', Base:money(DATA().metrics?.base_total || 0), Economia:money(DATA().metrics?.estimated_savings || 0), Foco:'Consolidar governança' }];
      return '<section id="indice"><div class="section-title"><div><h2>Índice PD&I ano a ano</h2><p>Pontuação calculada com base, RH, dispêndios, horas, economia e evidências históricas.</p></div></div><div class="section-body">' + chart('Índice PD&I ano a ano', current.map(r => ({ name:String(r.Ano), value:r.Índice })), 'number') + table('Índice e recomendação anual', current, ['Ano','Índice','Tendência','Variação','Diagnóstico','Base','Economia','Recomendação']) + '</div></section>';
    }
    function agents() {
      const endpoint = PORTAL.support_endpoint ? 'Envio automático configurado' : 'Endpoint de envio não configurado';
      return '<section id="agentes"><div class="section-title"><div><h2>Agentes e suporte</h2><p>IA limitada ao recorte filtrado e canal humano para abrir demanda.</p></div></div><div class="grid-2"><div class="panel"><div class="panel-head"><h2>Chatbot de projetos</h2><span class="pill">Escopo limitado</span></div><div class="messages" id="botMessages"></div><form class="chat-form" onsubmit="askBot(event)"><input id="botInput" placeholder="Pergunte sobre projetos, anos, descrição, valores ou riscos"><button class="primary">Enviar</button></form></div><div class="panel"><div class="panel-head"><h2>Falar com especialista</h2><span class="pill '+(PORTAL.support_endpoint?'ok':'warn')+'">'+endpoint+'</span></div><form onsubmit="openTicket(event)"><input id="ticketSubject" placeholder="Assunto da ordem de serviço"><textarea id="ticketBody" placeholder="Descreva a dúvida, projeto, ano e urgência"></textarea><div class="actions"><button class="primary">Enviar solicitação</button></div><p id="ticketStatus" class="toc-note">Para envio sem abrir e-mail, configure um endpoint interno que encaminhe para inovacao@taticcaconsulting.com.</p></form></div></div></section>';
    }
    function downloads() {
      const sheets = PORTAL.sheets_url ? '<a class="button" target="_blank" rel="noopener" href="'+esc(PORTAL.sheets_url)+'">Abrir Google Sheets</a>' : '<span class="pill warn">Google Sheets restrito: informar URL no gerador</span>';
      return '<section id="downloads" class="panel"><div class="panel-head"><h2>Downloads e congelamento</h2></div><div class="actions"><button onclick="window.print()">Baixar PDF / imprimir</button><button onclick="downloadFrozenHtml()">Baixar HTML congelado</button>'+sheets+'</div><p class="toc-note">O HTML congelado baixa uma cópia com os dados embutidos neste momento, útil para evidência de versão.</p></section>';
    }
    function renderControls() {
      $('companySelect').innerHTML = COMPANIES.map((c,i)=>'<option value="'+i+'">'+esc(c.company)+'</option>').join('');
      $('companySelect').value = String(state.company);
      $('yearSelect').innerHTML = '<option value="all">Todos os anos</option>' + years().map(y=>'<option value="'+esc(y)+'">'+esc(y)+'</option>').join('');
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
      renderControls();
      $('app').innerHTML = summary() + leiDoBem() + tecnoparque() + analytics() + evaluation() + indexSection() + agents() + downloads();
      renderBot();
    }
    function setCompany(value) { state.company=Number(value||0); state.year='all'; state.project='all'; state.expense='all'; state.q=''; render(); }
    function setFilter(key, value) { state[key] = key === 'q' ? (value || '') : (value || 'all'); render(); }
    function botAnswer(q) {
      const p = activeProject();
      if (!p) return 'Selecione um projeto para limitar o escopo da resposta.';
      const ql = projectQuality(p);
      const question = norm(q);
      if (question.includes('ano') || question.includes('hist') || question.includes('forca') || question.includes('força')) return 'Histórico conectado: ' + (ql.hist.slice(0,6).map(item => (item.year||'') + ' ' + short(item.name||item.summary,110)).join('; ') || 'sem narrativa histórica vinculada') + '. Índice técnico atual: ' + num(ql.score) + '/100 (' + ql.status + ').';
      if (question.includes('valor') || question.includes('despesa')) return 'Valores do recorte: investimentos ' + money(sum(ql.inv, ['Valor Incentivado','Valor'])) + ', RH filtrado ' + money(sum(projectRows('pessoal'), ['Total PD&I','Total PDI'])) + ', horas aceitas ' + num(sum(ql.accepted, ['Horas decimais','Horas'])) + '.';
      if (question.includes('risco') || question.includes('bom') || question.includes('qualidade')) return 'Avaliação técnica: ' + ql.status + ', risco ' + ql.risk + ', índice ' + num(ql.score) + '/100. Principais pontos: ' + (ql.element ? 'elemento inovador descrito; ' : 'elemento inovador fraco; ') + (ql.barrier ? 'barreira tecnológica descrita; ' : 'barreira tecnológica ausente; ') + (ql.accepted.length ? 'há atividades aceitas.' : 'faltam atividades aceitas.');
      return 'Projeto em foco: ' + p.title + '. Descrição: ' + short(cell(p.row,['Descrição']) || 'sem descrição', 360) + '. Índice técnico: ' + num(ql.score) + '/100. Avaliação: ' + (ql.element || 'elemento inovador não descrito na base filtrada.');
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
    window.setCompany=setCompany; window.setFilter=setFilter; window.askBot=askBot; window.openTicket=openTicket; window.downloadFrozenHtml=downloadFrozenHtml;
    render();
  </script>
</body>
</html>"""
    return html.replace("__TITLE__", escape(title)).replace("__PAYLOAD__", payload)
