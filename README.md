# AI Agent

A Windows and macOS desktop coding assistant powered by local Ollama models. It provides project management, chat, file previews, skills, MCP tools, persistent memory, and optional web access.

## Features

- Local Ollama chat with streaming responses
- Project selector and file preview
- Confirmed file creation, deletion, commands, web requests, and MCP calls
- Built-in Python help and downloadable skills
- Persistent memory and chat history
- Optional MCP servers
- Windows executable and macOS app bundle builds

## Requirements

- Windows 10 or 11, or macOS 12+
- Python 3.11+ (source use)
- [Ollama](https://ollama.com/) installed and running
- A supported Ollama model, such as `llama3.2`

## Run from source on Windows

```powershell
python -m pip install -r requirements.txt
python ai-agent.py
```

## Run from source on macOS

```bash
chmod +x build-macos.sh AI-Agent.command
./build-macos.sh run
```

Install Ollama, then pull a model:

```bash
ollama pull llama3.2
```

## Build the Windows executable

```powershell
.\build.bat
```

Choose PyInstaller for a quick executable or Nuitka for a native compiled executable. The PyInstaller output is under `dist\AI-Agent.exe`.

## Build the macOS app

```bash
./build-macos.sh build
```

The macOS application will be written to `dist/AI-Agent.app`. You can also double-click `AI-Agent.command` to start the source version.

## MCP configuration

Copy `mcp.example.json` to `mcp.json`, then configure only the MCP servers you trust. `mcp.json` is local configuration and should not be committed.

Example:

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\path\\to\\project"]
    }
  }
}
```

## Safety

The agent asks for confirmation before running commands or MCP tools, opening web pages, downloading skills, overwriting files, or deleting files. It is also restricted from writing outside the selected project directory.

## License

Add a license before publishing the repository. The included code is not yet accompanied by a license file.
