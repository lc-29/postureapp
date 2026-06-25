# Model Selection Report

Train dataset: `D:\posture_detection_app\dataset\processed\posture_data_2fps_combined_features.csv`

External dataset: `D:\posture_detection_app\dataset\processed\posture_external_test_2fps_combined_features.csv`

Registry: `D:\posture_detection_app\models\model_registry.json`

Selected model: `random_forest__ergonomic_14`

Selection rule: highest incorrect-class F1, then recall, then MCC.

## Ranked Models

| model_id | feature_count | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random_forest__ergonomic_14 | 14 | 0.821554 | 0.794655 | 0.919374 | 0.852477 | 0.813353 | 0.640480 | 0.822246 | 0.848708 | 0.059000 |
| logistic_regression__ergonomic_14 | 14 | 0.835382 | 0.947447 | 0.747945 | 0.835958 | 0.835380 | 0.694387 | 0.922632 | 0.933502 | 0.002000 |
| random_forest__normalized_99 | 99 | 0.771730 | 0.748442 | 0.893151 | 0.814418 | 0.758977 | 0.537798 | 0.858459 | 0.885517 | 0.074000 |
| hist_gradient_boosting__ergonomic_14 | 14 | 0.791264 | 0.824434 | 0.797652 | 0.810822 | 0.789009 | 0.578552 | 0.844196 | 0.860150 | 0.017000 |
| hist_gradient_boosting__combined_normalized_ergonomic | 113 | 0.776997 | 0.805478 | 0.794129 | 0.799764 | 0.774077 | 0.548253 | 0.812135 | 0.847777 | 0.015000 |
| random_forest__combined_raw_ergonomic | 113 | 0.693591 | 0.649471 | 0.985519 | 0.782960 | 0.631032 | 0.426939 | 0.782956 | 0.808605 | 0.084000 |
| random_forest__raw_99 | 99 | 0.692713 | 0.649186 | 0.983562 | 0.782135 | 0.630457 | 0.423371 | 0.732017 | 0.737897 | 0.062000 |
| svm_rbf__combined_normalized_ergonomic | 113 | 0.734197 | 0.724599 | 0.848532 | 0.781684 | 0.720996 | 0.456500 | 0.767976 | 0.810802 | 0.354000 |
| hist_gradient_boosting__raw_99 | 99 | 0.670764 | 0.630602 | 0.996869 | 0.772520 | 0.588405 | 0.393123 | 0.547026 | 0.600233 | 0.013000 |
| hist_gradient_boosting__normalized_99 | 99 | 0.673837 | 0.636248 | 0.976908 | 0.770608 | 0.603224 | 0.378464 | 0.700185 | 0.764083 | 0.017000 |
| svm_rbf__normalized_99 | 99 | 0.666155 | 0.627844 | 0.993738 | 0.769511 | 0.582129 | 0.379665 | 0.791504 | 0.836069 | 0.368000 |
| hist_gradient_boosting__combined_raw_ergonomic | 113 | 0.653863 | 0.618862 | 0.996477 | 0.763533 | 0.559007 | 0.356935 | 0.833311 | 0.870081 | 0.015000 |
| random_forest__combined_normalized_ergonomic | 113 | 0.723003 | 0.768369 | 0.724462 | 0.745770 | 0.720763 | 0.443028 | 0.827048 | 0.859353 | 0.073000 |
| svm_rbf__combined_raw_ergonomic | 113 | 0.597015 | 0.581872 | 1.000000 | 0.735675 | 0.444015 | 0.219044 | 0.662816 | 0.729730 | 0.281000 |
| mlp_sklearn__raw_99 | 99 | 0.583845 | 0.574028 | 1.000000 | 0.729375 | 0.414545 | 0.173555 | 0.573864 | 0.604353 | 0.007000 |
| mlp_sklearn__combined_raw_ergonomic | 113 | 0.582090 | 0.573593 | 0.992955 | 0.727142 | 0.417461 | 0.148659 | 0.646912 | 0.658693 | 0.009000 |
| svm_rbf__raw_99 | 99 | 0.575505 | 0.569169 | 1.000000 | 0.725440 | 0.395118 | 0.138049 | 0.645932 | 0.689481 | 0.311000 |
| logistic_regression__combined_normalized_ergonomic | 113 | 0.750658 | 0.972056 | 0.571820 | 0.720059 | 0.747643 | 0.581425 | 0.775520 | 0.856831 | 0.007000 |
| svm_rbf__ergonomic_14 | 14 | 0.617428 | 0.692053 | 0.572603 | 0.626687 | 0.617192 | 0.246069 | 0.697727 | 0.778356 | 0.469000 |
| logistic_regression__combined_raw_ergonomic | 113 | 0.681738 | 0.973436 | 0.444618 | 0.610425 | 0.670704 | 0.487902 | 0.765358 | 0.840618 | 0.008000 |

## Interpretation

- The selected model is the best model within this local protocol only.
- It must not be described as state-of-the-art against literature because datasets and protocols differ.
- If the selected model is not the current ANN app model, the app should load this registry before deployment.
