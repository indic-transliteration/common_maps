# Publishing: npm vs dart (pub.dev)

This repository uses a single Git repository to publish packages to both **npm** and **pub.dev** (Dart). The two publishing streams are completely independent and will not interfere with each other.

## How It Works

### npm Publishing (`package.json`)

- **Package name**: `@indic-transliteration/common_maps`
- **Version**: Managed in `package.json`
- **Files included**: Everything except what `.npmignore` lists

The `.npmignore` file explicitly excludes Dart-specific files and directories:
```
.dart_tool/
.pub/
pubspec.lock
.pub-cache/
build/
pubspec.yaml
lib/
tool/
test/
```

This means when you run `npm publish`, only the TOML map files and supporting files (like README, CHANGELOG, language_code_to_script.json) are included in the npm package.

### dart (pub.dev) Publishing (`pubspec.yaml`)

- **Package name**: `indic_transliteration_maps`
- **Version**: Managed in `pubspec.yaml`
- **Files included**: All non-ignored files, but typically uses `lib/` for Dart code

In this repository, the Dart package relies on the TOML files directly from the repository root (not from `lib/`). The Dart package metadata is in `pubspec.yaml`.

## Why They Don't Step On Each Other's Toes

1. **Different package names**: npm uses `@indic-transliteration/common_maps` while pub.dev uses `indic_transliteration_maps`

2. **Different version numbers**: They can be versioned independently. You can publish an npm update without changing the Dart version and vice versa.

3. **`.npmignore` separation**: The `.npmignore` ensures npm publishes only the data files (TOML, JSON) and not the Dart-specific files that would be meaningless in an npm context.

4. **No overlapping files**: The two publishing targets publish to completely separate registries with separate metadata files.

## Workflow

To update and publish:

1. **For npm**: Update `package.json` version, then run `npm publish`
2. **For pub.dev**: Update `pubspec.yaml` version, then run `dart pub publish`

Each can be updated and published independently based on their own release cycles.