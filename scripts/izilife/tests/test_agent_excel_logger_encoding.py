import io
import unittest

from agent_excel_logger import _Tee


class Cp1252Stream(io.StringIO):
    encoding = "cp1252"

    def write(self, value):
        value.encode(self.encoding)
        return super().write(value)


class AgentExcelLoggerEncodingTest(unittest.TestCase):
    def test_unicode_console_symbol_does_not_abort_agent(self):
        console = Cp1252Stream()
        tee = _Tee(console)

        tee.write("Attente ⏳ consentement")

        self.assertEqual(tee.buffer.getvalue(), "Attente ⏳ consentement")
        self.assertEqual(console.getvalue(), "Attente ? consentement")


if __name__ == "__main__":
    unittest.main()
