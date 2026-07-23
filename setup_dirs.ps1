$dirs = @(
    "docs/architecture", "docs/api", "docs/diagrams", "docs/screenshots",
    "frontend/public", "frontend/src/assets", "frontend/src/components",
    "frontend/src/pages", "frontend/src/services", "frontend/src/styles",
    "backend", "backend/app",
    "scripts"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
