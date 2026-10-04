# IT Project Management API

## 概要

FastAPI + PostgreSQLによる
IT案件管理システムです。

REST APIとして顧客情報を管理します。

## 技術スタック

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- pytest
- Docker
- Docker Compose

## 現在の機能

- [x] ユーザー登録
- [x] JWTログイン
- [x] JWT認証
- [x] 顧客登録
- [x] 顧客一覧
- [x] 顧客取得
- [x] 顧客更新
- [x] 顧客削除
- [x] pytestによるテスト
- [x] Docker環境構築
- [ ] 案件管理
- [ ] 見積管理
- [ ] ServiceNow連携
- [ ] AWSデプロイ
- [ ] CI/CD

## APIドキュメント

FastAPIのSwagger UIを使用します。

http://localhost:8000/docs

## 起動方法

```bash
docker compose up