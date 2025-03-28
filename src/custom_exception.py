import traceback
import sys


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super(CustomException, self).__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_traceback = error_detail.exc_info()
        filename = exc_traceback.tb_frame.f_code.co_filename
        linenumber = exc_traceback.tb_lineno

        return f"Error in {filename}, line {linenumber}: {error_message}"

    def __str__(self):
        return self.error_message

