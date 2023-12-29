# hd

hd (hexdump) is a modified version of hexdump / xxd that allows more flexibility for formatting
the byte values.

## Usage

Basic usage:

```
hd.py --input_file=INPUT_FILE
```

Arguments:

  - --input_file: th to input file.
  - --num_bytes: Number of bytes (from top of file) to read. Default: read all
  - --bytes_per_row: Number of bytes per row. Default: 10
  - -b: Enable binary output.
  - -h: Enable hex output.
  = -d: Enable decimal output.
