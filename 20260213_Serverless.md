# 環境構築ハンズオン（サーバレス）

## 概要
AWS CDKでサーバレスで動くアプリを構築する

## AWS CDK
- CDK(Cloud Development Kit)は JSON を生成（cdk.outに .template.json） 
- CDKの実行環境はnode.js
- プログラミング言語はPythonやTypeScriptsなど複数言語をサポートするが、ハンズオンはPythonを使用


## テキスト
https://tomomano.github.io/learn-aws-by-coding/

## サンプルコード
https://github.com/ayukat1016/learn-aws-by-coding

```sh
# リポジトリの取得
$ git clone https://github.com/ayukat1016/learn-aws-by-coding.git

# プロジェクトに移動
$ cd learn-aws-by-coding

# ブランチの切り替えと作成
$ git checkout -b feature/to_cdkv2_handson origin/feature/to_cdkv2_handson

# ブランチの確認
$ git branch
* feature/to_cdkv2_handson
  main
```

## 環境構築の前提
- asdfがインストール済み
- uvがインストール済み
- AWSアカウントでアクセスキー、シークレットキーを作成済み

## 実行環境のバージョン
- node.js:v20.20.0
- cdk:2.1104.0
- awscli:2.30.1
- python:3.12.10

## バージョン指定の手順
- asdfでnodo.jsをインストール
```sh
$ asdf plugin add nodejs
$ asdf install nodejs 20.20.0
$ asdf local nodejs 20.20.0
$ node --version
```

- cdkをインストール
```sh
$ npm install -g aws-cdk@2.1104.0
$ cdk --version
```

- asdfでawscliをインストール
```sh
$ asdf plugin add awscli
$ asdf install awscli 2.30.1
$ asdf local awscli 2.30.1
$ aws --version
```

- uvでpythonをインストール
```sh
$ uv python install 3.12.10
$ uv python pin 3.12.10
$ uv run python --version
```

## プロジェクト共通の実行手順

- プロファイルを未作成のとき実行
- AWSアカウントに紐づくアクセスキー、シークレットキーを指定
- regionは`ap-northeast-1`を指定
- formatは`json`を指定

```sh
# 新規プロファイルの作成
$ aws configure --profile abc
```

- プロファイルを指定

```sh
# プロファイルの設定
$ export AWS_PROFILE=abc

# AWSへの接続確認
$ aws sts get-caller-identity
```

- bootstrapを実行 
```sh
# アカウントは打ち換えること
$ cdk bootstrap aws://AWSアカウント/ap-northeast-1
```

## ハンズオンごとの実行手順

- ハンズオンのディレクトリごとに仮想環境`.venv`を構築、仮想環境でデプロイを実行する

```sh
# ハンズオンアプリへの移動
$ cd handson/bashoutter/

# 仮想環境の作成
$ uv venv

# 仮想環境へのライブラリインストール
$ uv pip install -r requirements.txt

# 仮想環境の起動
$ . .venv/bin/activate

# AWSリソースの作成
$ cdk deploy

# AWSリソースの削除
$ cdk destroy

# 仮想環境の停止
$ deactivate
```