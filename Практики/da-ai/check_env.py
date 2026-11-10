"""Проверка среды для практик «Анализ данных и ИИ».

Запуск:  uv run python check_env.py
Скрипт проверяет, что все библиотеки импортируются и работают,
и сохраняет тестовый график в файл check_plot.png.
"""
import importlib
import platform
import sys
import time
import warnings

warnings.filterwarnings("ignore")

OK, FAIL = "[ OK ]", "[FAIL]"
errors = 0


def step(name, func):
    global errors
    t = time.perf_counter()
    try:
        info = func()
        print(f"{OK} {name:<18} {info or ''}  ({time.perf_counter() - t:.1f} с)")
    except Exception as exc:  # noqa: BLE001
        errors += 1
        print(f"{FAIL} {name:<18} {type(exc).__name__}: {exc}")


print(f"Python {sys.version.split()[0]} | {platform.system()} {platform.release()} | {platform.machine()}")
print("-" * 60)

for mod in ["numpy", "pandas", "matplotlib", "seaborn", "sklearn",
            "lightgbm", "shap", "openpyxl", "streamlit", "jupyterlab"]:
    step(mod, lambda m=mod: getattr(importlib.import_module(m), "__version__", ""))


def test_pandas():
    import pandas as pd
    df = pd.DataFrame({"город": ["Пермь", "Тюмень", "Пермь"], "x": [1, 2, 3]})
    return f"groupby -> {df.groupby('город')['x'].sum().to_dict()}"


def test_sklearn():
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    X, y = make_classification(n_samples=500, random_state=0)
    return f"accuracy на обучении = {LogisticRegression(max_iter=500).fit(X, y).score(X, y):.2f}"


def test_lightgbm():
    import lightgbm as lgb
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=500, random_state=0)
    m = lgb.LGBMClassifier(n_estimators=20, verbose=-1).fit(X, y)
    return f"обучено деревьев: {m.n_estimators}"


def test_shap():
    import lightgbm as lgb
    import shap
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=300, n_features=5, random_state=0)
    m = lgb.LGBMClassifier(n_estimators=20, verbose=-1).fit(X, y)
    sv = shap.TreeExplainer(m).shap_values(X[:10])
    return f"значения SHAP посчитаны, форма {getattr(sv, 'shape', '?')}"


def test_plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["Пермь", "Тюмень"], [3, 2])
    ax.set_title("Кириллица в подписях")
    fig.savefig("check_plot.png", dpi=80, bbox_inches="tight")
    return "график сохранён в check_plot.png"


step("pandas: расчёт", test_pandas)
step("sklearn: модель", test_sklearn)
step("lightgbm: модель", test_lightgbm)
step("shap: расчёт", test_shap)
step("matplotlib: файл", test_plot)

print("-" * 60)
if errors:
    print(f"Найдено проблем: {errors}. Покажите этот экран преподавателю.")
    sys.exit(1)
print("СРЕДА ГОТОВА. Можно запускать Jupyter.")
