import unittest
from unittest.mock import patch, Mock
import utils  # The module where your Plotter class is defined

class TestTurnServo(unittest.TestCase):
    @patch('RPi.GPIO.setmode')
    @patch('RPi.GPIO.setup')
    @patch('RPi.GPIO.output')
    @patch('RPi.GPIO.PWM')
    def test_turn_servo(self, mock_pwm, mock_output, mock_setup, mock_setmode):
        # Create a mock PWM instance
        mock_pwm_instance = Mock()
        mock_pwm.return_value = mock_pwm_instance

        # Create an instance of your class
        plotter = utils.Plotter()

        # Call the method you want to test
        plotter.turn_servo()

        # Assert that the GPIO methods were called with the correct arguments
        mock_setmode.assert_called_once_with(utils.GPIO.BCM)
        mock_setup.assert_any_call(23, utils.GPIO.OUT)
        mock_setup.assert_any_call(24, utils.GPIO.OUT)
        mock_setup.assert_any_call(25, utils.GPIO.OUT)
        mock_output.assert_any_call(23, utils.GPIO.LOW)
        mock_output.assert_any_call(24, utils.GPIO.LOW)
        mock_pwm.assert_called_once_with(25, 1000)
        mock_pwm_instance.start.assert_called_once_with(25)
        mock_output.assert_any_call(23, utils.GPIO.HIGH)
        mock_output.assert_any_call(24, utils.GPIO.LOW)

if __name__ == '__main__':
    unittest.main()