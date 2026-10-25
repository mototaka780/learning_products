# IT Project Management API

## 概要

FastAPI、PostgreSQL、SQLAlchemyを使用して開発した、IT案件管理向けのREST APIです。

ユーザー認証、顧客管理、案件管理のAPIを実装し、JWTによる認証、pytestによる自動テスト、Docker Composeによる開発環境の構築に対応しています。

本プロジェクトは、API設計・実装・テスト・コンテナ化を通じて、クラウドネイティブなアプリケーション開発の実践スキルを習得することを目的としています。

## 技術スタック

- **言語:** Python
- **APIフレームワーク:** FastAPI
- **データベース:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **認証:** JWT
- **バリデーション:** Pydantic
- **テスト:** pytest、FastAPI TestClient
- **コンテナ:** Docker、Docker Compose
- **APIドキュメント:** Swagger UI（OpenAPI）

## 現在の実装状況

### 認証・ユーザー管理

- [x] ユーザー登録
- [x] JWTログイン
- [x] JWT認証
- [x] 認証が必要なAPIへのアクセス制御

### 顧客管理

- [x] 顧客登録
- [x] 顧客一覧取得
- [x] 顧客情報取得
- [x] 顧客情報更新
- [x] 顧客削除
- [x] CRUD処理の自動テスト

### 案件管理

- [x] 案件登録
- [x] 案件一覧取得
- [x] 案件IDによる案件取得
- [x] 顧客IDによる案件一覧取得
- [x] 案件情報更新
- [x] 案件削除
- [x] 存在しない案件へのアクセスに対する404処理
- [x] CRUD処理の自動テスト

### 開発・テスト環境

- [x] Docker Composeによる開発環境構築
- [x] PostgreSQLとの接続
- [x] pytestによる自動テスト
- [x] テスト用データベースの利用
- [x] APIの動作確認

### 今後の実装予定

- [ ] 見積管理
- [ ] ServiceNow連携
- [ ] AWSへのデプロイ
- [ ] CI/CDパイプライン構築

## テスト結果

実行コマンド：

```bash
docker compose exec api python -m pytest -v
```

**直近の実行結果：20 passed**

認証・顧客管理・案件管理などの自動テスト20件が成功しています。

※上記は直近のテスト実行結果です。ソースコード変更後は、再度テストを実行して確認してください。

## APIドキュメント

アプリケーション起動後、以下のURLからSwagger UIを利用できます。

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Swagger UIから、各APIのリクエストやレスポンスを確認できます。認証が必要なAPIは、JWTを使用して動作を確認します。

## 起動方法

### 1. リポジトリのディレクトリへ移動

```bash
cd C:\workspace\app
```

### 2. Docker Composeで起動

```bash
docker compose up -d --build
```

### 3. コンテナの状態を確認

```bash
docker compose ps
```

### 4. APIドキュメントを開く

ブラウザで以下にアクセスします。

http://localhost:8000/docs

### 5. 自動テストを実行

```bash
docker compose exec api python -m pytest -v
```

### 6. コンテナを停止

```bash
docker compose stop
```

## プロジェクトの構成

```text
app/
├── main.py
├── database.py
├── models/
├── schemas/
├── crud/
├── routers/
├── test/
├── utils/
├── config.py
├── Dockerfile
├── docker.compose.yml
├── requirement.txt
└── README.md
```

※実際のディレクトリ名やファイル構成に合わせて調整してください。

## 今後の拡張方針

1. 見積管理機能の実装
2. ServiceNowとの連携
3. AWS環境へのデプロイ
4. CI/CDパイプラインの構築
5. テストの拡充と品質改善

## 注意事項

- `.env` などの環境変数ファイル、JWT秘密鍵、パスワード、アクセストークンなどの機密情報はGitHubに公開しないでください。
- 公開リポジトリでは、実際の認証情報を含まない `.env.example` を用意することを推奨します。
- 本プロジェクトは開発・学習用途を想定しています。本番環境で利用する場合は、認証・認可、秘密情報管理、ログ、監視、データベースの運用設計などを追加で検討する必要があります。