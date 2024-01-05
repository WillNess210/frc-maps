from typing import List, Tuple, Dict
from svg import CountyMap
from .calculate_rank import calculate_rank
from markdown_table_generator import generate_markdown, table_from_string_list, Alignment

def generate_ranked_county_table(county_map: CountyMap, county_code_to_object_keys_dict: Dict[str, List[str]], object_type: str) -> str:
    # Generate markdown table
    rows: List[Tuple[str, int]] = []
    for county_code, object_keys in county_code_to_object_keys_dict.items():
        county = county_map.get_county(county_code)
        if county is None:
            continue
        rows.append([county.get_name(), len(object_keys)])

    # calculate ranks
    rows_with_rank = calculate_rank(rows, lambda row: row[1], reverse=True)
    rows_with_rank = [[row.get_rank()] + row.get_data() for row in rows_with_rank]

    # prepend header row
    rows = [['Rank', 'County', f'Number of {object_type}s']] + rows_with_rank
    # turn every row into strings
    rows = [[str(cell) for cell in row] for row in rows]

    table = table_from_string_list(rows, Alignment.CENTER)
    markdown = generate_markdown(table)
    return markdown