# Deployment QA Report

Ngay cap nhat: 2026-05-27

## QA status

| Hang muc | Trang thai | Ghi chu |
|---|---|---|
| Runtime path helper | DONE | `src/runtime_paths.py`. |
| First-run database init | DONE | `ensure_runtime_database()`. |
| PyInstaller spec | DONE | `build_scripts/posture_app.spec`. |
| Build script | DONE | `build_scripts/build_desktop_app.ps1`. |
| Dist smoke script | DONE | `build_scripts/smoke_test_dist.ps1`. |
| User README | DONE | `release_docs/README_RUN_APP.md`. |
| Release notes | DONE | `reports/DEPLOYMENT_RELEASE_NOTES.md`. |
| PyInstaller build | DONE | `dist/PostureDetectionApp/PostureDetectionApp.exe`. |
| Portable release zip | DONE | `release/PostureDetectionApp_0.1.0-demo.zip`. |
| Clean machine manual QA | PENDING | Can copy zip sang may Windows khong cai Python de test. |

## Build result

| Artifact | Value |
|---|---|
| Exe | `dist/PostureDetectionApp/PostureDetectionApp.exe` |
| Release folder | `release/PostureDetectionApp_0.1.0-demo/` |
| Release zip | `release/PostureDetectionApp_0.1.0-demo.zip` |
| Zip size | 661,155,257 bytes |
| Smoke script | PASS: runtime files OK |
| Expected runtime DB | `%LOCALAPPDATA%\PostureDetectionApp\posture_app.db` |

## SHA256

```text
CC5C2E2BD196229E7D0C755822493A8C86E969F4B5FF20375EA87C0C8C4C0482  dist/PostureDetectionApp/PostureDetectionApp.exe
CB19FEF50F3A46FBC53E3E903EB3ED0D0CDC99FFE5A91C608B6AF150F692A25F  dist/PostureDetectionApp/_internal/models/ann_best.keras
79E43E71E5D42DDAA92C29675003D243E283668DA3DF7CBD78372DA85F04036D  dist/PostureDetectionApp/_internal/models/scaler.pkl
904CCE2F3AA4B7828629D36F17DE2E6041CF34C2A8A544A53A80E7A012122607  release/PostureDetectionApp_0.1.0-demo.zip
```

## Manual QA checklist after build

- Double-click `dist/PostureDetectionApp/PostureDetectionApp.exe`.
- App opens without Python activated.
- Runtime DB appears at `%LOCALAPPDATA%\PostureDetectionApp\posture_app.db`.
- Model/scaler load in ANN mode.
- Webcam index `0` starts.
- Video file starts.
- Stop saves session.
- Light/Dark toggle works.
- Statistics dashboard opens.
- App closes without hanging.

## Notes

If the build fails because of TensorFlow/MediaPipe hidden imports or DLLs, keep
PyInstaller `onedir`, inspect the missing module name, and add it to
`hiddenimports` in `build_scripts/posture_app.spec`.
