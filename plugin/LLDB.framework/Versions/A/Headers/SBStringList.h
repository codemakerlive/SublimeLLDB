//===-- SBStringList.h ------------------------------------------*- C++ -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#ifndef LLDB_SBStringList_h_
#define LLDB_SBStringList_h_

#include <LLDB/SBDefines.h>

namespace lldb {

class SBStringList
{
public:

    SBStringList ();

    SBStringList (const lldb::SBStringList &rhs);
    
    const SBStringList &
    operator = (const SBStringList &rhs);

    ~SBStringList ();

    bool
    IsValid() const;

    void
    AppendString (const char *str);

    void
    AppendList (const char **strv, int strc);

    void
    AppendList (const lldb::SBStringList &strings);

    uint32_t
    GetSize () const;

    const char *
    GetStringAtIndex (size_t idx);

    void
    Clear ();

protected:
    friend class SBCommandInterpreter;
    friend class SBDebugger;

    SBStringList (const lldb_private::StringList *lldb_strings);

    const lldb_private::StringList *
    operator->() const;

    const lldb_private::StringList &
    operator*() const;

private:

    std::auto_ptr<lldb_private::StringList> m_opaque_ap;

};

} // namespace lldb

#endif // LLDB_SBStringList_h_
