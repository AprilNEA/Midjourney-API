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

### Use Our Service 使用我们的服务

<details><summary>正在开发中，当前不可用</summary>
<p>

```shell
curl -X 'POST' \
  'https://midjourney-api.sku.moe/v1/imagine' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'user_token: <你的 User Token>' \
  -d '{
  "prompt": "a beautiful girl"
}'
```

</p>
</details>

### Self-deployment 自部署

| Environment Variable | Description                                                    |
|----------------------|----------------------------------------------------------------|
| `SECRET`             | A secret key                                                   |
| `USER_TOKEN`         | Discord User Token which account that subscribes to Midjourney |
| `BOT_TOKEN`          | Bot token                                                      |
| `GUILD_ID`           | Guild ID                                                       |
| `CHANNEL_ID`         | Channel ID                                                     |
| `DATABASE_URL`       | Optional                                                       |

| 环境变量           | 说明                        |
|----------------|---------------------------|
| `SECRET`       | 私人密钥                      |
| `USER_TOKEN`   | 订阅了Midjourney的Discord用户令牌 |
| `BOT_TOKEN`    | 机器人 Token                 |
| `GUILD_ID`     | 公会ID                      |
| `CHANNEL_ID`   | 频道ID                      |
| `DATABASE_URL` | 可选                        |

#### Docker 容器

Pull 拉取

```docker
docker pull aprilnea/midjourney-api:latest
```

Run 运行

```docker
docker run -it \
-e SECRET="" \
-e USER_TOKEN="" \
-e BOT_TOKEN="" \
-e GUILD_ID="" \
-e CHANNEL_ID="" \
-e DATABASE_URL="" \ aprilnea/midjourney-api:latest
```

```shell
curl -X 'POST' \
  'https://127.0.0.1:8080/v1/imagine' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authentication: Bearer {SECRET}' \
  -d '{
  "prompt": "a beautiful girl"
}'
```

更多请查看[文档](https://midjourney.sku.moe/midjourney-api/prepare)

For more please check [documentation](https://midjourney.sku.moe/midjourney-api/prepare)

## Thanks 鸣谢

- [yokonsan/midjourney-api](https://github.com/yokonsan/midjourney-api)

## License

[MIT](./LICENSE)

----

**Midjourney-Web** © [AprilNEA](https://github.com/AprilNEA), Released under the [MIT](./LICENSE) License.

> Help me if you
> want: [GitHub Sponsor](https://github.com/sponsors/AprilNEA)  |  [爱发电](https://afdian.net/a/aprilnea)
>
> Telegram Channel [@AprilsBlog](https://t.me/AprilsBlog) · Twitter [@AprilNEA](https://twitter.com/AprilNEA)
