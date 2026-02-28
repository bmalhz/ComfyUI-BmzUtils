# ComfyUI-BmzUtils

Custom utility nodes for **ComfyUI**.

## Overview

**ComfyUI-BmzUtils** provides small, focused utility nodes to simplify common tasks inside ComfyUI flows.

## BmzJinja2String

**Purpose** — Render a Jinja2 template string using variables provided to the node.

**Behavior** — The node accepts a template string and a set of variables. It renders the template with the variables and outputs the rendered string. If a variable is missing, Jinja2's default behavior applies.

### Inputs

- **Template** (`str`) — The Jinja2 template text to render.
- **Variables** — One of:
  - **Dict** (`Dict[str, str]`) — A mapping of keys to values.
  - **Plain text** — A simple key/value list using the format shown below.

### Plain-text variable format

Provide variables as plain text using one variable per line. Each line must use `key:value`. Lines may be separated by a pipe `|` or by newlines. Example valid inputs:
