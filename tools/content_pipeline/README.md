# 合规短视频内容提效脚本（运动/营养/减脂）

> 这个脚本用于**基于你手工整理或官方渠道导出的热点线索**，自动生成 10 条短视频选题和脚本。  
> 不包含对小红书/微博/抖音/YouTube 的未授权爬取，也不用于规避平台规则。

## 1. 安装

```bash
pip install openai
```

## 2. 准备热点输入

编辑 `sample_trends.json`，字段示例：

- `platform`: 平台名
- `title`: 热门标题
- `summary`: 内容摘要
- `url`: 原链接（可选）

## 3. 运行

```bash
export OPENAI_API_KEY="你的key"
python tools/content_pipeline/viral_content_pipeline.py \
  --input tools/content_pipeline/sample_trends.json \
  --count 10 \
  --topic "中老年运动营养与科学减脂" \
  --out tools/content_pipeline/outputs
```

## 4. 自动化（每天执行）

Linux `crontab -e` 示例：

```cron
0 8 * * * /usr/bin/python /path/to/repo/tools/content_pipeline/viral_content_pipeline.py --input /path/to/repo/tools/content_pipeline/sample_trends.json --count 10 --out /path/to/repo/tools/content_pipeline/outputs
```

## 合规建议

- 使用平台官方 API、开放数据、或你本人账号可导出的数据。
- 生成内容前做事实核验，尤其是营养和健康建议。
- 避免“保证瘦”“治愈”等医疗承诺表述。
