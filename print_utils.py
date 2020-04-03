__HORIZONTAL_PADDING = 1

def print_2D_table(row_headers, col_headers, *rows):
    max_row_header_len = max(len(header) for header in row_headers)
    max_col_header_len = max(len(header) for header in col_headers)

    # Print col headers
    print(" "*(__HORIZONTAL_PADDING+max_row_header_len), end="")
    for header in col_headers:
        print(f"{header:^{max_col_header_len}}", end="")
    print("")

    # Print underline for col headers
    print(" "*(__HORIZONTAL_PADDING+max_row_header_len), end="")
    for header in col_headers:
        print(f"{'='*len(header):^{max_col_header_len}}", end="")
    print("")

    # Print row headers
    for header, row in zip(row_headers, rows):
        print(f"{header:>{__HORIZONTAL_PADDING + max_row_header_len}}", end="")
        for val in row:
            if type(val) == str:
                print(f"{val:<}", end="")
            else:
                print(f"{val:^{max_col_header_len}.3f}", end="")
        print("")
