Sublime Text 2 LLDB plugin
==========================

(last updated: 2012/07/11)

This is a plugin that allows users to debug programs in Sublime Text 2 using lldb. This plugin enabled command-line interaction with the lldb debugger, as well as Sublime Text 2 integration.

To report a bug or feature request please use GitHub's [project issues](https://github.com/filcab/SublimeLLDB/issues?sort=created&direction=desc&state=open) page.


Features
--------
All features are available on menus and/or Sublime Text's command pallette.

* Command-line interface to the lldb tool
* Start an lldb session with a predefined program, architecture, arguments, breakpoints, and lldb command prologue
* Attach to a program, and waiting for a program to start before an attach
* Connect to a running lldb debugserver
* Step over, into, and out of source lines/functions. Stepping a single thread.
* Send signals to the debugged process
* Set and toggle enabled state on breakpoints
* Process memory view
* Thread disassembly view
* Register view
* View loaded shared libraries
* Breakpoint and program counter markings on the source file buffer
* Execute any lldb command

* Xcode keybindings
* VS keybindings will be added on request. Please open a bug report with the equivalent keybindings in Visual Studio (Check the Xcode keybindings in the *Useful Keybound Commands* section)

* Event-driven to avoid any editing slow-downs due to the plugin.
* Lazy loading architecture so you won't notice the lldb is loaded until you call one of its commands.


Installation
------------
* Clone github repository to Sublime Text 2's “Packages” directory
* Restart Sublime Text 2


Usage
-----
Access plugin functionality using the menu items in Tools->LLDB or quickly access commands using Sublime Text 2's Command Pallette (all commands start with “LLDB: ”). All commands mentioned in this document are avilable in Sublime Text 2. To use, e.g. LldbDebugProgram with their lower-cased, underscore-separated names, e.g. `lldb_debug_program`.


Main Commands
-------------
The main points of entry for the plugin are:

* `LldbCommand`: Starts an lldb session, opening a debugger I/O view
* `LldbDebugProgram`: Starts the default program under an lldb session
* `LldbAttachProcess`: Asks for a process name or PID and attaches to it with lldb
* `LldbConnectDebugserver`: Asks for a remote address and connects to a running debugserver



Useful Keybound Commands
------------------------
* `super+shift+l`: (LldbCommand) Open lldb prompt (maybe starting lldb)

* `super+shift+k`: (LldbToggleOutputView) Show/hide the lldb i/o view
* `super+shift+alt+k`: (LldbClearOutputView) Clear the lldb i/o view

* Xcode-like commands (Mac OS X):
 * `super+ctrl+y`: (LldbContinue) Continue executing the program
 * `F6`: (LldbStepOver) Step over
 * `F7`: (LldbStepInto) Step into
 * `F8`: (LldbStepOut) Step out
 * `ctrl+F6`: (LldbStepOverInstruction) Step over instruction
 * `ctrl+shift+F6`: (LldbStepOverThread) Step over thread
 * `ctrl+F7`: (LldbStepIntoInstruction) Step into instruction
 * `ctrl+shift+F7`: (LldbStepIntoThread) Step into thread
 * `super+shift+m`: (LldbViewMemory) View process memory


Project Settings
----------------
Several settings are available to a Sublime Text 2 project, to allow it to specify a default executable, as well as command line arguments, architecture, and breakpoints to set.

* `lldb.exe` (`""`): Default program to run when executing `LldbDebugProgram`
* `lldb.args` (`[]`): Default command line arguments for the default program
* `lldb.arch` (`lldb.LLDB_ARCH_DEFAULT`): Default architecture for the default program
* `lldb.attach.wait_for_launch` (`false`): When attaching to a program, the plugin should wait for a command with the provided name, if no running program exists
* `lldb.breakpoints` (`[]`): Breakpoints to set for the default program


### Default program breakpoints
Each default program breakpoint may be represented in several ways:
* `"main"`: Breaks on a symbol named `main` (gdb-like variations with file+line are also available)
* `{ "file": "main.c", "line": 42 }`: Breaks on line 42 of file `main.c`


### Deprecated project settings
* `lldb.prologue` (`[]`): Array of commands to run at debugger startup. (Use `.lldbinit` files, instead)


Useful Settings
---------------
The LLDB plugin has several settings to change its behaviour. they are listed next, along with their default values and an explanation of what they change in the plugin.

### View settings
* `lldb.i/o.view.name` (`"lldb i/o"`): Name of the debugger I/O view
* `lldb.i/o.view.clear_on_startup` (`true`): Whether to clear the debugger I/O view at the start of a debugging session
* `lldb.layout.basic` (`{ ... }`): Default layout for the views when the debugger starts. It should contain groups for the source files and the debugger I/O view (they may be the same group). The default layout created two groups of tabs, with one spanning a majority of the screen.
* `lldb.layout.group.source_file` (`0`): Index of the group to use for source file views
* `lldb.layout.group.i/o` (`1`): Index of the group to use for the debugger I/O view

### Memory view settings
No verifications are made on the chosen sizes. For best results, `size` should be a multiple of `width`, which should be a multiple of `grouping`.

* `lldb.view.memory.size` (`512`): Total number of bytes to show on a “show memory” view
* `lldb.view.memory.width` (`32`): Number of bytes to show on each line of a “show memory” view
* `lldb.view.memory.grouping` (`8`): Number of bytes to show in each group on a “show memory” view

### View marker settings
* `lldb.markers.current_line.region_name` (`"lldb.location"`): Region name for current source line markers
* `lldb.markers.current_line.scope` (`"bookmark"`): Scope for current source line markers
* `lldb.markers.current_line.scope.crashed` (`"invalid"`): Scope for current source line markerswhen the program crashes
* `lldb.markers.current_line.type` (`"bookmark"`): Type for current source line markers

* `lldb.markers.breakpoint.enabled.region_name` (`"lldb.breakpoint.enabled"`): Region name for enabled breakpoints
* `lldb.markers.breakpoint.enabled.scope` (`"string"`): Scope for enabled breakpoints
* `lldb.markers.breakpoint.enabled.type` (`"circle"`): Type for enabled breakpoints

* `lldb.markers.breakpoint.disabled.region_name` (`"lldb.breakpoint.disabled"`): Region name for disabled breakpoints
* `lldb.markers.breakpoint.disabled.scope` (`"bookmark"`): Scope for disabled breakpoints
* `lldb.markers.breakpoint.disabled.type` (`"circle"`): Type for disabled breakpoints

### Backend settings
* `lldb.use_bundled_debugserver` (`false`): Whether to use the bundled LLDB.framework debugserver (more up-to-date) or an Apple provided one (Xcode required).


Other Useful Commands
---------------------

* LldbStopDebugging: Stops the inferior debug loop, killing (or detaching) the program being debugged
* LldbSendSignal: Asks the user for a signal number and sends that signal to the inferior program

* LldbListBreakpoints: Lists all defined breakpoints, in a format suitable for the `lldb.breakpoints` setting for a default program
* LldbBreakAt{Line,Symbol}: Breaks at the current line or symbol (Currently LldbBreakAtSymbol is not defined)
* LldbToggleEnableBreakpoints: For the first call disables every enabled breakpoint. The next time, it will enable every breakpoint it disabled.

* LldbViewSharedLibraries: Opens a view with a list of the loaded shared libraries
* LldbRegisterView: Opens a view with the current values for the machine registers in the current thread
* LldbDisassembleFrame: Opens a view with the disassembly of the current frame


Known bugs
----------
* The input reader thread is named (for Python) Dummy-N (N=1, ...). This is a Python problem (the LLDB library uses `pthread_setname_np` to name the thread).
* Lldb's `script` command may not work. A workaround is being devised for it.
* Sometimes Sublime Text 2 won't update the markers. For example, executing the LLDB command 'breakpoint disable' to disable all breakpoints may make the breakpoints disappear. They should reappear on the next step instruction.
* Depending on which view is selected, project settings may not propagate to the plugin's commands. This is a Sublime Text 2 limitation.
* The process being debugged has to be stopped before quitting Sublime Text 2 (otherwise, the program will crash). This is a bug with Sublime Text 2 not running the plugin's cleanup function when exiting.
* Disassembly views don't have breakpoint markers, yet.
* ...


`debugserver` binary
--------------------
The default `debugserver` binary that is used is the system one (when XCode or the command line tools are installed). If the bundled `debugserver` is to be used (e.g: newer `debugserver` with protocol enhancements), change the setting `lldb.use_bundled_debugserver`, in your settings `True` and sign the `<plugin folder>/lldb_plugin/LLDB.framework/Resources/debugserver` binary as instructed in the `docs/code-signing.txt` file in lldb's sources.


Debugging the plugin
--------------------
If, for some reason, you want some debug messages from the plugin, call, on plugin initialization, the `debug.set_debug` function, with some of the constants defined at the start of the plugin/debug.py file as argument (you can combine several constants with `|`).
