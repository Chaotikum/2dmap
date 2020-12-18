# Scripts

## Dependencies

`compress.py` braucht Pillow. Das kann zum Beispiel über `pip3 install pillow` installiert werden.

## compress.py

```
Combine all used tilesets into one large tileset containing only the actually used tiles.

positional arguments:
  input       input JSON file
  output      output directory

optional arguments:
  -h, --help  show this help message and exit
```

Beispiel:
```
python3 compress.py ../luebeck/innenstadt.json  ../compressed/
```

## merge.py

```
Merge adjacent layers in JSON tile maps if they do not contain tiles in the same positions.

positional arguments:
  input                 input JSON file
  output                output JSON file

optional arguments:
  -h, --help            show this help message and exit
  --ignore IGNORE [IGNORE ...]
                        Leave layers untouched with the given names.
  --ignore-suffix IGNORE_SUFFIX [IGNORE_SUFFIX ...]
                        Leave layers untouched whose names end with the given suffixes.
```

Beispiel:
```
python3 merge.py ../compressed/innenstadt.json ../compressed/innenstadt.json --ignore start --ignore-suffix _day _night _snow
```

## edit.py

```
Edit JSON tile maps.

positional arguments:
  input          input JSON file
  output         output JSON file

optional arguments:
  -h, --help     show this help message and exit
  --day DAY      Set the opacity of all layers whose name ends with _day
  --night NIGHT  Set the opacity of all layers whose name ends with _night
  --snow SNOW    Set the opacity of all layers whose name is weather_snow
```

Beispiel:
```
python3 edit.py ../compressed/innenstadt.json ../compressed/innenstadt.json --day 1 --night 0 --snow 0
```