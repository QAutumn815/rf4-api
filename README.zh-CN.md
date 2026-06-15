<div align="center">
    <a href="https://github.com/hurfy/rf4-api"><img src="https://github.com/user-attachments/assets/c1890100-fb8b-4ac4-a28d-5b097eb536b9" alt="rf4-api" /></a>
</div>

<div align="center">
    <a href="https://github.com/hurfy/rf4-api/issues"><img src="https://img.shields.io/github/issues/hurfy/rf4-api?style=for-the-badge" alt="open issues" /></a>
    <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="version" />
    <a href="LICENSE"><img src="https://img.shields.io/github/license/hurfy/rf4-api?style=for-the-badge" alt="license" /></a>
</div>

<br />

<div align="center">
  Russian Fishing 4 非官方渔获数据 API
</div>

<div align="center">
  <sub>
    Built with love
    &bull; 作者 <a href="https://github.com/hurfy">@hurfy</a>
    &bull; <a href="https://github.com/hurfy/rf4-api/graphs/contributors">贡献者</a>
  </sub>
</div>

---

## 📖 项目简介

**本项目仍在开发中！**

该项目的主要目标是从俄罗斯钓鱼 4（Russian Fishing 4）官方网站定时采集**渔获记录**、**玩家评级**和**比赛优胜者**数据，经过处理后以 REST API 和可浏览的 Web 页面两种形式呈现。爬取覆盖全部 10 个服务器区域和 3 种钓竿分类。

*我不拥有这些数据，仅进行采集并以方便使用的格式呈现。所有权利归 FishSoft LLC 所有。*

---

## ✨ 功能特性

### 📊 数据采集
| 功能 | 说明 |
|---|---|
| **绝对记录** | 全服历史渔获记录（所有区域和分类） |
| **周记录** | 每周渔获记录（按区域更新） |
| **玩家评级** | 玩家排名数据（等级、游戏时长） |
| **比赛优胜者** | 赛事排名（得分、奖品） |
| **10 个区域** | 全球、俄、德、美、法、中、波、韩、日、欧 |
| **3 种分类** | 标准记录、超轻竿、伸缩竿 |
| **鱼类图标缓存** | 自动下载并本地缓存鱼类图标，绕过防盗链 |

### 🌐 REST API
| 方法 | 接口地址 | 说明 |
|---|---|---|
| `POST` | `/v1/parse/` | 触发异步数据爬取（通过 Celery） |
| `DELETE` | `/v1/clear/` | 清空表数据 |
| `GET` | `/v1/records/abs/{region}/{category}/` | 获取绝对记录 |
| `GET` | `/v1/records/wk/{region}/{category}/` | 获取周记录 |
| `GET` | `/v1/ratings/{region}/` | 获取玩家评级 |
| `GET` | `/v1/winners/{region}/{category}/` | 获取比赛优胜者 |

每个 `GET` 接口均支持：

- **过滤** — 按鱼种、玩家、地点、鱼饵、体重范围、日期范围、排名、等级、分数、奖品等筛选
- **分页** — `?page=` 和 `?per_page=`（默认 25，最大 100）
- **排序** — `?ordering=<字段>`（加 `-` 前缀为降序）
- **格式转换** — `?in_gram=true`（重量转克）、`?in_days=true`（游戏时长转天）

### 🖥️ 可浏览 Web 页面
| 路由 | 页面 |
|---|---|
| `/` | 仪表盘（数据统计 + API 参考） |
| `/browse/records/{abs\|wk}/{region}/{category}/` | 渔获记录浏览（支持筛选） |
| `/browse/ratings/{region}/` | 玩家评级浏览（支持筛选） |
| `/browse/winners/{region}/{category}/` | 比赛优胜者浏览（支持筛选） |

### 📚 API 文档（自动生成）
| 路由 | 类型 |
|---|---|
| `/docs/` | OpenAPI 3.0 JSON Schema |
| `/docs/swagger/` | Swagger UI |
| `/docs/redoc/` | ReDoc UI |

### 🔧 后台管理
完整 Django Admin 后台（`/admin/`），支持数据模型的搜索、筛选和日期层级导航。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      爬取层                                  │
│  Selenium Chrome (无头) → HTML → BeautifulSoup → 结构化数据 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      处理层                                  │
│  DataProcessor（重量/日期清洗转换）                         │
│  FishImageCache（下载并缓存鱼类图标）                      │
│  DBProcessor（原子批量写入）                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据层                                  │
│  MySQL 数据库                                               │
│  模型: AbsoluteRecord, WeeklyRecord, Rating, Winner         │
└──────────┬──────────────────┬──────────────────┬─────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   REST API      │ │   Web 页面      │ │   API 文档          │
│  (DRF viewsets) │ │  (TemplateView) │ │  (drf-spectacular)  │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
```

### 数据流程

1. **爬取** — `ParsersManager` 协调各数据源的抓取器和解析器
2. **处理** — 原始数据经过清洗、转换（重量 → 千克，日期 → ISO 格式），鱼类图标缓存到本地
3. **存储** — 处理后的数据以原子事务批量写入 MySQL（全量替换旧数据）
4. **展示** — REST API 和 Web 页面均从同一数据库读取

爬取可通过 **Celery 异步任务** 或 **管理命令**（同步，无需 Celery）两种方式运行。

---

## 🧰 技术栈

| 类别 | 技术 |
|---|---|
| **框架** | Django 5.1 + Django REST Framework 3.15 |
| **数据库** | MySQL（PyMySQL） |
| **爬虫** | Selenium 4.23 + BeautifulSoup 4 |
| **任务队列** | Celery 5.4（Redis 作为消息代理） |
| **API 文档** | drf-spectacular（OpenAPI 3.0 / Swagger / ReDoc） |
| **过滤** | django-filter |
| **配置** | python-decouple（.env） |

---

## 🚀 快速开始

> 目前仅支持开发模式。

### 前置要求

- Python 3.10+
- MySQL 服务器
- Redis（Celery 需要）
- Chrome / Chromium（Selenium 爬取需要）

### 安装运行

```shell
# 克隆仓库
git clone https://github.com/hurfy/rf4-api.git
cd rf4-api

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 MySQL 连接信息和 Django 密钥

# 执行数据库迁移
python manage.py migrate

# 启动 Django 开发服务器
python manage.py runserver

# 在另一个终端启动 Celery 工作进程
celery -A worker.app worker -l INFO -c 1 -P solo

# 或执行一次性同步爬取（无需 Celery）
python manage.py scrape_all
```

### API 调用示例

```shell
# 获取全球区域标准分类的绝对记录
curl http://localhost:8000/v1/records/abs/gl/records/

# 获取美服超轻竿周记录
curl http://localhost:8000/v1/records/wk/us/ultralight/

# 获取欧服玩家评级，按玩家名筛选
curl "http://localhost:8000/v1/ratings/de/?player=Fisherman"

# 获取俄服伸缩竿比赛优胜者，最低分数 1000
curl "http://localhost:8000/v1/winners/ru/telestick/?min_score=1000"

# 触发全量数据爬取
curl -X POST http://localhost:8000/v1/parse/ \
  -H "Content-Type: application/json" \
  -d '{"tables": ["*"]}'

# 清空所有数据
curl -X DELETE http://localhost:8000/v1/clear/ \
  -H "Content-Type: application/json" \
  -d '{"tables": ["*"]}'
```

---

## 🌍 支持的区域

| 代码 | 区域 |
|---|---|
| `gl` | 全球 Global |
| `ru` | 俄罗斯 |
| `de` | 德国 |
| `us` | 美国 |
| `fr` | 法国 |
| `cn` | 中国 |
| `pl` | 波兰 |
| `kr` | 韩国 |
| `jp` | 日本 |
| `en` | 欧洲（英语） |

## 🎣 支持的分类

| 标识 | 说明 |
|---|---|
| `records` | 标准记录 |
| `ultralight` | 超轻竿 |
| `telestick` | 伸缩竿 |

---

## 📄 开源协议

基于 MIT 协议分发。详见 `LICENSE` 文件。

---

<div align="center">
  <sub>
    Built with love
    &bull; 作者 <a href="https://github.com/hurfy">@hurfy</a>
    &bull; <a href="https://github.com/hurfy/rf4-api/graphs/contributors">贡献者</a>
  </sub>
  <br />
  <sub>
    <em>所有游戏数据归 <a href="https://rf4game.com">FishSoft LLC</a> 所有。本项目与 FishSoft LLC 无任何关联，也未获其认可。</em>
  </sub>
</div>
