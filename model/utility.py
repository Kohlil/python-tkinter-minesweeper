import random

class Utility:
    
    @staticmethod
    def randomly_distribute_values_2d(array_shape, min_values, max_values, value=1):
        """
        Randomly distribute at least `min_values` and at most `max_values` in a 2D array.

        Parameters:
        - array_shape: tuple, dimensions of the array (rows, columns).
        - min_values: int, minimum number of values to distribute in the array.
        - max_values: int, maximum number of values to distribute in the array.
        - value: int or float, the value to be distributed. Default is 1.

        Returns:
        - list of lists: The 2D array with the values randomly distributed.
        """
        rows, cols = array_shape
        total_cells = rows * cols

        if min_values > max_values:
            raise ValueError("min_values cannot be greater than max_values")
        if max_values > total_cells:
            raise ValueError("max_values cannot exceed total number of cells")

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