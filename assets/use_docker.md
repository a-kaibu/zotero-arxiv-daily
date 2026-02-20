## 🐳 Docker Deployment

For users who prefer containerized deployment, we now provide Docker deployment options. This is particularly useful for:

- Running the service on your own server instead of GitHub Actions
- Better resource control (CPU/RAM allocation)
- Easier environment management
- Persistent logging
- **Prerequisites**:
  - Docker installed ([Installation Guide](https://docs.docker.com/engine/install/))
  - Docker Compose (usually included with Docker Desktop)
  - Configured Docker image registry mirror (for faster builds in some regions)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/TideDra/zotero-arxiv-daily.git
cd zotero-arxiv-daily
```

2. Build the Docker image (recommended for customization):
```bash
docker build . -t local/zotero-arxiv-daily:latest
```

3. Create necessary directories:
```bash
mkdir -p logs
```

4. Edit the `docker-compose.yml` file to configure your environment variables:
```yaml
environment:
    environment:
      # 必填参数（示例值）
      - ZOTERO_ID=1234567
      - ZOTERO_KEY=AbCdEfGhIjKlMnOpQrStUvWx
      - DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy

      # 可选参数（带默认值）
      - ZOTERO_IGNORE=already_read_papers
      - ARXIV_QUERY=cs.AI+cs.CV+cs.LG+cs.CL
      - SEND_EMPTY=False
      - MAX_PAPER_NUM=5
      - MODEL_NAME=hf.co/mmnga-o/NVIDIA-Nemotron-Nano-9B-v2-Japanese-gguf:Q4_K_M
      - LANGUAGE=English
      
      # 新增配置
      - HF_ENDPOINT=https://hf-mirror.com
      # - TZ=Asia/Shanghai  # 时区设置
      # - http_proxy=http://proxy.example.com:8080  # HTTP代理（可选）
      # - https_proxy=http://proxy.example.com:8080 # HTTPS代理（可选）
      # - no_proxy=localhost,127.0.0.1,.internal  # 代理排除项
```

5. Start the service:
```bash
docker compose up -d
```

### Key Features of Docker Deployment

- **Scheduled Execution**: By default runs daily at 8:00 AM (configurable in `command` section)
- **Log Persistence**: All logs are saved in the `logs/` directory
- **Resource Isolation**: Runs in a contained environment with all dependencies included
- **Easy Updates**: Simply rebuild the image when updating the service

### Configuration Options

You can customize the deployment by:

1. **Changing schedule time**: Edit the cron expression in `command` section (default: `0 8 * * *` means 8:00 AM daily)
2. **Proxy settings**: Uncomment and configure proxy environment variables if needed
3. **Timezone**: Uncomment `TZ` variable to set specific timezone (you may also need to comment `- /etc/localtime:/etc/localtime:ro`)

### Monitoring and Maintenance

- View logs:
```bash
docker logs zotero-arxiv-daily
```

- Stop the service:
```bash
docker compose down
```

- Update the service:
```bash
git pull origin main
docker compose down
docker compose up -d --build
```

### Why Choose Docker Deployment?

1. **Consistent Environment**: Eliminates "works on my machine" problems
2. **Resource Control**: Allocate specific CPU/RAM resources as needed
3. **Isolation**: Runs separately from your host system
4. **Portability**: Easy to move between different servers
5. **Persistent Storage**: Logs persist between container restarts
