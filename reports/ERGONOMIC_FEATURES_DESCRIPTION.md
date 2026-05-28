# Ergonomic Features Description

Updated: 2026-05-28

The ergonomic feature set is computed from MediaPipe Pose landmark coordinates.
It is intended to provide interpretable geometric indicators in addition to the
raw 99 landmark coordinates.

| Feature | Meaning |
|---|---|
| `shoulder_y_diff` | Absolute vertical difference between left and right shoulders. |
| `shoulder_tilt_angle` | Shoulder line angle in degrees. |
| `torso_lean_angle` | Torso centerline angle in degrees. |
| `head_offset_x` | Horizontal nose offset from shoulder midpoint. |
| `nose_to_shoulder_y` | Vertical nose position relative to shoulder midpoint. |
| `nose_shoulder_clearance_ratio` | Nose-shoulder clearance normalized by shoulder width. |
| `neck_compression_detected` | Binary indicator for deep neck compression. |
| `left_hand_mouth_ratio` | Left hand to mouth distance normalized by shoulder width. |
| `right_hand_mouth_ratio` | Right hand to mouth distance normalized by shoulder width. |
| `chin_rest_detected` | Binary hand-near-mouth/chin-rest indicator. |
| `shoulder_width` | 2D distance between shoulders. |
| `torso_length` | 2D distance from shoulder midpoint to hip midpoint. |
| `head_shoulder_distance` | 2D nose to shoulder-midpoint distance. |
| `min_hand_mouth_ratio` | Minimum of left/right hand-mouth ratios. |

Visibility note: the current 99-feature CSV stores x/y/z only and does not keep
MediaPipe visibility. Therefore `visibility_mean` is intentionally not used as
a numeric feature in this version.
