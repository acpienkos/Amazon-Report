# Actual environment failures and corrections

1. The pre-existing temporary Python executable did not return the expected diagnostics. The preserved Lab13 portable Python3.13.7 did; it was used read-only to inventory/hash history and prepare the isolated project runtime.
2. PowerShell Expand-Archive module could not load. Switched to Python's standard-library zipfile. No historical runtime was edited.
3. The initial sandbox network request to bootstrap.pypa.io failed. Retried through approved escalated execution; installation succeeded inside project1/.runtime.
4. A shell-escaped one-line HTML extraction command had a SyntaxError. Replaced it with inspect_sources.py/source_tables.py; saved raw HTML remains unchanged.
5. First Walmart annual URL returned HTTP404. SEC index search identified accession000010416926000055; corrected download succeeded. Both attempts remain in source_downloads.json.
6. First finance test run:46 passed,2 failed. Reverse DCF bracket contained an invalid terminal endpoint; direct PP&E addition check missed a mutated financed-asset amount. Corrected the bracket and accounting identity; all48 passed. Full failed log retained.
7. Streamlit AppTest initially failed because PyArrow's native DLL was blocked by Windows Application Control. Approved execution outside the sandbox produced the same block. Replaced Arrow table/Altair transports with HTML/SVG display inside Streamlit; no security policy was changed. All7 dashboard pages then executed successfully.

These are actual observed development failures. They are not claimed student-only assessment evidence or proof of independent human source verification.

Final financial review: a shell-escaped preparation command failed to parse before execution; prepare_review.py then created the adapted engine successfully. The first reviewed PDF-wrapper run failed to import review_documents because the embedded runtime omits the script directory from sys.path. Added that explicit path, regenerated successfully and retained the prior PDFs/source in review_snapshot/before-review.zip. This was an artifact-execution failure, not a change to financial assumptions. The 49-test prior build had passed despite economic omissions; the new source review and targeted tests address that gap.
