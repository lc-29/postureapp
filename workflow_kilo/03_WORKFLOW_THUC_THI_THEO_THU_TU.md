# 03. Workflow thuc thi theo thu tu

Dung file nay de biet nen giao task nao truoc cho Kilo Code Auto Free.

## Luong 1 - On dinh repo va tai lieu

1. TASK-001: sua README.
2. TASK-002: sua encoding file nho.
3. TASK-003: tao dataset manifest.
4. TASK-004: tao protocol thuc nghiem.

Ket qua mong doi: nguoi moi doc repo hieu can chay gi, du lieu hien co ra sao.

## Luong 2 - Test an toan

1. TASK-005: bien test webcam thanh manual/skip.
2. TASK-006: them unit test utils.
3. TASK-007: tao module baseline chung.
4. TASK-008: GUI dung module baseline chung.
5. TASK-009: test baseline voi landmark gia lap.
6. TASK-010: chuan hoa config.

Ket qua mong doi: co nen test nhanh, giam copy-paste logic, code de bao tri hon.

## Luong 3 - Danh gia khoa hoc

1. TASK-011: external evaluation.
2. TASK-012: threshold sweep.
3. TASK-013: video-wise evaluation placeholder.
4. TASK-014: feature extraction co metadata.
5. TASK-015: train script chap nhan metadata.
6. TASK-016: smoke train.
7. TASK-017: compare rule-based vs ANN.
8. TASK-018: ablation study nho.

Ket qua mong doi: co bang ket qua du tin cay hon de viet bao cao, dong thoi noi ro gioi han.

## Luong 4 - App va demo

1. TASK-019: kiem tra logging SQLite.
2. TASK-020: export thong ke.
3. TASK-021: message loi than thien.
4. TASK-022: huong dan demo video.
5. TASK-023: manual QA GUI.

Ket qua mong doi: demo duoc truoc hoi dong, co du lieu thong ke xuat ra.

## Luong 5 - Bao cao Springer va ban giao

1. TASK-024: skeleton paper.
2. TASK-025: method draft.
3. TASK-026: results draft.
4. TASK-027: figure/table plan.
5. TASK-028: related work todo.
6. TASK-029: final delivery checklist.
7. TASK-030: technical debt.

Ket qua mong doi: co bo khung paper, artifact, checklist va danh sach phan con yeu.

## Milestone hoan thanh

### Milestone M1 - Chay duoc va doc duoc

- TASK-001 den TASK-006 xong.
- `pytest` khong tu dong mo webcam.
- README khong loi encoding.

### Milestone M2 - Code sach hon

- TASK-007 den TASK-010 xong.
- Baseline logic co module dung chung.
- Co test baseline.

### Milestone M3 - Co ket qua khoa hoc

- TASK-011, TASK-012, TASK-013 xong.
- Neu co thoi gian: TASK-014 den TASK-018.
- Co local + external metrics va noi ro rui ro frame-wise split.

### Milestone M4 - San sang demo

- TASK-019 den TASK-023 xong.
- GUI QA checklist da tick thu cong.
- Export thong ke chay duoc.

### Milestone M5 - San sang viet/nop bao cao

- TASK-024 den TASK-030 xong.
- Co paper outline, method, results, figure/table plan.

## Cach giao viec hang ngay cho Kilo Code

Moi ngay chi nen giao 2-4 task nho. Vi du:

```text
Hom nay lam TASK-001. Chi sua README.md. Khong sua code.
```

Sau khi task pass:

```text
Lam tiep TASK-002. Chi sua docstring/comment trong cac file duoc phep.
```

Neu Kilo Code bi loi do dependency:

- Yeu cau no ghi ro dependency thieu.
- Khong de no cai goi moi neu khong can.
- Uu tien `py_compile` va test nho thay vi chay full app.
