# Plan: Songs as Git Repos

## Overview
Create a workflow where each Ableton song is its own git repository in `~/songs/`. This enables version control for music projects - track iterations, branch for remixes, collaborate, and never lose work.

## Directory Structure

```
~/songs/
├── .template/              # Template for new songs
│   ├── .gitignore
│   ├── README.md.template
│   └── init-song.sh        # Script to create new song repos
├── beat-001/
│   ├── .git/
│   ├── .gitignore
│   ├── README.md           # Notes, BPM, key, inspiration
│   ├── beat-001.als        # Main Ableton project
│   └── Samples/
│       └── Processed/      # Bounced/frozen clips (tracked)
├── remix-project/
│   └── ...
└── collab-track/
    └── ...
```

## What to Track vs Ignore

### Track (commit these)
- `.als` files (Ableton project - these are gzip XML, git handles well)
- `Samples/Processed/` - bounced/frozen audio you created
- `README.md` - song notes, BPM, key, ideas
- MIDI files if exported
- Stems for collaboration

### Ignore (in .gitignore)
- `Backup/` - Ableton's auto-backups (redundant with git)
- `Samples/Imported/` - samples from packs (large, already on disk)
- `*.asd` - Ableton analysis files (regenerated automatically)
- `.DS_Store`
- Ableton crash recovery files

## Implementation Steps

### 1. Create the songs directory and template
- Create `~/songs/.template/`
- Add `.gitignore` with Ableton-specific ignores
- Add `README.md.template` for song metadata
- Add `init-song.sh` script to bootstrap new repos

### 2. Create the init-song script
The script will:
- Take a song name as argument
- Create `~/songs/<song-name>/`
- Copy template files
- Initialize git repo
- Create initial commit
- Open in Ableton (optional)

### 3. Create a .gitignore for Ableton projects
```gitignore
# Ableton
Backup/
*.asd
Ableton Project Info/

# Samples - ignore imported, track processed
Samples/Imported/

# OS
.DS_Store
Thumbs.db

# Large media (use git-lfs if needed)
# *.wav
# *.aif
```

### 4. Create README template
```markdown
# Song Name

## Details
- **BPM**:
- **Key**:
- **Genre**:
- **Started**: YYYY-MM-DD

## Notes
-

## Versions
- v1: Initial idea
```

### 5. Optional: MCP tool integration
Add a tool to `ableton-mcp-server` that:
- Creates new song repos via Claude
- Saves current Ableton project to the song's repo
- Commits with auto-generated message based on changes

## Questions to Clarify

1. **Sample handling**: Do you want to track all audio files, or use git-lfs for large files?
2. **Naming convention**: Numbered (beat-001) or descriptive (summer-vibes)?
3. **Auto-commit**: Want Claude to auto-commit after significant changes?
4. **Ableton project location**: Keep Ableton's default location and symlink, or change Ableton's save location?

## Next Steps
1. Get answers to clarifying questions
2. Create the template structure
3. Write the init-song.sh script
4. Test with a new song
5. Optionally add MCP tools for song management
