# WangDianTong-Py

## Development

## 初始化开发环境:

    pip install pipenv
    cd /path/to/wangdiantong
    pipenv install --dev # 安装开发环境依赖包
    pipenv shell # 激活virtualenv环境

### 打版本

版本遵循[语义化版本](https://semver.org/lang/zh-CN/)格式, 使用bumpversion打版本

    pipenv run bumpversion major # 主版本号
    pipenv run bumpversion minor # 次版本号
    pipenv run bumpversion patch # 修订号
    pipenv run bumpversion release # 发布迭代

## Test
    pipenv run nosetests

## Features

* TODO
