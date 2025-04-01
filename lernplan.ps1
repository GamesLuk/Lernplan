docker run `
    --name lernplan `
    -p 6379:6379 `
    -v $(PSScriptRoot):/git `
    -v data:/data `
    gamesluk/lernplan:latest