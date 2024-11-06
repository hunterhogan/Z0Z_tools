# Z0Z_tools

"Z0Z_"- is a placeholder, and a Z0Z_tool is at best, a prototype.

## Install an arbitrary package with `pipAnything`

Try to install a package that doesn't have installation files.

```sh
python -m Z0Z_tools.pipAnything <pathPackage>
```

## Unpack and convert elements to `str` types with `stringItUp`

## Merge and/or lightly clean a dictionary of lists with `updateExtendPolishDictionaryLists`

- Merges multiple dictionaries of lists into a single dictionary.
- Optionally remove duplicates each list.
- Optionally sort each list.
- Optionally delete data that won't merge.

## Basic read/write WAV files with `readAudioFile` and `writeWav`

The only option is the sample rate.

## Use `loadWaveforms` to create one array of waveforms from multiple files

## Install this package

### From Github

```sh
pip install Z0Z_tools@git+https://github.com/hunterhogan/Z0Z_tools.git
```

### From a local directory

#### Windows

```powershell
git clone https://github.com/hunterhogan/Z0Z_tools.git \path\to\Z0Z_tools
pip install Z0Z_tools@file:\path\to\Z0Z_tools
```

#### POSIX

```bash
git clone https://github.com/hunterhogan/Z0Z_tools.git /path/to/Z0Z_tools
pip install Z0Z_tools@file:/path/to/Z0Z_tools
```

## Install updates

```sh
pip install --upgrade Z0Z_tools@git+https://github.com/hunterhogan/Z0Z_tools.git
```
