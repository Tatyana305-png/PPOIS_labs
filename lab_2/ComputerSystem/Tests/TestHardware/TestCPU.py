import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.CPU import CPU, CPUCore
from Exceptions.CPUOverheatException import CPUOverheatException


class TestCPU:
    @pytest.fixture
    def sample_cpu(self):
        return CPU("Intel", "Core i7", 4, 3.2)

    def test_cpu_initialization(self, sample_cpu):
        assert sample_cpu.brand == "Intel"
        assert sample_cpu.model == "Core i7"
        assert sample_cpu.cores == 4
        assert sample_cpu.speed == 3.2
        assert sample_cpu.temperature == 35.0
        assert sample_cpu.usage == 0.0

    def test_execute_instruction(self, sample_cpu):
        result = sample_cpu.execute_instruction("ADD R1, R2")
        assert "Выполнена инструкция: ADD R1, R2" in result
        assert sample_cpu.usage > 0
        assert sample_cpu.temperature > 35.0

    def test_cpu_overheat_exception(self, sample_cpu):
        sample_cpu.thermal_threshold = 40.0
        sample_cpu.temperature = 39.0

        with pytest.raises(CPUOverheatException):
            for _ in range(10):
                sample_cpu.execute_instruction("TEST")

    def test_cpu_cool_down(self, sample_cpu):
        sample_cpu.temperature = 80.0
        sample_cpu.cool_down()
        assert sample_cpu.temperature == 70.0

    def test_cpu_core_initialization(self):
        core = CPUCore(1, 3.2)
        assert core.core_id == 1
        assert core.speed == 3.2
        assert core.current_task is None
        assert not core.is_active

    def test_cpu_multiple_instructions(self):
        cpu = CPU("AMD", "Ryzen 5", 6, 3.6)
        for i in range(5):
            result = cpu.execute_instruction(f"MOV R{i}, #{i}")
            assert "Выполнена инструкция" in result
        assert cpu.temperature > 35.0
        assert cpu.usage > 0

    def test_cpu_core_task_management(self):
        core = CPUCore(0, 4.2)
        test_task = "calculation_task"

        core.assign_task(test_task)
        assert core.current_task == test_task
        assert core.is_active

        core.release_task()
        assert core.current_task is None
        assert not core.is_active