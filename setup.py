import cx_Freeze

executables = [cx_Freeze.Executable("run.py", base = "Win32GUI")]

cx_Freeze.setup(
	name = "2048 Solver",
	options={"build_exe":{"packages":["pygame", "tkinter"],
						"include_files": []}},
	
	description="AI that plays 2048",
	
	executables = executables
	)
	