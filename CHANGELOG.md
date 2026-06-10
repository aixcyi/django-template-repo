# 更新日志

项目版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)进行定义，本篇日志遵循
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 所提出的约定。

## Unreleased

### Changed

- 数据库配置模板从 Django Settings 文件移到 `./docs/` 下的 `DATABASE.md`、`STORAGE.md`。
- Redis 配置模板从 `README.md` 文件移到 `./docs/` 下的 `CACHE.md`。
- 添加重命名 Django Settings 所在目录的脚本 `./scripts/fit.py`。

### Fixed

- 更正 `HTTPMethod` 在 Python 3.10 的代替实现。
- 更正不兼容的 `HTTPMethod` 导入。

## [5.0.0] - 2026-06-09

### Added

- 新增 `ServiceRequest` 抽象基类（`utils/request.py`），封装外部服务的 URL 构建、查询参数和 GET/POST 方法。
- 新增微信小程序 API 集成（`api/wechat.py`），支持 `code2session` 和 `getAccessToken`。
- 新增 `WechatUser` 模型，关联微信 `openid`/`unionid`/`session` 信息。
- 新增 `MeowHandler` 上下文管理器（`commons/views.py`），自动将短篇上下文的异常转为 `MeowViewException` 以便自动响应。
- 新增 `Cacher` 缓存封装类（`utils/cache.py`），提供字典式操作和切片语法的超时设置。
- 新增 `HTTPMethod` 兼容枚举（`utils/http.py`），为 Python 3.10 回补 3.11 的 `http.HTTPMethod`。
- 新增 `MeowModelViewSet`，内置软删除和响应标准化的完整 CRUD 视图集。
- 新增兼容 S3/MinIO 的文件存储配置模板。

### Changed

- 包管理从 pip + `requirements.txt` 迁移至 uv + `pyproject.toml`。
- 重新编排用户模型，统一管理器命名。
- 默认启用 Django REST Framework 的 Token 认证。
- 统一全局异常处理机制，将 `MeowViewException` 作为项目统一业务异常类。
- 数据库配置模板从 `README.md` 移入 Django Settings 文件。
- 不再预设具体的数据库和缓存库依赖，由使用者按需安装。
- 统一使用 Ruff 格式化代码。

### Fixed

- 修正 `manage.py addapp` 命令的 settings 检测逻辑。
- 修正默认用户名的生成规则。
- 修正微信 API 端点与认证器。
- 更正用户管理器名称。

### Removed

- 使用 `zeraora~=0.4` 代替 `utils/models.py` 的 `SnakeModel` 和 `utils/string.py`。
- 移除间接依赖的 `utils/converters.py`。

## [4.x] 及更早版本

早期版本未进行正式的版本追踪和变更记录。
