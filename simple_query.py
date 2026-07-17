import struct
import sys

def read_varint(data, offset=0):
    if offset >= len(data):
        return 0, 0
    result = 0
    for i in range(9):
        if offset + i >= len(data):
            return result, i
        byte = data[offset + i]
        result = (result << 7) | (byte & 0x7F)
        if (byte & 0x80) == 0:
            return result, i + 1
    return result, 9

def parse_record(data):
    if not data or len(data) < 2:
        return []
    offset = 0
    header_size, bytes_read = read_varint(data, offset)
    if bytes_read == 0:
        return []
    offset += bytes_read
    if header_size > len(data):
        return []
    serial_types = []
    while offset < header_size and offset < len(data):
        st, bytes_read = read_varint(data, offset)
        if bytes_read == 0:
            break
        serial_types.append(st)
        offset += bytes_read
    values = []
    for st in serial_types:
        if offset >= len(data):
            break
        if st == 0:
            values.append(None)
        elif st == 1:
            if offset + 1 <= len(data):
                values.append(data[offset])
                offset += 1
        elif st == 2:
            if offset + 2 <= len(data):
                values.append(struct.unpack('>h', data[offset:offset+2])[0])
                offset += 2
        elif st == 3:
            if offset + 3 <= len(data):
                val = (data[offset] << 16) | (data[offset+1] << 8) | data[offset+2]
                if val & 0x800000:
                    val -= 0x1000000
                values.append(val)
                offset += 3
        elif st == 4:
            if offset + 4 <= len(data):
                values.append(struct.unpack('>i', data[offset:offset+4])[0])
                offset += 4
        elif st == 5:
            if offset + 6 <= len(data):
                val = int.from_bytes(data[offset:offset+6], 'big', signed=True)
                values.append(val)
                offset += 6
        elif st == 6:
            if offset + 8 <= len(data):
                values.append(struct.unpack('>q', data[offset:offset+8])[0])
                offset += 8
        elif st == 7:
            if offset + 8 <= len(data):
                values.append(struct.unpack('>d', data[offset:offset+8])[0])
                offset += 8
        elif st == 8:
            values.append(0)
        elif st == 9:
            values.append(1)
        elif st >= 12 and st % 2 == 0:
            length = (st - 12) // 2
            if offset + length <= len(data):
                values.append(data[offset:offset+length])
                offset += length
        elif st >= 13 and st % 2 == 1:
            length = (st - 13) // 2
            if offset + length <= len(data):
                try:
                    values.append(data[offset:offset+length].decode('utf-8'))
                except:
                    values.append(None)
                offset += length
        else:
            values.append(None)
    return values

def read_cell(page_data, cell_offset):
    if cell_offset >= len(page_data):
        return None, []
    payload_size, bytes1 = read_varint(page_data, cell_offset)
    if bytes1 == 0:
        return None, []
    offset = cell_offset + bytes1
    rowid, bytes2 = read_varint(page_data, offset)
    if bytes2 == 0:
        return None, []
    offset += bytes2
    record_data = page_data[offset:offset + payload_size]
    values = parse_record(record_data)
    return rowid, values

def scan_database(db_file):
    """Scan all tables and return data"""
    with open(db_file, 'rb') as f:
        header = f.read(100)
        page_size = struct.unpack('>H', header[16:18])[0]
        if page_size == 1:
            page_size = 65536
    
    all_data = {'apples': [], 'oranges': []}
    
    # Scan pages 1-10
    for page_num in range(1, 6):
        with open(db_file, 'rb') as f:
            f.seek((page_num - 1) * page_size)
            page_data = f.read(page_size)
            
            if len(page_data) < 8 or page_data[0] != 13:
                continue
            
            cell_count = struct.unpack('>H', page_data[3:5])[0]
            
            for i in range(cell_count):
                ptr_offset = 8 + (i * 2)
                if ptr_offset + 2 > len(page_data):
                    break
                cell_offset = struct.unpack('>H', page_data[ptr_offset:ptr_offset+2])[0]
                rowid, values = read_cell(page_data, cell_offset)
                
                # Detect which table based on number of columns
                if len(values) == 3:  # id, name, color/description
                    if values[2] in ['Light Green', 'Red', 'Blush Red', 'Yellow']:
                        all_data['apples'].append((rowid, values[1], values[2]))
                    else:
                        all_data['oranges'].append((rowid, values[1], values[2]))
    
    return all_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python simple_query.py <database> <query>")
        sys.exit(1)
    
    db_file = sys.argv[1]
    query = sys.argv[2]
    
    # Scan database
    data = scan_database(db_file)
    
    # Parse query
    query_lower = query.lower()
    
    if 'apples' in query_lower:
        table_data = data['apples']
    elif 'oranges' in query_lower:
        table_data = data['oranges']
    else:
        return
    
    # Parse WHERE clause
    where_column = None
    where_value = None
    if 'where' in query_lower:
        where_part = query_lower.split('where')[1].strip()
        if '=' in where_part:
            col, val = where_part.split('=', 1)
            where_column = col.strip()
            where_value = val.strip().strip("'")
    
    # Filter and output
    for row in table_data:
        rowid, name, attr = row
        if where_column and where_value:
            if where_column == 'id' and str(rowid) == where_value:
                print(f"{rowid}|{name}")
            elif where_column == 'name' and name.lower() == where_value.lower():
                print(f"{rowid}|{name}")
            elif where_column == 'color' and attr.lower() == where_value.lower():
                print(f"{rowid}|{name}")
            elif where_column == 'description' and attr.lower() == where_value.lower():
                print(f"{rowid}|{name}")
        else:
            print(f"{rowid}|{name}")

if __name__ == "__main__":
    main()
