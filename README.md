# hd

hd (hexdump) is like hexdump / xxd but allows more flexibility in formatting the byte values.

## Usage

Basic usage:

```
hd.py --input_file=INPUT_FILE
```

Arguments:

  - `--input_file`: The filepath to input file.
  - `--num_bytes`: Number of bytes to read. (default: read all)
  - `--bytes_per_row`: Number of bytes per row. (default: 10)
  - `-b`: Enable binary output.
  - `-h`: Enable hex output.
  - `-d`: Enable decimal output.

