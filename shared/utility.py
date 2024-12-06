import random
from icontract import require, ensure


class Utility:
    """Utility class containing helper methods for the Minesweeper game."""

    @staticmethod
    @require(
        lambda array_shape: isinstance(array_shape, tuple) and len(array_shape) == 2 and all(isinstance(dim, int) and dim > 0 for dim in array_shape),
        "array_shape must be a tuple of two positive integers"
    )
    @require(lambda min_values, max_values: min_values >= 0 and max_values >= 0, "min_values and max_values must be non-negative")
    @require(lambda min_values, max_values: min_values <= max_values, "min_values cannot be greater than max_values")
    @require(lambda array_shape, max_values: max_values <= array_shape[0] * array_shape[1],
             "max_values cannot exceed the total number of cells")
    @ensure(
        lambda result, array_shape: len(result) == array_shape[0] and all(len(row) == array_shape[1] for row in result),
        "The returned array must match the specified array_shape"
    )
    @ensure(
        lambda result, value, min_values, max_values: min_values <= sum(cell == value for row in result for cell in row) <= max_values,
        "The number of distributed values must be between min_values and max_values"
    )
    def randomly_distribute_values_2d(array_shape, min_values, max_values, value=1):
        """
        Randomly distribute a specified value in a 2D array, ensuring the count of distributed values
        is between min_values and max_values.

        Parameters:
        - array_shape (tuple): Dimensions of the array (rows, columns).
        - min_values (int): Minimum number of values to distribute in the array.
        - max_values (int): Maximum number of values to distribute in the array.
        - value (int or float): The value to be distributed. Default is 1.

        Returns:
        - list of lists: A 2D array with the values randomly distributed.

        Raises:
        - ValueError: If constraints on min_values, max_values, or array dimensions are violated.
        """
        rows, cols = array_shape

        # Initialize a 2D array of zeros
        array = [[0 for _ in range(cols)] for _ in range(rows)]

        # Flatten the 2D array indices into a list
        all_indices = [(i, j) for i in range(rows) for j in range(cols)]

        # Ensure the minimum number of values are distributed
        min_indices = random.sample(all_indices, k=min_values)
        for i, j in min_indices:
            array[i][j] = value

        # Distribute the remaining values to satisfy the maximum constraint
        remaining_values = max_values - min_values
        if remaining_values > 0:
            available_indices = [idx for idx in all_indices if array[idx[0]][idx[1]] == 0]
            additional_indices = random.sample(available_indices, k=remaining_values)
            for i, j in additional_indices:
                array[i][j] = value

        return array
