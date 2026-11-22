/**
 * House Price Predictor - Indian Currency & Numbering System (₹)
 * Formats prices in Indian Rupees (₹), Lakhs, and Crores.
 */

let modelInfo = {
    slope: 0.1656,
    intercept: 22.81
};

const areaInput = document.getElementById('area-input');
const btnPredict = document.getElementById('btn-predict');
const resultPriceMain = document.getElementById('result-price-main');
const resultPriceFull = document.getElementById('result-price-full');
const resultPriceLakh = document.getElementById('result-price-lakh');
const resultRate = document.getElementById('result-rate');
const chipButtons = document.querySelectorAll('.chip-btn');

// Formatter using Indian numbering system (e.g. 2,71,21,000)
const inrFormatter = new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0
});

document.addEventListener('DOMContentLoaded', async () => {
    setupEvents();
    await fetchModelParameters();
    calculatePrice();
});

function setupEvents() {
    areaInput.addEventListener('input', () => {
        calculatePrice();
        updateActiveChip();
    });

    areaInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            calculatePrice();
            triggerButtonFeedback();
        }
    });

    btnPredict.addEventListener('click', () => {
        calculatePrice();
        triggerButtonFeedback();
    });

    chipButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const size = btn.dataset.size;
            areaInput.value = size;
            calculatePrice();
            updateActiveChip();
            triggerButtonFeedback();
        });
    });
}

function triggerButtonFeedback() {
    btnPredict.style.transform = 'scale(0.98)';
    setTimeout(() => {
        btnPredict.style.transform = '';
    }, 120);
}

function updateActiveChip() {
    const val = parseFloat(areaInput.value);
    chipButtons.forEach(btn => {
        if (parseFloat(btn.dataset.size) === val) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

async function fetchModelParameters() {
    try {
        const res = await fetch('/api/model-info');
        const data = await res.json();
        if (data.status === 'success') {
            modelInfo.slope = data.model.slope;
            modelInfo.intercept = data.model.intercept;
            calculatePrice();
        }
    } catch (e) {
        console.error('Failed to load model parameters:', e);
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

// Core Prediction Calculation in Indian Rupees (₹)
function calculatePrice() {
    const size = parseFloat(areaInput.value);

    if (isNaN(size) || size <= 0) {
        resultPriceMain.textContent = '0';
        resultPriceFull.textContent = '₹ 0';
        resultPriceLakh.textContent = '(₹0 Lakh)';
        resultRate.textContent = '₹ 0 / sq ft';
        return;
    }

    // Model treats price in Lakhs:
    // e.g. 150 -> 150 Lakhs (1.5 Crore)
    // Formula: Price (Lakhs) = slope * size + intercept
    const slopeContribLakh = modelInfo.slope * size;
    const priceLakh = slopeContribLakh + modelInfo.intercept;
    
    // Total Price in Indian Rupees (1 Lakh = 100,000 Rupees)
    const totalRupees = Math.round(priceLakh * 100000);
    const ratePerSqft = Math.round(totalRupees / size);

    // Primary Display (e.g. 2.71 Crore or 85.50 Lakh)
    resultPriceMain.textContent = formatIndianUnits(totalRupees);

    // Full Amount with Indian comma grouping (e.g. ₹ 2,71,21,000)
    resultPriceFull.textContent = `₹ ${inrFormatter.format(totalRupees)}`;

    // In Lakhs (e.g. ₹271.21 Lakh)
    resultPriceLakh.textContent = `(₹${priceLakh.toFixed(2)} Lakh)`;

    // Rate per sq ft in Rupees
    resultRate.textContent = `₹ ${inrFormatter.format(ratePerSqft)} / sq ft`;
}
