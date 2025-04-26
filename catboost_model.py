import catboost as cb
import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error


base_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/training"
df = pd.read_feather(os.path.join(base_dir, "df_train.feather"))

""" ====================================================================================================================
    TRAIN / TEST SPLIT
==================================================================================================================== """
random_state = 21

val_size = 0.15
test_size = 0.15

features = ['covid', 'dow', 'year', 'bday', 'holiday', 'hurs', 'pr', 'rlds', 'rsds', 'sfcWind', 'tas', 'tasmax', 'tasmin'] + \
           [x + '_lag3' for x in ['hurs', 'pr', 'rlds', 'rsds', 'sfcWind', 'tas', 'tasmax', 'tasmin']]

#[x + '_lag' for x in [ 'hurs', 'pr', 'rlds', 'rsds', 'sfcWind', 'tasmax', 'tasmin']] + \
response = 'load'

X_train, X_val, y_train, y_val = train_test_split(
    df.dropna()[features], df.dropna()[response], test_size=val_size, random_state=random_state)

X_train, X_test, y_train, y_test = train_test_split(
    X_train, y_train, test_size=test_size/(1-val_size), random_state=random_state)

""" ====================================================================================================================
    CATBOOST
==================================================================================================================== """

model = cb.CatBoostRegressor(
    iterations=10000,
    depth=8,
    loss_function='RMSE'
)

f = model.fit(X_train, y_train, eval_set = (X_val, y_val))

""" ====================================================================================================================
    TEST PREDICTIONS AND METRICS
==================================================================================================================== """

y_test_pred = f.predict(X_test)

r2 = r2_score(y_test_pred, y_test)
print(r2)

mae = mean_absolute_error(y_test_pred, y_test)
print(mae)

rmse = root_mean_squared_error(y_test_pred, y_test)
print(rmse)

""" ====================================================================================================================
    RESIDUALS
==================================================================================================================== """

fig, ax = plt.subplots()
ax.scatter(y_test, y_test_pred, color='black', s=0.8, alpha=0.7)
ax.plot([5000, 11000], [5000, 11000], color='red')
ax.grid()
ax.set_title("Observed vs. Predicted Load")
ax.set_xlabel("Observed")
ax.set_ylabel("Predicted")
plt.show()

fig, ax = plt.subplots()
ax.scatter(y_test, y_test_pred-y_test, color='black', s=0.8, alpha=0.7)
ax.plot([5000, 11000], [0, 0], color='red')
ax.grid()
ax.set_title("Observed vs. Residual Load")
ax.set_xlabel("Observed")
ax.set_ylabel("Residual")
plt.show()

""" ====================================================================================================================
    FEATURES
==================================================================================================================== """

import pandas as pd
import matplotlib.pyplot as plt

# Get feature importance
importances = model.get_feature_importance()
feature_names = model.feature_names_

# Plot
pd.Series(importances, index=feature_names).sort_values().plot(kind='barh', figsize=(8, 6))
plt.title("CatBoost Feature Importance")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.show()

# Partial dependence plots
df_importance = pd.DataFrame({
    'importance' :importances,
    'feature':feature_names}).sort_values('importance', ascending=False)

for i in df_importance.head(5).index:
    _ = f.plot_partial_dependence(cb.Pool(X_test, y_test), features=[i])
    x = _[1]['layout']['xaxis']['tickvals']
    y = _[1]['data'][0]['y']

    fig, ax = plt.subplots(figsize=(3.5,2.7))
    ax.get_xaxis().set_visible(False)
    ax.plot(x,y)
    ax.set_title(df_importance.loc[i, 'feature'])
    plt.tight_layout()
    plt.show()

""" ====================================================================================================================
    PROJECTIONS - MAX
====================================================================================================== """

df['year_actual'] = df['year']
df['year'] = 2024
df['load_predict'] = f.predict(df[features])

pred99 = df.groupby('year_actual')['load_predict'].max()
#true99 = df.groupby('year_actual')['load'].max()
pred99 = pred99[pred99.index >= 2025]

fig, ax = plt.subplots()
ax.plot(pred99)
ax.set_title("Annual Maximum of Peak Load (Projected 2025-2100)")
ax.set_xlabel("Year")
ax.set_ylabel("Load")
plt.show()

""" ====================================================================================================================
    PROJECTIONS - THRESHOLD
==================================================================================================================== """

q = df[df['year_actual'].between(2020, 2024)]['load_predict'].quantile(0.95)
excess = df[df['load_predict'] >= q]['year_actual'].value_counts().reset_index().sort_values('year_actual')
excess = excess[excess['year_actual'] >= 2025]

fig, ax = plt.subplots()
ax.bar(x=excess['year_actual'], height=excess['count'], width=1.0)
ax.set_title("Days Exceeding Baseline p95 Peak Load (Projected 2025-2100)")
ax.set_xlabel("Year")
ax.set_ylabel("Days")
plt.show()