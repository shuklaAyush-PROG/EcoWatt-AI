/* ══════════════════════════════════════════════
   EcoWatt AI  — script.js
   ══════════════════════════════════════════════ */

/* ── CONSTANTS ── */
const EMISSION_FACTOR = 0.716;    // kg CO2 per kWh (India avg grid)
const SOLAR_PEAK_HOURS = 4.5;     // peak sun-hours/day (India avg)
const SOLAR_EFFICIENCY = 0.80;    // system efficiency

/* ── STATE ── */
let state = {
  calculated: false,
  watts: 0,
  quantity: 1,
  usageHours: 8,
  rate: 8,
  monthlyKwh: 0,
  monthlyBill: 0,
  solarKwp: 0,
  carbonKg: 0,
  score: 0,
};

/* ── CALCULATE ── */
function calculate() {
  const businessType = document.getElementById('businessType').value;
  const applianceEl  = document.getElementById('appliance');
  const watts        = parseFloat(applianceEl.options[applianceEl.selectedIndex]?.dataset?.watts || 0);
  const quantity     = parseFloat(document.getElementById('quantity').value) || 1;
  const usageHours   = parseFloat(document.getElementById('usageHours').value) || 8;
  const rate         = parseFloat(document.getElementById('elecRate').value) || 8;

  /* Validation */
  if (!businessType) { flashHint('Please select a Business Type.'); return; }
  if (!watts)        { flashHint('Please select an Appliance.'); return; }
  if (quantity < 1)  { flashHint('Quantity must be at least 1.'); return; }
  if (usageHours <= 0 || usageHours > 24) { flashHint('Enter valid usage hours (0.5 – 24).'); return; }

  /* Core calcs */
  const dailyKwh   = (watts / 1000) * quantity * usageHours;
  const monthlyKwh = dailyKwh * 30;
  const monthlyBill= monthlyKwh * rate;
  const carbonKg   = monthlyKwh * EMISSION_FACTOR;
  const solarKwp   = +(dailyKwh / (SOLAR_PEAK_HOURS * SOLAR_EFFICIENCY)).toFixed(2);
  const annualSavings = monthlyBill * 12 * 0.30;
  const yearlyCO2Saved = carbonKg * 12 * 0.8;
  const score      = calcScore(monthlyKwh, solarKwp, rate);

  /* Persist state */
  Object.assign(state, { calculated: true, watts, quantity, usageHours, rate, monthlyKwh, monthlyBill, solarKwp, carbonKg,annualSavings, yearlyCO2Saved, score 
    
  });
    localStorage.setItem(
  "ecowattData",
  JSON.stringify(state)
);

  /* Animate cards */
  animateValue('val-consumption', monthlyKwh, 1, ' kWh');
  animateValue('val-bill',        monthlyBill, 0, '', '₹');
  animateValue('val-solar',       solarKwp,   2, ' kWp');
  animateValue('val-carbon',      carbonKg,   1, ' kg');
  animateValue('val-savings', annualSavings, 0, '', '₹');
  animateValue('val-co2saved',yearlyCO2Saved,0,' kg');
  animateScore(score);

  /* Progress bars (relative to big reference numbers) */
  setBar('bar-consumption', monthlyKwh,  5000);
  setBar('bar-bill',        monthlyBill, 40000);
  setBar('bar-solar',       solarKwp,    50);
  setBar('bar-carbon',      carbonKg,    3600);
  setBar('bar-savings', annualSavings, 100000);
  setBar('bar-co2saved', yearlyCO2Saved, 10000);

  /* Recommendations */
  buildRecommendations(businessType, monthlyKwh, solarKwp, score, rate);

  /* Hint */
  document.getElementById('formHint').textContent = '✓ Analysis complete — scroll to view results.';
  document.getElementById('formHint').style.color = 'var(--lime)';

  /* Update simulator */
  updateComparison(
  applianceEl.value,
  monthlyBill
);
  updateSimulator();
  drawEnergyChart(monthlyKwh);
  calculateROI();

}


/* ── SCORE CALC ── */
function calcScore(kwh, solar, rate) {
  let score = 100;
  // Penalise heavy consumption
  if (kwh > 4000) score -= 40;
  else if (kwh > 2000) score -= 25;
  else if (kwh > 800)  score -= 12;
  // Penalise high solar need (means heavy usage)
  if (solar > 30) score -= 20;
  else if (solar > 10) score -= 10;
  // Penalise high tariff (indicates inefficiency incentive)
  if (rate > 12) score -= 5;
  return Math.max(10, Math.min(100, Math.round(score)));
}

/* ── ANIMATE VALUE ── */
function animateValue(id, end, decimals, suffix = '', prefix = '') {
  const el = document.getElementById(id);
  const start = 0; const dur = 1000; const startTime = performance.now();
  el.classList.add('animating');
  function step(now) {
    const progress = Math.min((now - startTime) / dur, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const current = start + (end - start) * ease;
    el.textContent = prefix + formatNum(current, decimals) + suffix;
    if (progress < 1) requestAnimationFrame(step);
    else { el.classList.remove('animating'); el.textContent = prefix + formatNum(end, decimals) + suffix; }
  }
  requestAnimationFrame(step);
}

function formatNum(n, dec) {
  if (n >= 1000) return (n / 1000).toFixed(dec > 0 ? 1 : 0) + 'k';
  return n.toFixed(dec);
}

/* ── ANIMATE SCORE ── */
function animateScore(score) {
  const el   = document.getElementById('val-score');
  const ring = document.getElementById('ringFill');
  const grade = document.getElementById('score-grade');
  const circumference = 2 * Math.PI * 50; // r=50

  let label, cls;
  if (score >= 80)      { label = '🌟 Excellent'; cls = 'grade-excellent'; }
  else if (score >= 60) { label = '✅ Good';      cls = 'grade-good'; }
  else if (score >= 40) { label = '⚠️ Fair';      cls = 'grade-fair'; }
  else                  { label = '❌ Poor';       cls = 'grade-poor'; }

  grade.textContent = label;
  grade.className = 'kpi-unit ' + cls;
  ring.style.stroke = score >= 80 ? 'var(--lime)' : score >= 60 ? 'var(--teal)' : score >= 40 ? 'var(--warn)' : 'var(--danger)';

  // Animate ring
  const dashLen = (score / 100) * circumference;
  ring.style.strokeDasharray = `${dashLen} ${circumference}`;

  // Animate number
  animateValue('val-score', score, 0);
}

/* ── SET BAR ── */
function setBar(id, value, max) {
  const pct = Math.min((value / max) * 100, 100);
  document.getElementById(id).style.width = pct + '%';
}

/* ── FLASH HINT ── */
function flashHint(msg) {
  const el = document.getElementById('formHint');
  el.textContent = '⚠ ' + msg;
  el.style.color = 'var(--warn)';
}

/* ── RECOMMENDATIONS ── */
function buildRecommendations(biz, kwh, solar, score, rate) {
  const list = document.getElementById('recoList');
  list.innerHTML = '';
  const tips = [];
  if(score >= 90){
  tips.push("Excellent energy efficiency. Maintain current practices and consider battery storage.");
}
else if(score >= 70){
  tips.push("Good performance. Replacing older appliances can further reduce consumption.");
}
else if(score >= 50){
  tips.push("Moderate efficiency. Focus on LED upgrades and smart energy monitoring.");
}
else{
  tips.push("High energy usage detected. Immediate efficiency improvements are recommended.");
}

  // Universal
  tips.push(`Install a ${solar.toFixed(1)} kWp rooftop solar system to potentially offset 80–100% of your consumption.`);

  if (kwh > 1000) tips.push('Your monthly load is high. Consider a energy audit to identify inefficient appliances.');
  if (rate > 10)  tips.push('Shift heavy loads to off-peak tariff hours (22:00–06:00) to reduce peak demand charges.');

  // Business-specific
  if (biz === 'restaurant' || biz === 'hotel') {
    tips.push('Install smart thermostats and LED kitchen lighting to cut HVAC and lighting loads by up to 35%.');
  } else if (biz === 'warehouse' || biz === 'school') {
    tips.push('Daylight harvesting with smart sensors can reduce lighting energy by 40% in large spaces.');
  } else if (biz === 'hospital') {
    tips.push('Prioritise UPS-backed solar with battery storage for critical medical load continuity.');
  } else if (biz === 'residential') {
    tips.push('Switch to 5-star BEE rated appliances; refrigerator and AC upgrades pay back in 2–3 years.');
  }

  if (score < 60) tips.push('Enrol in a carbon offset programme while upgrading to renewables for near-term neutrality.');
  tips.push(`Adding ${(solar * 1.1).toFixed(1)} kWp solar + battery storage could eliminate grid dependency entirely.`);
  tips.push('Consider a Power Purchase Agreement (PPA) for zero-capex solar access in commercial setups.');

  tips.forEach((tip, i) => {
    const li = document.createElement('li');
    li.className = 'reco-item';
    li.style.animationDelay = `${i * 80}ms`;
    li.textContent = tip;
    list.appendChild(li);
  });
}

/* ── EXPANSION SIMULATOR ── */
function updateSimulator() {
  const unitsEl = document.getElementById('simUnits');
  const hoursEl = document.getElementById('simHours');
  const addUnits = parseFloat(unitsEl.value) || 0;
  const addHours = parseFloat(hoursEl.value) || 0;

  document.getElementById('simUnitsVal').textContent = addUnits;
  document.getElementById('simHoursVal').textContent = addHours;

  // Update range track fill
  updateRangeTrack(unitsEl, 1, 50);
  updateRangeTrack(hoursEl, 0, 16);

  if (!state.calculated) return;

  const extraKwh  = ((state.watts / 1000) * (state.quantity + addUnits) * (state.usageHours + addHours) * 30)
                     - state.monthlyKwh;
  const totalBill = (state.monthlyKwh + extraKwh) * state.rate;
  const extraCost = extraKwh * state.rate;
  const extraCO2  = extraKwh * EMISSION_FACTOR;

  document.getElementById('sim-extra-kwh').textContent  = extraKwh.toFixed(0) + ' kWh';
  document.getElementById('sim-extra-cost').textContent = '₹' + extraCost.toFixed(0);
  document.getElementById('sim-total-bill').textContent = '₹' + totalBill.toFixed(0);
  document.getElementById('sim-extra-co2').textContent  = extraCO2.toFixed(1) + ' kg';
}

function updateRangeTrack(input, min, max) {
  const pct = ((input.value - min) / (max - min)) * 100;
  input.style.setProperty('--prog', pct + '%');
}

/* ── PDF DOWNLOAD ── */
function downloadPDF() {
  if (!state.calculated) {
    alert('Please run the analysis first before downloading the report.');
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
  const W = 210; const H = 297;

  // ── Background ──
  doc.setFillColor(8, 15, 10);
  doc.rect(0, 0, W, H, 'F');

  // ── Header bar ──
  doc.setFillColor(13, 26, 16);
  doc.rect(0, 0, W, 28, 'F');

  // ── Title ──
  doc.setTextColor(132, 218, 97);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(18);
  doc.text('EcoWatt AI', 14, 12);
  doc.setFontSize(9);
  doc.setTextColor(122, 155, 116);
  doc.text('Sustainable Energy Planning Report', 14, 19);

  // Date
  doc.setFontSize(8);
  doc.setTextColor(62, 94, 56);
  doc.text('Generated: ' + new Date().toLocaleString(), W - 14, 19, { align: 'right' });

  // ── Section helper ──
  function sectionHeader(label, y) {
    doc.setFillColor(20, 36, 22);
    doc.rect(10, y, W - 20, 8, 'F');
    doc.setTextColor(132, 218, 97);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.text(label, 14, y + 5.5);
    return y + 12;
  }

  function kpiRow(label, value, unit, y) {
    doc.setTextColor(122, 155, 116);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8.5);
    doc.text(label, 14, y);
    doc.setTextColor(230, 242, 224);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(11);
    doc.text(value, 110, y, { align: 'right' });
    doc.setTextColor(62, 94, 56);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.text(unit, 140, y);
    // Divider
    doc.setDrawColor(20, 36, 22);
    doc.setLineWidth(0.3);
    doc.line(14, y + 2, W - 14, y + 2);
    return y + 8;
  }

  // ── KPI Section ──
  let cy = sectionHeader('ENERGY METRICS', 34);
  cy = kpiRow('Monthly Consumption',   state.monthlyKwh.toFixed(1),  'kWh / month',   cy);
  cy = kpiRow('Monthly Electricity Bill', '₹' + state.monthlyBill.toFixed(0), 'INR / month', cy);
  cy = kpiRow('Solar Capacity Needed', state.solarKwp.toFixed(2),    'kWp system',    cy);
  cy = kpiRow('Carbon Footprint',      state.carbonKg.toFixed(1),    'kg CO₂ / month',cy);

  // Score
  cy += 2;
  cy = sectionHeader('SUSTAINABILITY SCORE', cy);
  doc.setTextColor(132, 218, 97);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(28);
  doc.text(state.score + ' / 100', W / 2, cy + 8, { align: 'center' });
  cy += 18;

  // ── Input Summary ──
  cy = sectionHeader('INPUT SUMMARY', cy);
  const applianceEl = document.getElementById('appliance');
  const bizEl = document.getElementById('businessType');
  const appName = applianceEl.options[applianceEl.selectedIndex]?.text || '—';
  const bizName = bizEl.options[bizEl.selectedIndex]?.text || '—';

  cy = kpiRow('Business Type', bizName, '',                   cy);
  cy = kpiRow('Appliance',     appName, '',                   cy);
  cy = kpiRow('Quantity',      state.quantity.toString(), 'units', cy);
  cy = kpiRow('Daily Usage',   state.usageHours + ' hrs', 'per day', cy);
  cy = kpiRow('Electricity Rate', '₹' + state.rate, 'per kWh', cy);

  // ── Recommendations ──
  cy += 2;
  cy = sectionHeader('AI RECOMMENDATIONS', cy);
  const items = document.querySelectorAll('.reco-item:not(.reco-item--placeholder)');
  doc.setFont('helvetica', 'normal');
  items.forEach((item, i) => {
    const txt = '• ' + item.textContent.trim();
    const lines = doc.splitTextToSize(txt, W - 28);
    doc.setTextColor(200, 230, 195);
    doc.setFontSize(8);
    doc.text(lines, 14, cy);
    cy += lines.length * 5 + 2;
    if (cy > H - 30) { doc.addPage(); doc.setFillColor(8,15,10); doc.rect(0,0,W,H,'F'); cy = 20; }
  });

  // ── Footer ──
  doc.setFillColor(13, 26, 16);
  doc.rect(0, H - 14, W, 14, 'F');
  doc.setTextColor(62, 94, 56);
  doc.setFontSize(7);
  doc.text('EcoWatt AI — Sustainable Energy Planning Assistant  |  Data is illustrative. Consult a certified energy auditor for professional advice.', W / 2, H - 5, { align: 'center' });

  doc.save('EcoWatt-AI-Report.pdf');
}

/* ── INIT RANGE TRACKS ── */
window.addEventListener('DOMContentLoaded', () => {
  updateRangeTrack(document.getElementById('simUnits'), 1, 50);
  updateRangeTrack(document.getElementById('simHours'), 0, 16);
});
window.addEventListener("load", () => {

  const saved =
    localStorage.getItem("ecowattData");

  if(saved){

    state = JSON.parse(saved);

    document.getElementById(
      "val-consumption"
    ).textContent =
      state.monthlyKwh.toFixed(1) + " kWh";

    document.getElementById(
      "val-bill"
    ).textContent =
      "₹" + state.monthlyBill.toFixed(0);

    document.getElementById(
      "val-solar"
    ).textContent =
      state.solarKwp.toFixed(2) + " kWp";

    document.getElementById(
      "val-carbon"
    ).textContent =
      state.carbonKg.toFixed(1) + " kg";

  }

});
function drawEnergyChart(monthlyKwh) {

  const ctx = document.getElementById("energyChart");

  if (!ctx) return;

  if (window.energyChartInstance) {
    window.energyChartInstance.destroy();
  }
  const data = [
  monthlyKwh * (0.85 + Math.random()*0.1),
  monthlyKwh * (0.90 + Math.random()*0.1),
  monthlyKwh * (0.95 + Math.random()*0.1),
  monthlyKwh,
  monthlyKwh * (1.00 + Math.random()*0.1),
  monthlyKwh * (1.05 + Math.random()*0.1)
];



  window.energyChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun"
      ],
      datasets: [{
        label: "Energy Consumption (kWh)",
        data: data,
        borderColor: "#84da61",
        backgroundColor: "rgba(132,218,97,0.15)",
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true
    }
  });
}
function calculateROI() {

  if (!state.calculated) return;

  const solarCost =
    state.solarKwp * 60000;

  const annualSavings =
    state.monthlyBill * 12 * 0.30;

  const paybackYears =
    solarCost / annualSavings;

  document.getElementById(
    "roi-cost"
  ).textContent =
    "₹" + solarCost.toLocaleString("en-IN");

  document.getElementById(
    "roi-savings"
  ).textContent =
    "₹" + annualSavings.toLocaleString("en-IN");

  document.getElementById(
    "roi-payback"
  ).textContent =
    paybackYears.toFixed(1) + " yrs";
    const status =
  document.getElementById("roi-status");

if(paybackYears < 7){
  status.textContent =
    "🔥 Excellent Solar Investment";
}
else if(paybackYears < 12){
  status.textContent =
    "✅ Good Investment";
}
else{
  status.textContent =
    "⚠ Long Payback Period";
}
}
const themeBtn =
document.getElementById(
  "themeToggle"
);

if(
  localStorage.getItem("theme")
  === "light"
){
  document.body.classList.add(
    "light-mode"
  );

  themeBtn.textContent =
    "☀️ Light Mode";
}

themeBtn.addEventListener(
  "click",
  () => {

    document.body.classList.toggle(
      "light-mode"
    );

    if(
      document.body.classList.contains(
        "light-mode"
      )
    ){
      themeBtn.textContent =
        "☀️ Light Mode";

      localStorage.setItem(
        "theme",
        "light"
      );
    }
    else{

      themeBtn.textContent =
        "🌙 Dark Mode";

      localStorage.setItem(
        "theme",
        "dark"
      );
    }

  }
);
function updateComparison(appliance, monthlyBill) {

  let efficientBill = monthlyBill * 0.7;

  document.getElementById("comparisonBox").innerHTML = `
    <p><strong>Current Monthly Cost:</strong> ₹${monthlyBill.toFixed(0)}</p>
    <p><strong>Efficient Appliance Cost:</strong> ₹${efficientBill.toFixed(0)}</p>
    <p><strong>Potential Savings:</strong> ₹${(monthlyBill-efficientBill).toFixed(0)}</p>
  `;
}