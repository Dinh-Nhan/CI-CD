# Scripts

## lint-all.sh

Script kiểm tra OpenAPI spec với 2 bước:

### Bước 1: Kiểm tra inline schema trong paths/
- Dùng `grep` để check trực tiếp file (không qua Spectral)
- Bắt lỗi nếu có `schema:` với `type: object/array` mà không có `$ref`
- **Không bị ảnh hưởng bởi Spectral resolve**

### Bước 2: Validate toàn bộ document
- Dùng Spectral với `.spectral.yaml`
- Validate schemas, operationId, readOnly, etc.
- Cho phép Spectral resolve `$ref` để validate đầy đủ

## Cách dùng

```bash
# Chạy trực tiếp
bash scripts/lint-all.sh

# Hoặc qua npm
npm run lint:api
```

## Tại sao cần 2 bước?

Spectral tự động resolve `$ref` trước khi apply rules, nên không thể phân biệt:
- Schema được reference qua `$ref` (ĐÚNG ✅)
- Schema được định nghĩa inline (SAI ❌)

Giải pháp: Check inline schema bằng `grep` trước khi Spectral resolve.
