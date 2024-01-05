from typing import List, Callable, Any, TypeVar, Generic

T = TypeVar('T')

class DataWithRank(Generic[T]):
    def __init__(self, data: T, rank: str):
        self.__data = data
        self.__rank = rank

    def get_data(self) -> T:
        return self.__data
    
    def get_rank(self) -> str:
        return self.__rank
    

def calculate_rank(data_list: List[T], get_sort_value_from_data: Callable[[T], int], reverse: bool = False) -> List[DataWithRank[T]]:
    '''
    Function that calculates the rank of each item in a list of data and sorts it in order.

    Args:
        data_list (List[Any]): The list of data to calculate the rank of.
        get_sort_value_from_data (Callable[[Any], int]): A function that takes in a data item and returns a value to sort by.
        reverse (bool, optional): Whether to sort the data in reverse order. Defaults to False.

    Returns:
        List[DataWithRank]: A list of DataWithRank objects that contain the original data and the rank of the data.

    Example:
        data_list = [['a', 1], ['b', 2], ['c', 2], ['d', 3]]
        def get_sort_value_from_data(data):
            return data[1]
        calculate_rank(data_list, get_sort_value_from_data)
        # returns [DataWithRank(['d', 3], '1'), DataWithRank(['b', 2], 'T2'), DataWithRank(['c', 2], 'T2'), DataWithRank(['a', 1], '4')
        # summary: d=1, b=T2, c=T2, a=4
    '''
    # sort the data
    data_list.sort(key=get_sort_value_from_data, reverse=reverse)
    # calculate ranks
    data_with_rank = []
    current_rank = 1

    for i, i_data in enumerate(data_list):
        i_value = get_sort_value_from_data(i_data)
        # determine if we need to prepend T to the rank
        prepend_t = False
        tied_with_previous = False
        if i > 0:
            previous_value = get_sort_value_from_data(data_list[i - 1])
            if i_value == previous_value:
                prepend_t = True
                tied_with_previous = True
        else:
            next_value = get_sort_value_from_data(data_list[i + 1])
            if i_value == next_value:
                prepend_t = True

        if not prepend_t and i < len(data_list) - 1:
            next_value = get_sort_value_from_data(data_list[i + 1])
            if i_value == next_value:
                prepend_t = True

        if not tied_with_previous:
            current_rank = i + 1

        i_rank = str(current_rank) if not prepend_t else f'T{current_rank}'
        
        i_with_rank = DataWithRank(i_data, i_rank)
        data_with_rank.append(i_with_rank)
    
    return data_with_rank
