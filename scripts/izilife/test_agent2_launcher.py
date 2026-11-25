import argparse,unittest
from pathlib import Path
from agent2_launcher import stages
class LauncherTest(unittest.TestCase):
    def test_all_plan_contains_four_safe_stages(self):
        args=argparse.Namespace(task="all",env="local",zone="lille",city="lille",territorial_config=None,report_dir=Path("reports"),apply=False,maximum=5,file=None,confirm_production=None)
        names=[name for name,_ in stages(args)];self.assertEqual(["curate_places","pages","event_improver","manual_events","territorial","external_content","enrichment","transfers"],names)
    def test_prod_apply_requires_global_confirmation(self):
        args=argparse.Namespace(task="transfers",env="prod",zone="lille",city="lille",territorial_config=None,report_dir=Path("reports"),apply=True,maximum=5,file=None,confirm_production=None)
        with self.assertRaises(SystemExit):stages(args)
if __name__=="__main__":unittest.main()
