# README-only technical cold run

PASS; operator: Codex, not independent student/partner evidence.

Environment: Isolated official Python3.13.7 embedded archive; project1/requirements.txt installed separately in .review-runtime; no copied site-packages. Installation log records initial setup; reruns reuse only that pinned environment.

Started 2026-10-19T19:48:15.329930+00:00; finished 2026-10-19T19:48:18.785500+00:00; elapsed 3.46s.

First failure in this fresh run: None

Command: C:\Users\acpie\Documents\Codex\amazon-report-upload\project1\.review-runtime\python.exe -B project1/analysis.py

Exit 0; 0.20s

PROVISIONAL EDUCATIONAL VALUATION | as of 2026-09-10 | do not initiate
FCFF base $39.05; valid low/base/high subset $58.06-$58.06; WACC 11.672580%; g 2.50%
Infeasible low/base/high cases: ['base', 'low']




Command: C:\Users\acpie\Documents\Codex\amazon-report-upload\project1\.review-runtime\python.exe -B project1/tests/test_project.py

Exit 0; 0.18s

test_01_legacy_fcfe_regression (__main__.ProjectTests.test_01_legacy_fcfe_regression) ... ok
test_02_legacy_complete_statement_snapshot (__main__.ProjectTests.test_02_legacy_complete_statement_snapshot) ... ok
test_03_synthetic_known_answer (__main__.ProjectTests.test_03_synthetic_known_answer) ... ok
test_04_signed_cashflow_known_answer (__main__.ProjectTests.test_04_signed_cashflow_known_answer) ... ok
test_05_history_revenue_and_capex (__main__.ProjectTests.test_05_history_revenue_and_capex) ... ok
test_06_history_source_artifact_checks (__main__.ProjectTests.test_06_history_source_artifact_checks) ... ok
test_07_five_years (__main__.ProjectTests.test_07_five_years) ... ok
test_08_balance_sheets (__main__.ProjectTests.test_08_balance_sheets) ... ok
test_09_cashflow_articulation (__main__.ProjectTests.test_09_cashflow_articulation) ... ok
test_10_working_capital (__main__.ProjectTests.test_10_working_capital) ... ok
test_11_ppe_continuity (__main__.ProjectTests.test_11_ppe_continuity) ... ok
test_12_finance_lease_continuity (__main__.ProjectTests.test_12_finance_lease_continuity) ... ok
test_13_operating_lease_continuity (__main__.ProjectTests.test_13_operating_lease_continuity) ... ok
test_14_debt_and_equity_continuity (__main__.ProjectTests.test_14_debt_and_equity_continuity) ... ok
test_15_fcff_components (__main__.ProjectTests.test_15_fcff_components) ... ok
test_16_fcff_independent_cfo_route (__main__.ProjectTests.test_16_fcff_independent_cfo_route) ... ok
test_17_actual_negative_fcff_retained (__main__.ProjectTests.test_17_actual_negative_fcff_retained) ... ok
test_18_wacc_components (__main__.ProjectTests.test_18_wacc_components) ... ok
test_19_wacc_growth_boundaries (__main__.ProjectTests.test_19_wacc_growth_boundaries) ... ok
test_20_nonfinite_boundary (__main__.ProjectTests.test_20_nonfinite_boundary) ... ok
test_21_bridge_identity (__main__.ProjectTests.test_21_bridge_identity) ... ok
test_22_bridge_no_operating_lease_double_count (__main__.ProjectTests.test_22_bridge_no_operating_lease_double_count) ... ok
test_23_diluted_share_reconciliation (__main__.ProjectTests.test_23_diluted_share_reconciliation) ... ok
test_24_synthetic_monotonicity (__main__.ProjectTests.test_24_synthetic_monotonicity) ... ok
test_25_terminal_reinvestment_identity (__main__.ProjectTests.test_25_terminal_reinvestment_identity) ... ok
test_26_peer_enterprise_definition (__main__.ProjectTests.test_26_peer_enterprise_definition) ... ok
test_27_peer_ebitda_definitions (__main__.ProjectTests.test_27_peer_ebitda_definitions) ... ok
test_28_pe_has_no_debt_subtraction (__main__.ProjectTests.test_28_pe_has_no_debt_subtraction) ... ok
test_29_peer_policy_exclusion (__main__.ProjectTests.test_29_peer_policy_exclusion) ... ok
test_30_peer_dates (__main__.ProjectTests.test_30_peer_dates) ... ok
test_31_peer_negative_denominator (__main__.ProjectTests.test_31_peer_negative_denominator) ... ok
test_32_leave_one_out (__main__.ProjectTests.test_32_leave_one_out) ... ok
test_33_scenario_isolation (__main__.ProjectTests.test_33_scenario_isolation) ... ok
test_34_restored_base (__main__.ProjectTests.test_34_restored_base) ... ok
test_35_funding_failure_retained (__main__.ProjectTests.test_35_funding_failure_retained) ... ok
test_36_reverse_boundaries (__main__.ProjectTests.test_36_reverse_boundaries) ... ok
test_37_reverse_repricing (__main__.ProjectTests.test_37_reverse_repricing) ... ok
test_38_deliberate_high_risk_failure (__main__.ProjectTests.test_38_deliberate_high_risk_failure) ... ok
test_39_deliberate_cash_failure (__main__.ProjectTests.test_39_deliberate_cash_failure) ... ok
test_40_historical_preservation (__main__.ProjectTests.test_40_historical_preservation) ... ok
test_41_original_edition_a_copy (__main__.ProjectTests.test_41_original_edition_a_copy) ... ok
test_42_business_revenue_reconciles (__main__.ProjectTests.test_42_business_revenue_reconciles) ... ok
test_43_operating_fcff_unaffected_by_financing (__main__.ProjectTests.test_43_operating_fcff_unaffected_by_financing) ... ok
test_44_market_data_evidence (__main__.ProjectTests.test_44_market_data_evidence) ... ok
test_45_tax_normalization_no_financing_shield (__main__.ProjectTests.test_45_tax_normalization_no_financing_shield) ... ok
test_46_terminal_growth_coupled_reinvestment (__main__.ProjectTests.test_46_terminal_growth_coupled_reinvestment) ... ok
test_47_stub_discounting (__main__.ProjectTests.test_47_stub_discounting) ... ok
test_48_source_download_integrity (__main__.ProjectTests.test_48_source_download_integrity) ... ok
test_49_reported_to_normalized_income (__main__.ProjectTests.test_49_reported_to_normalized_income) ... ok
test_50_known_investment_outflows (__main__.ProjectTests.test_50_known_investment_outflows) ... ok
test_51_known_july_issuance (__main__.ProjectTests.test_51_known_july_issuance) ... ok
test_52_core_base_not_funding_valid (__main__.ProjectTests.test_52_core_base_not_funding_valid) ... ok
test_53_terminal_opening_asset_depreciation (__main__.ProjectTests.test_53_terminal_opening_asset_depreciation) ... ok
test_54_terminal_ebit_schedule (__main__.ProjectTests.test_54_terminal_ebit_schedule) ... ok
test_55_strategic_no_double_count (__main__.ProjectTests.test_55_strategic_no_double_count) ... ok
test_56_strategic_haircut_labeled (__main__.ProjectTests.test_56_strategic_haircut_labeled) ... ok
test_57_financing_investment_not_in_fcff (__main__.ProjectTests.test_57_financing_investment_not_in_fcff) ... ok
test_58_date_cash_bridge_known_transactions (__main__.ProjectTests.test_58_date_cash_bridge_known_transactions) ... ok
test_59_named_nonrecurring_cost_normalization (__main__.ProjectTests.test_59_named_nonrecurring_cost_normalization) ... ok

----------------------------------------------------------------------
Ran 59 tests in 0.057s

OK





Command: C:\Users\acpie\Documents\Codex\amazon-report-upload\project1\.review-runtime\python.exe -B project1/test_app.py

Exit 0; 2.02s

All 7 dashboard pages executed successfully under Streamlit AppTest.


2026-10-19 15:48:16.317 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.


Server: {'command': ['C:\\Users\\acpie\\Documents\\Codex\\amazon-report-upload\\project1\\.review-runtime\\python.exe', '-m', 'streamlit', 'run', 'project1/app.py', '--server.address', '127.0.0.1', '--server.port', '8502', '--server.headless', 'true', '--browser.gatherUsageStats', 'false'], 'health': 'ok', 'status': 'PASS'}

Initial development failure, before this fresh run: native PyArrow DLL blocked by Windows Application Control. Changed dashboard to HTML/SVG rendering inside Streamlit; no Windows security configuration was changed. AppTest then passed all seven pages. See environment_failures.md. A real independently observed human cold run remains pending if required by the brief.