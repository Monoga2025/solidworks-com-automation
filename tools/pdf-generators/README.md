# pdf-generators

ReportLab/openpyxl scripts that produced personal study guides for the SolidWorks quizzes. Standalone, not used by the runner. Install with `pip install reportlab openpyxl`.

| Script | Output |
|---|---|
| `generate_quiz1.py` | Threaded-union guide |
| `generate_union_appendix.py` | Appendix with thread calculations |
| `generate_gears_flex_pdf.py` | Quick-run guide for the helical-gear quiz |
| `generate_master_pdf.py`, `generate_pdf_tutorial.py`, `generate_quiz_field_guide.py` | Longer step-by-step gear guides |
| `prepare_workbook.py` | Fills a gear calculation workbook (template not included) |
| `extract_dense_storyboards.py` | Frame storyboards from a screen recording (video not included) |

Source videos, course PDFs and templates are intentionally not in this repository; some scripts expect paths you must supply. Student data is placeholder only.
