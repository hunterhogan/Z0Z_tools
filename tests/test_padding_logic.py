"""
Tests for padding logic in loadWaveforms and loadSpectrograms.

This test file validates the padding logic fix for GitHub issue #4.
"""
import numpy as np
import pytest
import tempfile
from pathlib import Path
from Z0Z_tools.ioAudio import loadWaveforms, loadSpectrograms, writeWAV
from Z0Z_tools.theTypes import WaveformMetadata
from unittest.mock import patch


class TestPaddingLogic:
    """Test suite for padding logic functionality."""

    def test_loadWaveforms_handlesFilesOfDifferentLengths(self) -> None:
        """Test that loadWaveforms correctly handles files of different lengths without broadcasting errors."""
        sample_rate = 44100
        
        # Create test waveforms of different lengths
        duration1 = 0.1  # 0.1 seconds
        duration2 = 0.05  # 0.05 seconds
        
        length1 = int(sample_rate * duration1)
        length2 = int(sample_rate * duration2)
        
        # Create distinct waveforms for easy verification
        waveform1 = np.array([
            np.ones(length1, dtype=np.float32),     # Left channel: all 1.0
            np.ones(length1, dtype=np.float32) * 2  # Right channel: all 2.0
        ])
        
        waveform2 = np.array([
            np.ones(length2, dtype=np.float32) * 3,  # Left channel: all 3.0
            np.ones(length2, dtype=np.float32) * 4   # Right channel: all 4.0
        ])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = Path(temp_dir) / "test1.wav"
            file2 = Path(temp_dir) / "test2.wav"
            
            writeWAV(file1, waveform1, sample_rate)
            writeWAV(file2, waveform2, sample_rate)
            
            # This should not raise a broadcasting exception
            array_waveforms = loadWaveforms([file1, file2], sample_rate)
            
            # Verify correct shape (channels, max_length, num_files)
            expected_shape = (2, length1, 2)  # length1 is longer
            assert array_waveforms.shape == expected_shape
            
            # Verify file 1 data (should fill its entire allocated space)
            assert np.allclose(array_waveforms[0, :length1, 0], 1.0)
            assert np.allclose(array_waveforms[1, :length1, 0], 2.0)
            
            # Verify file 2 data (should be at beginning with trailing zeros)
            assert np.allclose(array_waveforms[0, :length2, 1], 3.0)
            assert np.allclose(array_waveforms[1, :length2, 1], 4.0)
            # Check trailing zeros
            assert np.allclose(array_waveforms[:, length2:, 1], 0.0)

    def test_loadSpectrograms_handlesFilesOfDifferentLengths(self) -> None:
        """Test that loadSpectrograms correctly handles files of different lengths without errors."""
        sample_rate = 44100
        
        # Create test waveforms of different lengths (need sufficient length for STFT)
        duration1 = 0.25  # 0.25 seconds
        duration2 = 0.15  # 0.15 seconds
        
        length1 = int(sample_rate * duration1)
        length2 = int(sample_rate * duration2)
        
        # Create sine waves with different frequencies
        t1 = np.linspace(0, duration1, length1, False)
        t2 = np.linspace(0, duration2, length2, False)
        
        waveform1 = np.array([
            np.sin(2 * np.pi * 440 * t1),  # 440 Hz
            np.sin(2 * np.pi * 440 * t1)
        ], dtype=np.float32)
        
        waveform2 = np.array([
            np.sin(2 * np.pi * 880 * t2),  # 880 Hz
            np.sin(2 * np.pi * 880 * t2)
        ], dtype=np.float32)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = Path(temp_dir) / "test1.wav"
            file2 = Path(temp_dir) / "test2.wav"
            
            writeWAV(file1, waveform1, sample_rate)
            writeWAV(file2, waveform2, sample_rate)
            
            # This should not raise an exception
            array_spectrograms, metadata = loadSpectrograms([file1, file2], sample_rate)
            
            # Verify correct number of files
            assert array_spectrograms.shape[-1] == 2
            assert len(metadata) == 2
            
            # Verify metadata contains correct lengths
            assert metadata[0]['lengthWaveform'] == length1
            assert metadata[1]['lengthWaveform'] == length2
            
            # Both should have zero leading/trailing padding in current implementation
            assert metadata[0]['samplesLeading'] == 0
            assert metadata[0]['samplesTrailing'] == 0
            assert metadata[1]['samplesLeading'] == 0
            assert metadata[1]['samplesTrailing'] == 0

    def test_loadWaveforms_paddingLogicConsistency(self) -> None:
        """Test that the padding logic is consistent and predictable."""
        sample_rate = 1000  # Use low sample rate for simple math
        
        # Create very simple test case: 10 samples vs 5 samples
        waveform1 = np.array([
            np.arange(10, dtype=np.float32),      # [0, 1, 2, ..., 9]
            np.arange(10, dtype=np.float32) + 10  # [10, 11, 12, ..., 19]
        ])
        
        waveform2 = np.array([
            np.arange(5, dtype=np.float32) + 100,      # [100, 101, 102, 103, 104]
            np.arange(5, dtype=np.float32) + 200       # [200, 201, 202, 203, 204]
        ])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = Path(temp_dir) / "long.wav"
            file2 = Path(temp_dir) / "short.wav"
            
            writeWAV(file1, waveform1, sample_rate)
            writeWAV(file2, waveform2, sample_rate)
            
            array_waveforms = loadWaveforms([file1, file2], sample_rate)
            
            # Expected shape: (2 channels, 10 samples, 2 files)
            assert array_waveforms.shape == (2, 10, 2)
            
            # File 1 (long) should match exactly (accounting for any minor floating point differences)
            np.testing.assert_allclose(array_waveforms[0, :, 0], np.arange(10), atol=1e-5)
            np.testing.assert_allclose(array_waveforms[1, :, 0], np.arange(10) + 10, atol=1e-5)
            
            # File 2 (short) should be placed at beginning with trailing zeros
            np.testing.assert_allclose(array_waveforms[0, :5, 1], np.arange(5) + 100, atol=1e-5)
            np.testing.assert_allclose(array_waveforms[1, :5, 1], np.arange(5) + 200, atol=1e-5)
            np.testing.assert_allclose(array_waveforms[:, 5:, 1], 0.0, atol=1e-5)

    def test_loadWaveforms_withNonZeroPadding(self) -> None:
        """Test that loadWaveforms handles non-zero samplesLeading and samplesTrailing correctly."""
        sample_rate = 1000
        
        # Create a simple 5-sample waveform
        waveform = np.array([
            np.ones(5, dtype=np.float32),      # [1, 1, 1, 1, 1]
            np.ones(5, dtype=np.float32) * 2   # [2, 2, 2, 2, 2]
        ])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.wav"
            writeWAV(file_path, waveform, sample_rate)
            
            # Mock the metadata to have non-zero padding
            def mock_getWaveformMetadata(listPathFilenames, sampleRate):
                return {
                    0: WaveformMetadata(
                        pathFilename=str(listPathFilenames[0]),
                        lengthWaveform=5,
                        samplesLeading=2,   # 2 samples of leading padding
                        samplesTrailing=3   # 3 samples of trailing padding  
                    )
                }
            
            with patch('Z0Z_tools.ioAudio.getWaveformMetadata', side_effect=mock_getWaveformMetadata):
                array_waveforms = loadWaveforms([file_path], sample_rate)
                
                # Expected shape: (2 channels, 10 samples total, 1 file)
                # 2 leading + 5 waveform + 3 trailing = 10 total
                assert array_waveforms.shape == (2, 10, 1)
                
                # Check leading padding (should be zeros)
                np.testing.assert_allclose(array_waveforms[:, :2, 0], 0.0, atol=1e-5)
                
                # Check waveform data (should be at positions 2-6)
                np.testing.assert_allclose(array_waveforms[0, 2:7, 0], 1.0, atol=1e-5)
                np.testing.assert_allclose(array_waveforms[1, 2:7, 0], 2.0, atol=1e-5)
                
                # Check trailing padding (should be zeros)
                np.testing.assert_allclose(array_waveforms[:, 7:, 0], 0.0, atol=1e-5)