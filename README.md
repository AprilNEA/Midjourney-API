<div align="center">

<h1 align="center">Midjourney API</h1>

Best Unofficial Midjourney API

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/AprilNEA/Midjourney-API)]()

[Document](https://midjourney.sku.moe) / [Discord](https://discord.gg/y4vxgqfUW) / [Telegram](https://github.com/AprilNEA/ChatGPT-Admin-Web)

[GitHub Sponsor](https://github.com/sponsors/AprilNEA) / [爱发电](https://afdian.net/a/aprilnea)


</div>

## Features 功能

- [x] `/v1/trigger` Get related task results 获取相关任务结果
- [x] `/v1/imagine` Trigger the drawing task 触发绘画任务
- [ ] upscale
- [ ] variation
- [ ] reset
- [ ] upload
- [ ] Generate Prompt by uploading image name
- [ ] Send image message, return image link, for image generation function
- [ ] **Multiple Midjourney accounts**


## Start 开始

### Docker 容器

Pull 拉取

```docker
docker pull aprilnea/midjourney-api:latest
```

Run 运行

```docker
docker run -it -e USER_TOKEN="" \
-e BOT_TOKEN="" \
-e GUILD_ID="" \
-e CHANNEL_ID="" \
-e DATABASE_URL="" \ aprilnea/midjourney-api:latest
```

更多请查看[文档](https://midjourney.sku.moe/midjourney-api/prepare)

For more please check[documentation](https://midjourney.sku.moe/midjourney-api/prepare)

## Thanks 鸣谢

- [yokonsan/midjourney-api](https://github.com/yokonsan/midjourney-api)

## Donate 捐赠

感谢您的激励，能让该项目持续发展。

Thank you for inspiring and being able to keep the program going.

[GitHub Sponsor](https://github.com/sponsors/AprilNEA)  |  [爱发电](https://afdian.net/a/aprilnea)

<img src="https://hits-app.vercel.app/hits?url=https%3A%2F%2Fgithub.com%2FAprilNEA%2FMidjourney-API" />
