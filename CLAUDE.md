# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hwnorm2** builds `keydoc/keydoc_glob1.sqlite` — the cross-dictionary headword index used by `csl-apidev`'s glob/prefix search (`dalglob.php`). It extends hwnorm1 by constructing "keydoc" documents (groups of dictionary entries sharing a headword) with normalized spelling variants and an inverted index for fast lookup.

Assumed local directory layout:
```
cologne/
  hwnorm2/          ← this repo
  csl-orig/         ← source digitization files
  hwnorm1/          ← hwnorm1c normalization tables
  csl-apidev/       ← deployment target for keydoc_glob1.sqlite
```

## Architecture

| File/Directory | Purpose |
|---|---|
| `redo.sh` | Main orchestrator: calls `redo_one_all.sh` → `redo_merge.sh` → `redo_final_all.sh` → `redo_glob1.sh` |
| `redo_one_all.sh` | Runs `redo_one.sh <dict>` for each dict in `dictlist.txt` |
| `redo_merge.sh` | Merges per-dictionary keydoc data into a combined index |
| `redo_final_all.sh` | Adds pointer tables and builds the inverted index |
| `redo_glob1.sh` | Builds `keydoc/keydoc_glob1.sqlite` from the final merged data |
| `dictlist.txt` | List of dictionary codes included in the keydoc index |
| `keydoc/` | Pipeline scripts and output SQLite files |
| `keydoc/distincthws/` | Per-dictionary distinct headword extraction (`redo.sh` inside) |
| `keydoc/work/` | Intermediate working files (not tracked by git) |
| `keydoc/previous/` | Archived outputs from prior pipeline runs |

### Pipeline Steps

```
sh redo_one_all.sh    # Build per-dict keydoc documents and normalizations
sh redo_merge.sh      # Merge all dicts into combined keydoc index
sh redo_final_all.sh  # Add cross-reference pointers, build inverted index
sh redo_glob1.sh      # Build keydoc_glob1.sqlite for API glob search
```

### Deployment

After building, move `keydoc/keydoc_glob1.sqlite` to `csl-apidev/sample/` (for local XAMPP) or the Cologne server, then push both repos and pull on Cologne.

### Local vs Cologne

`redo.sh` takes one argument: `xampp` or `cologne`. This controls server-specific path resolution in the sub-scripts.

## Common Commands

### Full rebuild (local XAMPP)
```bash
sh redo.sh xampp
```

### Full rebuild (Cologne server)
```bash
sh redo.sh cologne
```

### Rebuild only distinct headword lists (faster, from `keydoc/distincthws/`)
```bash
cd keydoc/distincthws
sh redo.sh
```

### Adding a new dictionary
Edit `dictlist.txt` to add the new dictionary code, then run the full rebuild.

## Dependencies

- **Python 3**
- **sqlite3** CLI
- **csl-orig** sibling repo — source digitization files
- **hwnorm1** sibling repo — `hwnorm1c.txt` normalization tables
