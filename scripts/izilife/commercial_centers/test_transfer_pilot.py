import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from openpyxl import load_workbook
from transfer_pilot import init,process

class TransferPilotTest(unittest.TestCase):
    def test_plan_then_apply_uses_frozen_hash_and_confirmation(self):
        root=Path(__file__).resolve().parents[3]/"tmp";root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            path=Path(tmp)/"transfer.xlsx";init(path);wb=load_workbook(path);ws=wb["Transferts"]
            ws["B2"]="source";ws["D2"]="destination";wb.save(path)
            plan={"can_apply":True,"plan_hash":"a"*64,"actions":[],"blockers":[]}
            with patch("transfer_pilot.post",return_value={"plan":plan}):process(path,"local",False)
            wb=load_workbook(path);ws=wb["Transferts"];self.assertEqual("planned",ws["J2"].value);self.assertEqual("a"*64,ws["L2"].value)
            ws["I2"]="APPLY";ws["J2"]="pending";wb.save(path);captured={}
            def fake_post(env,endpoint,payload):captured.update(payload);return {"success":True,"result":{"source_archived":True}}
            with patch("transfer_pilot.post",side_effect=fake_post):process(path,"local",True)
            self.assertEqual("LOCATION_TRANSFER_APPLY",captured["confirm_apply"]);self.assertEqual("a"*64,captured["plan_hash"])
            self.assertEqual("done",load_workbook(path)["Transferts"]["J2"].value)
if __name__=="__main__":unittest.main()
