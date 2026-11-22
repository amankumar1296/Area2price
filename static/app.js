/**
 * ESTATEIQ · SENIOR ARCHITECTURAL VALUATION ENGINE
 * Real-time Indian Real Estate (₹) Valuation & Vector Telemetry
 */

let modelInfo = {
    slope: 0.1656,
    intercept: 22.81,
    minSize: 500,
    maxSize: 3000
};

// UI Elements
const areaInput = document.getElementById('area-input');
const areaSlider = document.getElementById('area-slider');
const btnMinus = document.getElementById('btn-step-minus');
const btnPlus = document.getElementById('btn-step-plus');
const archetypeBadge = document.getElementById('archetype-badge');
const archetypeButtons = document.querySelectorAll('.archetype-btn');

// Valuation Display Elements
const resultPriceMain = document.getElementById('result-price-main');
const resultPriceFull = document.getElementById('result-price-full');
const resultPriceLakh = document.getElementById('result-price-lakh');
const resultRate = document.getElementById('result-rate');
const resultEmi = document.getElementById('result-emi');
const resultIntercept = document.getElementById('result-intercept');
const resultSlope = document.getElementById('result-slope');
const formulaDisplay = document.getElementById('formula-display');

// Blueprint Space Allocation Elements
const blueprintCalcTag = document.getElementById('blueprint-calc-tag');
const planLiving = document.getElementById('plan-living');
const planMaster = document.getElementById('plan-master');
const planBed2 = document.getElementById('plan-bed2');
const planUtil = document.getElementById('plan-util');

// SVG Telemetry Elements
const svgRadarDot = document.getElementById('svg-radar-dot');
const svgRadarPulse = document.getElementById('svg-radar-pulse');
const svgCrosshairX = document.getElementById('svg-crosshair-x');

// Formatter using Indian numbering system
const inrFormatter = new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0
});

document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
    await fetchModelParameters();
    syncCalculations();
});

function setupEventListeners() {
    // Numeric Input Event
    areaInput.addEventListener('input', () => {
        let val = parseFloat(areaInput.value);
        if (!isNaN(val)) {
            if (val >= 500 && val <= 3500) {
                areaSlider.value = val;
            }
            updateSliderFill();
            syncCalculations();
            updateActiveArchetype(val);
        }
    });

    // Range Slider Event
    areaSlider.addEventListener('input', () => {
        areaInput.value = areaSlider.value;
        updateSliderFill();
        syncCalculations();
        updateActiveArchetype(parseFloat(areaSlider.value));
    });

    // Stepper Buttons (+/- 50 sq ft)
    btnMinus.addEventListener('click', () => {
        let current = parseFloat(areaInput.value) || 1500;
        let next = Math.max(400, current - 50);
        areaInput.value = next;
        areaSlider.value = Math.min(3500, Math.max(500, next));
        updateSliderFill();
        syncCalculations();
        updateActiveArchetype(next);
    });

    btnPlus.addEventListener('click', () => {
        let current = parseFloat(areaInput.value) || 1500;
        let next = Math.min(5000, current + 50);
        areaInput.value = next;
        areaSlider.value = Math.min(3500, Math.max(500, next));
        updateSliderFill();
        syncCalculations();
        updateActiveArchetype(next);
    });

    // Archetype Preset Chips
    archetypeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const size = parseFloat(btn.dataset.size);
            const label = btn.dataset.label;
            areaInput.value = size;
            areaSlider.value = size;
            updateSliderFill();
            syncCalculations();
            updateArchetypeUI(btn, label);
        });
    });

    updateSliderFill();
}

function updateSliderFill() {
    if (!areaSlider) return;
    const min = parseFloat(areaSlider.min) || 500;
    const max = parseFloat(areaSlider.max) || 3500;
    const val = parseFloat(areaSlider.value) || 1500;
    const percentage = ((val - min) / (max - min)) * 100;
    areaSlider.style.background = `linear-gradient(to right, #10b981 0%, #10b981 ${percentage}%, rgba(255,255,255,0.08) ${percentage}%, rgba(255,255,255,0.08) 100%)`;
}

function updateActiveArchetype(currentSize) {
    let closestBtn = null;
    let minDiff = Infinity;
    let activeLabel = "Custom Configuration";

    archetypeButtons.forEach(btn => {
        const btnSize = parseFloat(btn.dataset.size);
        const diff = Math.abs(currentSize - btnSize);
        if (diff < minDiff && diff <= 100) {
            minDiff = diff;
            closestBtn = btn;
            activeLabel = btn.dataset.label;
        }
    });

    archetypeButtons.forEach(btn => btn.classList.remove('active'));
    if (closestBtn) {
        closestBtn.classList.add('active');
        archetypeBadge.textContent = closestBtn.dataset.label;
    } else {
        if (currentSize < 900) archetypeBadge.textContent = "Compact Studio";
        else if (currentSize < 1400) archetypeBadge.textContent = "2 BHK Apartment";
        else if (currentSize < 1900) archetypeBadge.textContent = "3 BHK Premium";
        else if (currentSize < 2400) archetypeBadge.textContent = "4 BHK Luxury";
        else archetypeBadge.textContent = "Estate Villa / Penthouse";
    }
}

function updateArchetypeUI(activeBtn, label) {
    archetypeButtons.forEach(btn => btn.classList.remove('active'));
    activeBtn.classList.add('active');
    archetypeBadge.textContent = label;
}

async function fetchModelParameters() {
    try {
        const res = await fetch('/api/model-info');
        const data = await res.json();
        if (data.status === 'success') {
            modelInfo.slope = data.model.slope;
            modelInfo.intercept = data.model.intercept;
            if (formulaDisplay) {
                formulaDisplay.textContent = `Price (Lakhs) = ${modelInfo.slope.toFixed(4)} × (Area sq ft) + ${modelInfo.intercept.toFixed(2)}`;
            }
            if (resultIntercept) {
                resultIntercept.textContent = `₹ ${modelInfo.intercept.toFixed(2)} Lakh`;
            }
            if (resultSlope) {
                resultSlope.textContent = `₹ ${Math.round(modelInfo.slope * 100000).toLocaleString('en-IN')} / sq ft`;
            }
            syncCalculations();
        }
    } catch (e) {
        console.warn('API model info fetched fallback to client baseline:', e);
    }
}

// Convert amount in Rupees to Lakhs / Crores string
function formatIndianUnits(amount) {
    if (amount >= 10000000) {
        // >= 1 Crore (1,00,00,000)
        return (amount / 10000000).toFixed(2) + ' Crore';
    } else if (amount >= 100000) {
        // >= 1 Lakh (1,00,000)
        return (amount / 100000).toFixed(2) + ' Lakh';
    } else if (amount >= 1000) {
        return (amount / 1000).toFixed(1) + ' Thousand';
    } else {
        return inrFormatter.format(amount);
    }
}

// Compute Estimated 20-Year Home Loan Monthly EMI (20% Down, 8.5% p.a.)
function calculateEMI(totalPriceRupees) {
    const loanAmount = totalPriceRupees * 0.80; // 80% financing
    const annualRate = 8.5; // 8.5% typical home loan interest in India
    const monthlyRate = annualRate / (12 * 100);
    const months = 20 * 12; // 240 months

    const emi = (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);
    
    if (emi >= 100000) {
        return `₹ ${(emi / 100000).toFixed(2)} L / mo`;
    } else {
        return `₹ ${inrFormatter.format(Math.round(emi))} / mo`;
    }
}

// Dynamic Real-time Calculations
function syncCalculations() {
    const size = parseFloat(areaInput.value);

    if (isNaN(size) || size <= 0) {
        resultPriceMain.textContent = '0';
        resultPriceFull.textContent = '₹ 0';
        resultPriceLakh.textContent = '₹0 Lakh';
        resultRate.textContent = '₹ 0 / sq ft';
        resultEmi.textContent = '₹ 0 / mo';
        return;
    }

    // Mathematical formula: Price (Lakhs) = slope * size + intercept
    const priceLakh = modelInfo.slope * size + modelInfo.intercept;
    const totalRupees = Math.round(priceLakh * 100000);
    const ratePerSqft = Math.round(totalRupees / size);

    // 1. Primary Headline Price (e.g. 2.71 Crore)
    resultPriceMain.textContent = formatIndianUnits(totalRupees);

    // 2. Full Amount with Indian Commas (e.g. ₹ 2,71,21,000)
    resultPriceFull.textContent = `₹ ${inrFormatter.format(totalRupees)}`;

    // 3. Lakh Subtitle
    resultPriceLakh.textContent = `₹${priceLakh.toFixed(2)} Lakh`;

    // 4. Rate per sq ft
    resultRate.textContent = `₹ ${inrFormatter.format(ratePerSqft)} / sq ft`;

    // 5. Estimated Loan EMI
    resultEmi.textContent = calculateEMI(totalRupees);

    // 6. Update Space Allocation Blueprint
    updateBlueprintAllocation(size);

    // 7. Update Dynamic SVG Regression Telemetry Chart
    updateSVGChartTelemetry(size, priceLakh);
}

// Proportionate Space Allocation Breakdown
function updateBlueprintAllocation(size) {
    if (blueprintCalcTag) {
        blueprintCalcTag.textContent = `${inrFormatter.format(Math.round(size))} SQ FT UNIT`;
    }
    if (planLiving) planLiving.textContent = `${Math.round(size * 0.35)} sq ft`;
    if (planMaster) planMaster.textContent = `${Math.round(size * 0.25)} sq ft`;
    if (planBed2) planBed2.textContent = `${Math.round(size * 0.20)} sq ft`;
    if (planUtil) planUtil.textContent = `${Math.round(size * 0.20)} sq ft`;
}

// Update SVG Live Radar Position
function updateSVGChartTelemetry(size, priceLakh) {
    if (!svgRadarDot || !svgCrosshairX) return;

    // SVG bounds: X in [40, 440], Y in [140, 20]
    const svgMinX = 40;
    const svgMaxX = 440;
    const svgMinY = 135; // lowest price
    const svgMaxY = 25;  // highest price

    const minSizeDomain = 500;
    const maxSizeDomain = 3000;
    const minPriceDomain = 100; // ~100 Lakhs
    const maxPriceDomain = 520; // ~520 Lakhs

    // Calculate clamped normalized ratio
    const sizeClamped = Math.max(minSizeDomain, Math.min(maxSizeDomain, size));
    const sizeRatio = (sizeClamped - minSizeDomain) / (maxSizeDomain - minSizeDomain);
    const targetX = svgMinX + sizeRatio * (svgMaxX - svgMinX);

    // Calculate Price Ratio along regression
    const priceClamped = Math.max(minPriceDomain, Math.min(maxPriceDomain, priceLakh));
    const priceRatio = (priceClamped - minPriceDomain) / (maxPriceDomain - minPriceDomain);
    const targetY = svgMinY - priceRatio * (svgMinY - svgMaxY);

    // Move SVG Elements
    svgRadarDot.setAttribute('cx', targetX);
    svgRadarDot.setAttribute('cy', targetY);

    if (svgRadarPulse) {
        svgRadarPulse.setAttribute('cx', targetX);
        svgRadarPulse.setAttribute('cy', targetY);
    }

    svgCrosshairX.setAttribute('x1', targetX);
    svgCrosshairX.setAttribute('x2', targetX);
    svgCrosshairX.setAttribute('y1', targetY);
}
