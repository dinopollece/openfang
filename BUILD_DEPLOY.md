# DoVi OpenFang - Build & Deploy Guide

## Quick Start

### Build ARM64 Image (for Raspberry Pi 5)

```bash
cd openfang

docker buildx build \
  --platform linux/arm64 \
  --tag ghcr.io/dinopollece/openfang:latest \
  --tag ghcr.io/dinopollece/openfang:arm64 \
  --load \
  .
```

### Push to GHCR

```bash
docker push ghcr.io/dinopollece/openfang:latest
docker push ghcr.io/dinopollece/openfang:arm64
```

### Deploy to Raspberry Pi 5

```bash
# On Raspberry Pi:
cd ~/dovi-openfang/openfang

# Pull latest image
docker compose pull

# Start container
docker compose up -d

# Verify health
curl http://localhost:4200/api/health
```

## Files Modified from Official OpenFang

### 1. `Dockerfile`
- Based on official OpenFang Dockerfile (portable multi-arch)
- Added labels for P1 improvements versioning
- **NO changes to build logic** - keeps official portability

### 2. `docker-compose.yml`
- Based on official OpenFang docker-compose.yml
- Changed image from build local to `ghcr.io/dinopollece/openfang:latest`
- Simplified to essential config only

### 3. `.github/workflows/release.yml`
- Based on official OpenFang release workflow
- Changed registry from `ghcr.io/rightnow-ai/openfang` to `ghcr.io/dinopollece/openfang`
- **All other logic remains same** - multi-arch build, automated releases

## What Changed (P1 Improvements)

The only code changes are in static files:
- `crates/openfang-api/static/index_body.html` - UI fixes
- `crates/openfang-api/static/css/components.css` - Styling improvements
- `crates/openfang-api/static/css/layout.css` - Layout improvements

These changes are baked into the binary during build - no Dockerfile changes needed.

## Automated Releases (Optional)

To trigger automated multi-arch builds:

```bash
cd openfang

# Tag release
git tag v1.0.1-p1-improvements
git push origin v1.0.1-p1-improvements

# GitHub Actions will:
# 1. Build multi-arch (amd64 + arm64)
# 2. Push to ghcr.io/dinopollece/openfang:latest
# 3. Push to ghcr.io/dinopollece/openfang:1.0.1-p1-improvements
# 4. Create GitHub release
```

## Verification

After deploying to Pi, verify P1 improvements:

1. **Smooth Streaming**: Chat response should fade in word-by-word (no pulsing)
2. **Subtle Shadows**: Message bubbles have soft shadows (0 2px 8px rgba(0,0,0,0.04))
3. **Premium Code Blocks**: Code blocks have copy button integrated
4. **Compact Mode**: Toggle in sidebar for compact message view

## Troubleshooting

### Build fails on ARM
- Verify Dockerfile doesn't use `target-cpu=native`
- Use `--platform linux/arm64` flag

### Container won't start on Pi
- Check logs: `docker compose logs`
- Verify image architecture: `docker inspect ghcr.io/dinopollece/openfang:latest | grep Architecture`
- Ensure Pi has enough memory (4GB minimum recommended)

### Pull from GHCR fails
- Verify you're logged in: `docker login ghcr.io`
- Check image exists: `docker manifest inspect ghcr.io/dinopollece/openfang:latest`

## Resources

- Official OpenFang: https://github.com/RightNow-AI/openfang
- OpenFang Docs: https://openfang.sh
- Docker Buildx: https://docs.docker.com/buildx/working-with-buildx/
