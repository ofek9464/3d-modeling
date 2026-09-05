# BlenderMCP

The modeling MCP used in this project is [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp). The tested combination was **blender-mcp 1.9.1**, add-on protocol **5**, and **Blender 5.2.1 LTS**. A local MCP client successfully initialized and read the open Blender scene.

The PEQ export and rendering scripts use Blender's Python interface directly. No printer-control MCP was used, and no credentials or printer connection details are included.

## Setup

1. Install [Blender](https://www.blender.org/download/) and [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Install the matching Blender add-on:

   ```sh
   uvx --python 3.11 blender-mcp==1.9.1 install-addon
   ```

3. In Blender, enable **Interface: MCP for Blender** under **Edit → Preferences → Add-ons**. In its preferences, turn off telemetry if you do not want it to collect prompts, code, and screenshots. Leave external asset services disabled unless you intend to use them.
4. Merge [codex.example.toml](codex.example.toml) into your Codex configuration, or register the same command with the CLI:

   ```sh
   codex mcp add blender --env BLENDER_HOST=127.0.0.1 --env BLENDER_PORT=9876 --env BLENDER_MCP_DISABLE_TELEMETRY=1 -- uvx --python 3.11 blender-mcp==1.9.1
   ```

5. Keep Blender open with the add-on server running on localhost. If it does not start automatically, use **Start MCP Server** in the viewport sidebar. Restart Codex if necessary to load the registered tools.

The Blender add-on needs the graphical application running. A background `blender --background` process cannot serve interactive MCP commands. If Codex cannot find `uvx`, use its absolute executable path in your local configuration.

An alternative is an isolated Python environment with [requirements.txt](requirements.txt), then registering that environment's `blender-mcp` executable. Do not commit the environment or personal Codex configuration.
