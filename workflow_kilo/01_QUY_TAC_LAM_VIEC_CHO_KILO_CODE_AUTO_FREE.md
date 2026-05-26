# 01. Quy tac lam viec cho Kilo Code Auto Free

File nay dung de giao viec cho Kilo Code khi dung model Auto Free. Nguyen tac chinh: moi lan chi giao mot nhiem vu nho, ro dau vao/dau ra, it file, co cach kiem tra cu the.

## Gioi han moi phien lam viec

- Chi lam 1 task ID moi lan.
- Uu tien sua 1-3 file moi task.
- Khong refactor lon neu task khong yeu cau.
- Khong train model dai, khong chay webcam, khong mo GUI neu khong duoc yeu cau rieng.
- Khong xoa dataset, model, database hay video.
- Truoc khi sua file, doc file lien quan va ghi tom tat ngan.
- Sau khi sua, chay lenh kiem tra nho nhat co the.
- Neu task qua lon, dung lai va de xuat tach thanh task con.

## Mau prompt nen dua cho Kilo Code

```text
Ban dang lam trong repo posture_detection_app.
Hay thuc hien dung task [TASK_ID] trong workflow_kilo/02_BACKLOG_NHIEM_VU_DEN_KHI_HOAN_THANH.md.

Yeu cau:
- Chi sua cac file duoc task cho phep.
- Khong xoa dataset/model/database/video.
- Khong chay webcam/GUI/training dai.
- Neu can refactor ngoai pham vi, hay dung lai va bao cao.
- Sau khi sua, chay lenh verify trong task.
- Tra loi bang: file da sua, thay doi chinh, lenh verify va ket qua.
```

## Cach doc backlog

Moi task co cac truong:

- `Muc tieu`: tai sao can lam.
- `Pham vi`: file/thu muc duoc sua.
- `Cach lam goi y`: huong di de model free khong phai tu suy luan qua rong.
- `Verify`: lenh hoac buoc kiem tra.
- `Done khi`: tieu chi chap nhan.

## Thu tu uu tien

1. Tai lieu va encoding de nguoi khac doc duoc.
2. Test nho va import an toan.
3. Tach module dung chung de giam trung lap.
4. Script danh gia external/subject-wise.
5. Cai tien ung dung va logging.
6. Chuan bi bao cao Springer.

## Lenh an toan nen dung

```powershell
python -m pytest tests/test_imports.py
python -m pytest tests/test_utils.py
python src/3_database_setup.py
python src/5_train_ann_local.py --epochs 2 --patience 1 --output-dir models/tmp_smoke
```

Lenh can tranh trong model free neu khong co task ro:

```powershell
python src/4_main_desktop_app.py
python src/1_rule_based_baseline.py
python src/2_extract_features.py
python src/5_train_ann_local.py
```

Ly do: cac lenh nay co the mo camera/GUI, xu ly video lau hoac train lau.

## Quy tac dat ten branch/commit neu co Git sau nay

- Branch: `task/TASK_ID-mo-ta-ngan`
- Commit: `TASK_ID: mo ta thay doi`
- Vi du: `TASK-006: add external evaluation script`

Repo hien tai khong co `.git`, nen chua ap dung commit.
