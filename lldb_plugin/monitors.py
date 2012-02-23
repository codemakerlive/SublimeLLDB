# -*- mode: python; coding: utf-8 -*-

import sublime

import Queue
import select
import threading

from root_objects import lldb_instance, lldb_view_write


def debug_thr():
    print ('thread id: ' + threading.current_thread().name)
    # traceback.print_stack()


def debug(str):
    print str


def debugif(b, str):
    if b:
        debug(str)


lldb_i_o_thread = None
lldb_markers_thread = None
lldb_last_location_view = None
lldb_file_markers_queue = Queue.Queue()


def launch_monitor(fun, name='monitor thread'):
    t = threading.Thread(target=fun, name=name)
    t.daemon = True
    t.start()


def launch_i_o_monitor():
    global lldb_i_o_thread
    if lldb_i_o_thread and not lldb_i_o_thread.is_alive():
        lldb_i_o_thread.join()

    lldb_i_o_thread = launch_monitor(lldb_i_o_monitor,
                                     name='lldb i/o monitor')


def launch_markers_monitor():
    global lldb_markers_thread
    if lldb_markers_thread and not lldb_markers_thread.is_alive():
        lldb_markers_thread.join()

    lldb_markers_thread = launch_monitor(lldb_markers_monitor,
                                         name='lldb file markers monitor')


def lldb_i_o_monitor():
    debug_thr()
    debug('i/o monitor: started')

    while lldb_instance() != None:
        lldberr = None  # lldb_instance.GetErrorFileHandle()
        lldbout = None  # lldb_instance.GetOutputFileHandle()

        debug('i/o monitor: lldberr: ' + lldberr.__str__())
        debug('i/o monitor: lldbout: ' + lldbout.__str__())

        debug('i/o monitor: waiting for select')

        input = []
        if lldbout:
            input.append(lldbout)
        if lldberr:
            input.append(lldberr)

        if len(input) > 0:
            input, output, x = select.select(input, [], [])
        else:
            # We're not waiting for input, set a timeout
            input, output, x = select.select(input, [], [], 1000)

        for h in input:
            str = h.read()
            if h == lldbout:
                sublime.set_timeout(lambda: lldb_view_write(str), 0.01)
            if h == lldberr:
                # We're sure we read something
                str.replace('\n', '\nerr> ')
                str = 'err> ' + str
                sublime.set_timeout(lambda: lldb_view_write(str), 0.01)

    debug('i/o monitor: stopped')


def lldb_markers_monitor():
    debug_thr()
    debug('markers monitor: started')
    # In the future, use lldb events to know what to update
    while True:
        v = lldb_file_markers_queue.get(True)
        m = v['marks']
        w = v['window']
        f = v['after']
        debug('markers mon: ' + str(lldb_file_markers_queue.qsize()))

        debug('markers monitor, got: ' + str(v))
        if 'pc' == m:
            update_code_view(w)
        elif 'bp' == m:
            update_breakpoints(w)
        elif 'all' == m:
            update_code_view(w)
            update_breakpoints(w)
        elif 'quit' == m:
            update_code_view(w)
            if f is not None:
                sublime.set_timeout(f, 0)
            return

        if f is not None:
                sublime.set_timeout(f, 0)

    debug('markers monitor: stopped')


def update_code_view(window):
    global lldb_last_location_view
    if lldb_last_location_view is not None:
        # WARNING!! Fix this! (erase_regions noton the main thread)
        sublime.set_timeout(
            lambda: lldb_last_location_view.erase_regions("lldb-location"), 0)

    if lldb_instance():
        entry = lldb_instance().current_line_entry()

        if entry:
                (directory, file, line, column) = entry
                filename = directory + '/' + file

                loc = filename + ':' + str(line) + ':' + str(column)

                def temp_function():
                    window.focus_group(0)
                    view = window.open_file(loc, sublime.ENCODED_POSITION)
                    window.focus_view(view)

                    global lldb_last_location_view
                    lldb_last_location_view = view
                    debug('marking loc at: ' + str(view))
                    region = [view.full_line(
                                view.text_point(line - 1, column - 1))]
                    sublime.set_timeout(lambda:
                        view.add_regions("lldb-location", \
                                         region, \
                                         "entity.name.class", "bookmark", \
                                         sublime.HIDDEN), 100)

                sublime.set_timeout(temp_function, 0)
                return

    debug("No location info available")


def update_breakpoints(window):
    debug_thr()

    def bulk_update():
        for w in sublime.windows():
            for v in w.views():
                v.erase_regions("lldb-breakpoint")
                for bp in breakpoints:
                    for bp_loc in bp.line_entries():
                        if bp_loc and v.file_name() == bp_loc[0] + '/' + bp_loc[1]:
                            debug('marking: ' + str(bp_loc) + ' at: ' + v.file_name() + ' (' + v.name() + ')')
                            v.add_regions("lldb-breakpoint", \
                                [v.full_line(
                                    v.text_point(bp_loc[2] - 1, bp_loc[3] - 1))], \
                                "string", "circle", \
                                sublime.HIDDEN)

    if lldb_instance():
        breakpoints = lldb_instance().breakpoints()
    else:
        # Just erase the current markers
        breakpoints = []

    sublime.set_timeout(bulk_update, 0)
