__ROW_HEADER_PADDING = 2
__COL_HEADER_PADDING = 8

def print_2D_table(row_headers, col_headers, *rows):
    max_row_header_len = max(len(header) for header in row_headers)
    max_col_header_len = max(len(header) for header in col_headers)

    total_row_header_padding = __ROW_HEADER_PADDING + max_row_header_len

    # Print col headers
    print(" "*total_row_header_padding, end="")
    for header in col_headers:
        print(f"{header:<{len(header) + __COL_HEADER_PADDING}}", end="")
    print("")

    # Print underline for col headers
    print(" "*total_row_header_padding, end="")
    for header in col_headers:
        print(f"{'-'*len(header):<{len(header) + __COL_HEADER_PADDING}}", end="")
    print("")

    # Print row headers
    for header, row in zip(row_headers, rows):
        print(f"{header:>{max_row_header_len}}{' '*__ROW_HEADER_PADDING}", end="")
        for colheader, val in zip(col_headers, row):
            if type(val) == str:
                print(f"{val:<}", end="")
            elif type(val) == int:
                print(f"{val:<{len(colheader) + __COL_HEADER_PADDING}d}", end="")
            else:
                print(f"{val:<{len(colheader) + __COL_HEADER_PADDING}.3f}", end="")
        print("")

def print_table(row_headers, *rows):
    max_row_header_len = max(len(header) for header in row_headers)

    for header, row in zip(row_headers, rows):
        print(f"{header:>{max_row_header_len}}{' '*__ROW_HEADER_PADDING}", end="")
        for val in row:
            if type(val) == str:
                print(f"{val:<}", end="")
            elif type(val) == int:
                print(f"{val:<{__COL_HEADER_PADDING}d}", end="")
            else:
                print(f"{val:<{__COL_HEADER_PADDING}.3f}", end="")
        print("")
