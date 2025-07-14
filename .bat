run_dashboard.bat
``> Hit Enter

---

### 🔹 2. Add This Code to `run_dashboard.bat`

```bat
@echo off
cd /d %~dp0
streamlit run dashboard/streamlit_dashboard.py
pause

