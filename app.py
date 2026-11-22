import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(basedir, "templates"),
    static_folder=os.path.join(basedir, "static")
)

# ------------------------------------------------------------
# 1. DATASET SETUP & ML MODEL TRAINING
# ------------------------------------------------------------
sizes = np.array([750, 1000, 1200, 1500, 1800, 2000, 2200, 2500])
prices = np.array([150, 185, 220, 275, 310, 350, 390, 440])

# Prepare for Scikit-Learn
X = sizes.reshape(-1, 1)
y = prices

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train Scikit-Learn Linear Regression
sklearn_model = LinearRegression()
sklearn_model.fit(X_train, y_train)

y_pred_test = sklearn_model.predict(X_test)
mse_sklearn = mean_squared_error(y_test, y_pred_test)
rmse_sklearn = np.sqrt(mse_sklearn)
r2_sklearn = r2_score(y_test, y_pred_test)

slope_sklearn = float(sklearn_model.coef_[0])
intercept_sklearn = float(sklearn_model.intercept_)

# ------------------------------------------------------------
# 2. GRADIENT DESCENT FROM SCRATCH
# ------------------------------------------------------------
m_gd = 0.0
b_gd = 0.0
alpha_m = 0.0000001   # Stable learning rate for slope
alpha_b = 0.01        # Stable learning rate for intercept
n = len(sizes)
gd_history = []

for epoch in range(3001):
    y_pred_gd = m_gd * sizes + b_gd
    error = y_pred_gd - prices
    dm = (2 / n) * np.dot(error, sizes)
    db = (2 / n) * np.sum(error)
    m_gd = m_gd - alpha_m * dm
    b_gd = b_gd - alpha_b * db
    mse = float(np.mean(error ** 2))

    if epoch % 150 == 0:
        gd_history.append({
            "epoch": int(epoch),
            "m": round(float(m_gd), 4),
            "b": round(float(b_gd), 2),
            "mse": round(mse, 2)
        })

gd_final = {
    "m": round(float(m_gd), 4),
    "b": round(float(b_gd), 2)
}

# Pre-calculate benchmark test houses
benchmark_sizes = [900, 1350, 1750, 2100, 2400]
benchmark_preds = sklearn_model.predict(np.array(benchmark_sizes).reshape(-1, 1))

# Continuous line points for chart rendering (500 to 3000 sq ft)
line_x = np.linspace(500, 3000, 60)
line_y = sklearn_model.predict(line_x.reshape(-1, 1))
regression_line_data = [{"size": round(float(x), 1), "price": round(float(yp), 2)} for x, yp in zip(line_x, line_y)]


# ------------------------------------------------------------
# 3. ROUTES & API
# ------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/model-info", methods=["GET"])
def get_model_info():
    test_results = []
    for x_val, actual, pred in zip(X_test.flatten(), y_test, y_pred_test):
        test_results.append({
            "size": int(x_val),
            "actual": float(actual),
            "predicted": round(float(pred), 2),
            "residual": round(float(actual - pred), 2)
        })

    train_data = [
        {"size": int(x), "price": float(p)}
        for x, p in zip(X_train.flatten(), y_train)
    ]

    all_data = [
        {"size": int(x), "price": float(p)}
        for x, p in zip(sizes, prices)
    ]

    benchmarks = [
        {
            "size": int(s),
            "predicted_k": round(float(p), 2),
            "predicted_usd": round(float(p * 1000), 2)
        }
        for s, p in zip(benchmark_sizes, benchmark_preds)
    ]

    avg_price_per_sqft = float(np.mean(prices * 1000 / sizes))

    return jsonify({
        "status": "success",
        "model": {
            "slope": round(slope_sklearn, 4),
            "intercept": round(intercept_sklearn, 2),
            "equation": f"Price = {slope_sklearn:.4f} × Size + {intercept_sklearn:.2f}",
            "r2": round(r2_sklearn, 4),
            "mse": round(mse_sklearn, 2),
            "rmse": round(rmse_sklearn, 2),
            "avg_price_per_sqft": round(avg_price_per_sqft, 2)
        },
        "gd_model": {
            "final": gd_final,
            "history": gd_history,
            "learning_rate": alpha_m,
            "total_epochs": 3000
        },
        "dataset": {
            "all": all_data,
            "train": train_data,
            "test": test_results,
            "regression_line": regression_line_data,
            "benchmarks": benchmarks,
            "min_size": int(sizes.min()),
            "max_size": int(sizes.max()),
            "min_price": float(prices.min()),
            "max_price": float(prices.max())
        }
    })


@app.route("/api/predict", methods=["GET", "POST"])
def predict():
    try:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            size = float(data.get("size", 1600))
        else:
            size = float(request.args.get("size", 1600))

        if size <= 0:
            return jsonify({"status": "error", "message": "House size must be greater than 0"}), 400

        pred_k = float(sklearn_model.predict(np.array([[size]]))[0])
        pred_usd = pred_k * 1000
        gd_pred_k = float(m_gd * size + b_gd)
        gd_pred_usd = gd_pred_k * 1000

        slope_component = slope_sklearn * size
        price_per_sqft = pred_usd / size

        return jsonify({
            "status": "success",
            "size": size,
            "predicted_k": round(pred_k, 2),
            "predicted_usd": round(pred_usd, 2),
            "gd_predicted_k": round(gd_pred_k, 2),
            "gd_predicted_usd": round(gd_pred_usd, 2),
            "price_per_sqft": round(price_per_sqft, 2),
            "breakdown": {
                "slope_contribution": round(slope_component, 2),
                "intercept_contribution": round(intercept_sklearn, 2),
                "formula": f"(${slope_sklearn:.4f} × {size:,.0f}) + ${intercept_sklearn:.2f}K = ${pred_k:,.2f}K"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/batch-predict", methods=["POST"])
def batch_predict():
    try:
        data = request.get_json() or {}
        custom_sizes = data.get("sizes", [])
        if not custom_sizes:
            return jsonify({"status": "error", "message": "No sizes provided"}), 400

        preds = sklearn_model.predict(np.array(custom_sizes).reshape(-1, 1))
        results = [
            {
                "size": int(s),
                "predicted_k": round(float(p), 2),
                "predicted_usd": round(float(p * 1000), 2)
            }
            for s, p in zip(custom_sizes, preds)
        ]
        return jsonify({"status": "success", "predictions": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting House Price Predictor UI on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
