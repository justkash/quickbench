__HORIZONTAL_PADDING = 3

def print_2D_table(row_headers, col_headers, rows):
    max_row_header_len = max(len(header) for header in row_headers)
    max_col_header_len = max(len(header) for header in col_headers)

    print(max_row_header_len)

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


if __name__ == "__main__":
    colheaders = ["Average", "Min", "Max", "Standard Deviation", "Variance"]
    rowheaders = ["Elapsed Time (ms)",  "User Time (ms)", "Sys Time (ms)", "Peak Memory Usage (kB)", "# of Minor Page Faults", "# of Major Page Faults"]
    print_2D_table(rowheaders, colheaders, [])
