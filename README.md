# 🏡 House Price Prediction using Linear Regression & Gradient Descent
**AI/ML Foundations - Session 21**

An interactive Machine Learning project implementing Scikit-Learn Linear Regression and Gradient Descent from scratch, coupled with a luxury glassmorphism web dashboard.

---

## 🚀 Quick Start

### 1. Launch the Web UI (Interactive Dashboard)
Double-click `run_app.bat` or run:
```bash
python app.py
```
Then visit **[http://localhost:5000](http://localhost:5000)** in your web browser.

### 2. Run the Original Standalone ML Script
Double-click `run_cli.bat` or run:
```bash
python house_price_prediction.py
```

---

## ✨ Features

- **Linear Regression Pipeline**:
  - Dataset exploration, summary statistics, and size-to-price mapping.
  - 75% / 25% Train-Test split.
  - Evaluation metrics: $R^2$ Score (0.9859), Mean Squared Error (MSE), Root Mean Squared Error (RMSE).
- **Gradient Descent from Scratch**:
  - Iterative parameter updates ($m$ slope and $b$ intercept) over 3,000 epochs.
  - Step-by-step history and MSE convergence tracking.
- **Modern Web Dashboard**:
  - **Real-Time Interactive Predictor**: Adjust house size via slider or input and receive instantaneous price valuations in `$K` and `$ USD`.
  - **Calculation Breakdown**: Full transparency into $Price = m \times Size + b$, plus estimated 30-year mortgage rates.
  - **Dynamic Chart.js Visualizations**:
    - Scatter plots with training points, test points, regression line, and live prediction marker.
    - Toggleable residual lines.
    - Gradient Descent loss curve and line evolution scrubber/player.
    - Residuals & error bar chart.
  - **Benchmark Predictions Table**: Test properties (900, 1350, 1750, 2100, 2400 sq ft) plus custom house valuation.
  - **Complete Dataset Explorer**: Full 8-property data table with split categorization and individual predict actions.

---

## 📁 Project Structure

```
HOUSE PREDICTION/
├── app.py                      # Flask web server & REST API
├── house_price_prediction.py   # Standalone ML pipeline script with Matplotlib plots
├── templates/
│   └── index.html              # Modern glassmorphism HTML5 template
├── static/
│   ├── style.css               # Luxury dark design system & responsive styling
│   └── app.js                  # Real-time calculations & Chart.js engine
├── run_app.bat                 # 1-click launcher for the Web UI
├── run_cli.bat                 # 1-click launcher for the CLI script
└── README.md                   # Documentation
```
