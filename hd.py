#!/usr/bin/python3

import sys, getopt, os

OFFSET_COL_NAME = "OFFSET"

# Total number of spaces to pad around the width.
SPACE_PADDING = 2

# Separator used in between format types.
VALUE_SEPARATOR = "-"

def format_byte(byte, enable_hex, enable_decimal, enable_binary, value_width=15):
  # Simplify the 0 case. It's not really useful seeing the different representations of 0.
  if byte.hex() == "00":
    return "0"

  outputs = []
  if enable_decimal:
    outputs += [f"{int(byte.hex(), 16):>3}"]
  if enable_hex:
    outputs += [byte.hex().upper()]
  if enable_binary:
    outputs += ["{:08b}".format(int(byte.hex(), 16))]

  return VALUE_SEPARATOR.join(output for output in outputs)
 
def print_header(bytes_per_row, offset_width, value_width):
  # The ^ character means center alignment.
  headers = [f"{OFFSET_COL_NAME:^{offset_width}}"]
  headers += [f"{str(index):^{value_width}}" for index in list(range(bytes_per_row))]
  header = '|'.join(f"{header:^{len(header) + SPACE_PADDING}}" for header in headers)
  header = '|' + header + '|'

  dashed_row = ['-' * len(val) for val in headers]
  dashed_row_str = '|'.join(f"{value:^{len(value) + SPACE_PADDING}}" for value in dashed_row)
  dashed_row_str = '|' + dashed_row_str + '|'

  # Print column names and a dashed row.
  print(header)
  print(dashed_row_str)
 
def print_row(output, offset_width, value_width):
  row = [f"{output[0]:>{offset_width}}"]
  row += [f"{value:^{value_width}}" for value in output[1:]]
  print('|' + '|'.join(f"{value:^{len(value) + SPACE_PADDING}}" for value in row) + '|')

def process(input_file, num_bytes, bytes_per_row, enable_hex, enable_decimal, enable_binary):
  formats = []
  if enable_decimal:
    formats += ["DECIMAL"]
  if enable_hex:
    formats += ["HEX"]
  if enable_binary:
    formats += ["BINARY"]
    
  print(f"format: {VALUE_SEPARATOR.join(formats)}\n")

  # Number of bytes read so far.
  bytes_read = 0

  # Width of each value cell, calculated based on the formats needed to be shown.
  value_width = 0

  # Number of types (hex, binary, decimal) that will be shown.
  type_count = 0

  if enable_hex:
    value_width += 2
    type_count += 1
  if enable_decimal:
    value_width += 3
    type_count += 1
  if enable_binary:
    value_width += 8
    type_count += 1

  # Calculate offset and value widths.
  offset_width = max(len(str(num_bytes)), len(OFFSET_COL_NAME))
  value_width += (type_count - 1)

  with open(input_file, mode='rb') as file:
    print_header(bytes_per_row, offset_width, value_width)
    output = []
    while (byte:= file.read(1)):
      # Insert the offset byte before the first byte in the row.
      if len(output) == 0:
        output = [bytes_read]

      bytes_read += 1

      output += [format_byte(byte, enable_hex, enable_decimal, enable_binary)]
      finished_processing = (bytes_read == int(num_bytes))
      if bytes_read % bytes_per_row == 0 or finished_processing:
        print_row(output, offset_width, value_width)
        output = []
        if finished_processing:
          break
  print(f"\nRead {bytes_read} bytes.")

def usage():
  '''
  --input_file: Path to input file.
  --num_bytes: Number of bytes (from top of file) to read. Default: read all
  --bytes_per_row: Number of bytes per row. Default: 10
  -b: Enable binary output.
  -h: Enable hex output.
  -d: Enable decimal output.
  '''
  print("Usage: hd.py --input_file=INPUT_FILE --num_bytes -b (binary) -h (hex) -d (decimal)")

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hdb",
                               ["input_file=", "num_bytes=", "bytes_per_row="])
  except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

  input_file = None
  num_bytes = None
  bytes_per_row = 10

  enable_hex = True
  enable_hex_override = False

  enable_decimal = True
  enable_decimal_override = False

  enable_binary = True
  enable_binary_override = False

  for opt, arg in opts:
    if opt == "--input_file":
      input_file = arg
    elif opt == "--num_bytes":
      num_bytes = int(arg)
    elif opt == "--bytes_per_row":
      bytes_per_row = int(arg)
    elif opt == "-h":
      enable_hex_override = True
    elif opt == "-d":
      enable_decimal_override = True
    elif opt == "-b":
      enable_binary_override = True
    else:
      assert False, "Unhandled option"

  if input_file is None:
    usage()
    sys.exit(2)

  # If num_bytes is not specified, process the whole file.
  file_size = os.path.getsize(input_file)
  if num_bytes is None:
    num_bytes = file_size
  else:
    num_bytes = min(num_bytes, file_size)

  if enable_hex_override or enable_decimal_override or enable_binary_override:
    enable_hex = enable_hex_override
    enable_decimal = enable_decimal_override
    enable_binary = enable_binary_override

  process(input_file, num_bytes, bytes_per_row, enable_hex, enable_decimal, enable_binary)

if __name__ == '__main__':
  main()
