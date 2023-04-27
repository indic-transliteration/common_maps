## Intro
Shared string to string maps stored as TOML files, used for transliteration from one script to another.

Example users: [sanscript.js](https://github.com/indic-transliteration/sanscript.js) and [indic_transliteration_py](https://github.com/indic-transliteration/indic_transliteration_py).

## Notes
- The schema definition implicitly specifies a default (with possible alternates). So, we have itrans as well as itrans_lowercase.
- Currently we don't support inheritance and overriding of schemas - so there exist related copies like itrans and itrans_dravidian.
