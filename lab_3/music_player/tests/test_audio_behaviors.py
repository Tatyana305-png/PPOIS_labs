import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from behaviors.audio_behaviors import AudioFileManager, AudioAnalyzer, AudioEffects
from models.audio_models import Song


class TestAudioBehaviors(unittest.TestCase):

    def setUp(self):
        self.audio_manager = AudioFileManager()
        self.audio_analyzer = AudioAnalyzer()
        self.audio_effects = AudioEffects()
        self.song = Song("/music/test.mp3", "Test Song", 180, "Test Artist", "Test Album")

    def test_load_audio_file(self):
        loaded_song = self.audio_manager.load_audio_file("/music/test.mp3")
        self.assertIsInstance(loaded_song, Song)
        self.assertEqual(loaded_song.title, "Beautiful Song")

    def test_validate_audio_file(self):
        is_valid = self.audio_manager.validate_audio_file(self.song)
        self.assertTrue(is_valid)

    def test_extract_metadata(self):
        metadata = self.audio_manager.extract_metadata(self.song)
        self.assertEqual(metadata['title'], "Test Song")
        self.assertEqual(metadata['artist'], "Test Artist")
        self.assertEqual(metadata['album'], "Test Album")

    def test_analyze_bpm(self):
        bpm = self.audio_analyzer.analyze_bpm(self.song)
        self.assertEqual(bpm, self.song.bpm)

    def test_detect_key(self):
        key = self.audio_analyzer.detect_key(self.song)
        self.assertEqual(key, self.song.key)

    def test_analyze_loudness(self):
        loudness = self.audio_analyzer.analyze_loudness(self.song)
        self.assertEqual(loudness, -10.0)

    def test_apply_reverb(self):
        result = self.audio_effects.apply_reverb(self.song, 0.5)
        self.assertTrue(result)

    def test_apply_equalizer(self):
        eq_settings = {"low": 2, "mid": 0, "high": -1}
        result = self.audio_effects.apply_equalizer(self.song, eq_settings)
        self.assertTrue(result)

    def test_change_pitch(self):
        result = self.audio_effects.change_pitch(self.song, 2)
        self.assertTrue(result)

    def test_convert_audio_format(self):
        result = self.audio_manager.convert_audio_format(self.song, "wav")
        self.assertTrue(result)
        self.assertEqual(self.song.format, "wav")


if __name__ == '__main__':
    unittest.main()