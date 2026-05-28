# Data Availability And Ethics Statement

Ngay cap nhat: 2026-05-27

## Data availability

Du lieu hien co trong project gom:

- Raw training videos trong `dataset/raw_videos/`.
- Raw external videos trong `dataset/external_videos/`.
- Processed landmark CSV trong `dataset/posture_data_2fps.csv` va `dataset/posture_external_test_2fps.csv`.
- Ket qua thuc nghiem trong `reports/results/`.

Raw videos hien tai la du lieu cuc bo cua project va chua duoc cong bo nhu mot public benchmark. Neu nop bao cao/paper, nen ghi:

> The dataset used in this study is project-specific and currently available locally for academic assessment. Public release requires privacy review because videos may contain identifiable body/face information.

## Privacy considerations

Video posture data co the chua thong tin nhan dien ca nhan:

- Khuon mat hoac mot phan khuon mat.
- Dang nguoi, ti le co the, trang phuc.
- Khong gian lam viec/hoc tap xung quanh.

Vi vay, neu chia se du lieu ra ngoai, can:

1. Xin dong y ro rang cua nguoi tham gia.
2. An danh ten file neu can.
3. Cat/blur vung nhan dien neu phu hop.
4. Khong dua raw videos len public repository neu chua co consent.
5. Chia se landmark CSV thay vi raw video khi muc tieu chi la tai lap thuat toan.

## Intended use

He thong duoc thiet ke de:

- Ho tro nhac nho tu the khi lam viec voi may tinh.
- Minh hoa pipeline AI ung dung voi webcam va MediaPipe.
- Phuc vu do an/khoa luan/thuc nghiem hoc thuat.

## Prohibited or unsupported use

He thong khong duoc trinh bay nhu:

- Cong cu chan doan y te.
- Thiet bi ergonomic certification.
- He thong giam sat lao dong bat buoc.
- Cong cu danh gia suc khoe ca nhan co tinh phap ly.

## Participant and consent status

Metadata hien tai cho thay ten file co participant IDs nhu `P01`, `P03`, `P04`, `P05`, `P06`, nhung project chua co statement day du ve:

- So nguoi tham gia chinh xac.
- Tuoi/gioi/chieu cao.
- Dieu kien dong y.
- Dieu kien camera/anh sang.

Day la han che can ghi ro trong bao cao. Neu tiep tuc phat trien, nen tao `dataset/metadata/participants.csv` voi cac cot toi thieu:

- `participant_id`
- `consent_status`
- `recording_date`
- `camera_type`
- `view_angle`
- `lighting_condition`
- `notes`

Khong nen ghi demographic nhay cam neu khong can cho muc tieu nghien cuu.

## Bias and limitations

- Dataset con nho va co the nghieng theo mot vai nguoi/goc quay.
- Camera view khac nhau co the lam model sai.
- Anh sang, trang phuc, background, ghe/ban khac nhau co the anh huong MediaPipe.
- External set hien tai co 10 videos, chua du de ket luan robust generalization.

## Safe paper wording

> The system is intended as an assistive ergonomic reminder and research prototype. It does not provide medical diagnosis. The current dataset is project-specific and requires additional metadata, consent documentation, and person-wise evaluation before public release or broad deployment claims.
