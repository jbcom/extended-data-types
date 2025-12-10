---
inclusion: always
---

# Local Agent Operations

These rules apply when operating in a local agent environment (Kiro, Claude Code CLI).

## Authentication

Local agents have pre-authenticated GitHub CLI access:

```bash
# No explicit token needed for gh commands
gh pr create --title "feat: new feature"
gh issue list
gh api repos/:owner/:repo

# For jbcom org repos, use explicit token if needed
GH_TOKEN="$GITHUB_TOKEN" gh <command>
```

## Git Operations

Use non-interactive flags for headless operation:

```bash
# View commits without pager
git --no-pager log --oneline -10

# Interactive rebase without editor prompt
GIT_EDITOR=true git rebase -i HEAD~3

# Amend without editor
git commit --amend --no-edit

# Push with force-with-lease (safer than --force)
git push --force-with-lease
```

## Environment Differences from Cloud Agents

| Aspect | Local Agent | Cloud Agent |
|--------|-------------|-------------|
| GitHub CLI | Pre-authenticated | Requires `GH_TOKEN` |
| File access | Full system access | Container-scoped |
| MCP servers | Local stdio | Remote via gateway |
| Git config | Usually configured | May need setup |
| Editor prompts | Can spawn | Blocked |

## MCP Server Access

Local agents use stdio-based MCP servers directly:
- Server processes spawn locally
- Direct communication without network overhead
- Configuration in `.kiro/settings/mcp.json`

## File System Access

Local agents have full access to:
- `~/src/` - All jbcom repositories
- Project files and directories
- System tools and binaries

## Session Persistence

Local agents maintain context between runs:
- Memory bank in `memory-bank/` directory
- Git state persists
- Environment variables preserved
