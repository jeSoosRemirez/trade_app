import pandas as pd
import os

class File:
    """
    The base File class that provides basic methods for
    data storing and retrieving.
    In the inherited classes 'filename' should be provided as
    default value in __init__ args.
    """
    files_path = "database/files/"

    def __init__(self, filename):
        self.filename = filename

    def get_data(self, key_name: str = None, arg: str = None) -> pd.DataFrame:
        """
        Get all data from file, if key_name and arg are provided then get data that
        match key_name and arg.
        Probable ERRORS could be caused if file is empty.

        Args:
            key_name (str, optional): if provided then will be used in filter as key
            arg (str, optional): if provided then will be used in filter as value

        Returns:
            pd.DataFrame: data from file
        """
        data = pd.read_csv(os.path.join(File.files_path, self.filename+".csv"))
        if arg:
            data = data.query(f"{key_name} == {arg}")
            return data

        return data

    def post_data(self, data: dict) -> bool:
        """
        Post data to file.

        Args:
            data (dict): data to append

        Returns:
            bool: True if success
        """
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data, index=[0])
        data.to_csv(
            os.path.join(File.files_path, self.filename+".csv"),
            mode="a",
            index=False,
            header=True
            )

        return True


class UserFile(File):
    def __init__(self, filename="users"):
        self.filename = filename


class OrderFile(File):
    def __init__(self, filename="orders"):
        self.filename = filename


class HistoricalDataFile(File):
    def __init__(self, filename="historical_data"):
        self.filename = filename
