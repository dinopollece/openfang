## Health Stack

- typecheck: cargo build --workspace --lib
- lint: cargo clippy --workspace --all-targets -- -D warnings
- test: cargo test --workspace
- shell: shellcheck scripts/install.sh

## Raspberry Pi release/deploy (fork)

- Pushing to `release/**` builds the ARM64 binary and uploads a tarball plus SHA-256 as a GitHub Actions artifact, retained for 3 days. It does not deploy to the Pi or create a GitHub Release.
- Deploy manually over SSH (`dovi-pi`): update `~/Projects/openfang` to the same release branch, back up `~/.openfang/bin/openfang`, stop `openfang.service`, then run `OPENFANG_BINARY=/path/to/openfang bash ~/Projects/openfang/dovi/deploy.sh`. The script installs the agent bundle and restarts the service.
- Keep this workflow and its artifacts on `dinopollece/openfang-dovi`; do not publish to the upstream OpenFang repository.
