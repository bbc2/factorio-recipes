#!/bin/bash
set -o errexit
set -o nounset

base="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
factorio_path="$1"

eval $(luarocks path)
export LUA_PATH="$factorio_path/data/base/prototypes/recipe/?.lua;$factorio_path/data/base/?.lua;$factorio_path/data/core/lualib/?.lua;$LUA_PATH"
lua "$base/extract_recipes.lua"
