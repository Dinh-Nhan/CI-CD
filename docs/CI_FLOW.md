# CI/CD Flow - API Governance

## 📊 Quy trình tự động khi tạo PR

```
┌─────────────────────────────────────────────────────────────┐
│  Developer tạo PR vào main/develop                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions: ci.yaml                                     │
│  Trigger: pull_request                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Job 1: Validate (validate.yaml)                            │
├─────────────────────────────────────────────────────────────┤
│  1. Checkout code                                            │
│  2. Setup Node.js 20                                         │
│  3. npm ci                                                   │
│  4. npm run lint:api                                         │
│     ├─ Step 1: Check inline schema (bash)                   │
│     │  └─ grep patterns trong paths/                        │
│     └─ Step 2: Spectral validation                          │
│        └─ operationId, readOnly, responses                  │
│  5. npm run validate:api (Redocly)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ├─ PASS ✅
                      │    │
                      │    ▼
                      │  ┌──────────────────────────────────┐
                      │  │  Job 2: Diff (diff.yaml)         │
                      │  │  - So sánh thay đổi              │
                      │  │  - Comment vào PR                │
                      │  └────────┬─────────────────────────┘
                      │           │
                      │           ▼
                      │  ┌──────────────────────────────────┐
                      │  │  Job 3: Build (build.yaml)       │
                      │  │  - Bundle OpenAPI                │
                      │  │  - Build docs HTML               │
                      │  │  - Upload artifact               │
                      │  └────────┬─────────────────────────┘
                      │           │
                      │           ▼
                      │  ┌──────────────────────────────────┐
                      │  │  ✅ PR ready to merge            │
                      │  └──────────────────────────────────┘
                      │
                      └─ FAIL ❌
                           │
                           ▼
                      ┌──────────────────────────────────┐
                      │  ❌ PR blocked                    │
                      │  - Show errors in Actions        │
                      │  - Developer phải sửa            │
                      └──────────────────────────────────┘
```

## 🔄 Quy trình sau khi merge

```
┌─────────────────────────────────────────────────────────────┐
│  PR được merge vào main                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions: deploy.yaml                                 │
│  Trigger: push to main                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ├─ Job 1: Validate (lại)
                      │
                      ├─ Job 2: Build docs
                      │  └─ redocly build-docs
                      │
                      ├─ Job 3: Deploy to GitHub Pages
                      │  └─ https://<user>.github.io/<repo>/
                      │
                      └─ Job 4: Notify Slack
                         └─ Gửi thông báo thành công
```

## ⚡ Timeline ước tính

| Step | Thời gian | Có thể fail? |
|------|-----------|--------------|
| Checkout | ~5s | Không |
| Setup Node | ~10s | Không |
| npm ci | ~30s | Có (nếu package.json lỗi) |
| Check inline schema | ~2s | **Có** (nếu có inline schema) |
| Spectral lint | ~5s | **Có** (nếu vi phạm rules) |
| Redocly validate | ~3s | **Có** (nếu OpenAPI invalid) |
| Diff | ~5s | Không |
| Build docs | ~10s | Có (nếu bundle lỗi) |
| **Tổng** | **~70s** | |

## 🎯 Các điểm kiểm tra quan trọng

### ✅ Sẽ PASS nếu:
- Không có inline schema trong `paths/`
- operationId đúng format `verbNoun`
- Trường `id`, `created_at`, `updated_at` có `readOnly: true`
- OpenAPI syntax hợp lệ

### ❌ Sẽ FAIL nếu:
- Có inline schema trong `paths/`
- operationId sai format
- Thiếu `readOnly` cho các trường bắt buộc
- OpenAPI syntax lỗi
- Circular references

### ⚠️ WARNING (không block PR):
- Thiếu response 401, 404, 500
- Thiếu description
- Thiếu examples

## 🔧 Debug khi CI fail

### 1. Xem logs trong GitHub Actions
```
Actions tab → Click vào run → Click vào failed job
```

### 2. Chạy lại local
```bash
npm run lint:api
```

### 3. Kiểm tra từng bước
```bash
# Chỉ check inline schema
bash scripts/lint-all.sh

# Chỉ Spectral
npm run lint:spectral

# Chỉ Redocly
npm run validate:api
```

## 📞 Liên hệ

Nếu gặp vấn đề với CI/CD, liên hệ:
- Team Lead: @team-lead
- DevOps: @devops-team
- Slack: #api-governance
