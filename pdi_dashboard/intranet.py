from __future__ import annotations

import json
from html import escape

from .html import slim_analysis


def render_intranet_site(
    analyses: list[dict],
    *,
    title: str = "Intranet PD&I",
    sheets_url: str = "",
) -> str:
    payload = json.dumps(
        {"companies": [slim_analysis(item) for item in analyses], "sheets_url": sheets_url},
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
      --ink:#17211e; --muted:#65726e; --line:#dbe3df; --bg:#f6f8f7; --panel:#ffffff;
      --green:#13795b; --blue:#315f9d; --amber:#a76617; --red:#a33b2f; --teal:#0f766e;
      --shadow:0 14px 34px rgba(25,38,35,.08);
    }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--ink); font:14px/1.5 Arial, Helvetica, sans-serif; }
    .shell { display:grid; grid-template-columns:270px minmax(0,1fr); min-height:100vh; }
    aside { position:sticky; top:0; height:100vh; padding:18px; border-right:1px solid var(--line); background:#fff; overflow:auto; }
    main { padding:20px; }
    .client-area { color:var(--muted); font-weight:800; font-size:12px; text-transform:uppercase; }
    h1 { margin:6px 0 14px; font-size:22px; line-height:1.15; }
    h2 { margin:0; font-size:17px; }
    h3 { margin:0 0 8px; font-size:13px; text-transform:uppercase; color:var(--muted); }
    nav { display:grid; gap:8px; margin-top:14px; }
    nav a { color:var(--ink); text-decoration:none; padding:9px 10px; border:1px solid var(--line); border-radius:8px; background:#f9fbfa; font-weight:800; }
    select, input, textarea, button { font:inherit; }
    select, input, textarea { width:100%; border:1px solid var(--line); border-radius:8px; padding:10px 11px; background:white; color:var(--ink); }
    textarea { min-height:96px; resize:vertical; }
    button, .button { border:1px solid var(--line); border-radius:8px; padding:10px 12px; background:white; color:var(--ink); font-weight:850; cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; justify-content:center; }
    button.primary, .button.primary { background:var(--teal); border-color:var(--teal); color:white; }
    .filters { display:grid; grid-template-columns:1.3fr 1fr 1.1fr 1fr; gap:10px; margin:0 0 16px; }
    section { margin-bottom:18px; scroll-margin-top:16px; }
    .panel { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:15px; box-shadow:var(--shadow); }
    .panel-head { display:flex; justify-content:space-between; gap:12px; align-items:start; margin-bottom:12px; }
    .grid-2 { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:14px; }
    .grid-3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }
    .kpi { border:1px solid var(--line); border-radius:8px; padding:12px; background:#fbfcfc; }
    .kpi span { display:block; color:var(--muted); font-size:11px; font-weight:850; text-transform:uppercase; }
    .kpi b { display:block; margin-top:5px; font-size:20px; }
    .kpi small { display:block; margin-top:4px; color:var(--muted); }
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
      .filters, .grid-2, .grid-3 { grid-template-columns:1fr; }
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
        <select id="yearSelect" onchange="setFilter('year', this.value)" aria-label="Ano"></select>
        <select id="projectSelect" onchange="setFilter('project', this.value)" aria-label="Projeto"></select>
        <select id="expenseSelect" onchange="setFilter('expense', this.value)" aria-label="Tipo de despesa"></select>
        <input id="searchInput" oninput="setFilter('q', this.value)" placeholder="Buscar na memória, projeto ou atividade">
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
      return rows('projetos').map((row, i) => {
        const title = String(cell(row, ['Projeto']) || 'Projeto ' + (i+1)).trim();
        return { id:'p'+i, title, code:projectCode(row), row };
      });
    }
    function filteredProjects() {
      const q = norm(state.q);
      return projects().filter(p => {
        if (state.project !== 'all' && p.id !== state.project) return false;
        if (q && !norm([p.title, p.code, cell(p.row,['Descrição'])].join(' ')).includes(q)) return false;
        return true;
      });
    }
    function activeProject() { return filteredProjects()[0] || projects()[0]; }
    function projectRows(key, p=activeProject()) {
      const q = norm(state.q);
      if (!p || state.project === 'all') return rows(key).filter(row => !q || norm(JSON.stringify(row)).includes(q));
      const code = norm(p.code);
      const title = norm(p.title);
      return rows(key).filter(row => {
        const text = norm(JSON.stringify(row));
        return (!q || text.includes(q)) && ((code && text.includes(code)) || (title.length > 12 && text.includes(title.slice(0,80))));
      });
    }
    function expenses() {
      const set = new Set(['all']);
      rows('investimentos').forEach(row => { const v = cell(row, ['Natureza', 'Tipo de despesa']); if (v) set.add(v); });
      return [...set];
    }
    function filteredInvestments() {
      return projectRows('investimentos').filter(row => state.expense === 'all' || norm(cell(row, ['Natureza', 'Tipo de despesa'])) === norm(state.expense));
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
    function strengths() {
      const m = DATA().metrics || {};
      const out = [];
      if (Number(m.base_total||0)>0) out.push('Base econômica de PD&I quantificada e pronta para narrativa executiva.');
      if (Number(m.projects_incentivized||0)>0) out.push('Carteira com projetos incentivados identificados.');
      if (Number(m.eligible_hours||0)>0) out.push('Timesheet técnico com horas elegíveis para sustentar execução.');
      if ((DATA().history?.years || []).length) out.push('Memória histórica disponível para demonstrar evolução e continuidade.');
      return out.length ? out : ['Há dados carregados para iniciar estruturação do programa de PD&I.'];
    }
    function improvements() {
      const m = DATA().metrics || {};
      const out = [];
      if (!Number(m.eligible_hours||0)) out.push('Padronizar timesheet técnico com atividade, etapa, evidência e critério de incentivo.');
      if (!Number(m.investment_incentivized||0)) out.push('Reconciliar investimentos por projeto, natureza, fornecedor e justificativa técnica.');
      if (!(DATA().history?.projects || []).length) out.push('Criar memória anual de projetos com objetivo, incerteza, testes, resultados e valores.');
      out.push('Usar rotina mensal de revisão para reduzir risco de glosa e vender suporte técnico recorrente.');
      return out;
    }
    function agentAssessment() {
      const p = activeProject();
      const work = projectRows('trabalho', p);
      const inv = filteredInvestments();
      const accepted = work.filter(row => boolCell(row, ['Projeto incentivado?']) && boolCell(row, ['Atividade incentivada?']));
      const desc = cell(p?.row || {}, ['Descrição']);
      const element = cell(p?.row || {}, ['Elemento tecnologicamente novo ou inovador', 'Elemento inovador']);
      const barrier = cell(p?.row || {}, ['Barreira ou desafio tecnológico a superar', 'Risco tecnológico']);
      const status = element && barrier && accepted.length ? 'Defensável tecnicamente' : element || barrier || accepted.length ? 'Defensável com ressalvas' : 'Precisa de documentação técnica';
      return '<div class="panel"><div class="panel-head"><h2>Agente de avaliação PD&I</h2><span class="pill '+(status.includes('ressalvas')?'warn':status.includes('Precisa')?'bad':'ok')+'">'+esc(status)+'</span></div>' +
        '<ul class="list"><li><b>Projeto:</b> '+esc(p?.title || 'Carteira')+'</li><li><b>Tese técnica:</b> '+esc(short(desc || element || 'Sem tese técnica suficiente na base filtrada.', 380))+'</li><li><b>Incerteza/barreira:</b> '+esc(short(barrier || 'Não localizada de forma explícita.', 300))+'</li><li><b>Execução:</b> '+num(sum(accepted, ['Horas decimais','Horas']))+' horas aceitas em '+num(accepted.length)+' linhas.</li><li><b>Valores:</b> '+money(sum(inv, ['Valor Incentivado','Valor']))+' em investimentos filtrados.</li></ul></div>';
    }
    function table(title, data, cols) {
      const body = (data||[]).slice(0,500).map(row => '<tr>'+cols.map(c => '<td>'+esc(row[c] ?? '')+'</td>').join('')+'</tr>').join('');
      return '<div class="panel"><div class="panel-head"><h2>'+esc(title)+'</h2><span class="pill">'+num((data||[]).length)+' linhas</span></div><div class="table-wrap"><table><thead><tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr></thead><tbody>'+body+'</tbody></table></div></div>';
    }
    function summary() {
      const m = DATA().metrics || {};
      const inv = filteredInvestments();
      const people = projectRows('pessoal');
      const historyYears = DATA().history?.years || [];
      return '<section id="resumo"><div class="grid-3">' +
        kpi('Base PD&I', money(m.base_total || (m.people_pdi_total||0)+(m.investment_incentivized||0)), 'Lei do Bem') +
        kpi('Economia estimada', money(m.estimated_savings || 0), 'IRPJ/CSLL') +
        kpi('Anos de memória', num(historyYears.length), 'Histórico carregado') +
        kpi('Projetos', num(m.projects_total || projects().length), num(m.projects_incentivized || 0)+' incentivados') +
        kpi('Investimentos filtrados', money(sum(inv, ['Valor Incentivado','Valor'])), state.expense === 'all' ? 'Todos os tipos' : state.expense) +
        kpi('RH filtrado', money(sum(people, ['Total PD&I','Total PDI'])), 'Projeto/filtro atual') +
      '</div></section>';
    }
    function leiDoBem() {
      const m = DATA().metrics || {};
      return '<section id="lei" class="grid-2"><div class="panel"><div class="panel-head"><h2>Lei do Bem</h2></div><ul class="list"><li>Base PD&I conciliada: <b>'+money(m.base_total || 0)+'</b></li><li>Exclusão adicional: <b>'+money(m.exclusion_total || 0)+'</b></li><li>Economia fiscal: <b>'+money(m.estimated_savings || 0)+'</b></li><li>Risco central: manter vínculo entre incerteza tecnológica, execução e valor.</li></ul></div>'+agentAssessment()+'</section>';
    }
    function tecnoparque() {
      return '<section id="tecnoparque" class="panel"><div class="panel-head"><h2>Tecnoparque</h2><span class="pill warn">Módulo comercial</span></div><p>Área para consolidar oportunidades de parceria, infraestrutura, ecossistema de inovação, ICTs, laboratórios, projetos de continuidade e suporte técnico recorrente.</p><ul class="list"><li>Mapear projetos com potencial de laboratório, validação, prototipagem ou ensaio.</li><li>Relacionar maturidade técnica com necessidade de suporte mensal.</li><li>Transformar lacunas documentais em plano de horas e renovação contratual.</li></ul></section>';
    }
    function analytics() {
      const work = projectRows('trabalho');
      const inv = filteredInvestments();
      return '<section id="analiticos" class="grid-2">' +
        chart('Atividades por horas', group(work, ['Atividade realizada','Atividade'], ['Horas decimais','Horas'], 10), 'number', 'blue') +
        chart('Despesas por natureza', group(inv, ['Natureza','Tipo de despesa'], ['Valor Incentivado','Valor'], 10), 'money', 'amber') +
        table('Projetos filtrados', filteredProjects().map(p => ({ Projeto:p.title, Código:p.code, Status: boolCell(p.row,['Incentivado?']) ? 'Incentivado' : 'Revisar', Descrição: short(cell(p.row,['Descrição']), 220) })), ['Projeto','Código','Status','Descrição']) +
        table('Investimentos filtrados', inv.map(row => ({ Fornecedor:cell(row,['Fornecedor']), Natureza:cell(row,['Natureza']), Valor:money(numCell(row,['Valor Incentivado','Valor'])), Descrição:short(cell(row,['Descrição','Objetivo do gasto']), 180) })), ['Fornecedor','Natureza','Valor','Descrição']) +
      '</section>';
    }
    function evaluation() {
      return '<section id="avaliacao" class="grid-2">' +
        '<div class="panel"><div class="panel-head"><h2>Pontos fortes</h2></div><ul class="list">'+strengths().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
        '<div class="panel"><div class="panel-head"><h2>Melhorias recomendadas</h2></div><ul class="list">'+improvements().map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></div>' +
      '</section>';
    }
    function indexSection() {
      const rows = (DATA().history?.years || []).map(row => ({ Ano:row.year, Índice:programScoreForYear(row), Diagnóstico:scoreBand(programScoreForYear(row)), Base:money(row.base_total || 0), Economia:money(row.estimated_savings || 0), Foco: programScoreForYear(row) < 65 ? 'Plano de ação e evidências' : 'Escalar suporte e governança' }));
      const current = rows.length ? rows : [{ Ano:DATA().year || 'Atual', Índice:programScoreForYear({base_total:DATA().metrics?.base_total, estimated_savings:DATA().metrics?.estimated_savings}), Diagnóstico:'Ano corrente', Base:money(DATA().metrics?.base_total || 0), Economia:money(DATA().metrics?.estimated_savings || 0), Foco:'Consolidar governança' }];
      return '<section id="indice">' + chart('Índice PD&I ano a ano', current.map(r => ({ name:String(r.Ano), value:r.Índice })), 'number') + table('Índice e recomendação anual', current, ['Ano','Índice','Diagnóstico','Base','Economia','Foco']) + '</section>';
    }
    function agents() {
      return '<section id="agentes" class="grid-2"><div class="panel"><div class="panel-head"><h2>Chatbot de projetos</h2><span class="pill">Escopo limitado</span></div><div class="messages" id="botMessages"></div><form class="chat-form" onsubmit="askBot(event)"><input id="botInput" placeholder="Pergunte sobre projetos, anos, descrição, valores ou riscos"><button class="primary">Enviar</button></form></div><div class="panel"><div class="panel-head"><h2>Falar com especialista</h2></div><form onsubmit="openTicket(event)"><input id="ticketSubject" placeholder="Assunto da ordem de serviço"><textarea id="ticketBody" placeholder="Descreva a dúvida, projeto, ano e urgência"></textarea><div class="actions"><button class="primary">Abrir ordem por e-mail</button><a class="button" href="mailto:inovacao@taticcaconsulting.com">Enviar e-mail direto</a></div></form></div></section>';
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
      const ps = projects();
      $('projectSelect').innerHTML = '<option value="all">Todos os projetos</option>' + ps.map(p=>'<option value="'+esc(p.id)+'">'+esc((p.code || 'Projeto')+' · '+short(p.title,80))+'</option>').join('');
      $('projectSelect').value = ps.some(p=>p.id===state.project) ? state.project : 'all';
      state.project = $('projectSelect').value;
      $('expenseSelect').innerHTML = expenses().map(v=>'<option value="'+esc(v)+'">'+esc(v === 'all' ? 'Todas as despesas' : v)+'</option>').join('');
      $('expenseSelect').value = state.expense;
      $('searchInput').value = state.q;
    }
    function render() {
      renderControls();
      $('app').innerHTML = summary() + leiDoBem() + tecnoparque() + analytics() + evaluation() + indexSection() + agents() + downloads();
      renderBot();
    }
    function setCompany(value) { state.company=Number(value||0); state.year='all'; state.project='all'; state.expense='all'; state.q=''; render(); }
    function setFilter(key, value) { state[key]=value || 'all'; render(); }
    function botAnswer(q) {
      const p = activeProject();
      if (!p) return 'Selecione um projeto para limitar o escopo da resposta.';
      const m = DATA().metrics || {};
      if (norm(q).includes('ano') || norm(q).includes('hist')) return 'Histórico encontrado: ' + ((DATA().history?.projects || []).slice(0,6).map(item => (item.year||'') + ' ' + short(item.name||item.summary,90)).join('; ') || 'sem narrativa histórica vinculada.');
      if (norm(q).includes('valor') || norm(q).includes('despesa')) return 'Valores do recorte: base PD&I ' + money(m.base_total || 0) + ', investimentos filtrados ' + money(sum(filteredInvestments(), ['Valor Incentivado','Valor'])) + ', RH filtrado ' + money(sum(projectRows('pessoal'), ['Total PD&I','Total PDI'])) + '.';
      return 'Projeto em foco: ' + p.title + '. Descrição: ' + short(cell(p.row,['Descrição']) || 'sem descrição', 360) + '. Avaliação: ' + (cell(p.row,['Elemento tecnologicamente novo ou inovador','Elemento inovador']) || 'elemento inovador não descrito na base filtrada.');
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
    function openTicket(ev) {
      ev.preventDefault();
      const subject = encodeURIComponent($('ticketSubject').value || 'Ordem de serviço PD&I');
      const body = encodeURIComponent(($('ticketBody').value || '') + '\\n\\nEmpresa: ' + DATA().company + '\\nProjeto: ' + (activeProject()?.title || 'Todos') + '\\nAno: ' + state.year);
      window.location.href = 'mailto:inovacao@taticcaconsulting.com?subject=' + subject + '&body=' + body;
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
