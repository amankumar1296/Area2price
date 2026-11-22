# ============================================================
# HOUSE PRICE PREDICTION USING LINEAR REGRESSION
# AI/ML Foundations - Session 21
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# ------------------------------------------------------------
# 2. CREATE HOUSE PRICE DATASET
# ------------------------------------------------------------

# House sizes in square feet
sizes = np.array([
    750,
    1000,
    1200,
    1500,
    1800,
    2000,
    2200,
    2500
])

# House prices in thousands of dollars
prices = np.array([
    150,
    185,
    220,
    275,
    310,
    350,
    390,
    440
])


# ------------------------------------------------------------
# 3. EXPLORE THE DATA
# ------------------------------------------------------------

df = pd.DataFrame({
    "House Size (sq ft)": sizes,
    "Price ($K)": prices
})

print("\nHOUSE PRICE DATASET")
print("=" * 45)

print(df.to_string(index=True))

print("\nDataset Information")
print("-" * 45)

print(
    f"Minimum Size : {sizes.min()} sq ft"
)

print(
    f"Maximum Size : {sizes.max()} sq ft"
)

print(
    f"Minimum Price: ${prices.min()}K"
)

print(
    f"Maximum Price: ${prices.max()}K"
)


# ------------------------------------------------------------
# 4. VISUALIZE THE DATA
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    sizes,
    prices,
    color="blue",
    s=100,
    edgecolors="black"
)

for x, y in zip(sizes, prices):

    plt.annotate(
        f"${y}K",
        (x, y),
        textcoords="offset points",
        xytext=(5, 5)
    )

plt.xlabel("House Size (sq ft)")
plt.ylabel("Price ($K)")

plt.title("House Size vs House Price")

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 5. GRADIENT DESCENT FROM SCRATCH
# ============================================================

print("\n")
print("=" * 60)
print("GRADIENT DESCENT")
print("=" * 60)

# Initial values
m = 0.0
b = 0.0

# Learning rate (0.0000001 ensures numerical stability with unnormalized house sizes)
alpha = 0.0000001

# Number of data points
n = len(sizes)

# Store training history
history = []


# ------------------------------------------------------------
# Gradient Descent Training
# ------------------------------------------------------------

for epoch in range(3000):

    # Prediction
    y_pred_gd = m * sizes + b

    # Error
    error = y_pred_gd - prices

    # Gradient for slope
    dm = (2 / n) * np.dot(error, sizes)

    # Gradient for intercept
    db = (2 / n) * np.sum(error)

    # Update parameters
    m = m - alpha * dm

    b = b - alpha * db

    # Mean Squared Error
    mse = np.mean(error ** 2)

    # Save every 300 epochs
    if epoch % 300 == 0:

        history.append(
            (
                epoch,
                round(m, 4),
                round(b, 2),
                round(mse, 2)
            )
        )

        print(
            f"Epoch {epoch:4d} | "
            f"m = {m:7.4f} | "
            f"b = {b:7.2f} | "
            f"MSE = {mse:10.2f}"
        )


print("\nFinal Gradient Descent Parameters")

print(
    f"Slope (m)     = {m:.4f}"
)

print(
    f"Intercept (b) = {b:.2f}"
)


# ------------------------------------------------------------
# 6. VISUALIZE GRADIENT DESCENT
# ------------------------------------------------------------

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)


# ----- MSE curve -----

epochs_h = [
    h[0]
    for h in history
]

mses_h = [
    h[3]
    for h in history
]

axes[0].plot(
    epochs_h,
    mses_h,
    marker="o",
    linewidth=2
)

axes[0].set_xlabel("Epoch")

axes[0].set_ylabel("MSE")

axes[0].set_title(
    "MSE During Gradient Descent"
)

axes[0].grid(True)


# ----- Regression line evolution -----

x_range = np.linspace(
    700,
    2600,
    100
)

for epoch, slope, intercept, mse in history:

    axes[1].plot(
        x_range,
        slope * x_range + intercept,
        linewidth=1.5,
        alpha=0.7
    )


axes[1].scatter(
    sizes,
    prices,
    color="black",
    s=70
)

axes[1].set_xlabel(
    "House Size (sq ft)"
)

axes[1].set_ylabel(
    "Price ($K)"
)

axes[1].set_title(
    "Regression Line Learning"
)

axes[1].grid(True)


plt.tight_layout()

plt.show()


# ============================================================
# 7. PREPARE DATA FOR SCIKIT-LEARN
# ============================================================

# sklearn expects X to be 2-dimensional

X = sizes.reshape(-1, 1)

# Target variable

y = prices


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)


print("\n")
print("=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)

print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples :",
    len(X_test)
)


# ============================================================
# 9. TRAIN LINEAR REGRESSION MODEL
# ============================================================

model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# ============================================================
# 10. MAKE TEST PREDICTIONS
# ============================================================

y_pred = model.predict(
    X_test
)


# ============================================================
# 11. MODEL EVALUATION
# ============================================================

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    y_pred
)


print("\n")
print("=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(
    f"Slope     (m) = {model.coef_[0]:.4f}"
)

print(
    f"Intercept (b) = {model.intercept_:.2f}"
)

print("\nModel Equation:")

print(
    f"Price = {model.coef_[0]:.4f} × Size "
    f"+ {model.intercept_:.2f}"
)

print("\nEvaluation")

print(
    f"MSE  = {mse:.2f}"
)

print(
    f"RMSE = {rmse:.2f} ($K)"
)

print(
    f"R²   = {r2:.4f}"
)


# ============================================================
# 12. DISPLAY ACTUAL VS PREDICTED VALUES
# ============================================================

print("\n")
print("=" * 60)
print("ACTUAL VS PREDICTED")
print("=" * 60)

for size, actual, predicted in zip(
    X_test.flatten(),
    y_test,
    y_pred
):

    print(
        f"Size: {size:4d} sq ft | "
        f"Actual: ${actual:6.1f}K | "
        f"Predicted: ${predicted:6.1f}K"
    )


# ============================================================
# 13. REGRESSION LINE + RESIDUALS
# ============================================================

x_line = np.linspace(
    700,
    2600,
    100
).reshape(-1, 1)

y_line = model.predict(
    x_line
)

# Residual = Actual - Predicted

residuals = y_test - y_pred


fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)


# ------------------------------------------------------------
# Regression Line
# ------------------------------------------------------------

axes[0].scatter(
    X_train,
    y_train,
    label="Training Data",
    s=100
)

axes[0].scatter(
    X_test,
    y_test,
    label="Test Data",
    s=120,
    marker="^"
)

axes[0].plot(
    x_line,
    y_line,
    linewidth=2.5,
    label="Regression Line"
)


# Draw residual lines

for xi, yi, yp in zip(
    X_test.flatten(),
    y_test,
    y_pred
):

    axes[0].plot(
        [xi, xi],
        [yi, yp],
        linestyle="--",
        linewidth=1.5
    )


axes[0].set_xlabel(
    "House Size (sq ft)"
)

axes[0].set_ylabel(
    "Price ($K)"
)

axes[0].set_title(
    "Regression Line + Residuals"
)

axes[0].legend()

axes[0].grid(True)


# ------------------------------------------------------------
# Residual Plot
# ------------------------------------------------------------

axes[1].bar(
    range(len(y_test)),
    residuals
)

axes[1].axhline(
    0,
    linestyle="--",
    linewidth=1.5
)

axes[1].set_xlabel(
    "Test House Number"
)

axes[1].set_ylabel(
    "Error ($K)"
)

axes[1].set_title(
    f"Residuals | RMSE = {rmse:.2f}K"
)

axes[1].grid(True)


plt.tight_layout()

plt.show()


# ============================================================
# 14. PREDICT NEW HOUSE PRICES
# ============================================================

print("\n")
print("=" * 60)
print("HOUSE PRICE PREDICTIONS")
print("=" * 60)


# New houses

test_houses = [
    900,
    1350,
    1750,
    2100,
    2400
]


# Convert to 2D array

new_house_data = np.array(
    test_houses
).reshape(-1, 1)


# Predict prices

predictions = model.predict(
    new_house_data
)


# ------------------------------------------------------------
# Display predictions
# ------------------------------------------------------------

print(
    f"{'Size (sq ft)':<20}"
    f"{'Predicted Price':>20}"
)

print("-" * 40)


for size, prediction in zip(
    test_houses,
    predictions
):

    print(
        f"{size:<20,}"
        f"${prediction * 1000:>18,.0f}"
    )


print("-" * 40)


# ============================================================
# 15. MODEL SUMMARY
# ============================================================

print("\nMODEL SUMMARY")
print("=" * 60)

print(
    f"Equation: Price = "
    f"{model.coef_[0]:.2f} × Size "
    f"+ {model.intercept_:.2f}"
)

print(
    f"R² Score: {r2:.4f}"
)

print(
    f"Model explains approximately "
    f"{r2 * 100:.1f}% of price variation."
)


# ============================================================
# 16. BAR CHART OF NEW PREDICTIONS
# ============================================================

plt.figure(
    figsize=(9, 5)
)

bars = plt.bar(
    [str(x) for x in test_houses],
    predictions * 1000
)


# Add price labels

for bar, value in zip(
    bars,
    predictions
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"${value * 1000:,.0f}",
        ha="center",
        va="bottom"
    )


plt.xlabel(
    "House Size (sq ft)"
)

plt.ylabel(
    "Predicted Price ($)"
)

plt.title(
    "Predicted House Prices"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.show()


# ============================================================
# 17. CUSTOM HOUSE PREDICTION
# ============================================================

print("\n")
print("=" * 60)
print("CUSTOM HOUSE PRICE PREDICTOR")
print("=" * 60)


# Change this value to predict another house

custom_size = 1600


custom_prediction = model.predict(
    np.array([[custom_size]])
)[0]


print(
    f"\nHouse Size: {custom_size:,} sq ft"
)

print(
    f"Predicted Price: "
    f"${custom_prediction * 1000:,.0f}"
)


# ============================================================
# PROJECT COMPLETE
# ============================================================

print("\n")
print("=" * 60)
print("HOUSE PRICE PREDICTION PROJECT COMPLETED!")
print("=" * 60)
