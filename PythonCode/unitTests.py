import unittest
from unittest.mock import patch, MagicMock
import pyGUI
class TestisNumber(unittest.TestCase):
    @patch('pyGUI.set_error_label')
    def test_invalid_inputs(self, mock_display_error):
        invalid_inputs = [
            ("00010", False),
            ("00010", True),
            ("10.5", False),
            ("-10.5", False),
            ("10.0.1", True),
            ("", True),
            ("   ", True),
            ("abc", True),
        ]
        for input_value, can_float in invalid_inputs:
            with self.subTest(input=input_value, canFloat=can_float):
                self.assertFalse(pyGUI.is_number(input_value, can_float))
    @patch('pyGUI.set_error_label')
    def test_valid_inputs(self, mock_display_error):
        valid_inputs = [
            (" 10 ", False),
            ("10", False),
            ("-10", False),
            ("0", False),
            ("0.0", True),
            ("10.5", True),
            (" 10.5 ", True),
            ("-5.5", True),
            ("-5", True),
        ]
        for input_value, can_float in valid_inputs:
            with self.subTest(input=input_value, canFloat=can_float):
                self.assertTrue(pyGUI.is_number(input_value, can_float))

class TestTimeAtPeakEntry(unittest.TestCase):
    @patch('pyGUI.set_error_label')
    def test_invalid_inputs(self, mock_display_error):
        invalid_inputs = [
            "test",
            "",
            "-5",
            "0",
            "60001",
            "00010"
        ]
        for input_value in invalid_inputs:
            with self.subTest(input=input_value):
                self.assertFalse(pyGUI.check_time_at_peak_entry(input_value))
    @patch('pyGUI.set_error_label')
    def test_valid_inputs(self, mock_display_error):
        valid_inputs = [
            "10",
            "1",
            "60000",
            "10.5",
            " 10 ",
        ]
        for input_value in valid_inputs:
            with self.subTest(input=input_value):
                self.assertTrue(pyGUI.check_time_at_peak_entry(input_value))

class TestNumCyclesEntry(unittest.TestCase):
    @patch('pyGUI.set_error_label')
    def test_invalid_inputs(self, mock_display_error):
        invalid_inputs = [
            "test",
            "",
            "-5",
            "0",
            "60001",
            "1.0",
            "00010"
        ]
        for input_value in invalid_inputs:
            with self.subTest(input=input_value):
                self.assertFalse(pyGUI.check_num_cycles_entry(input_value))
    @patch('pyGUI.set_error_label')
    def test_valid_inputs(self, mock_display_error):
        valid_inputs = [
            "10",
            "1",
            "60000",
            " 10 ",
        ]
        for input_value in valid_inputs:
            with self.subTest(input=input_value):
                self.assertTrue(pyGUI.check_num_cycles_entry(input_value))

class TestDutyCycleEntry(unittest.TestCase):
    @patch('pyGUI.set_error_label')
    def test_invalid_inputs(self, mock_display_error):
        invalid_inputs = [
            "test",
            "",
            "-5",
            "60001",
            "00010"
        ]
        for input_value in invalid_inputs:
            with self.subTest(input=input_value):
                self.assertFalse(pyGUI.check_duty_cycle_entry(input_value))
    @patch('pyGUI.set_error_label')
    def test_valid_inputs(self, mock_display_error):
        valid_inputs = [
            "10",
            "100",
            " 10 ",
            "1.0",
            "0",
        ]
        for input_value in valid_inputs:
            with self.subTest(input=input_value):
                self.assertTrue(pyGUI.check_duty_cycle_entry(input_value))

class TestCloseApplication(unittest.TestCase):
    @patch('pyGUI.root')
    def test_close_application(self, mock_root):
        pyGUI.close_application()
        mock_root.destroy.assert_called_once()

class TestClearErrorLabels(unittest.TestCase):
    def setUp(self):
        self.mock_label1 = MagicMock()
        self.mock_label2 = MagicMock()
        pyGUI.error_labels = [self.mock_label1, self.mock_label2]
    def test_clear_error_labels(self):
        pyGUI.clear_error_labels()
        self.mock_label1.destroy.assert_called_once()
        self.mock_label2.destroy.assert_called_once()
        self.assertEqual(pyGUI.error_labels, [])

class TestClearPWMLabel(unittest.TestCase):
    def setUp(self):
        self.mock_pwm_label = MagicMock()
        pyGUI.pwm_label = self.mock_pwm_label
    def test_clear_pwm_label(self):
        pyGUI.clear_pwm_label()
        self.mock_pwm_label.destroy.assert_called_once()
        self.assertIsNone(pyGUI.pwm_label)

class TestCheckSquareType(unittest.TestCase):
    def test_valid_inputs(self):
        self.assertEqual(pyGUI.check_square_type(1), "negative")
        self.assertEqual(pyGUI.check_square_type(0),"positive")
    def test_invalid_inputs(self):
        self.assertEqual(pyGUI.check_square_type(10), "unknown")
        self.assertEqual(pyGUI.check_square_type(-1), "unknown")
        self.assertEqual(pyGUI.check_square_type(1.0), "unknown")
        self.assertEqual(pyGUI.check_square_type(-1.0), "unknown")
        self.assertEqual(pyGUI.check_square_type(0.0), "unknown")
        self.assertEqual(pyGUI.check_square_type(-0.0), "unknown")
        self.assertEqual(pyGUI.check_square_type("djhagfsjlk"), "unknown")

class TestSendToArduino(unittest.TestCase):
    @patch('pyGUI.serial.Serial')
    def test_send_to_arduino(self, MockSerial):
        mock_serial_instance = MockSerial.return_value
        time_at_peak_value = "100"
        num_cycles_value = "50"
        duty_cycle_value = "75"
        square_type_value = "positive"
        pyGUI.send_to_arduino(mock_serial_instance, time_at_peak_value, num_cycles_value, duty_cycle_value, square_type_value)
        expected_data = f"{time_at_peak_value},{num_cycles_value},{duty_cycle_value},{square_type_value}\n"
        mock_serial_instance.write.assert_called_once_with(expected_data.encode('utf-8'))
    @patch('pyGUI.serial.Serial')
    def test_send_to_arduino_empty_values(self, MockSerial):
        mock_serial_instance = MockSerial.return_value
        time_at_peak_value = ""
        num_cycles_value = ""
        duty_cycle_value = ""
        square_type_value = ""
        pyGUI.send_to_arduino(mock_serial_instance, time_at_peak_value, num_cycles_value, duty_cycle_value, square_type_value)
        expected_data = ",,,\n"
        mock_serial_instance.write.assert_called_once_with(expected_data.encode('utf-8'))
    @patch('pyGUI.serial.Serial')
    def test_send_to_arduino_special_characters(self, MockSerial):
        mock_serial_instance = MockSerial.return_value
        time_at_peak_value = "10@"
        num_cycles_value = "!50$"
        duty_cycle_value = "&75*"
        square_type_value = "ahdfsgjdhasg"
        pyGUI.send_to_arduino(mock_serial_instance, time_at_peak_value, num_cycles_value, duty_cycle_value, square_type_value)
        expected_data = f"{time_at_peak_value},{num_cycles_value},{duty_cycle_value},{square_type_value}\n"
        mock_serial_instance.write.assert_called_once_with(expected_data.encode('utf-8'))

class TestMainLoop(unittest.TestCase):
    def setUp(self):
        self.mock_time_entry = MagicMock()
        self.mock_cycles_entry = MagicMock()
        self.mock_duty_entry = MagicMock()
        self.mock_square_entry = MagicMock()
        pyGUI.time_entry = self.mock_time_entry
        pyGUI.cycles_entry = self.mock_cycles_entry
        pyGUI.duty_entry = self.mock_duty_entry
        pyGUI.square_entry = self.mock_square_entry
    @patch('pyGUI.serial.Serial')
    @patch('pyGUI.clear_error_labels')
    @patch('pyGUI.clear_pwm_label')
    @patch('pyGUI.check_time_at_peak_entry')
    @patch('pyGUI.check_num_cycles_entry')
    @patch('pyGUI.check_duty_cycle_entry')
    def test_main_loop_function_calls(self, mock_check_duty, mock_check_cycles, mock_check_time, mock_clear_pwm, mock_clear_error, mock_serial):
        self.mock_time_entry.get.return_value = "100"
        self.mock_cycles_entry.get.return_value = "50"
        self.mock_duty_entry.get.return_value = "75"
        self.mock_square_entry.get.return_value = "unknown"
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = True
        pyGUI.main_loop()
        mock_clear_error.assert_called_once()
        mock_clear_pwm.assert_called_once()
        mock_check_time.assert_called_once_with("100")
        mock_check_cycles.assert_called_once_with("50")
        mock_check_duty.assert_called_once_with("75")
        mock_serial.assert_called_once_with('COM3', 9600, timeout=2)
        mock_serial_instance.write.assert_called_once_with(b'100,50,75,unknown\n')
        mock_serial_instance.close.assert_called_once()
    @patch('pyGUI.serial.Serial')
    @patch('pyGUI.clear_error_labels')
    @patch('pyGUI.clear_pwm_label')
    @patch('pyGUI.check_time_at_peak_entry')
    @patch('pyGUI.check_num_cycles_entry')
    @patch('pyGUI.check_duty_cycle_entry')
    def test_main_loop_serial_connection_error(self, mock_check_duty, mock_check_cycles, mock_check_time, mock_clear_pwm, mock_clear_error, mock_serial):
        self.mock_time_entry.get.return_value = "100"
        self.mock_cycles_entry.get.return_value = "50"
        self.mock_duty_entry.get.return_value = "75"
        self.mock_square_entry.get.return_value = "negative"
        mock_serial.side_effect = pyGUI.serial.SerialException
        with patch('pyGUI.set_pwm_label') as mock_set_pwm_label:
            pyGUI.main_loop()
            mock_set_pwm_label.assert_called_once_with("Unable to Connect to Arduino")
    @patch('pyGUI.serial.Serial')
    @patch('pyGUI.clear_error_labels')
    @patch('pyGUI.clear_pwm_label')
    @patch('pyGUI.check_time_at_peak_entry')
    @patch('pyGUI.check_num_cycles_entry')
    @patch('pyGUI.check_duty_cycle_entry')
    def test_main_loop_no_serial_call_on_invalid_inputs(self, mock_check_duty, mock_check_cycles, mock_check_time, mock_clear_pwm, mock_clear_error, mock_serial):
        self.mock_time_entry.get.return_value = "100000"
        self.mock_cycles_entry.get.return_value = "50"
        self.mock_duty_entry.get.return_value = "75"
        self.mock_square_entry.get.return_value = "negative"
        pyGUI.main_loop()

class TestCenterWindow(unittest.TestCase):
    def setUp(self):
        self.mock_window = MagicMock()
    def test_center_window_small_on_large_screen(self):
        self.mock_window.winfo_screenwidth.return_value = 1920
        self.mock_window.winfo_screenheight.return_value = 1080
        pyGUI.center_window(self.mock_window, 400, 300)
        self.mock_window.geometry.assert_called_once_with('400x300+760+390')
    def test_center_window_medium_on_large_screen(self):
        self.mock_window.winfo_screenwidth.return_value = 1920
        self.mock_window.winfo_screenheight.return_value = 1080
        pyGUI.center_window(self.mock_window, 800, 600)
        self.mock_window.geometry.assert_called_once_with('800x600+560+240')
    def test_center_window_full_screen(self):
        self.mock_window.winfo_screenwidth.return_value = 1920
        self.mock_window.winfo_screenheight.return_value = 1080
        pyGUI.center_window(self.mock_window, 1920, 1080)
        self.mock_window.geometry.assert_called_once_with('1920x1080+0+0')
    def test_center_window_small_on_medium_screen(self):
        self.mock_window.winfo_screenwidth.return_value = 1280
        self.mock_window.winfo_screenheight.return_value = 720
        pyGUI.center_window(self.mock_window, 100, 50)
        self.mock_window.geometry.assert_called_once_with('100x50+590+335')
    def test_center_window_large_on_small_screen(self):
        self.mock_window.winfo_screenwidth.return_value = 800
        self.mock_window.winfo_screenheight.return_value = 600
        pyGUI.center_window(self.mock_window, 900, 700)
        self.mock_window.geometry.assert_called_once_with('900x700+-50+-50')

class TestSetPwmLabel(unittest.TestCase):
    @patch('pyGUI.tk.Label')
    @patch('pyGUI.root.after')
    def test_set_pwm_label(self, mock_after, mock_label):
        mock_label_instance = MagicMock()
        mock_label.return_value = mock_label_instance
        test_text = "Test PWM Label"
        pyGUI.set_pwm_label(test_text)
        mock_label.assert_called_once_with(
            pyGUI.error_frame,
            text=test_text,
            font=("Helvetica", 16),
            fg=pyGUI.maroon,
            bg=pyGUI.entry_background_color
        )
        mock_label_instance.grid.assert_called_once_with(
            row=0, column = 0, pady=5
        )
        mock_after.assert_called_once_with(10000, mock_label_instance.destroy)

class TestSetErrorLabel(unittest.TestCase):
    @patch('pyGUI.create_and_position_error_label')
    def test_set_error_label_time(self, mock_create_and_position):
        mock_label_instance = MagicMock()
        mock_create_and_position.return_value = mock_label_instance
        pyGUI.set_error_label("time", "Invalid time input")
        mock_create_and_position.assert_called_once_with("Invalid time input", 0)
        self.assertIn(mock_label_instance, pyGUI.error_labels)
    @patch('pyGUI.create_and_position_error_label')
    def test_set_error_label_cycle(self, mock_create_and_position):
        mock_label_instance = MagicMock()
        mock_create_and_position.return_value = mock_label_instance
        pyGUI.set_error_label("cycle", "Invalid cycle input")
        mock_create_and_position.assert_called_once_with("Invalid cycle input", 1)
        self.assertIn(mock_label_instance, pyGUI.error_labels)
    @patch('pyGUI.create_and_position_error_label')
    def test_set_error_label_duty(self, mock_create_and_position):
        mock_label_instance = MagicMock()
        mock_create_and_position.return_value = mock_label_instance
        pyGUI.set_error_label("duty", "Invalid duty cycle input")
        mock_create_and_position.assert_called_once_with("Invalid duty cycle input", 2)
        self.assertIn(mock_label_instance, pyGUI.error_labels)

class TestCreateAndPositionErrorLabel(unittest.TestCase):
    @patch('pyGUI.tk.Label')
    def test_create_and_position_error_label(self, mock_label):
        mock_label_instance = MagicMock()
        mock_label.return_value = mock_label_instance
        error_message = "Test Error"
        row_value = 10
        result = pyGUI.create_and_position_error_label(error_message, row=row_value)
        mock_label.assert_called_once_with(
            pyGUI.center_frame,
            text=error_message,
            font=("Arial", 12, "bold"),
            fg="red",
            bg=pyGUI.background_color,
        )
        mock_label_instance.grid.assert_called_once_with(
            row=row_value, column=0, pady=5
        )
        self.assertEqual(result, mock_label_instance)

if __name__ == '__main__':
    unittest.main()
