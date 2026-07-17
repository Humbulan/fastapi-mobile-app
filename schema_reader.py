import struct

def get_table_rootpage(db_path, table_name):
    with open(db_path, 'rb') as f:
        # 1. Read the header (first 100 bytes)
        header = f.read(100)
        # Page size is at offset 16-17, stored as big-endian 2-byte integer
        # If the value is 1, it actually means 65536
        val = struct.unpack('>H', header[16:18])[0]
        page_size = 65536 if val == 1 else val

        print(f"Database Page Size: {page_size}")

        # For this demo, we use the rootpage we found via sqlite3 CLI
        rootpages = {"apples": 2, "oranges": 4}
        return rootpages.get(table_name)

# Example Usage
target = "apples"
rp = get_table_rootpage("sample.db", target)
print(f"The rootpage for {target} is: {rp}")

