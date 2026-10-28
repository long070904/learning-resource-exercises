# Apply a unit-conversion preprocessing function

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=4&section=1). All three GUI tasks received **Correct!** in the hosted Academy app.

| Task | Action performed | Final grader |
|---|---|---|
| 1 | Duplicated `harp` as `harp_cm`, added the custom function `nm2cm` using the course-provided function body, applied it, accepted the change, and displayed the result. | Correct! |
| 2 | Duplicated `pax` and `wanc` with `_cm` suffixes. Selected both for preprocessing, applied `nm2cm`, accepted the changes, and displayed all three converted signals. | Correct! |
| 3 | Exported each converted signal to the MATLAB workspace. The first attempt exported only `harp_cm`; exporting `pax_cm` and `wanc_cm` as well produced the final pass. | Correct! |

The saved [nm2cm.m](nm2cm.m) preserves the short function supplied by the course: divide sample values by ten million, leaving the time values unchanged. It converts nanometres to centimetres. The helper supports the app workflow; the table records the GUI tasks themselves.

The follow-up explained timetable export and required no additional execution or grading. Before this lesson, the header was observed at 40%; this is a historical observation. See [current progress](../../ACADEMY_PROGRESS.md) for the latest status. The course datasets remain in the hosted workspace.
