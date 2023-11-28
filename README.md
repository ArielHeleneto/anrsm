# Another RISC-V SDK Manager

这是一个 RISC-V SDK 管理器。

## 目标

- 实现一个管理 RISC-V ToolChain、sysroot、[QEMU](https://www.qemu.org/) 等工具组合的系统。
- 多平台、架构支持。
- 用户自定义订阅源

## 功能

### 当前已实现的功能

```bash
anrsm config get [OPTIONS] ITEM 
anrsm config set [OPTIONS] ITEM VALUE
anrsm config unset [OPTIONS] ITEM
anrsm source cache [OPTIONS] Package Name
anrsm source expand [OPTIONS] Package Name Destination
anrsm source info [OPTIONS] Package Name
anrsm source list [OPTIONS]
anrsm source update [OPTIONS] [SOURCEURL]
anrsm hullo [OPTIONS]
```

### 未来可能实现的功能

- 按照元数据文件展开项目并安装依赖的能力
- 展开 `source` 用的文件的文件。

### 目前需要的修复

- 打包以直接安装到目标平台并测试
- 调整 `settings.toml` 位置到 `~/settings.toml` 以便用户调整。
- 清理和改善代码重复。
- 丰富和调整部分命令参数，特别是 `helper` 部分。
- 使用 [Rich](https://github.com/Textualize/rich) 改善输出内容。
- 检查边界状况和改善代码质量。
- 修复 `~` 不可用的问题。
- 修复架构检测问题。
- 修复在相同位置设置软链接时重复文件的问题。
- 修复在 Windows 上检查设置软链接时缺少权限的问题。

## 技术栈

当前使用的技术栈如下。

- 纯粹的 Python
- [Typer](https://typer.tiangolo.com/)：Typer，构建出色的 CLI。易于编码。基于 Python 类型提示。
- [Dynaconf](https://www.dynaconf.com/)：Python 的配置管理。
- [Rich](https://github.com/Textualize/rich)：Rich 是一个 Python 库，可以为您在终端中提供富文本和精美格式。
- [Requests](https://pypi.org/project/requests/)：Requests 是一个简单而优雅的 HTTP 库。
- [Poetry](https://python-poetry.org/)：Python 打包和依赖管理变得简单。

## 源

### 源描述文件

目前，托管了源描述文件 [source.json](example/source.json) 在项目内。

[source-example.json](example/source-example.json) 是一个源的最小示例。

### 软件包描述文件

[metadata-example.json](example/metadata-example.json) 是一个软件包描述文件的最小示例。
