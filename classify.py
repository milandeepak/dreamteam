import argparse
import time
import threading

from mediapipe.tasks import python
from mediapipe.tasks.python.audio.core import audio_record
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from utils import Plotter


def run_audio_classification(model: str, max_results: int, score_threshold: float,
                             overlapping_factor: float, sample_rate: int = 16000, plotter: Plotter = None) -> None:
    """Continuously run inference on audio data acquired from the device."""
    if (overlapping_factor < 0) or (overlapping_factor >= 1.0):
        raise ValueError('Overlapping factor must be between 0.0 and 0.9')

    if (score_threshold < 0) or (score_threshold > 1.0):
        raise ValueError('Score threshold must be between (inclusive) 0 and 1.')

    classification_result_list = []

    def save_result(result: audio.AudioClassifierResult, timestamp_ms: int):
        result.timestamp_ms = timestamp_ms
        classification_result_list.append(result)

        # Update the GUI with classification results
        if plotter:
            plotter.plot(result)

    # Initialize the audio classification model.
    base_options = python.BaseOptions(model_asset_path=model)
    options = audio.AudioClassifierOptions(
        base_options=base_options, running_mode=audio.RunningMode.AUDIO_STREAM,
        max_results=max_results, score_threshold=score_threshold,
        result_callback=save_result)
    classifier = audio.AudioClassifier.create_from_options(options)

    # Initialize the audio recorder and a tensor to store the audio input.
    buffer_size = 15600  # Adjust buffer size as needed
    num_channels = 1
    audio_format = containers.AudioDataFormat(num_channels, sample_rate)
    record = audio_record.AudioRecord(num_channels, sample_rate, buffer_size)
    audio_data = containers.AudioData(buffer_size, audio_format)

    # Calculate the interval between inferences based on the sample rate and buffer size.
    input_length_in_seconds = buffer_size / sample_rate
    interval_between_inference = input_length_in_seconds * (1 - overlapping_factor)
    pause_time = interval_between_inference * 0.1
    last_inference_time = time.time()

    # Start audio recording in the background.
    record.start_recording()

    # Loop until the user closes the classification results plot.
    while True:
        # Wait until at least interval_between_inference seconds have passed since
        # the last inference.
        now = time.time()
        diff = now - last_inference_time
        if diff < interval_between_inference:
            time.sleep(pause_time)
            continue
        last_inference_time = now

        # Load the input audio from the AudioRecord instance and run classification.
        data = record.read(buffer_size)
        audio_data.load_from_array(data)
        classifier.classify_async(audio_data, time.time_ns() // 1_000_000)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path to the custom audio classification model (TFLite format).',
        required=False,
        default='yamnet.tflite')
    parser.add_argument(
        '--maxResults',
        help='Maximum number of results to show.',
        required=False,
        default=5)
    parser.add_argument(
        '--overlappingFactor',
        help='Target overlapping between adjacent inferences. Value must be in (0, 1)',
        required=False,
        default=0.5)
    parser.add_argument(
        '--scoreThreshold',
        help='The score threshold of classification results.',
        required=False,
        default=0.0)
    args = parser.parse_args()

    # Create the Plotter instance for displaying classification results
    plotter = Plotter()

    # Create a thread for running the audio classification process
    audio_thread = threading.Thread(target=run_audio_classification,
                                    args=(args.model, int(args.maxResults), float(args.scoreThreshold),
                                          float(args.overlappingFactor), 16000, plotter))
    audio_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
    audio_thread.start()

    # Start the GUI
    plotter.root.mainloop()


if __name__ == '__main__':
    main()