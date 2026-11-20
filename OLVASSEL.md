# AI Agent

A Windows and macOS desktop coding assistant powered by local Ollama models.

## macOS

```bash
chmod +x build-macos.sh AI-Agent.command
./build-macos.sh run
```

Build a macOS app bundle:

```bash
./build-macos.sh build
```

The result is `dist/AI-Agent.app`.

## Windows

Run the application from source:

```powershell
python ai-agent.py
```

You can also double-click `AI-Agent.exe` from `dist\AI-Agent.exe` after building.

## Build

Double-click `build.bat` and choose:

1. **PyInstaller**: fast build, no source protection
2. **Nuitka**: native Windows build, longer first build

The executable will be created in `dist\AI-Agent.exe`.

Ollama must be installed and running. If `ollama.exe` is not found in `PATH`, you can place it beside the executable.

## Models

The default model is `llama3.2`. Model selection is limited to models that fit the detected available VRAM.

## Safety

- Every command requires confirmation.
- Dangerous commands receive a separate warning.
- Existing files are confirmed before overwrite and preserved with a `.bak` copy.
- Skill downloads require confirmation and are stored under `skills/_letoltott/`.
- MCP tool calls require confirmation.
- File operations are restricted to the selected project directory.

## Skills

Place a skill in `skills/<name>/SKILL.md`. Each skill should contain `name` and `description` fields in YAML front matter.

## MCP servers

Copy `mcp.example.json` to `mcp.json` and configure trusted servers only.

## Markers

The model can use these markers:

| Marker | Action |
|---|---|
| `[FILE: name.py]` + code block | Create or overwrite a project file |
| `[FOLDER: name]` | Create a folder |
| `[COMMAND: ...]` | Run a command after confirmation |
| `[SKILL: name]` | Load a skill |
| `[MODULE: name]` | Read Python module help |
| `[SKILL_DOWNLOAD: url]` | Download a skill after confirmation |
| `[MCP: server.tool {"param": "value"}]` | Call an MCP tool after confirmation |
