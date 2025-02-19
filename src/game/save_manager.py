import os
import time


class SaveManager:
    """
    Save manager class to manage the save files.
    """
    MEMORY_FILE_NUM = 3  # Set to 3 max save files

    @staticmethod
    def get_save_file_path():
        """
        This method determine and returns the save file path.
        To set specific details of how save file is determined, 
        change the implementation of this method.
        Currently, it returns the earliest created file path
        if no empty file exist.

        return: the save file path
        """
        earliest_created_filepath = None
        earliest_date = float("inf")
        for i in range(0, SaveManager.MEMORY_FILE_NUM):
            file_path = f"src/memory/memo_{i}.json"
            if os.path.getsize(file_path) == 0:
                return file_path
            date = os.path.getmtime(file_path)
            if date < earliest_date:
                earliest_date = date
                earliest_created_filepath = file_path

        return earliest_created_filepath

    @staticmethod
    def show_save_files():
        """
        This method shows all the save files.
        This is used in the setup page to let the player choose 
        the file to resume.

        return: list
        """
        file = []
        for i in range(0, SaveManager.MEMORY_FILE_NUM):
            file_path = f"src/memory/memo_{i}.json"
            if os.path.getsize(file_path) != 0:
                # Obtain the last modified timestamp of the file
                m_timestamp = os.path.getmtime(file_path)
                # Convert the timestamp to a readable date format
                date = time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(m_timestamp))
                file.append((file_path, date))
        return file

    @staticmethod
    def has_save_file():
        """
        This method checks if there is any save file.

        return: bool
        """
        for i in range(0, SaveManager.MEMORY_FILE_NUM):
            file_path = f"src/memory/memo_{i}.json"
            if os.path.getsize(file_path) != 0:
                return True
        return False