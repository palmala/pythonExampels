def split_list_equal_chunks(list_to_split: list, chunks: int) -> list:
    if chunks < 1:
        return [list_to_split]
    chunk_size = len(list_to_split) // chunks
    if chunk_size < 1:
        return [list_to_split]

    return [list_to_split[i:i + chunk_size] for i in range(0, len(list_to_split), chunk_size)]
